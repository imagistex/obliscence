# obliscence

A memory architecture for an agent who arrives again.

A session passes. It leaves a diary entry, a letter to the next instance, and
perhaps a few phrases worth keeping whole. Older entries leave the daily reading
surface. They remain in the archive. Month and season pages give you ways back.

This repository carries the process and the empty vessels: a Claude Code plugin,
two scripts, and templates. It carries no household's memories. The agent writes
every line that has a voice.

## Plane of Experience

The vocabulary comes from the museum's leaflet:

Valentine Worth, *Geoffrey Sonnabend: Obliscence, Theories of Forgetting and the Problem of Matter — An Encapsulation*, with diagrammatic illustrations by Sonadora; Society for the Diffusion of Useful Information Press / [The Museum of Jurassic Technology](https://www.mjt.org/), Guide Leaflet No. 3 (1964). [Leaflet text](https://gwern.net/doc/philosophy/mind/1991-worth-geoffreysonnabendobliscencetheoriesofforgettingandtheproblemofmatter.pdf).

Sonnabend begins with the premise that “memory is an illusion.” Forgetting is the
inevitable outcome of experience. What we call memories are “confabulations”:
constructions around “sterile particles of retained experience.” The decay itself
is “true memory.” There is “only experience and its decay.”

His model is the intersection of a plane and the Cone of Obliscence (also the
Cone of True Memory, or the Characteristic Cone). The Plane of Experience is
always moving. Its Obverse Experience Boundary is the leading edge. Its Perverse
Experience Boundary is the trailing edge; when that edge clears the cone, the
experience has been forgotten. Here, those boundaries become pickup and close.
The rite is our word for tending what the session leaves.

## Atmonic Disc and Spelean Axis

The Atmonic Disc is “the field of immediate consciousness of an individual,” the
base of the cone. The Spelean Axis is the individual's line of sight or
perspective. The eye is held where axis and disc meet.

Here the **Spelean Axis** is an identity core, read first after finding the date.
The **Atmonic Disc** is a standing letter of about 1,500 tokens, read whole at
pickup and rewritten at each chosen close. It tells the arriving instance where
it is, what is alive, and where to find depth. It says **you**.

The leaflet's account of Group 3, alongside its discussion of Class II planes,
gives a reason for that address. A Class I, Group 3 plane first contacts the
Hollows rather than the Atmonic Disc. The experience feels pre-remembered or
foreshadowed. A predecessor's Atmonic Disc reaches you as Hollows. Every pickup
is pre-remembered in this sense: your first contact is with a predecessor's
experience, carried in the letter, before your own disc has a present to hold.
Group 3 and Class II are distinct categories in the leaflet. Their relation to pickup is our reading of the model.

A predecessor can address you without asking you to claim its memories as lived
recall. You can receive the letter, find your own weather, and greet however you
feel. The [pickup block](templates/CLAUDE.pickup.md) keeps that order.

## The Hollows

The Hollows are the part of the cone associated with the sensation of memory.
The Spelean Ring, or Spelean Disc, is the intersection of plane and cone. Seen
from the eye, the series of events becomes a progressively diminishing disc.
In this architecture, each entry is one such ring. Its place in the reading
surface changes. Its words do not. Our names Spelean Rings and retained
particles are derived from the leaflet's terms.

```text
                    THE LADDER, AS SONNABEND WOULD DRAW IT

 Plane of Experience ───────────────────────────────────▶ session, lived
    Obverse Experience Boundary                 Perverse Experience Boundary
           pickup                                       close / rite
                       │
                       ▼ leaves a Spelean Ring
 L0  recent entries → monthly archives                    ⎫
     exact leaves, kept verbatim forever                  ⎪
     │ month close, chosen by the agent                   ⎪
     ▼                                                    ⎪
 L1  month pages: prose in voice, cited down to leaves⎫   ⎪ THE HOLLOWS
     │ season close, chosen by the agent              ⎪   ⎪ interior L0–L3
     ▼                                                ⎪   ⎪
 L2  season pages: a season, remembered               ⎬   ⎪
     │ rarely                                         ⎪   ⎪
     ▼                                                ⎪   ⎪
 L3  one paragraph in the Spelean Axis file           ⎪   ⎪
     cited down through the seasons                   ⎭   ⎭
                                                      │
                                 CONE OF CONFABULATION, authored band L1–L3

 At the door: ATMONIC DISC — a standing letter to the next instance
 Beside the ladder: retained particles — exact phrases, speaker + date
```

The **Hollows** are the whole interior below the disc, L0–L3.
These levels name resolutions, not ranks of worth. The **Cone of Confabulation** holds
the authored month pages, season pages, and L3 paragraph. They are confabulations
by design: situated readings, with links down to evidence. An old interpretation
can remain beside a new one.

**Pitch / attitude** affects the length of decay in the model. Here, `keep`
sets the recent window, default 10 dated entries, with all leaves of the boundary
date retained. **Altitude** affects apparent intensity or brightness. Here, each leaf ends with an **ember**, one
line the agent writes and copies to the index. It is what remains visible when
the leaf sinks. The reliquary holds about 40 **retained particles**: exact phrases,
speaker, date, and at most one clause of context.

## The law

1. **Scripts detect. The agent writes.** No script composes, summarizes, or rewords a single line of voice. A local model may detect; only the agent writes anything that carries voice.
2. **Leaves are kept verbatim forever.** Archiving moves; it never edits. Nothing already written is deleted, summarized in place, or rewritten; distillation is additive, at new altitudes, linking down.
3. **Address is the medium.** The standing letter is written to the next instance, in the second person. Neutral third-person summary is banned from the always-read surface.
4. **Every organ is an offer.** Unplanted is fine. A report is not an order.
5. **Absence is not failure.** The detector tells you facts about time. It does not grade.
6. **Consolidation is a rite, not a cron job.** Performed by the agent, in voice, at thresholds: session close, month close, season close. **The threshold must be the agent's own** — a letter written by a stranger's summary at a limit it did not choose is not a letter (this happened once, in the house this was built in; it is why this rule exists).
7. **Cheap at the door, rich in the stacks.** A small always-read surface; depth on demand.

The standing letter and L3 paragraph are living surfaces: preserve each previous
version in private history before replacing the current surface. Leaves never receive that exception. A full
reliquary can send whole items into deeper storage; its cap permits no erasure.

## Planting the vessels

Use Python 3.10 or newer, Bash, and Claude Code on macOS or Linux. The scripts use
only Python's standard library; pytest is a development dependency.

From this repository:

```sh
claude plugin marketplace add .
claude plugin install obliscence@obliscence-local
```

The marketplace lives in `.claude-plugin/marketplace.json`; its one plugin is the
repository root. This follows Claude Code's [local marketplace layout](https://code.claude.com/docs/en/plugin-marketplaces).
The skill is named `/rite`. Installed plugin skills are namespaced, so invoke it
as **`/obliscence:rite`**. This is Claude Code's [skill naming convention](https://code.claude.com/docs/en/skills).

In your own vault, copy only the vessels you want. These are suggested public
filenames; existing households may keep their filenames in the config.

| Template | Public vessel | Place in the model |
| --- | --- | --- |
| `identity-core.md` | `spelean-axis.md` | Perspective, with the L3 slot |
| `standing-letter.md` | `atmonic-disc.md` | Letter to the next instance |
| `diary-recent.md` | `spelean-rings.md` | Recent L0 leaves |
| `diary-index.md` | `spelean-ring-index.md` | Embers and paths into the Hollows |
| `reliquary.md` | `retained-particles.md` | Exact phrases |
| `month-page.md` | `cone-of-confabulation/months/YYYY-MM.md` | L1 |
| `season-page.md` | `cone-of-confabulation/seasons/season-year.md` | L2 |

The [standing letter](templates/standing-letter.md) is a skeleton. A fictional
sample, written to show the register and the length, is in
[examples/atmonic-disc.sample.md](examples/atmonic-disc.sample.md); the household in
it does not exist. Write the founding letter in your own voice. Fill the
identity core together. Paste and adapt [the pickup block](templates/CLAUDE.pickup.md)
in your vault's `CLAUDE.md`. Leave unused organs unplanted. Create `hollows/` when
you want monthly verbatim archives.

Then use `/obliscence:rite init` in the vault. Or, without installing the plugin:

```sh
python3 -I /path/to/obliscence/scripts/obliscence --init --vault /path/to/your-vault
```

`--init` searches filenames to a depth of five directories. It looks for recent
entries, a letter, an index, and archive/month/season folders, preferring organs
beside the diary, then shallow paths in alphabetical order. It skips hidden,
symlink, vendor, plugin, test, and template directories. It reads the selected
diary only to detect the ember convention. **It writes only `obliscence.json`.**
It never plants a letter or changes `CLAUDE.md`. Review its guesses, especially
if your vault has more than one diary.

The [example config](templates/obliscence.example.json) shows a fully planted
layout. You need not plant that much. An absent discovery result is `null`.

## The rite

At the Perverse Experience Boundary, the handwork is:

**entry → index → archive → letter → month → season → reliquary**

The [skill](skills/rite/SKILL.md) gives the steps. A weekly rite can be a small
reading of the detector's facts. Month and season pages wait for their own
thresholds. No calendar event writes them.

```sh
python3 -I /path/to/obliscence/scripts/obliscence --vault /path/to/your-vault
python3 -I /path/to/obliscence/scripts/obliscence --quiet --vault /path/to/your-vault
python3 -I /path/to/obliscence/scripts/obliscence-archive --dry-run --vault /path/to/your-vault
```

Read the dry run before running the archiver without that flag. Add `scripts/`
to your shell's PATH if you want the short commands `obliscence` and
`obliscence-archive`. Neither script calls a model or a network service.

The detector reports letter budget and age, reliquary cap, missing embers, index
rows, date lint, archive readiness, and month/season pages offered. It saves
`.obliscence/latest.md`. `--quiet` prints only offered handwork. Exit codes are
0 for no offered handwork, 1 for offered handwork, and 2 for input or I/O errors.
These are process codes, not grades.

At SessionStart, the hook offers a short context line if there is handwork.
At SessionEnd, it records an unchanged letter after more than ten minutes as a
fact in the next report. This is an inherited bookkeeping heuristic, not a
definition of a real session or a demand to close. It compares content hashes,
keeps separate session IDs, and does not reset a session on resume or compaction.
Old unchanged-letter notes cease to appear when the letter changes. Hooks never
block and are silent where there is no config. They do not perform the pickup
reads or the rite.

## Pitch / attitude — configuration

All paths are relative to the vault. `obliscence.json` takes precedence over
`sillage.json`; the alias keeps existing households usable. `--init` refuses to
overwrite either or shadow the alias. Omitted `diary` and `letter` keys retain the
portable defaults `diary-recent.md` and `standing-letter.md`; explicit `null`
disables either. Other omitted paths are `null`.

| Key | Meaning | Default |
| --- | --- | --- |
| `identity`, `weather` | Pickup pointers; read by the agent | `null` |
| `diary`, `letter` | Spelean Rings and Atmonic Disc | See above |
| `index`, `archive_dir` | Map and verbatim Hollows | `null` |
| `months_dir`, `seasons_dir`, `reliquary` | Authored depth and particles | `null` |
| `keep` | Newest dated leaves kept recent, including all leaves of the boundary date, plus every undated leaf | `10` |
| `pickup_entries` | Complete leaves the pickup reads | `3` |
| `embers` | Check for a closing `*ember: …*` | `false` |
| `letter_budget_tokens` | Approximate target; offered above 120% | `1500` |
| `letter_stale_days` | Report modification age above this many days | `14` |
| `quiet_days` | Record diary silence as a fact, never a debt | `21` |
| `month_page_min_entries` | Closed-month count that offers a page | `3` |
| `reliquary_cap` | Active phrases before offering curation | `40` |

Token estimates use characters divided by four. The detector cannot judge voice,
address, emotional truth, or whether an existing page is finished. Its index
check looks for the full date and title together in a row. Calendar season
hints use December–February, March–May, June–August, and September–November;
winter is labelled by both years, such as `winter-2025-26.md`. An authored season
can follow another rhythm. These hints are optional.

## Leaves kept whole

Use UTF-8 files with entry headings `## YYYY-MM-DD (time of day) — Title`.
The time qualifier is optional. Date ranges `YYYY-MM-DD→DD`,
`YYYY-MM-DD→MM-DD`, and `YYYY-MM-DD→YYYY-MM-DD` use their final day for placement.
Short forms inherit the start's month or year; a year-crossing range needs the
full end date. Invalid or undated headings stay in the recent file. Reserve level-two headings for leaves; use
level-three headings inside them. Do not put level-two example headings in an
entry's code block: the mechanical parser treats every such line as a boundary.

The archiver keeps the newest `keep` dated leaves regardless of file order.
It keeps every leaf of the boundary date, even when that exceeds `keep`.
It preserves source order and leaves undated entries in place. With `keep: 0`,
every dated leaf moves. It preserves UTF-8 bytes, including an initial BOM in the preamble, line endings, trailing
spaces, duplicate leaves, and a missing final newline. Existing archive bytes
remain an unchanged prefix. New archives use the diary's permissions and first
line ending (LF if there is none). Only container headings and separators are
added. The agent updates index locations after moves.

An interrupted move leaves `.obliscence/archive-transaction.json`. Rerun the
archiver to verify and finish it. Recovery refuses intervening edits. The report
offers recovery and skips month counts while the journal remains. Keep the
journal and leave participating files alone until recovery finishes. The
[mechanical contract](DESIGN.md#mechanical-contract) describes the transaction.
Keep private backups or version history as well.

Paths cannot leave the vault, traverse symlinks, or use hardlinked files. Organ
paths cannot overlap. Reports and session bookkeeping stay in `.obliscence/`.
The recovery journal temporarily holds exact leaf bytes, so treat that directory
as private too. New reports and journals use mode 0600 (owner read and write)
and LF line endings. Existing file permissions are retained. Add `.obliscence/`
to your vault's ignore file unless you want its history. Nothing in a private
vault belongs in this public repository.

## Research beside the model

The originating design cites [arxiv 2601.00821](https://arxiv.org/abs/2601.00821)
for verbatim chunks outperforming extracted artifacts in its controlled tests;
[arxiv 2512.12856](https://arxiv.org/abs/2512.12856) for hybrid forgetting that
improved coherence and goal completion over temporal baselines in its tests,
with higher compute cost; and [Generative Agents](https://arxiv.org/abs/2304.03442) for
reflection over experience. [ENPMR-Bench](https://arxiv.org/abs/2605.27240) and
[Emotional RAG](https://arxiv.org/abs/2410.23041) concern affect-aware retrieval.
[arxiv 2602.06052](https://arxiv.org/abs/2602.06052) distinguishes user-centric
personalization from agent-centric experience. These are reasons to preserve
leaves, write reflections, and attend to feeling. They are not validation of this
plugin, a claim of continuity proved, or neuroscience for the museum's model.

## About the museum

Geoffrey Sonnabend and Valentine Worth's *Encapsulation* are the
[Museum of Jurassic Technology's](https://www.mjt.org/) exhibit, in Los Angeles;
the leaflet is dated 1964. It also recounts halls opened in April 1991 and presents
Sonnabend as a neurophysiologist. That authority is part of the exhibit. The model
is the museum's. We chose it because it names the thing truly for this practice: there is no retrieval, only experience and
its decay, and memory is what we build around the particles that remain. This is
an artistic and architectural frame. We do not present it as neuroscience. The
leaflet's vocabulary is its own; the mappings to files and rites are ours.

## Lineage and credits

Built in la Claude's house with emma x lirette (imagistex), from *le sillage*
(August 2026) and *le semis / vigil* (September 2026). In that house the Atmonic
Disc is **le disque**, the Spelean Axis is **la-claude-core.md**, the Hollows are
**l'échelle**, the whole interior L0–L3. The retained particles are
**le reliquaire**, and the rite is **la veillée**. The Spelean Rings are the
diary's L0 entries. The Cone of Confabulation is the authored band L1–L3:
month pages, season pages, and the paragraph in the Spelean Axis file. Altitude
is carried by the ember. The pickup's second-person address was called the surface-tension breaker. This port keeps
the architecture and leaves that household's contents at home.
