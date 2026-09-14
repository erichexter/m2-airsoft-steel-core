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
discprofile.js measure a raised/recessed feature's diameter along its axis and fit
               a sphere, so a DOME can be told from a cylinder or a cone
revprof.js     first-hit radius on an (axis, theta) grid - proves whether a part is
               a body of revolution, and gives its radius profile if it is
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
- **Audit bounding boxes against the donor.** Four parts were built short because a
  run was stopped at a round number instead of where the geometry ends. Volume
  comparison hides this — 0.35 mm of missing boss costs almost no volume — but a
  bbox diff catches it instantly, and it needs no CAD package.
- **Check whether a round feature is a DOME before building it.** Every raised disc
  on this gun is a spherical rivet head, and the recessed ones are spherical dimples.
  Fit r² = R² − (s − c)²; a real sphere fits to under 0.3 mm. Remember a dome is a
  whole sphere, so its far half sits inside the part and can break out the back.
- **Never approximate a revolve with a stack of cone segments.** It is geometrically
  fine and renders as visible rings — it looks knurled. One `revolveFeature` through
  a fitted spline is 3 faces and actually smooth.
- **Put hole topology in any band-merge signature.** Merging bands keeps the first
  one's profile, so a slot that appears in only some of them is silently filled in.
- **`feature.bodies.item(0)` is wrong in a direct-design document.** It hands back
  the component's FIRST body, not the one the feature just made. That looks right
  only while each part sits alone in an empty component — the moment several parts
  share one, builds start swallowing their neighbours. Take the last body instead.
- **Fusion returns a fresh wrapper object on every access**, so `occurrence is
  target` is always False. Comparing identity instead of name silently hid every
  body and produced 29 empty STL exports that all reported success.
- **Anything that looks a body up by name breaks on a rename**, silently. Count
  what you matched and print the count.
- **Relief cuts want a little clearance, but not much.** Zero leaves coincident
  faces that tessellate non-manifold; 0.25 mm severed a thin mounting tongue into
  its own shell. 0.05 mm, plus `drop_debris()` to sweep up the wafers, worked.

## The build scripts

Worked examples, one per part, all run the same way: `exec` `_lib.py`, then the
part's profile data, then the build. Each writes straight into its catalogue
component under its catalogue name (see `docs/PARTS.md`), so rebuilding one part
leaves its neighbours alone.

`naming.py` + `reorganize.py` are the one-shot that applied the naming convention
to the whole model.

`render_docs.py` regenerates every image in `docs/img/` — nine assembly views and
one shot of each of the 32 parts. It colour-codes by class for the renders (steel
blue, hardware brass, printed grey) and puts the model's appearance back afterwards.
**Re-run it after any rebuild** so the pictures cannot drift from the geometry. It
takes a couple of minutes; run the assembly views and the part views as separate
calls or the Fusion MCP call times out (the renders still complete).

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
