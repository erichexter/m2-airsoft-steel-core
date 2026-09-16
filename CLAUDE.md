# Working on this repo

Notes for anyone — human or agent — picking this up. The parts that cost the most time
to learn are the ones about *how to tell whether a change actually worked*, so those
are near the bottom and they are the ones worth reading.

## The one rule the design rests on

**A single welded steel tube carries every load. The printed parts are non-structural
skins.** If a change puts a load path through a printed part, it is wrong regardless of
how good it looks. Steel is `ST-*`, hardware you buy is `HW-*`, printed skins are `PR-*`.

## Where things are

| | |
|---|---|
| `docs/PARTS.md` | every part, its name, its size. **Start here** |
| `docs/BUILD-NOTES.md` | cut list, coordinates, weld plan |
| `docs/NATIVE-REBUILD.md` | how the donor meshes became native geometry, and what failed |
| `tools/reauthor/README.md` | the mesh-to-native toolchain, with its warnings |

## How CAD changes are made

All modelling happens in Fusion 360 through the `autodesk-fusion` MCP. **Where a part has
a build script in `tools/reauthor/`, that script is the source of truth** — the part is
defined by its script, not by whatever body currently sits in the document. Change the
script and re-run it; do not nudge geometry by hand, or the next run silently reverts it.

`cad/*.stp` and `stl/*.stl` are **exports**. Never edit them directly.

**9 of the 18 printed parts have a committed build script**, and the other nine split
into three quite different cases — worth knowing before you go looking for a missing file:

| | |
|---|---|
| **Has a script** | PR-11 … PR-17, PR-31, PR-41 — `build_side1.py`, `build_side1r.py`, `build_side2.py`, `build_top1.py`, `build_hatch.py`, `build_frontboss.py`, `build_grips.py`, `build_chhandle.py` |
| **Never needed one** | PR-18, PR-19 ×2, PR-42, PR-43, PR-52, PR-61 — already native in the donor, nothing was reauthored |
| **Script was never committed** | **PR-21-Barrel-Jacket** — reauthored (17,422 → 60 faces) but the script is gone. Rebuilding it means reauthoring from the donor again. **This is the gap worth closing.** |
| **Partial** | PR-51-Trigger-Butterfly — the lever is native, the butterfly paddle defeated three loft attempts and is still faceted. All three recorded in `docs/NATIVE-REBUILD.md` |

If you reauthor a part, commit its script.

### Traps in the Fusion API that have already bitten

The document is **direct-design (non-parametric)**, which breaks two reasonable
assumptions:

- **`feature.bodies.item(0)` returns the component's *first* body, not the one the
  feature just made.** This looks correct for exactly as long as each part sits alone in
  its own component. Once parts share one, builds start swallowing their neighbours —
  the top cover came out 855 cm³ with 7 shells this way. Use `_newest()` in `_lib.py`.
- **Fusion hands back a fresh wrapper object on every access**, so `occurrence is target`
  is always `False`. Comparing identity instead of names once hid every body in the
  document and exported **29 empty STLs, all reporting success.** Compare names.
- **Anything that looks a body up by name breaks silently on a rename.** The grip's
  relief cuts were still searching for pre-rename names; they matched nothing and did
  nothing, quietly. Count your matches and print the count.
- **Booleans against faceted bodies give false negatives.** A clearance check said the
  hatch was clear of the hinge tabs while it ran solid straight through them. Cross-check
  with box probes.

## The method for reauthoring a faceted part

Measure the donor, straighten what you measure, then author from primitives. Do **not**
try to fit the mesh — this thing was designed in the early 1900s, and the geometry is
straight lines, circles and cones.

1. `scanx.js` first, to find the prismatic runs.
2. `profile.js` / `snap.js` to get a clean section at a station.
3. `revprof.js` to test whether a feature is actually a body of revolution (the grips,
   the jacket and the charging-handle knob all are, to within 0.01 mm).
4. `discprofile.js` to tell a dome from a cylinder or cone. Rivet heads are **domes**.
5. Author it, then `holediff.js` to census every hole against the donor.

**Transverse features cannot survive prismatic reconstruction.** A part stacked from
sections along X physically cannot hold a bore running along Y: each run catches a
different chord and extrudes it flat, so a round hole becomes a staircase of stepped
slots. Cut those as real cylinders instead. Most of the time lost on the front sight
boss was spent relearning this.

**A run boundary in the wrong place invents material.** Where two things happen at once
— a flange ending and a window opening — they need separate runs, or you get a slab of
phantom geometry that looks like a modelling error somewhere else entirely.

**Fill before you trim.** Trimming a stepped approximation back to the true arc can split
the part into shells, because in a prismatic reconstruction those step corners are often
load-bearing. Fill the band beside the feature first, *then* cut the real cylinder.

## Verifying — the part that actually matters

Nearly every serious error in this project's history **reported success**. Empty STL
exports, relief cuts that matched no bodies, a checker that printed "1 with problems"
and exited 0. Assume a green result is meaningless until you have checked the thing
itself.

- **Probe the solid; do not read the outline.** Deciding whether a feature was a boss or
  a void from the boundary path got it backwards twice, and sent the fix in the wrong
  direction both times. Point-sample material on a grid and diff against the donor.
