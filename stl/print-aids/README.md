# Print aids

**Not design geometry.** These are the fitted parts with sacrificial pads added for bed
adhesion. Print these *instead of* the versions in `stl/`, then snap the pads off.

| file | |
|---|---|
| `PR-11-Side-Rear-L-ears.stl` | four ⌀20 × 0.6 mm mouse-ear pads at the contact-patch corners |
| `PR-12-Side-Rear-R-ears.stl` | the same |

Regenerate with `tools/reauthor/print_aids.py`.

## Why only these two

They are the 295.6 mm parts. PLA contracts about 0.4% as it cools, so each one is trying
to shrink **~1.2 mm along its length — 0.6 mm at each end** — and that force peels the end
corners off the bed. Nothing else in the set is both this long and this flat.

## Why not just a brim

The design sits at the bed limit on purpose: `BUILD-NOTES.md` puts the seam at X −265
because *"max forward is X −260.6 before Side_1 exceeds the 300 mm bed."* At 295.6 mm on a
300 mm bed there is **about 1.1 mm of margin at each end** — nowhere near enough for a brim
in the direction the part is actually contracting.

So the pads grow **sideways** instead. Across the part there is 165 mm of spare bed, so each
pad reaches 10 mm past the edge in Z while adding only 1 mm in X. It still resists the
lifting moment at the corner, which is the whole job. Added bond: **~157 mm² per corner,
6.3 cm² total.**

## Two things that will bite

**Footprint is 297.6 × 155.1 mm — 1.2 mm clear at each end on a 300 mm bed.** Centre it
properly. If the slicer nudges the part even 1.5 mm off centre, a pad is off the plate.

**Pad thickness is tied to layer height.** 0.6 mm is exactly two layers at 0.3 mm. A pad
thinner than one layer either vanishes at slice time or gets rounded up unpredictably, and
a single layer tears instead of snapping when you pull it. **If you change layer height,
change `PAD_T` and regenerate.**
