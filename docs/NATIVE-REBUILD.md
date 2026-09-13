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
| 2 | `Top1` | 1,169 | ✅ **done** → **49** | — | All planes + 6 cylinders, no NURBS at all. Volume −0.9%. |
| 3 | `Hatch` | 2,772 | ✅ **done** → **122** | — | Prismatic runs + straight ramps. Volume −1.4%. **Fixed a real interference** — see below. |
| 4 | `Trigger` | 611 | ⚠ **partial** | mixed | The lever *is already native*; the butterfly paddle is sculpted artwork that defeated three reconstruction attempts. See below. |
| 5 | `Side_L2` | 1,913 | ☐ todo | fair | Forward side panel — flat, moderate surface detail. |
| 6 | `Side_R2` | 2,289 | ☐ todo | fair | Mirror of the above. |
| 7 | `FrontBoss` | 1,705 | ☐ todo | fair | Front boss and sight base. Blocky but fiddly. |
| 8 | `Side_L1` | 6,631 | ☐ todo | **hard** | Rear side panel — CH slot, rivet rows, raised panels. Most detail of any skin. |
| 9 | `Side_R1` | 5,230 | ☐ todo | **hard** | Mirror, plus the ⌀6 pin drift hole. |
| 10 | `CH_Handle` | 10,134 | ✖ **not worth it** | poor | Organic knurled grip. Primitives would look worse than the donor. |
| 11 | `Grip_Assembly` | 17,621 | ✖ **not worth it** | poor | Spade grips — organic, knurled, the most sculptural part on the gun. |

**Already native, nothing to do:** core tube, all 11 weldments, `Cradle_F2_HopUp`, `CH_Carrier`,
`CH_Shoe`, `Trigger_Switch_Carrier`, `Bot1`, `Bot2`.

**Remaining faceted total:** 46,546 faces across 8 bodies (was 49,876 across 10).

Converted so far: `Barrel_Jacket` 17,422→60, `Hatch` 2,772→122, `Top1` 1,169→49.
**21,363 faces of donor mesh replaced by 231 native ones.**

---

## The hatch could not close — found by rebuilding it

The steel hinge tabs are 1/8 in plate at Y ±19.18…22.35 with an arc top of r8 about
the hinge pin at (X −9, Z 62.5), rising to Z 70.5. **The donor cover is solid straight
through that corridor.** Fitted as drawn it fouls the tabs by roughly 12 mm and cannot
shut. The donor's clearance slots only begin at X −18; the tabs start at X −22 and are
already 66 mm tall by X −18.

This never showed up in the earlier clash audit because **the boolean against the
faceted donor reported "clear"** — a false negative. Probing the same corridor with
small boxes and reading the volumes showed it 100% solid. Faceted-body booleans cannot
be trusted; see `tools/reauthor/README.md`.

The native cover cuts the clearance as an **r8.5 arc about the hinge pin**, not a plain
slot — the tab has to clear at every angle of the swing, not just when shut. Verified:
0.00000 cm³ overlap with both tabs.

> The faceted `Hatch` still carries this fault. Print `Hatch_native.stl`.

---

## Trigger — the lever is native, the paddle is not

The functional half was already native and stays exact: riser X −580…−568 (Y ±7,
Z −6…32), arm X −568…−526 (Y ±6, Z −6…8), ⌀4.20 pivot bore on the Y axis at X −552,
⌀6 spring peg, ⌀3 front anchor.

The butterfly paddle resisted three separate reconstructions:

| attempt | result |
|---|---|
| Loft, arc-length resampling | Sections twisted — no point correspondence between them |
| Loft, angular resampling about the centroid | Filled the V notch; the sections are crescents, not star-shaped |
| Two-view silhouette intersection | Over-fills the wings — 840 mm² against an actual 396 mm² |

It is a compound-curved paddle with serrated thumb pads: the same class as
`CH_Handle` and `Grip_Assembly`, and the same verdict. Every attempt looked worse
beside the donor than the donor does. Left faceted at 611 faces, which is cheap.

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

### 2b. For plate and box parts, scan for prismatic runs first
`tools/reauthor/scanx.js` plots cross-sectional area against station. Long stretches
of identical area are constant-section runs — extrude those. Steps between them are
where the profile changes. The hatch turned out to be five constant runs and two
straight ramps; Top1 was six runs and six blind holes.

**Straighten before authoring.** `snap.js` clusters measured coordinates onto shared
values. The M2 was designed in 1918 out of flat plate — the wobble in the mesh is scan
noise, not intent, and straight lines both read better and model smaller. Keep the
round-number tolerance under 0.06 mm so real dimensions (12.70 = ½ in) survive.

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

---

## Hatch and Top1 — what was built

| | Hatch faceted | Hatch native | Top1 faceted | Top1 native |
|---|---|---|---|---|
| Faces | 2,772 | **122** | 1,169 | **49** |
| Volume | 516.81 cm³ | 509.83 | 472.87 cm³ | 468.63 |
| Difference | — | −1.4% | — | −0.9% |
| Symmetric difference vs donor | — | 2.2% | — | 1.3% |

**Hatch**: main run X −333…−119, widening to the front block over −119…−108, the
underside opening −101…−40, nose taper −32…−16, front sight aperture to −4.4. Three
hinge knuckles (r3.47 about Y 24.5, Z 67.03) and the rear sight base as a truncated
pyramid — which is what the donor actually is, a trapezoid in both elevations, not a
dome.

**Top1**: constant width Y ±25.8 throughout. Rear underside notches, a crowned main
run, the tall rear-sight block X −495…−432.5 with straight ramps at both ends, and six
⌀3.40 blind holes (Z 30.5…51.0) at X −526.7 / −413.5 / −356.9, Y ±18.

Top1 is entirely planes and cylinders — no NURBS at all.

### Still missing
- Hatch: the small top-centre slot near the rear (X ≈ −325) is not reproduced.
- Both: the donor's corner radii are replaced by straight chamfers, which is where
  most of the ~1% volume difference comes from. This is deliberate — the M2 is a
  plate-and-rivet design, and straight chamfers read closer to the real gun than
  the mesh's rounded-over edges do.
