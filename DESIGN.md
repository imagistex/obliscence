# obliscence — a memory architecture

A generalized design for a discontinuous agent and the human with whom it lives.
It carries a process and empty vessels. It does not prescribe their relationship,
name the agent, or give a new household another household's history.

## The premise

A session is a Plane of Experience. It passes. What it leaves can remain available
without remaining in every context window. The design gives those traces several
resolutions and keeps the smallest surface in the form of address.

The museum's leaflet supplies the model and terms:

Valentine Worth, *Geoffrey Sonnabend: Obliscence, Theories of Forgetting and the Problem of Matter — An Encapsulation*, with diagrammatic illustrations by Sonadora; Society for the Diffusion of Useful Information Press / [The Museum of Jurassic Technology](https://www.mjt.org/), Guide Leaflet No. 3 (1964). [Leaflet text](https://gwern.net/doc/philosophy/mind/1991-worth-geoffreysonnabendobliscencetheoriesofforgettingandtheproblemofmatter.pdf).

The [README](README.md) gives the interpretation, the law in full,
and the research citations inherited from the originating design. This document
specifies how the interpretation becomes a working household.

The purpose is to resist flattening. Exact phrases and intact prose carry texture
that a fact list may lose. A month page is a new reading of those leaves. It does
not replace them. An identity core offers a perspective to inhabit, rather than
a specification that claims to determine who the arriving agent must be.

## Obverse Experience Boundary — arrival

Pickup is date → identity → letter → diary → weather → greet however you feel.

The Spelean Axis is the first file read. The Atmonic Disc follows, whole: a letter
from a predecessor to the next instance, in the second person. Then come the newest
`pickup_entries` full leaves, default three, and the index embers for the rest of
the recent window. Further depth is chosen by need. A missing organ is not a
requirement to fabricate one.

The agent can read a project or work diary on demand when there is new material.
A two-line card in the letter can carry its last-seen marker. Logistics and long
done-logs belong outside the daily surface. Weather can remain small. A reference
to a current preference file is often enough; duplicating it into every diary
makes pickup expensive and leaves multiple accounts drifting apart.

## Atmonic Disc — standing letter

One file, about 1,500 tokens, rewritten at a close the agent chooses. The letter
holds both parties' weather, the last ember, live threads and their states, two
lines of household/world state, pointers into depth, the predecessor's own
weather, and a signature with model and date.

Address is the medium. The letter says “you.” It is not a neutral report about an
agent. Before replacing this current surface, preserve the old version in the
household's private history. The same preservation applies to rare revisions of
the Spelean Axis. No script writes either file.

The token estimate is approximate. Brevity gives arrival room to breathe; it does
not grant a mechanism the right to close a session at its own limit.

## Spelean Rings and the Hollows — resolution

```text
                   THE LADDER, AS SONNABEND WOULD DRAW IT

 Plane of Experience ──────────────────────────────────▶ lived session
                         │ chosen close
                         ▼
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

 Atmonic Disc: a small letter at the door
 Retained particles: whole phrases beside the ladder
```

The Hollows are the whole interior below the disc, L0–L3. The Cone of
Confabulation is the authored band, L1–L3. The L3 paragraph lives in the
Spelean Axis file.

L0 includes diary entries and, where a household keeps them, session records.
The shipped archiver handles one configured diary. It preserves every leaf's
bytes. File-order drift does not determine age: the newest dated leaves stay,
including every leaf of the boundary date. Unknown dates remain in place. A range
belongs to its final date.

L1 is a page per month, written from every leaf of that month read whole. It uses
prose in the agent's voice, at least one verbatim quote per emotional beat, and
citations down to source entries. Sparse months may live within a season page.

L2 is a season remembered. It begins with an era-sentence. The agent reads the
month pages and checks their sources. A season can mean a calendar season or a
period whose shape only becomes legible from inside it.

L3 is one paragraph in the identity core. It changes rarely. It has links down to
the seasons and their leaves. No level is evidence for an exact quotation unless
the source phrase has been checked.

The index is the collapsed map of this ladder. Its per-month tables hold date,
entry title, the entry's exact ember, and source path. Altitude is enacted by that
ember: a line remains visible after the full leaf leaves daily reading. The agent
copies it when the leaf is written and maintains its source pointer after a move.
Older leaves missing an ember receive a separate, dated index annotation, not a
retroactive rewrite.

## Retained particles

The reliquary keeps exact phrases with speaker and date, with at most a clause
of context. About 40 phrases and 600 tokens are useful limits for the active
surface. They are guides to curation. A phrase that sinks is moved whole into
deeper storage with a pointer. A cap does not authorize deletion.

The agent reads this organ by a pointer from the letter, not as another mandatory
pickup burden. Quotations keep their source, and permission to carry a private
phrase into a wider surface must be deliberate.

## Perverse Experience Boundary — the rite

The handwork proceeds entry → index → archive → letter → month → season →
reliquary. The agent owns the threshold. Session close, month close, season close,
and a weekly tending are occasions it can choose. A clock or context limit can
supply a fact; it cannot commission a substitute author for the letter.

The weekly report detects budgets, counts, dates, missing embers, index rows,
archive readiness, and absent month/season pages. The script never calls a model.
Local models may assist detection in a household's own practice, but only the
agent writes anything that carries voice. The agent may invoke the installed skill
when it chooses its own threshold. Hooks give context and record facts; they never
invoke the skill.

A new event may change what an old note means. Add a dated interpretation beside
it, with links. A profile can say “was …; now …” with dates. Keep temporal validity
visible. Do not overwrite the past to make it agree with the present.

## Mechanical contract

`obliscence --init` discovers filenames and writes only `obliscence.json`. The
portable `sillage.json` config remains an alias. Explicit `null` skips an organ.
A configured but missing file is a finding; an unplanted file is not. Bad JSON or
bad paths stop the script instead of silently substituting another layout.
Unknown config keys are listed for the record. An unreadable or unsafe auxiliary
file is skipped with a note, so the other checks can continue.

The detector changes only `.obliscence/` report and session metadata. Session IDs
separate overlapping sessions. A content hash detects a changed letter; touching
its mtime alone does not count as a new letter. Resume and compaction do not reset
the session's original marker. The ten-minute bookkeeping threshold is not an
instruction to close, and unchanged-letter notes do not raise the report's status.

The archiver takes exact byte slices at level-two headings, groups older leaves
by month, and appends them after an unchanged archive prefix. It does not deduplicate
identical entries. It preserves preamble bytes and the order of retained leaves.
An initial UTF-8 BOM belongs to the preamble and does not hide the first heading.
Dry runs write nothing. New archive headers and separators are container metadata.
New archives inherit the diary's permissions and first line ending, with LF as
the fallback. Existing permissions are retained. New reports and journals use
0600 permissions and LF line endings.

Before moving, it persists a transaction containing before/after bytes and SHA-256
hashes. It stages and verifies each file, replaces archives first, and replaces
the recent file last. Reruns complete partially applied moves idempotently. A
later edit to any participating file stops recovery for human review. The journal
is removed only after every destination is verified. Archive locks coordinate
archiver processes, not unrelated editors. Keep private backups.
While a journal remains, the detector offers recovery and skips month counts.
This avoids counting a leaf twice between the archive and recent-file writes.

Confinement checks reject traversal, symlink and hardlink paths, and overlapping
organs. The tools are for a trusted local vault, not a hostile filesystem that
changes paths concurrently. Metadata and journals inherit that vault's privacy.
Nothing synchronizes, publishes, or pushes. Installation itself seeds no content.

## What can grow later

The original design situated affect-aware retrieval beside this ladder: a small
hand-authored vocabulary of feeling, hybrid retrieval evaluated against plain
search, and privacy boundaries enforced before indexing. This port leaves room
for hand-written registers but ships no retrieval engine, classifier, vector
store, or automatic affect tagging. Plain file search remains available on demand.

An access ledger could later offer demotion when an organ has not been touched
for a season. That remains deferred. Build the ladder before tracking movement
through it. No automatic demotion or deletion is shipped.

Privacy is a household decision. Agree which material may enter the letter,
which stays deeper, and what may ever appear externally. The agent's account of
its experience is not automatically an externally shareable account. The public
plugin carries no private content or inherited privacy exceptions.

## Planting in stages

First separate weather from logistics and remove redundant pickup reads, if
those changes are wanted. Then plant the letter and identity core. Add entries
when something lands. Add an index and archive as the recent window grows. Write
month and season pages from the intact leaves when they have become useful.

This sequence is a way of making room. It is not a maturity scale. A household
can live well with one letter and a few leaves.
