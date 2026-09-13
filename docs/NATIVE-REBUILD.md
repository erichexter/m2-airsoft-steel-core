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
| 1 | `Grip_Assembly` | 17,621 | ✅ **1,463** | −2.0% | Two handgrips are **exact revolves**; frame is a stack of plan sections. |
| 2 | `Barrel_Jacket` | 17,422 | ✅ **60** | −27% | Revolution + regular hole pattern. 290× reduction. |
| 3 | `CH_Handle` | 10,134 | ✅ **73** | +0.6% | Knob is an **exact revolve** — 3 faces. Plate, arm, 4 × ⌀8 nut pockets. |
| 4 | `Side_L1` | 6,631 | ✅ **262** | −0.9% | CH slot, 16 domed rivets, ⌀19 boss, five stepped tiers. |
| 5 | `Side_R1` | 5,230 | ✅ **162** | −2.7% | Domed rivets, the ⌀6 pin drift hole, the top bracket. |
| 6 | `Hatch` | 2,772 | ✅ **138** | −1.2% | Prismatic runs + straight ramps. **Fixed a real interference** — see below. |
| 7 | `Side_R2` | 2,289 | ✅ **75** | −1.6% | Spherical rivet dimples, conical boss where the left has a rear panel. |
| 8 | `Side_L2` | 1,913 | ✅ **84** | −1.7% | Layered plate, 9 dimples at 18.31 pitch, 6 M3 bosses. |
| 9 | `FrontBoss` | 1,705 | ✅ **304** | −1.7% | Front sight hood and post, 12 rectangular standoff ribs. |
| 10 | `Top1` | 1,169 | ✅ **61** | −0.9% | Planes + cylinders only. Six ⌀8 bridging bosses under the deck. |
| 11 | `Trigger` | 611 | ⚠ **partial** | — | The lever *is already native*; the butterfly paddle defeated three attempts. |

**Already native, nothing to do:** core tube, all 11 weldments, `Cradle_F2_HopUp`, `CH_Carrier`,
`CH_Shoe`, `Trigger_Switch_Carrier`, `Bot1`, `Bot2`.

### Where it landed

**66,886 faces of donor mesh replaced by 2,682 native ones — a 25× reduction**, across every part
except the trigger's butterfly paddle. Each is a single watertight shell, and **every bounding box
now matches its donor to better than 0.25 mm** in all three axes.

Volumes land within 2.7% except the jacket, which is a deliberate simplification. The whole printed
set is 2,962 cm³ native against 3,229 cm³ faceted.

Only 611 faces remain faceted, and only the paddle within that.

### The two I wrongly wrote off

The first version of this table marked `CH_Handle` and `Grip_Assembly` "not worth it — organic,
knurled, the most sculptural parts on the gun." **Both are wrong.** Measured with the same
first-hit-radius method used on the jacket:

| | axis | agreement across rays |
|---|---|---|
| CH knob | Y at (X −286.80, Z 48.875) | **0.008 mm** over 64 rays |
| Handgrips | Z at (X −613.81, Y ±62.23) | **0.006 mm** over 48 rays |

They are not knurled at all. They are **turned** — bodies of revolution to eight microns, the
easiest case there is. Each is now a single revolve of **3 faces**. What made them look organic in
the browser was 10,000 triangles, which is exactly the trap this document already warned about for
the side panels, and I walked into it twice more.

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

> This is now the **only** faceted part left, and only its paddle.

The functional half was already native and stays exact: riser X −580…−568 (Y ±7,
Z −6…32), arm X −568…−526 (Y ±6, Z −6…8), ⌀4.20 pivot bore on the Y axis at X −552,
⌀6 spring peg, ⌀3 front anchor.

The butterfly paddle resisted three separate reconstructions:

| attempt | result |
|---|---|
| Loft, arc-length resampling | Sections twisted — no point correspondence between them |
| Loft, angular resampling about the centroid | Filled the V notch; the sections are crescents, not star-shaped |
| Two-view silhouette intersection | Over-fills the wings — 840 mm² against an actual 396 mm² |

It is a compound-curved paddle with serrated thumb pads. Note that the same verdict was
originally given to `CH_Handle` and `Grip_Assembly` and was **wrong for both** — they turned
out to be exact revolves. The difference is that those two are round about an axis and this
is not: the paddle's sections are crescents that change character along the sweep. Left
faceted at 611 faces, which is cheap.

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

---

## Rivets are round-head rivets

Every raised disc on the gun is a **spherical dome**, not a flat-topped cylinder. Fitted against
r² = R² − (Y − Yc)² off the donor mesh:

