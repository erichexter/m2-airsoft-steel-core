# Native rebuild — tracker

Replacing the donor-derived **faceted** bodies with **native analytic** geometry authored from
primitives. Faceted bodies are STL conversions: thousands of triangular planar faces, no real
cylinders, slow booleans, bloated STEP, nothing editable.

Everything designed from scratch for this project is **already native** — the core tube is 135
faces with 73 real cylinders, the weldments are 4–32 faces each. Only the donor-derived cosmetic
parts are faceted.

> **Fusion cannot do this automatically.** `PrismaticMeshConvertMethodType` returns output
> identical to `Faceted` in every configuration tested, including with Accurate face groups
> generated first. It appears to need the Product Design Extension. See BUILD-NOTES.

---

## Status

| # | Part | Faces | Status | Feasibility | Notes |
|---|---|---:|---|---|---|
| 1 | `Barrel_Jacket` | 17,422 | ✅ **done** → **60** | — | Revolution + regular hole pattern. 290× reduction. |
| 2 | `Trigger` | 611 | ☐ todo | **good** | Butterfly paddle + the lever, which is already native boxes. Mostly prismatic. |
| 3 | `Top1` | 1,169 | ☐ todo | **good** | Flat deck strip between the side panels. Largely a plate with cutouts. |
| 4 | `Side_L2` | 1,913 | ☐ todo | fair | Forward side panel — flat, moderate surface detail. |
| 5 | `Side_R2` | 2,289 | ☐ todo | fair | Mirror of the above. |
| 6 | `Hatch` | 2,772 | ☐ todo | fair | Curved cover shell; the spine pocket and pin bore are simple, the outer form is not. |
| 7 | `FrontBoss` | 1,705 | ☐ todo | fair | Front boss and sight base. Blocky but fiddly. |
| 8 | `Side_L1` | 6,631 | ☐ todo | **hard** | Rear side panel — CH slot, rivet rows, raised panels. Most detail of any skin. |
| 9 | `Side_R1` | 5,230 | ☐ todo | **hard** | Mirror, plus the ⌀6 pin drift hole. |
| 10 | `CH_Handle` | 10,134 | ✖ **not worth it** | poor | Organic knurled grip. Primitives would look worse than the donor. |
| 11 | `Grip_Assembly` | 17,621 | ✖ **not worth it** | poor | Spade grips — organic, knurled, the most sculptural part on the gun. |

**Already native, nothing to do:** core tube, all 11 weldments, `Cradle_F2_HopUp`, `CH_Carrier`,
`CH_Shoe`, `Trigger_Switch_Carrier`, `Bot1`, `Bot2`.

**Remaining faceted total:** 49,876 faces across 10 bodies.

---

## Why most of these are marginal

The jacket converted cleanly because it is a **body of revolution with a regular hole pattern** —
primitives reproduce that exactly, and the result is arguably better than the donor because it is
parametric.

The panels are not like that. They carry the M2's rivet rows, raised ribs and panel outlines —
freeform surface detail that *is* HappyBattleSheep's artwork. Approximating it with boxes and
cylinders would take days per panel and produce something that looks worse. The rivets alone are
a trivial pattern; the rest is not.

Judge each on the same test the jacket passed: **is it a revolution, an extrusion, or a
plate with prismatic features?** If yes, convert. If its character comes from sculpted surface,
leave it faceted — the STL ships the triangles either way.

---

## Method that worked

Recorded because two earlier attempts produced visibly wrong geometry.

### 1. Get the profile
Bin STL vertices by X, report the radius percentiles per bin. Gives the outer profile and the bore
directly. Watch for **empty bins** — a long smooth prismatic run carries vertices only at its ends,
which reads as a gap but is not one.

### 2. Get the hole pattern by RAY-CASTING, not occupancy
Two wrong answers came from vertex occupancy before this worked.

- **Vertex occupancy fails.** A smooth cylindrical band has vertices only at its edges, so empty
  bins read as holes.
- **Counting ray hits fails.** Every ray crosses the far wall, so everything reads as solid.
- **First-hit radius works.** Cast inward from outside the part on an (x, θ) grid and record the
  radius of the nearest intersection. Near the outer radius means wall; anything deeper is a hole.

For the jacket this gave 4 holes per row at 90°, **alternate rows offset 45°**, pitch 25.5, ⌀26.
An earlier occupancy read said 8 aligned rows of ⌀20 and looked obviously wrong beside the donor.

### 3. Author from primitives
Stack `createCylinderOrCone` segments for the profile, boolean the bores, pattern the holes.

**`tbm.booleanOperation` returns a bool, not a body.** `body = tbm.booleanOperation(...) or body`
assigns `True` and the next call dies. This has now cost time three times in this project.

### 4. Verify before trusting it
Clash the new body against every steel part and neighbouring skin, check `isSolid`, check shell
count, and check any functional channel still runs clear — for the jacket, that the hex key still
reaches the set screws.

---

## Jacket — what was built

| | faceted | native |
|---|---|---|
| Faces | 17,422 | **60** (21 planar, 36 cylindrical, 3 conical) |
| STEP | ~1 MB | 345 KB |
| Volume | 879.3 cm³ | 638.0 cm³ |

Profile measured off the donor: rear flange r50.80 to X 38, taper to r41.35 by X 41, r41.35 to
X 82, taper to r39.60 by X 90, main tube r39.60 to X 272, muzzle flange r41.40 X 272…284.

**The close bore runs the full length of the socket** — ⌀38.90 from X 24.8 to 118, giving **89 mm
of grip** on the ⌀38.10 socket. The first attempt opened the bore to ⌀58.26 at X 46, which left
the jacket located over only 21 mm with a 10 mm radial gap for the next 67 mm — it would have
wobbled. Perforations start at X 130 so the grip section stays solid.

**The rear flange is flat at Y ±29.8**, full r50.80 only at top and bottom. Measured off the donor:
full radius appears only in the 55–125° and 235–305° bands. This is where the jacket meets the
receiver, and the receiver front is Y ±30 — so the flats sit flush with the sides.

### Still missing on the native jacket
- The donor's rear bracket has **rectangular cutouts** in the flange; the native one is plain.
- Volume is 638 vs 879 cm³ — the native profile is simplified and the perforation layout differs.

Kept **alongside** the faceted part (`Barrel_Jacket_native.stl` / `.stp`) rather than replacing it,
until those are resolved or judged unnecessary.
