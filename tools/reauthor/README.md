# Reauthoring tools

Turning a donor STL skin into native Fusion geometry. The method that works is
**measure the mesh, straighten the measurements, author from clean primitives** —
never trust a mesh-to-BRep convert, and never approximate a plate with a loft.

## The pipeline

```
bbox.js        bounding box + dominant facet normal, to find the plate axis
scanx.js       cross-sectional area vs station -> where the prismatic runs and
               the breakpoints are.  THIS IS THE FIRST THING TO RUN.
profile.js     exact cross-section at one station, chained into loops, holes
               classified by containment, corners preserved (RDP)
snap.js        straighten: heavy RDP, then cluster coordinates onto shared values.
               The M2 is a 1918 sheet-and-plate design; mesh wobble is scan noise.
               Also splits ROUND loops out of the profile into `circles` (holes)
               and `discs` (rivet heads) so the build can cut/add them as real
               cylinders - a circle that goes through RDP comes back a triangle.
ascii.js       print a profile as an ASCII occupancy map so you can see it
sections.js    many sections at once, for the rare part that really is lofted
silhouette.js  rasterised projection outline (useful, but see the warning below)
_lib.py        Fusion side: sketch a region on any plane, extrude it, loft between
               regions, plus mm-based box/cylinder primitives
```

Typical run:

```bash
node scanx.js Hatch.stl x -334 -4 5            # find the runs
node profile.js Hatch.stl x -180 0.15 --json h_main.json
node snap.js h_main.json 0.6 0.05 0.30         # -> h_main_s.json
node ascii.js h_main_s.json                    # eyeball it
```

then feed the snapped regions to `extrude_region` / `loft_regions` in Fusion.
`build_hatch.py` and `build_top1.py` are worked examples.

## Warnings paid for the hard way

- **Vertex-based slab filtering fails on prismatic runs.** A 200 mm straight run
  carries vertices only at its ends — one triangle spans the whole length. Filtering
  triangles "whose vertices lie in X between a and b" returns nothing in the middle
  of the part. Always slice with a plane (`profile.js`), never bin vertices.
- **Booleans against faceted bodies lie.** The donor hatch reported *clear* of the
  steel hinge tabs while being solid straight through them. Cross-check any
  mesh-body clash result by intersecting with small probe boxes and reading volumes.
- **`tbm.booleanOperation` returns a bool, not a body.** Assigning its result to the
  body variable stores `True` and the next call dies. Four times now.
- **Don't loft a shape whose character changes.** Lofting the trigger's butterfly
  paddle produced melted geometry three different ways (arc-length resampling,
  angular resampling, and two-view silhouette intersection). Loft only where the
  section stays the same *kind* of shape along the run.
- **Snapping must not eat real dimensions.** An early pass rounded 12.70 — half an
  inch, the tube notch — up to 13. Keep the round-number tolerance under 0.06 mm.

## The build scripts

Worked examples, one per part, all run the same way: `exec` `_lib.py`, then the
part's profile data, then the build.

```
build_top1.py       simplest - six prismatic runs and six blind holes
build_hatch.py      prismatic runs, straight ramps, swept hinge clearance
build_side2.py      layered plate, one function building both hands via a sign flip
build_side1.py      five stepped tiers, rivet heads, d19 boss
build_side1r.py     same, plus arithmetic rivet rows and a trimmed overhang
build_frontboss.py  six runs including twelve rectangular standoff ribs
```

Two habits worth keeping:

- **Generate regular patterns arithmetically, don't read them back.** Reading the
  rear rivet rows off the mesh missed a head and gave different diameters row to
  row. Two lines of `start + pitch * i` is exact and self-documenting.
- **Build mirrored parts from one function with a sign parameter.** `Side_L2` and
  `Side_R2` differ in exactly two features; a shared builder makes that explicit
  instead of letting the pair drift.