| feature | centre \|Y\| | R | max deviation |
|---|---:|---:|---:|
| `Side_L1` rivet heads ×16 | 33.546 | 4.219 | 0.23 mm |
| `Side_R1` rivet heads ×16 | 33.525 | 4.223 | 0.25 mm |
| `Side_L1` upper studs ×4 | 28.953 | 3.380 | 0.10 mm |
| `Side_L1` mid studs ×3 | 35.554 | 4.394 | 0.11 mm |
| `Side_R1` tier studs ×2 / ×4 | 28.346 / 28.966 | 5.269 / 3.360 | 0.15 mm |
| `Side_R1` bracket rivet | 44.529 | 5.138 | 0.29 mm |

The two rear panels carry the *same* rivet, agreeing to 0.005 mm. The first pass built the left
ones as flat cylinders and the right ones as cones, which is what made the two sides look different.

**The inset holes are spherical too.** The forward panels' rivet detail is a ⌀5.9 spherical dimple
2.1 mm deep (R 3.125 about \|Y\| 31.035); the first pass measured the diameter *deep inside* the
dimple and cut ⌀1.50 pin holes — wrong in both size and shape. The small recesses on the rear
panels are likewise spherical (R 2.95 on the left about \|Y\| 37.28, R 3.00 on the right about
34.01), not flat-bottomed bores. The ⌀9.98 recesses genuinely are flat-bottomed cylinders.

A dome is a whole sphere, so its far hemisphere sits *inside* the panel and can break out through
the inboard face — `Side_R1` ended up 2.3 mm inside the tube before the parts were clipped back
to the tube face at \|Y\| 25.40.

---

## Four truncations, found by auditing bounding boxes

After fixing one shortfall by hand it was obvious to check them all. Comparing each native part's
bounding box against its donor found four, every one a case of stopping at a round number instead
of where the geometry ends:

| part | axis | donor | first pass | short |
|---|---|---:|---:|---:|
| `Side_R1` | Y max | 49.70 | 46.20 | **3.50 mm** |
| `Hatch` | X min | −334.34 | −333.00 | **1.34 mm** |
| `Side_L1` | Y min | −62.30 | −61.50 | **0.80 mm** |
| `Top1` | Z min | 30.15 | 30.50 | **0.35 mm** |

- `Side_R1` — a domed rivet on the bracket's centre pad, lopped off by a tier ending at 46.2.
- `Hatch` — a rear end chamfer over X −334.3…−332, asymmetric: it tapers on the −Y side and the
  top while Y max stays 34.90.
- `Side_L1` — the ⌀18.98 boss is flat-ended at \|Y\| 62.25, not 61.50.
- `Top1` — the one that mattered: **six ⌀8 bridging bosses under the deck** at the M3 positions,
  standing 0.35 mm proud. The same bosses the side panels carry, the ones that land the deck on the
  tube. They had been omitted entirely and the holes drilled straight through a flat face.

**Make the bounding-box audit routine.** It is cheap, it needs no Fusion, and it catches exactly
the class of error that volume comparison hides — 0.35 mm of missing boss costs almost no volume.

---

## Grips and charging handle — what was built

**CH_Handle**, 73 faces. One revolve for the knob (Y −171.45…−58, r 9.97 at the tip swelling to
15.83 and back to 11.67), the mounting plate over Y −58…−48, and the flat arm X −386…−280 over
Y −48…−38 carrying **four ⌀8 blind nut pockets** at X −370 / −340 / −310 / −290, Z −5, entered
from the outboard face. Plus the ⌀19 boss at (X −293.6, Z −8.02).

**Grip_Assembly**, 1,463 faces. Two revolved handgrips — barrel-shaped, r 12.81 at the base
swelling to 15.87 and shouldered into a domed top at Z 72.1 — on a frame built from **33 horizontal
plan sections**.

An earlier attempt extruded the fore-aft *side* profile across the full width and trimmed it
against one plan section per half. That was 10% light and it also filled in the slot the trigger
passes through. The spine's plan changes shape the whole way up; it is not a slab with a constant
outline. Sampling the plan every 1 mm, cutting bands at the real transitions and merging identical
ones gives 33 bands and lands within 2%.

The mounting tongue reaches into the receiver, so the grip is relieved against the tube, the
backplate and its bosses, and against the **trigger swept through its 6° of travel** — otherwise it
fouls partway through the pull rather than at rest.

---

## Two more lessons

**Do not approximate a revolve with a stack of cone segments.** Forty-four segments through the
measured radius profile is geometrically fine and renders as visible rings — it looks *knurled*,
which is the one thing these turned parts are not. A single `revolveFeature` through a fitted
spline is 3 faces and actually smooth.

**When merging bands, put hole topology in the merge signature.** Merging two bands keeps the
first one's profile. If a slot appears in only some bands of a group, merging silently fills it
back in — which is how the trigger's clearance slot disappeared.
