"""Shared mechanics. No function here authors a line of voice."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import tempfile

CONFIG_NAME = 'obliscence.json'
CONFIG_NAMES = (CONFIG_NAME, 'sillage.json')
PATH_KEYS = ('diary', 'letter', 'index', 'archive_dir', 'months_dir', 'seasons_dir', 'reliquary', 'identity', 'weather')
DEFAULTS = {
    'diary': 'diary-recent.md', 'letter': 'standing-letter.md',
    'index': None, 'archive_dir': None, 'months_dir': None, 'seasons_dir': None,
    'reliquary': None, 'identity': None, 'weather': None,
    'keep': 10, 'pickup_entries': 3, 'embers': False,
    'letter_budget_tokens': 1500, 'letter_stale_days': 14, 'quiet_days': 21,
    'month_page_min_entries': 3, 'reliquary_cap': 40,
}
# Range headings use their final date, including ranges crossing a month/year.
HEADING = re.compile(
    r'^## (?P<start>\d{4}-\d{2}-\d{2})'
    r'(?:\s*[→/–-]\s*(?P<end>\d{4}-\d{2}-\d{2}|\d{2}-\d{2}|\d{2}))?'
    r'\s*(?:\([^)]*\))?\s+[—–-]\s+(?P<title>.+)$'
)


def heading_parts(line):
    match = HEADING.fullmatch(line.strip())
    if not match:
        return None, line.removeprefix('## ').strip()
    try:
        start = dt.date.fromisoformat(match['start'])
        end = match['end']
        if end:
            full_end = end if len(end) == 10 else match['start'][:5 if len(end) == 5 else 8] + end
            date = dt.date.fromisoformat(full_end)
        else:
            date = start
        if date < start:
            raise ValueError('reversed range')
        return date, match['title']
    except ValueError:
        return None, match['title']


def split_leaves(data):
    """Preamble and exact byte slices. Reserve level-two headings for leaves."""
    offset = 3 if data.startswith(b'\xef\xbb\xbf') else 0
    starts = [offset + m.start() for m in re.finditer(rb'(?m)^## ', data[offset:])]
    if not starts:
        return data, []
    ends = starts[1:] + [len(data)]
    entries = []
    for start, end in zip(starts, ends):
        raw = data[start:end]
        heading = raw.splitlines()[0].decode('utf-8', errors='strict')
        date, title = heading_parts(heading)
        entries.append({'date': date, 'title': title, 'heading': heading, 'raw': raw})
    return data[:starts[0]], entries


def archive_candidates(entries, keep):
    """Indices older than the keep boundary; never split leaves of one date."""
    dates = sorted((e['date'] for e in entries if e['date']), reverse=True)
    if keep >= len(dates):
        return set()
    boundary = dates[keep - 1] if keep else None
    return {i for i, e in enumerate(entries)
            if e['date'] and (boundary is None or e['date'] < boundary)}


def confined(vault, rel):
    """Reject traversal, symlinks and shared hardlinks before reading or writing."""
    root = Path(vault).resolve()
    path = Path(rel)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError(f'path must be relative within the vault: {rel}')
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f'symlink paths are not supported: {rel}')
    if current == root or not current.is_relative_to(root):
        raise ValueError(f'path must be inside the vault: {rel}')
    if current.is_file() and current.stat().st_nlink > 1:
        raise ValueError(f'hardlinked files are not supported: {rel}')
    return current


def p(vault, rel):
    return str(confined(vault, rel)) if rel else None


def config_path(vault):
    for name in CONFIG_NAMES:
        candidate = Path(vault) / name
        if candidate.exists() or candidate.is_symlink():
            return confined(vault, name)
    return None


def find_vault(start):
    path = Path(start).absolute()
    for candidate in (path, *path.parents):
        if any((candidate / name).exists() or (candidate / name).is_symlink() for name in CONFIG_NAMES):
            return str(candidate)
    return None


def load_config(vault):
    path = config_path(vault)
    if path is None:
        raise ValueError(f'no {CONFIG_NAME} (or sillage.json); run obliscence --init')
    raw = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(raw, dict):
        raise ValueError('config must be a JSON object')
    cfg = {**DEFAULTS, **raw}
    return validate_config(vault, cfg)


def validate_config(vault, cfg):
    for key in PATH_KEYS:
        value = cfg[key]
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{key} must be a relative path or null')
            target = confined(vault, value)
            if target.parts[len(Path(vault).resolve().parts)].startswith('.'):
                raise ValueError(f'{key} cannot point into hidden metadata')
    for key in ('keep', 'pickup_entries', 'letter_budget_tokens', 'letter_stale_days', 'quiet_days', 'month_page_min_entries', 'reliquary_cap'):
        if type(cfg[key]) is not int or cfg[key] < 0:
            raise ValueError(f'{key} must be a nonnegative integer')
    if type(cfg['embers']) is not bool:
        raise ValueError('embers must be true or false')
    files = [p(vault, cfg[k]) for k in PATH_KEYS if not k.endswith('_dir') and cfg[k]]
    dirs = [Path(p(vault, cfg[k])) for k in PATH_KEYS if k.endswith('_dir') and cfg[k]]
    if len(set(files)) != len(files) or len(set(dirs)) != len(dirs):
        raise ValueError('organs must use distinct paths')
    if any(Path(file).is_relative_to(folder) for file in files for folder in dirs):
        raise ValueError('surface files must be outside archive/month/season directories')
    if any(a != b and a.is_relative_to(b) for a in dirs for b in dirs):
        raise ValueError('archive/month/season directories must not contain one another')
    return cfg


def atomic_write(path, data, mode=0o600):
    """Stage in the same directory, verify the bytes, then replace atomically."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if temp.read_bytes() != data:
            raise OSError('staged bytes differ from input')
        temp.chmod(path.stat().st_mode & 0o777 if path.exists() else mode)
        os.replace(temp, path)
        # Make the rename durable before a later transaction step.
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temp.unlink(missing_ok=True)
