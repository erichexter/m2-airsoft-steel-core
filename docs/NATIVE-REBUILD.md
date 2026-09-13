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

| # | Part | Faces | Status | Volume | Notes |
|---|---|---:|---|---:|---|
| 1 | `Barrel_Jacket` | 17,422 | ✅ **60** | −27% | Revolution + regular hole pattern. 290× reduction. |
| 2 | `Top1` | 1,169 | ✅ **49** | −0.9% | All planes + 6 cylinders, **no NURBS at all**. |
| 3 | `Hatch` | 2,772 | ✅ **122** | −1.5% | Prismatic runs + straight ramps. **Fixed a real interference** — see below. |
| 4 | `Side_L2` | 1,913 | ✅ **93** | −1.5% | Layered plate, 9 rivets at 18.31 pitch, 6 M3 bosses. |
| 5 | `Side_R2` | 2,289 | ✅ **84** | −1.4% | Same, but a conical boss where the left has a rear panel. |
| 6 | `Side_L1` | 6,631 | ✅ **279** | −1.2% | CH slot, 16 rivet heads, ⌀19 boss, five stepped tiers. |
| 7 | `Side_R1` | 5,230 | ✅ **172** | −2.4% | Conical rivets, the ⌀6 pin drift hole, the top bracket. |
| 8 | `FrontBoss` | 1,705 | ✅ **304** | −1.7% | Front sight hood and post, 12 rectangular standoff ribs. |
| 9 | `Trigger` | 611 | ⚠ **partial** | — | The lever *is already native*; the butterfly paddle defeated three attempts. |
| 10 | `CH_Handle` | 10,134 | ✖ not worth it | — | Organic knurled grip. Primitives would look worse than the donor. |
| 11 | `Grip_Assembly` | 17,621 | ✖ not worth it | — | Spade grips — the most sculptural part on the gun. |

**Already native, nothing to do:** core tube, all 11 weldments, `Cradle_F2_HopUp`, `CH_Carrier`,
`CH_Shoe`, `Trigger_Switch_Carrier`, `Bot1`, `Bot2`.

### Where it landed

**39,131 faces of donor mesh replaced by 1,163 native ones — a 34× reduction**, across all eight
parts that were worth converting. Every one is a single watertight shell, within 2.4% of the donor
volume, and clear of all 12 steel bodies.

What is left faceted is 28,366 faces in three parts, and all three are deliberate: the two grips
and the charging-handle knob are sculpted artwork, and so is the trigger's butterfly paddle. The
STL ships the same triangles either way — nothing is lost by leaving them.

Skin-to-skin overlap across the whole native set is **0.065 cm³**, all of it in the castellated
joints where `Side_?2` interlocks with `Side_?1`: about 0.02 mm of average interference over a
1,300 mm² joint. That is snapping noise, an order of magnitude under the layer height.

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

## What I got wrong about the panels

An earlier version of this document said the side panels were marginal — that their rivet rows and
raised ribs were freeform artwork that boxes and cylinders would only make worse, and that each
would take days.

That was wrong, and measuring them properly is what showed it. The rivets are a **linear pattern**:
nine at 18.31 mm on `Side_L2`, and two rows of eight at 36.85 and 28.30 on the rear panels. The
raised "ribs" are **flat tiers at constant depth**. The panel outlines are straight lines with
chamfered corners and castellated interlocking tabs. The only genuinely freeform things on the gun
are the two grips, the charging-handle knob, and the trigger paddle.

The test still holds — **is it a revolution, an extrusion, or a plate with prismatic features?** —
but you have to run the scan before answering it. Eyeballing a dense mesh makes everything look
organic, because tessellation looks organic.

The other half of the correction came from Eric: *map it to normal straight lines, this thing was
designed in the early 1900s, it's not complicated.* That is exactly right, and it is why `snap.js`
exists. The wobble in the donor mesh is scan noise on top of what was originally flat plate, and
straightening it produces geometry that is both smaller and closer to the real gun.

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

---

## The panels — what was built

All four side panels are plates normal to Y, built as stacked constant-depth tiers with the
holes cut as real cylinders rather than snapped polygons.

### Side_L2 / Side_R2 (forward)

| tier | \|Y\| | content |
|---|---|---|
| plate | 25.85 … 30.00 | outline, CH-side castellations, 9 rivet dimples |
| raised panel | 30.00 … 38.00 | front panel; the left also has a rear panel to 40.50 |
| outer tier | 38.00 … 44.00 | two regions, chamfered to 49.09 |
| bosses | 25.40 … 25.85 | 6 × ⌀8 bridging to the tube face |

Rivets: 9 × ⌀1.50 at Z −39.80, pitch **18.306**, from X −169.55. Fasteners: 6 × ⌀3.40 at
X −242.40 / −122.90 / −63.10, Z +8.00 / −24.00, plus one ⌀7.52 at X −115.98, Z 0.

**The two are not mirrors.** The left carries a raised rear panel (1,180 mm², 12.3 cm³); the right
has a conical boss at X −222.7, Z 31.0 instead. That is the whole 12 cm³ difference between them.

### Side_L1 / Side_R1 (rear)

Five tiers from the plate at \|Y\| 25.85–30 out to 46.5 (left) or 46.2 (right). The charging-handle
slot is **198.3 × 10.18 mm** at Z −13.04…−2.86, and it runs through *both* panels — the carrier
sandwiches the tube, so both skins need the clearance.

Two rivet rows, generated arithmetically rather than read back off the mesh (the read missed a head
and gave different diameters row to row):

- Z −55.50, from X −541.84, pitch 36.852, 8 heads
- Z +56.30, from X −541.84, pitch 28.298, 8 heads

Left-only: the ⌀19 boss at X −293.8, Z −29.6 standing 15 mm proud. Right-only: the ⌀6 pin drift
hole at X −552, Z 1, and the raised bracket on the top edge — which is **three ⌀12 pads on a flat
bar**, not the wavy outline the mesh traces.

The donor drafts continuously through these tiers; the native version steps. That is the deliberate
trade and it is where the 4–6% symmetric difference comes from — the M2's side plate is stamped
sheet with stepped panels, and straight steps read closer to the real gun than a smooth taper does.

### FrontBoss

Six prismatic runs along X, from the twelve plain rectangular standoff ribs on the rear face
(X −13.35…−3.0) out to the sight hood and post (X 8…19). Entirely planar — 304 faces, of which most
are the hood's polygonal arc.

---

## Two more interferences, both mine

Found by clashing the finished native set against itself. Neither existed in the donor:

- **Hatch nose into the FrontBoss ribs, 0.375 cm³.** I held the nose at full width (Y ±30) to
  X −12; the standoff ribs start at X −13.35. The donor narrows between −14 and −12. Fixed by
  narrowing at −13.50.
- **Side_R1 bracket into the hatch skirt, 0.095 cm³.** The tier under that bracket stops at
  X −334.4, which is exactly where the top cover starts. Past that the bracket overhangs the
  cover, so its underside has to begin outboard of it — the donor does the same. Fixed by trimming
  the overhang back to \|Y\| 34.95.

Both are the kind of thing that only shows up once the geometry is clean enough to boolean
honestly. Against the faceted donors, these checks returned "clear".
