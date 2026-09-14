# Wrap-around cutting template — 2×3 core tube

For marking out the tube by hand. Generated from the model, not transcribed:

```
node tools/makewrap.js wrap.json templates
```

| | |
|---|---|
| `wrap.json` | the source data — unrolled outlines, fold lines, extents |
| `M2_tube_wrap.svg` | one sheet, 1:1, **619.5 × 273.5 mm** including margin |
| `M2_tube_wrap_tiled.html` | the same drawing across **6 letter pages**, 12 mm overlap |

## Printing it

### At home — 6 letter sheets

Open `M2_tube_wrap_tiled.html` in Chrome or Edge and Ctrl-P:

| setting | value |
|---|---|
| Paper | Letter |
| Layout | Landscape |
| Margins | **Default** — the page sets its own 8 mm; "None" also works |
| Scale | **Custom → 100**, never "Fit to printable area" |
| Headers and footers | **off** — they push the drawing and force a rescale |

Six sheets come out labelled `r1c1 … r2c3`, row-major: top row left→right is the
breech half, bottom row is the muzzle half. **Measure the 100 mm bar on every sheet
before you cut anything** — it is printed on all six, because duplex and n-up
settings can scale sheets unevenly. Then trim each sheet on the grey corner crop
marks, overlap 12 mm, and tape.

### Copy shop or plotter — one sheet

Send `M2_tube_wrap.svg`. It is **619.5 × 273.5 mm**, so it needs a 24" roll, A1, or
ARCH D — it will *not* fit ARCH C (610 mm is 9.5 mm short). Ask for **100%, no
scaling, no fit-to-media**, and measure the calibration bar when you collect it.

## Using it

The drawing is the tube's perimeter unrolled flat. **The seam is on the bottom
centreline**, so the wrap runs: bottom(right half) → right side → top → left side →
bottom(left half). Breech is at the left of the sheet, muzzle at the right.

1. **Check the scale first.** There is a 100 mm calibration bar on the single sheet
   and on every one of the six tiled sheets. Measure them. If one isn't 100 mm your
   printer scaled the page and everything downstream is wrong — reprint with scaling
   off ("Actual size" / 100%, not "Fit to page").
2. Wrap it around the tube with the paper's edge flush to the **breech end** and the
   seam running down the **bottom** face centreline. It should meet itself exactly —
   the perimeter is 243.53 mm.
3. Tape, then centre-punch or scribe through the outlines.

## Reading the drawing

- **Solid black** — cut these.
- **Red dashed** — corner tangents, i.e. where the tube's R0.240" radii begin. These
  are fold lines for the paper, **not cuts**. They also tell you when a cut crosses a
  corner rather than staying on a flat.
- **Grey dashed rectangle** — the wrap boundary.
- **Grey vertical lines** — every 50 mm, labelled with the model's X coordinate.
  X is negative toward the breech; X 0 is near the muzzle end, so the numbers count
  up as you move right.

## Watch for

**The air line hole sits on the seam.** It's ⌀12.7 centred on the bottom centreline
at X −410, so it appears as two half-circles, one at each edge of the sheet. They
join when wrapped.

**The top opening runs corner to corner.** The cut at Z +24 lands 0.004 mm below the
corner tangent, so over X −310…−2 the entire top face and both upper radii are
removed. On the flat it is the full band between u 92.88 and 150.65.

**The belt slot and the top opening are one aperture.** They meet at X −141 and there
is no web between them.

**Locating tabs are material to leave, not remove.** Both ends carry 25 mm tabs on the
top and bottom faces — front at X +20…+26.35, rear at X −563.18…−560. Cut around them.

## Known model artifact

The tube body carries some 0.01 mm proud steps on the left wall, left over from
filling in an earlier charging-handle aperture. They are filtered out of this template
(by face area and coplanar-normal tests) and are far below any hand-marking tolerance,
but they are why the body has 101 faces where a clean build has 81. Worth rebuilding
the tube from the canonical script before sending the STEP anywhere for quoting.