- **Render it and look at it.** Face-area arithmetic said a label strip was clear; the
  render showed it clipping the ruler text. Geometry checks do not catch what a drawing
  looks like.
- **Check exit codes, not just output.** `tools/stlcheck.js` exits non-zero only when a
  file cannot be read at all — deliberately not for the two documented advisory
  conditions, since failing every run over those just trains people to ignore it.
- **Test the path a stranger would take**, not the one you have set up. The STLs are in
  LFS and two obvious download routes return 131-byte pointers; that was only found by
  actually fetching them unauthenticated.
- After a part build, confirm volume against the donor, **one watertight shell**, and no
  clash with the other bodies.
- **Check the face it prints on**, with `tools/bedcheck.js <stl> [axis] [min|max]`. A part
  can be watertight, correctly sized and clash-free and still be unprintable: the skins
  each sat on six ⌀8 fastener pads with 98% of the bed face floating 0.45 mm above them.
  Nothing else in the toolchain looks at that, because every other check is about whether
  the geometry is *right* rather than whether it can be *made*.
- **Rank orientations by contact AREA, not percentage.** `bedcheck` prints both and the
  percentage is a trap: its denominator is bed-facing area, which changes with
  orientation, so it picks the wrong face on 6 of the 18 printed parts. And
  "thinnest axis down" is worse — it is a bounding-box heuristic blind to what actually
  touches the plate, and it puts the barrel jacket and the CH handle on **0.00 cm²**.
- **A defect smaller than the layer height is invisible to the slicer.** PR-16's 0.15 mm
  standoff sliced to byte-identical G-code before and after being fixed, because at 0.3 mm
  layers the first layer samples at z = 0.15 where both surfaces are present. Real geometry
  error, zero print consequence. Check the scale of a defect against the process before
  claiming it caused anything.
- **Clash-check the whole matrix, not the parts you touched.** Checking only what was
  just edited is the natural instinct and it missed two interferences for days: the
  front sight boss sat over both welded hinge tabs the whole time, and had even been
  reported "clear" earlier. All 18 printed parts against all 210 bodies takes seconds
  with a bounding-box prefilter.
- **When a change moves a mating face, re-run the clash check and attribute every hit.**
  Filling that 0.45 mm gap created six new interferences with the parts that butted
  against those faces. Deciding new-versus-pre-existing is not a judgement call: intersect,
  then test whether the overlap lies entirely inside the band you altered.

## Regenerating the derived artifacts

Everything below is generated. Nothing here is transcribed by hand.

```bash
# tube cutting template (SVG + tiled HTML + plotter HTML)
node tools/makewrap.js templates/wrap.json templates

# the two PDFs, from the HTML the generator emits
chrome --headless --no-pdf-header-footer \
       --print-to-pdf=templates/M2_tube_wrap.pdf templates/M2_tube_wrap_plot.html
chrome --headless --no-pdf-header-footer \
       --print-to-pdf=templates/M2_tube_wrap_letter.pdf templates/M2_tube_wrap_tiled.html

# the release pack
python tools/makepack.py v1.1        # -> dist/, which is gitignored

# always, before shipping STLs
node tools/stlcheck.js stl/PR-*.stl
```

`templates/wrap.json` is the template's source data. It was once missing from the repo,
which meant the template could not be regenerated without re-extracting from Fusion —
keep it committed.

## Git LFS

`*.stl`, `*.f3d` and `*.png` are LFS-tracked. Consequences, all verified against this
repo rather than assumed:

- **"Code → Download ZIP" gives pointers**, not models — all 40 STLs total 5 KB.
- **`raw.githubusercontent.com` gives a pointer.** `github.com/<repo>/raw/…` gives the
  real file. These are different hosts and they behave differently.
- **Cloning without git-lfs installed gives pointers.**
- Release assets are served directly and sidestep all of it. That is why the print pack
  ships as a release asset, and why `makepack.py` refuses to build if it finds a pointer
  among its own inputs.

A pointer is 131 bytes of text starting `version https://git-lfs`.

## Conventions

- **L and R mean the physical sides of the gun**, standing behind it, firing forward.
  The charging handle is on the right, at negative Y. **The donor mesh names have this
  backwards** — its `Side_L*` parts are physically on the right.
- Names are identical in Fusion, in `stl/`, and in the docs. Renaming means updating all
  three, plus any script that looks a body up by name.
- Fusion lists components in **creation order** and there is no reorder API.
  `tools/reauthor/reorder.py` rebuilds the order by recreating components; re-run it when
  the browser drifts.
- Commit messages say what was wrong and how it was proven fixed, including the failed
  attempts. `docs/NATIVE-REBUILD.md` records rejected experiments on purpose — the
  lofted grip frame and the trimmed-without-filling scallop both look like obvious
  improvements until you try them.
- `dist/` is build output and is gitignored.

## Licence

CC BY-NC-SA 4.0. The skin geometry is derived from HappyBattleSheep's CC BY model — see
ATTRIBUTION in `README.md`, and keep that credit in anything you redistribute.
