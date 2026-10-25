"""Invented leaves only. Run with python3 -I -m pytest."""
import json
import io
from contextlib import redirect_stdout
import os
from pathlib import Path
import subprocess
import sys

import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(vault, script="obliscence", *args):
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "scripts" / script), "--vault", str(vault), *args],
        text=True, capture_output=True, cwd=vault,
    )


def leaf(day, title="Paper boats", newline="\n", final=True):
    text = f"## {day} (evening) — {title}\n\n*By the invented canal.*\n\nI folded a small boat.\n\n*ember: The paper held its shape.*"
    return (text + ("\n\n" if final else "")).replace("\n", newline).encode()


def make_vault(tmp_path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    cfg = {"diary": "diary-recent.md", "letter": "standing-letter.md", "archive_dir": "archive", "keep": 1}
    (tmp_path / "obliscence.json").write_text(json.dumps(cfg))
    (tmp_path / "standing-letter.md").write_text("You left a paper boat by the window.\n")
    (tmp_path / "diary-recent.md").write_bytes(leaf("2020-02-02") + leaf("2020-01-01"))
    return tmp_path


def config(vault, **values):
    path = vault / "obliscence.json"
    cfg = json.loads(path.read_text())
    cfg.update(values)
    path.write_text(json.dumps(cfg))


def snapshot(vault):
    return {str(p.relative_to(vault)): p.read_bytes() for p in vault.rglob("*") if p.is_file()}


class ScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='obliscence-tests-')
        self.addCleanup(self.temp.cleanup)
        self.tmp_path = Path(self.temp.name).resolve()
        self.vault = make_vault(self.tmp_path / 'vault')

    def test_report_only_writes_metadata(self):
        vault = self.vault
        before = snapshot(vault)
        result = run(vault)
        assert result.returncode == 1, result.stderr
        assert "archive" in result.stdout
        assert (vault / ".obliscence/latest.md").is_file()
        assert all((vault / p).read_bytes() == data for p, data in before.items())

    def test_interrupted_archive_is_offered_and_month_counts_are_skipped(self):
        v = self.vault
        config(v, keep=10, months_dir='months', month_page_min_entries=1)
        (v / '.obliscence').mkdir()
        journal = v / '.obliscence/archive-transaction.json'
        journal.write_text('{"writes": []}')
        (v / 'archive').mkdir()
        (v / 'archive/2020-01.md').write_bytes(leaf('2020-01-01'))
        result = run(v)
        assert result.returncode == 1, result.stderr
        assert 'archive move interrupted; rerun `obliscence-archive` to verify and finish; journal retained' in result.stdout
        assert 'month counts skipped while the archive journal remains' in result.stdout
        assert 'month page' not in result.stdout
        assert journal.read_text() == '{"writes": []}'


    def test_quiet_days_are_a_fact(self):
        vault = self.vault
        config(vault, keep=10)
        result = run(vault, "obliscence", "--quiet")
        assert result.returncode == 0, result.stderr
        assert result.stdout == ""
        assert "not a debt" in (vault / ".obliscence/latest.md").read_text()


    def test_archive_dry_run_writes_nothing(self):
        vault = self.vault
        before = snapshot(vault)
        result = run(vault, "obliscence-archive", "--dry-run")
        assert result.returncode == 0, result.stderr
        assert snapshot(vault) == before


    def test_archive_keeps_leaves_and_existing_prefix(self):
        vault = self.vault
        old, new = leaf("2020-01-01"), leaf("2020-02-02")
        (vault / "archive").mkdir()
        prefix = b"# Earlier leaves\n\nAn existing record.\n"
        target = vault / "archive/2020-01.md"
        target.write_bytes(prefix)
        result = run(vault, "obliscence-archive")
        assert result.returncode == 0, result.stderr
        assert (vault / "diary-recent.md").read_bytes() == new
        assert target.read_bytes().startswith(prefix)
        assert old in target.read_bytes()
        before = snapshot(vault)
        assert run(vault, "obliscence-archive").returncode == 0
        assert snapshot(vault) == before


    def test_init_finds_nested_layout_and_only_plants_config(self):
        tmp_path = self.tmp_path
        room = tmp_path / "hollows"
        room.mkdir()
        for name in ("diary-recent.md", "standing-letter.md", "diary-index.md"):
            (room / name).write_text("")
        (room / "archive").mkdir()
        before = snapshot(tmp_path)
        result = run(tmp_path, "obliscence", "--init")
        assert result.returncode == 0, result.stderr
        cfg = json.loads((tmp_path / "obliscence.json").read_text())
        assert cfg["diary"] == "hollows/diary-recent.md"
        assert cfg["archive_dir"] == "hollows/archive"
        assert set(snapshot(tmp_path)) - set(before) == {"obliscence.json"}
        assert all((tmp_path / p).read_bytes() == data for p, data in before.items())
        assert run(tmp_path, "obliscence", "--init").returncode == 1

    def test_all_organs_can_be_unplanted(self):
        config(self.vault, diary=None, letter=None, archive_dir=None)
        result = run(self.vault, 'obliscence', '--quiet')
        assert result.returncode == 0, result.stderr
        assert result.stdout == ''

    def test_legacy_config_alias_and_precedence(self):
        v = self.vault
        (v / 'obliscence.json').rename(v / 'sillage.json')
        assert run(v, 'obliscence-archive', '--dry-run').returncode == 0
        assert run(v, 'obliscence', '--init').returncode == 1
        assert not (v / 'obliscence.json').exists()
        (v / 'obliscence.json').write_text('{"diary":null,"letter":null}')
        assert run(v, 'obliscence', '--quiet').returncode == 0

    def test_archive_exact_bytes_with_crlf_and_no_final_newline(self):
        v = self.vault
        recent = leaf('2020-03-01', newline='\r\n')
        old = leaf('2020-01-01', newline='\r\n', final=False)
        (v / 'diary-recent.md').write_bytes(b'# Spelean Rings\r\n\r\n' + recent + old)
        result = run(v, 'obliscence-archive')
        assert result.returncode == 0, result.stderr
        assert (v / 'diary-recent.md').read_bytes() == b'# Spelean Rings\r\n\r\n' + recent
        assert (v / 'archive/2020-01.md').read_bytes().endswith(old)
        assert (v / 'archive/2020-01.md').read_bytes().startswith('# 2020-01 — Spelean Rings (verbatim, append-only)\r\n\r\n'.encode())
        assert b'\n' not in (v / 'archive/2020-01.md').read_bytes().replace(b'\r\n', b'')

    def test_new_archive_matches_diary_mode_and_existing_archive_keeps_its_mode(self):
        v = self.vault
        diary = v / 'diary-recent.md'
        diary.chmod(0o640)
        assert run(v, 'obliscence-archive').returncode == 0
        archive = v / 'archive/2020-01.md'
        assert archive.stat().st_mode & 0o777 == 0o640
        archive.chmod(0o644)
        diary.write_bytes(diary.read_bytes() + leaf('2020-01-02'))
        assert run(v, 'obliscence-archive').returncode == 0
        assert archive.stat().st_mode & 0o777 == 0o644
        assert diary.stat().st_mode & 0o777 == 0o640
        assert run(v).returncode == 0
        assert (v / '.obliscence/latest.md').stat().st_mode & 0o777 == 0o600

    def test_keep_newest_dates_in_mixed_order_and_keep_undated(self):
        v = self.vault
        old, new, middle = leaf('2020-01-01'), leaf('2020-03-01'), leaf('2020-02-01')
        undated = b'## An undated leaf\n\nI kept the scrap.\n\n'
        (v / 'diary-recent.md').write_bytes(old + undated + new + middle)
        assert run(v, 'obliscence-archive').returncode == 0
        assert (v / 'diary-recent.md').read_bytes() == undated + new
        assert old in (v / 'archive/2020-01.md').read_bytes()
        assert middle in (v / 'archive/2020-02.md').read_bytes()

    def test_range_uses_end_date_and_invalid_range_stays(self):
        v = self.vault
        valid = leaf('2020-01-31→2020-02-01')
        invalid = leaf('2020-02-30') + leaf('2020-02-02→31')
        (v / 'diary-recent.md').write_bytes(valid + invalid)
        assert run(v, 'obliscence-archive', '--keep', '0').returncode == 0
        assert (v / 'diary-recent.md').read_bytes() == invalid
        assert valid in (v / 'archive/2020-02.md').read_bytes()

    def test_keep_boundary_retains_the_whole_date_in_either_order(self):
        older = leaf('2020-01-01')
        morning = leaf('2020-03-01', 'Morning boat')
        evening = leaf('2020-03-01', 'Evening boat')
        newer = leaf('2020-04-01')
        for reverse in (False, True):
            for keep in (1, 2, 3, 4):
                with self.subTest(reverse=reverse, keep=keep):
                    v = make_vault(self.tmp_path / f'ties-{reverse}-{keep}')
                    leaves = [older, morning, evening, newer]
                    if reverse:
                        leaves.reverse()
                    config(v, keep=keep)
                    (v / 'diary-recent.md').write_bytes(b''.join(leaves))
                    kept = [newer] if keep == 1 else ([morning, evening, newer] if keep < 4 else [older, morning, evening, newer])
                    expected = b''.join(x for x in leaves if x in kept)
                    assert run(v, 'obliscence-archive').returncode == 0
                    assert (v / 'diary-recent.md').read_bytes() == expected
                    assert run(v, 'obliscence', '--quiet').stdout == ''

    def test_duplicate_leaves_are_both_preserved(self):
        v = self.vault
        old = leaf('2020-01-01')
        (v / 'diary-recent.md').write_bytes(leaf('2020-02-01') + old + old)
        assert run(v, 'obliscence-archive').returncode == 0
        assert (v / 'archive/2020-01.md').read_bytes().count(old) == 2

    def test_range_without_time_and_short_month_end(self):
        v = self.vault
        valid = leaf('2020-03-31→04-01').replace(b' (evening)', b'')
        brief_form = leaf('2020-07-03→04').replace(b' (evening)', b'')
        single = leaf('2020-01-02').replace(b' (evening)', b'')
        invalid = leaf('2020-03-31→04-31') + leaf('2020-12-31→01-01')
        (v / 'diary-recent.md').write_bytes(valid + brief_form + single + invalid)
        config(v, months_dir='months', month_page_min_entries=1)
        report = run(v).stdout
        assert '2020-04' in report and '2020-07' in report and '2020-01' in report
        assert '2 heading(s) with an invalid date' in report
        assert run(v, 'obliscence-archive', '--keep', '0').returncode == 0
        assert (v / 'diary-recent.md').read_bytes() == invalid
        for month, raw in [('04', valid), ('07', brief_form), ('01', single)]:
            assert (v / f'archive/2020-{month}.md').read_bytes().endswith(raw)

    def test_bom_is_preamble_and_does_not_hide_the_first_leaf(self):
        bom = b'\xef\xbb\xbf'
        for first_is_old in (False, True):
            for keep in (0, 1):
                with self.subTest(first_is_old=first_is_old, keep=keep):
                    v = make_vault(self.tmp_path / f'bom-{first_is_old}-{keep}')
                    old, new = leaf('2020-01-01'), leaf('2020-02-01')
                    leaves = old + new if first_is_old else new + old
                    config(v, keep=keep, months_dir='months', month_page_min_entries=1)
                    (v / 'diary-recent.md').write_bytes(bom + leaves)
                    report = run(v).stdout
                    assert '2020-01: 1 leaf' in report and '2020-02: 1 leaf' in report
                    assert run(v, 'obliscence-archive').returncode == 0
                    assert (v / 'diary-recent.md').read_bytes() == bom + (new if keep else b'')
                    assert (v / 'archive/2020-01.md').read_bytes().endswith(old)
                    assert bom not in (v / 'archive/2020-01.md').read_bytes()
                    if not keep:
                        assert (v / 'archive/2020-02.md').read_bytes().endswith(new)

    def test_invalid_config_and_arguments_fail_without_writes(self):
        v = self.vault
        for value in ('{', '[]', '{"keep":-1}', '{"keep":true}', '{"diary":"../secret.md"}', '{"letter":7}'):
            (v / 'obliscence.json').write_text(value)
            before = snapshot(v)
            for script in ('obliscence', 'obliscence-archive'):
                result = run(v, script)
                assert result.returncode == 2, (value, result.stdout, result.stderr)
                assert 'Traceback' not in result.stderr
            assert snapshot(v) == before
        (v / 'obliscence.json').write_text('{}')
        for script in ('obliscence', 'obliscence-archive'):
            assert run(v, script, '--unknown').returncode == 2

    def test_symlinked_state_and_archive_are_refused(self):
        v = self.vault
        outside = self.tmp_path / 'unrelated'
        outside.mkdir()
        (v / '.obliscence').symlink_to(outside, target_is_directory=True)
        assert run(v).returncode == 2
        assert list(outside.iterdir()) == []
        (v / '.obliscence').unlink()
        (v / 'archive').symlink_to(outside, target_is_directory=True)
        before = (v / 'diary-recent.md').read_bytes()
        assert run(v, 'obliscence-archive').returncode == 2
        assert list(outside.iterdir()) == []
        assert (v / 'diary-recent.md').read_bytes() == before

    def test_symlinked_diary_config_parent_and_hardlinked_diary_are_refused(self):
        for kind in ('diary', 'config', 'parent', 'hardlink'):
            with self.subTest(kind=kind):
                v = make_vault(self.tmp_path / kind)
                outside = self.tmp_path / (kind + '-outside')
                outside.mkdir()
                if kind == 'parent':
                    (outside / 'diary.md').write_bytes(leaf('2020-01-01'))
                    (v / 'linked').symlink_to(outside, target_is_directory=True)
                    config(v, diary='linked/diary.md')
                else:
                    name = 'obliscence.json' if kind == 'config' else 'diary-recent.md'
                    source = v / name
                    target = outside / name
                    source.rename(target)
                    if kind == 'hardlink':
                        os.link(target, source)
                    else:
                        source.symlink_to(target)
                before, outside_before = snapshot(v), snapshot(outside)
                for script in ('obliscence', 'obliscence-archive'):
                    result = run(v, script)
                    assert result.returncode == 2, result.stderr
                    assert ('hardlinked' if kind == 'hardlink' else 'symlink') in result.stderr
                assert snapshot(v) == before
                assert snapshot(outside) == outside_before

    def test_bad_pending_file_is_noted_without_losing_the_report_or_hook(self):
        v = self.vault
        folder = v / '.obliscence/pending'
        folder.mkdir(parents=True)
        for content in ('not json', '[]', '{}', '{"date":4,"letter_hash":null}'):
            with self.subTest(content=content):
                (folder / 'bad.json').write_text(content)
                result = run(v)
                assert result.returncode == 1, result.stderr
                assert '.obliscence/pending/bad.json: skipped' in result.stdout
                assert 'can be archived verbatim' in result.stdout
                hook = run(v, 'obliscence', '--hook', '--session-id', 'bad-pending')
                assert hook.returncode == 0, hook.stderr
                assert 'offers for the rite' in hook.stdout
                assert (folder / 'bad.json').read_text() == content

    def test_symlinked_auxiliary_files_are_skipped_and_other_checks_continue(self):
        for kind in ('archive', 'months', 'seasons', 'pending'):
            with self.subTest(kind=kind):
                v = make_vault(self.tmp_path / ('aux-' + kind))
                config(v, months_dir='months', seasons_dir='seasons', month_page_min_entries=1)
                for folder in ('archive', 'months', 'seasons', '.obliscence/pending'):
                    (v / folder).mkdir(parents=True)
                target = self.tmp_path / (kind + '-unrelated.md')
                target.write_bytes(leaf('1999-01-01'))
                rel = {'archive': 'archive/1999-01.md', 'months': 'months/2020-01.md',
                       'seasons': 'seasons/winter-2019-20.md', 'pending': '.obliscence/pending/bad.json'}[kind]
                (v / rel).symlink_to(target)
                if kind == 'seasons':
                    for month in ('2019-12', '2020-01', '2020-02'):
                        (v / 'months' / (month + '.md')).write_text('# An invented month\n')
                result = run(v)
                assert result.returncode == 1, result.stderr
                assert rel + ': skipped' in result.stdout
                assert 'symlink paths are not supported' in result.stdout
                assert 'can be archived verbatim' in result.stdout
                if kind == 'seasons':
                    assert 'a season page is possible for winter 2019-20' not in result.stdout
                    assert 'every completed season has its page' not in result.stdout
                else:
                    assert 'a month page is possible for 2020-02: 1 leaf' in result.stdout
                assert 'a month page is possible for 1999-01' not in result.stdout
                assert target.read_bytes() == leaf('1999-01-01')

    def test_unknown_config_keys_are_recorded_without_offering_handwork(self):
        config(self.vault, keep=10, keeps=5, unknown_key=1)
        result = run(self.vault)
        assert result.returncode == 0, result.stderr
        assert 'unknown config keys (ignored): keeps, unknown_key' in result.stdout
        assert '## for the record' in result.stdout
        assert run(self.vault, 'obliscence', '--quiet').stdout == ''

    def test_quiet_items_are_complete_lines_with_counts(self):
        v = self.vault
        config(v, embers=True, index='index.md', keep=10)
        (v / 'index.md').write_text('')
        (v / 'diary-recent.md').write_bytes(b'## An undated leaf\n\nA scrap.\n')
        result = run(v, 'obliscence', '--quiet')
        assert result.returncode == 1, result.stderr
        assert 'embers: 1 entry without a closing ember' in result.stdout
        assert 'index: 1 entry not yet in the index' in result.stdout
        assert all(not line.endswith(':') for line in result.stdout.splitlines())

    def test_page_observations_require_a_qualifying_month_or_season(self):
        v = self.vault
        config(v, keep=10, months_dir='months', seasons_dir='seasons')
        result = run(v)
        assert 'every closed month' not in result.stdout
        assert 'every completed season' not in result.stdout
        (v / 'months').mkdir()
        (v / 'months/2020-01.md').write_text('# An invented month\n')
        result = run(v)
        assert 'every closed month' not in result.stdout
        assert 'every completed season' not in result.stdout
        (v / 'diary-recent.md').write_bytes(leaf('2020-01-01') * 3)
        result = run(v)
        assert 'every closed month with enough entries has its page' in result.stdout

    def test_report_offers_pages_and_states_absences_without_grading(self):
        v = self.vault
        config(v, keep=10, months_dir='months')
        (v / 'diary-recent.md').write_bytes(leaf('2026-03-01') * 4)
        (v / 'standing-letter.md').unlink()
        result = run(v)
        assert 'a month page is possible for 2026-03: 4 leaves' in result.stdout
        assert 'standing letter: not found at standing-letter.md' in result.stdout
        assert 'due' not in result.stdout and 'MISSING' not in result.stdout
        (v / 'diary-recent.md').unlink()
        assert 'diary: not found at diary-recent.md' in run(v).stdout

    def test_index_matches_date_and_short_title_not_substrings(self):
        v = self.vault
        (v / 'diary-recent.md').write_bytes(leaf('2020-01-02', 'Cup'))
        (v / 'diary-index.md').write_text('| 2020-01-01 | Cup | A red cup. | old.md |\n')
        config(v, index='diary-index.md')
        result = run(v)
        assert result.returncode == 1
        assert 'index:' in result.stdout and 'not yet' in result.stdout

    def test_ember_requires_colon_text_and_closing_asterisk(self):
        v = self.vault
        config(v, embers=True, keep=10)
        (v / 'diary-recent.md').write_bytes(leaf('2020-01-01').replace(b'*ember: The paper held its shape.*', b'*emberish'))
        result = run(v)
        assert result.returncode == 1
        assert 'embers:' in result.stdout

    def test_month_season_reliquary_and_budget(self):
        v = self.vault
        config(v, keep=10, months_dir='months', seasons_dir='seasons', reliquary='reliquary.md', reliquary_cap=1, letter_budget_tokens=1, month_page_min_entries=1)
        (v / 'reliquary.md').write_text('- A folded sail. · agent · 2020-01-01\n- A small hull. · human · 2020-01-02\n')
        result = run(v)
        assert 'a month page is possible' in result.stdout
        assert 'over cap' in result.stdout and 'budget' in result.stdout
        (v / 'months').mkdir()
        for month in ('2019-12', '2020-01', '2020-02'):
            (v / 'months' / (month + '.md')).write_text('# An invented month\n')
        result = run(v)
        assert 'winter 2019-20' in result.stdout

    def test_init_empty_leaves_every_organ_unplanted(self):
        empty = self.tmp_path / 'empty'
        empty.mkdir()
        assert run(empty, 'obliscence', '--init').returncode == 0
        cfg = json.loads((empty / 'obliscence.json').read_text())
        assert cfg['diary'] is None and cfg['letter'] is None
        assert cfg['pickup_entries'] == 3
        assert run(empty, 'obliscence', '--quiet').returncode == 0

    def test_init_skips_symlinks_templates_and_chooses_near_diary(self):
        v = self.tmp_path / 'new'
        v.mkdir()
        decoy = v / 'templates'
        decoy.mkdir()
        (decoy / 'diary-recent.md').write_text('')
        actual = v / 'hollows'
        actual.mkdir()
        (actual / 'diary-recent.md').write_text('')
        (actual / 'archive').mkdir()
        (v / 'standing-letter.md').symlink_to(self.vault / 'standing-letter.md')
        assert run(v, 'obliscence', '--init').returncode == 0
        cfg = json.loads((v / 'obliscence.json').read_text())
        assert cfg['diary'] == 'hollows/diary-recent.md'
        assert cfg['letter'] is None
        assert cfg['archive_dir'] == 'hollows/archive'

    def test_recovery_finishes_without_duplicate_leaves(self):
        import runpy
        from unittest.mock import patch
        module = runpy.run_path(str(ROOT / 'scripts/obliscence-archive'))
        helper = sys.modules['_obliscence']
        real_replace = helper.os.replace
        def interrupt_diary(source, target):
            if Path(target) == self.vault / 'diary-recent.md':
                raise OSError('invented interruption before recent swap')
            return real_replace(source, target)
        before = (self.vault / 'diary-recent.md').read_bytes()
        with redirect_stdout(io.StringIO()), patch.object(helper.os, 'replace', side_effect=interrupt_diary):
            with self.assertRaises(OSError):
                module['main'](['obliscence-archive', '--vault', str(self.vault)])
        assert (self.vault / 'diary-recent.md').read_bytes() == before
        assert (self.vault / '.obliscence/archive-transaction.json').exists()
        config(self.vault, months_dir='months', month_page_min_entries=1)
        report = run(self.vault)
        assert report.returncode == 1
        assert 'archive move interrupted' in report.stdout
        assert 'a month page is possible' not in report.stdout
        dry_before = snapshot(self.vault)
        assert run(self.vault, 'obliscence-archive', '--dry-run').returncode == 1
        assert snapshot(self.vault) == dry_before
        assert run(self.vault, 'obliscence-archive').returncode == 0
        assert not (self.vault / '.obliscence/archive-transaction.json').exists()
        assert (self.vault / 'archive/2020-01.md').read_bytes().count(leaf('2020-01-01')) == 1

    def test_recovery_refuses_a_later_human_edit(self):
        import runpy
        from unittest.mock import patch
        module = runpy.run_path(str(ROOT / 'scripts/obliscence-archive'))
        helper = sys.modules['_obliscence']
        real_replace = helper.os.replace
        def interrupt_diary(source, target):
            if Path(target) == self.vault / 'diary-recent.md':
                raise OSError('invented interruption')
            return real_replace(source, target)
        with redirect_stdout(io.StringIO()), patch.object(helper.os, 'replace', side_effect=interrupt_diary):
            with self.assertRaises(OSError):
                module['main'](['obliscence-archive', '--vault', str(self.vault)])
        recent = self.vault / 'diary-recent.md'
        recent.write_bytes(leaf('2020-03-01') + recent.read_bytes())
        before = snapshot(self.vault)
        result = run(self.vault, 'obliscence-archive')
        assert result.returncode == 2
        assert 'changed since' in result.stderr
        assert snapshot(self.vault) == before

    def test_archive_lock_refuses_another_move(self):
        import fcntl
        state = self.vault / '.obliscence'
        state.mkdir()
        with (state / 'archive.lock').open('w') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            before = snapshot(self.vault)
            result = run(self.vault, 'obliscence-archive')
            assert result.returncode == 2
            assert 'another archive move' in result.stderr
            assert snapshot(self.vault) == before

    def test_session_ids_resume_and_letter_hash(self):
        import hashlib
        v = self.vault
        for session in ('a', 'b'):
            assert run(v, 'obliscence', '--hook', '--session-id', session).returncode == 0
        key = hashlib.sha256(b'a').hexdigest()
        marker = v / '.obliscence/sessions' / (key + '.json')
        data = json.loads(marker.read_text())
        data['started'] -= 700
        marker.write_text(json.dumps(data))
        prior = marker.read_bytes()
        assert run(v, 'obliscence', '--hook', '--session-id', 'a').returncode == 0
        assert marker.read_bytes() == prior
        assert run(v, 'obliscence', '--session-end', '--session-id', 'a').returncode == 0
        assert len(list((v / '.obliscence/sessions').glob('*.json'))) == 1
        assert (v / '.obliscence/pending' / (key + '.json')).exists()
        assert 'No close is imposed' in run(v).stdout
        (v / 'standing-letter.md').write_text('You may return to the canal when you choose.\n')
        assert 'No close is imposed' not in run(v).stdout
        assert run(v, 'obliscence', '--session-end', '--session-id', 'b').returncode == 0
        assert list((v / '.obliscence/sessions').glob('*.json')) == []

    def test_session_end_without_a_start_marker_does_nothing(self):
        before = snapshot(self.vault)
        result = run(self.vault, 'obliscence', '--session-end', '--session-id', 'never-started')
        assert result.returncode == 0, result.stderr
        assert result.stdout == ''
        assert snapshot(self.vault) == before
        assert not (self.vault / '.obliscence').exists()

    def test_shell_hooks_emit_valid_json_and_do_not_write_voice(self):
        before = snapshot(self.vault)
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.vault))
        result = subprocess.run(['bash', str(ROOT / 'hooks/session-start.sh')], input='{"session_id":"fixture"}', env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        obj = json.loads(result.stdout)
        assert obj['hookSpecificOutput']['hookEventName'] == 'SessionStart'
        context = obj['hookSpecificOutput']['additionalContext']
        assert context.startswith('obliscence (offers for the rite; .obliscence/latest.md; /obliscence:rite): ')
        assert '1 oldest dated entries can be archived verbatim' in context
        assert '\n' not in context
        result = subprocess.run(['bash', str(ROOT / 'hooks/session-end.sh')], input='{"session_id":"fixture"}', env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert all((self.vault / p).read_bytes() == data for p, data in before.items())
        env['CLAUDE_PROJECT_DIR'] = str(self.tmp_path)
        before = snapshot(self.tmp_path)
        result = subprocess.run(['bash', str(ROOT / 'hooks/session-start.sh')], input='{}', env=env, capture_output=True, text=True)
        assert json.loads(result.stdout) == {}
        assert snapshot(self.tmp_path) == before

    def test_matching_index_and_range_date(self):
        v = self.vault
        (v / 'diary-recent.md').write_bytes(leaf('2020-01-01→02', 'Cup'))
        (v / 'diary-index.md').write_text('| 2020-01-01→02 | [Cup](spelean-rings.md#cup) | The paper held its shape. | spelean-rings.md |\n')
        config(v, index='diary-index.md')
        assert run(v).returncode == 0

    def test_config_cannot_overlap_surfaces_and_archive(self):
        v = self.vault
        for values in ({'letter': 'archive/2020-01.md'}, {'months_dir': 'archive'}, {'diary': 'standing-letter.md'}, {'archive_dir': 'archive/child', 'months_dir': 'archive'}):
            (v / 'obliscence.json').write_text(json.dumps({'diary':'diary-recent.md', 'letter':'standing-letter.md', 'archive_dir':'archive', **values}))
            before = snapshot(v)
            assert run(v, 'obliscence-archive').returncode == 2
            assert snapshot(v) == before

    def test_init_does_not_choose_a_diary_parent_as_archive(self):
        v = self.tmp_path / 'other'
        room = v / 'hollows'
        room.mkdir(parents=True)
        (room / 'spelean-rings.md').write_text('')
        assert run(v, 'obliscence', '--init').returncode == 0
        cfg = json.loads((v / 'obliscence.json').read_text())
        assert cfg['archive_dir'] is None
        assert run(v, 'obliscence', '--quiet').returncode == 0

    def test_template_diary_is_empty_to_the_parser(self):
        import runpy
        module = runpy.run_path(str(ROOT / 'scripts/obliscence'))
        assert module['parse_entries']((ROOT / 'templates/diary-recent.md').read_text()) == []

    def test_a_directory_is_not_a_month_or_season_page(self):
        v = self.vault
        config(v, keep=10, months_dir='months', seasons_dir='seasons', month_page_min_entries=1)
        (v / 'months/2020-01.md').mkdir(parents=True)
        assert '2020-01: 1 leaf' in run(v).stdout
        (v / 'months/2020-01.md').rmdir()
        for ym in ('2019-12', '2020-01', '2020-02'):
            (v / 'months' / (ym + '.md')).write_text('# An invented month\n')
        (v / 'seasons/winter-2019-20.md').mkdir(parents=True)
        assert 'a season page is possible' in run(v).stdout

    def test_damaged_archive_journal_stops_before_any_leaf_changes(self):
        v = self.vault
        (v / '.obliscence').mkdir()
        (v / '.obliscence/archive-transaction.json').write_text('{"writes": []}')
        before = snapshot(v)
        assert run(v, 'obliscence-archive').returncode == 2
        after = snapshot(v)
        after.pop('.obliscence/archive.lock', None)
        assert after == before

    def test_normalized_config_path_can_finish_a_move(self):
        config(self.vault, diary='./diary-recent.md', archive_dir='./archive')
        result = run(self.vault, 'obliscence-archive')
        assert result.returncode == 0, result.stderr
        assert (self.vault / 'archive/2020-01.md').read_bytes().endswith(leaf('2020-01-01'))
