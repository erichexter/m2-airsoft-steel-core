# Bed levelling test

`bed-level-squares.stl` — five concentric single-layer frames. Nothing else. Regenerate with `node tools/bedlevel.js`.

**`tools/bedlevel.js` is the source of truth for the STL.** There is also a copy in the
Fusion model (`tools/reauthor/build_bedlevel.py` → `00_Ref_Test_Artifacts` /
`RF-90-Bed-Level-Squares`) so the thing can be seen and measured alongside the gun. The
constants are duplicated in both files and nothing keeps them in step — change one,
change the other.

Two things about where the Fusion copy lives, both deliberate: it sits in a `00_Ref_*`
component, which every clash and audit script in this repo skips, and it is parked at
**Z −400**, well clear of a gun that bottoms out at Z −92. Without both, a 290 mm square
lying at the origin would intersect the tube and most of the skins, and every
interference check in the project would come back garbage.

Built for the **K1 Max at 0.6 nozzle / 0.3 mm layer**. Three numbers are tied to that:

| | | why |
|---|---|---|
| height | **0.30 mm** | exactly one layer. A test artifact thinner than the layer height gets rounded up or dropped at slice time — the trap `PR-16`'s 0.15 mm standoff fell into |
| width | **1.20 mm** | exactly two 0.6 mm beads. Slices predictably anywhere, and under-squish shows as a visible gap down the middle |
| outer frame | **290 mm** | Creality Print refuses real geometry at 297.6 mm on this bed — bracketed at 296.1 rejected / 294.6 accepted. 290 leaves margin without giving up the edges, which are the part you care about |

**Change the layer height → change `H` in `tools/bedlevel.js` and regenerate.**

## Printing it

- **No brim, no raft, no supports.** 0% infill is irrelevant, it is one layer.
- Same first-layer settings you intend to use for real parts, or the test tells you
  nothing about them.
- 5 separate shells is expected, one per frame.

## Reading it

Look at each ring, and compare sides *within* a ring rather than between rings:

| what you see | what it means |
|---|---|
| glassy, wide, beads merged flat | over-squished — nozzle too low there |
| rounded, narrow, a gap down the middle | under-squished — nozzle too high there |
| one side of a ring differs from the opposite side | **tilt**, not nozzle height |
| outer ring poor, inner rings fine | the bed is domed or the mesh does not reach the edges |

The concentric layout is what separates those last two from a simple Z-offset error: a
Z-offset problem looks the same everywhere, tilt does not.


## Context for this machine

The stored mesh on this K1 Max spans **0.665 mm** — 2.2 layer heights at 0.3 mm — with
the left end at +0.44 to +0.21 and the right at +0.10 to +0.12. The probe grid also stops
at x 295 while parts run to x 297.8, so the outer few mm are extrapolated. Expect the
right side to read under-squished relative to the left until that is fixed.
