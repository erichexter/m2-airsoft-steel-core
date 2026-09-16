# Printing the skins

Everything in the table below that is a **coordinate, footprint or orientation is measured
from the model** by `tools/bedcheck.js` and `tools/stlcheck.js`. Everything that is a
temperature or a speed is a **starting point** from one reported failure on one machine —
tune it.

Reference machine: **Creality K1 Max**, 300 × 300 × 300, textured PEI, **0.6 nozzle at
0.3 mm layer height**, PLA.

---

## Orientation — this is the part that matters

Each part goes on the face with the **largest measured flat contact area**. For the skins
that is the tube-mating (inner) face, which is what `tools/reauthor/flatten_mating.py`
made flat and what lets you iron the outside.

**Measure the area, not a percentage.** `bedcheck` reports both, and ranking by
"% of bed-facing area" picks the **wrong face on 6 of these 18 parts** — the denominator
changes with orientation, so a face with 73.7% of a tiny bed-facing total beats one with
42.7% of a large one while having a tenth the actual contact. Rank by cm².

| part | bed face | contact | height |
|---|---|---:|---:|
| `PR-11-Side-Rear-L` | Y min | 333.10 cm² | 24 mm |
| `PR-12-Side-Rear-R` | Y max | 337.45 cm² | 37 mm |
| `PR-13-Side-Front-L` | Y min | 218.80 cm² | 24 mm |
| `PR-14-Side-Front-R` | Y max | 218.80 cm² | 24 mm |
| `PR-15-Top-Deck` | Z min | 106.34 cm² | 66 mm |
| `PR-16-Top-Cover` | Z min, **rotated 45° about Z** | 118.77 cm² | 30 mm |
| `PR-17-Front-Sight-Boss` | X max | 32.41 cm² | 38 mm |
| `PR-18-Bottom-Rear` | Z max | 133.29 cm² | 26 mm |
| `PR-19-Bottom-Front-L` / `-R` | Y min | 11.06 cm² | 3 mm |
| `PR-21-Barrel-Jacket` | X max | 22.59 cm² | 262 mm |
| `PR-31-Spade-Grips` | Z min | 9.00 cm² | 126 mm |
| `PR-41-CH-Handle` | Y max | 14.96 cm² | 133 mm |
| `PR-42-CH-Carrier` | Y min | 15.96 cm² | 16 mm |
| `PR-43-CH-Shoe` | Y min | 4.95 cm² | 8 mm |
| `PR-51-Trigger-Butterfly` | Z min | 6.72 cm² | 63 mm |
| `PR-52-Trigger-Switch-Carrier` | Z max | 12.24 cm² | 43 mm |
| `PR-61-Engine-Cradle` | Z min | 57.90 cm² | 43 mm |

**"Thinnest axis down" is a bounding-box heuristic and it is blind to what is actually
touching the plate.** It fails on round shells and tall organic shapes. Placed that way,
`PR-21-Barrel-Jacket` and `PR-41-CH-Handle` both get **0.00 cm²** of flat contact — a
cylinder lying down touches on a *line* — and `PR-51` gets 0.08 cm². All three would have
gone to the plate resting on nothing.

Check any part with `node tools/bedcheck.js <stl> <axis> <min|max>`.

---

## The long panels warp, and a brim will not save them

`PR-11` and `PR-12` are 295.6 mm long. PLA contracts about 0.4% as it cools, so each is
trying to shrink **~1.2 mm along its length, 0.6 mm at each end**, and that force peels the
end corners off the plate.

A brim is not available in the direction that matters. The design sits at the bed limit on
purpose — `BUILD-NOTES.md` puts the seam at X −265 because *"max forward is X −260.6 before
Side_1 exceeds the 300 mm bed"* — which leaves **about 1.1 mm at each end.**

**Print `stl/print-aids/PR-11-Side-Rear-L-ears.stl` and `-PR-12-Side-Rear-R-ears.stl`
instead of the plain versions.** Four ⌀20 × 0.6 mm pads at the corners, growing sideways
into the 165 mm of spare bed rather than lengthwise into the 1.1 mm that is not there.
Snap them off afterwards.

The pads are **0.6 mm = exactly two layers at 0.3 mm**. A pad thinner than one layer gets
dropped or rounded up at slice time and looks like the fix failing. **Change layer height →
change `PAD_T` in `tools/reauthor/print_aids.py` and regenerate.**

`PR-13` / `PR-14` have 14 mm to spare. Just use a normal brim on those.

---

## Settings

Ordered by how much they mattered on the reported failure.

| | setting | why |
|---|---|---|
| 1 | **Auxiliary / side fan OFF for the first ~10 layers** | The K1 Max stock PLA profile runs it hard and it blows straight across a 296 mm first layer. Biggest single lever. |
| 2 | **Part cooling 0% for layers 1–3**, then ramp | Same reason, less severe. |
| 3 | **Keep the enclosure shut** | Chamber heat works *for* you against warping. Stock PLA profiles often want the door open — wrong for parts this long. |
| 4 | **First layer 30–50 mm/s, reduced acceleration** | The K1 Max does 20,000 mm/s². That is real shear on a marginally-attached 296 mm part. |
| 5 | **Bed 60 °C, soak 5+ min** | The edges lag the centre sensor, and these parts end exactly at the edge. |
| 6 | **Z-offset one notch lower** | At 0.6/0.3 an under-squished first layer still looks fine. |

**Do not add glue stick to textured PEI for PLA.** It generally *reduces* grip — it is for
PETG release and smooth sheets. Wash the plate with **dish soap and warm water**, not IPA;
IPA smears skin oils rather than removing them. Handle it by the edges.

**The usable envelope is smaller than 300 mm for real geometry.** Creality Print 7.2
refuses to place a 297.6 mm part at all — *"Nothing to be sliced … no object is fully
inside the print volume"* — while a featureless box of the same size slices fine.
Bracketed on the real mesh: **297.6 rejected, 296.1 rejected, 294.6 slices**, and
`PR-18` at 295.6 slices. Treat ~296 mm as the practical ceiling, not 300.

This is why the corner pads add **zero** length: they sit tangent to the part's ends, so
the eared files are 295.6 mm, exactly the same as the plain ones. The bond they add comes
from the half-disc overhanging *sideways*, which costs nothing in the constrained axis.

**A defect smaller than the layer height is invisible to the slicer.** PR-16 had an
0.15 mm standoff and sliced to **identical G-code before and after the fix — 171.99 g both
times.** At 0.3 mm layers the first layer is sampled mid-layer at z = 0.15, where both the
pads and the "floating" face are present. The fix added 1.39 cm³ and the floating band is
1.335 cm³ — i.e. the fix added exactly the material the slicer was already ignoring. The
geometry is correct now and it matters at finer layer heights, but **it changed nothing
about this print.** Check a defect against layer height before calling it a print problem.

**`brim_type = outer_brim` is silently ignored by Creality Print 7.2** and falls back to
`auto_brim`, which often decides a large flat part needs no brim at all. Accepted values in
that build are `auto_brim`, `outer_only`, `no_brim`.

---

## Debugging a failure

Match the symptom before changing anything:

| what you see | what it is | what to change |
|---|---|---|
| Corners lift at the **ends of the long axis**, middle stays down | contraction / warp | ears, fan, chamber heat |
| Whole part breaks free early, first layer **shiny, not squished** | Z-offset or bed temp | squish and temperature |
| Fails **hours in**, partway up | draft or cooling | close the enclosure, drop fan |
| **Nothing sticks anywhere** from the start | surface contamination | wash the plate — *this* is when glue is the answer |

**Validate settings on `PR-13` or `PR-14` first.** They are 271 mm with brim room, so if
those still lift, the problem is the plate or the Z-offset and the ears will not save the
long ones either. Six hours is a long time to find that out on `PR-12`.

---

## Material

**3,542 cm³ across 18 parts — about 4.4 kg of PLA at 100% infill**, and considerably less
in practice. These are non-structural skins; the steel carries everything. There is no
reason to print them solid.
