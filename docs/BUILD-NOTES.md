# M2 Airsoft — Steel Core Conversion

Working notes for the Browning M2 airsoft build. Fusion doc:
`Browning_M2_0.50_cal_Machine_Gun_V.02-FS-R_-_corpus` in the **MaDuce** project.
Started 2026-09-09.

**Concept:** one simple structural box in steel — not printed — carrying all loads, with the
printed parts reduced to non-structural outer skins bolted/epoxied on, plus printed internals
holding the airsoft engine and hop-up.

---

## Coordinate system

**+X is forward (muzzle), −X rearward. Y = 0 / Z = 0 is the barrel axis.** All mm.

The source model is a **faceted STL conversion** — every face is planar, there are no analytic
cylinders, so bores cannot be snapped to and must be found by probing. Face counts 2.7k–11k per body.

---

## STEEL CUT LIST

| # | Part | Stock | Cut size | Qty | Wt |
|---|---|---|---|---|---|
| 1 | Core tube | 2" × 3" × 0.120" wall rect tube | 22-7/8" | 1 | 6.37 lb |
| 2 | Pintle tabs | 1/2" plate | 1.81" × 1.81" blank | 2 | 0.35 ea |
| 3 | Barrel front plate | 1/4" plate | 2" × 3" | 1 | 0.36 |
| 4 | Barrel socket | **1-1/2" OD × 0.156" wall round tube** | **4"** | 1 | 0.75 |
| 5 | Hatch spine | 1/8" × 1" flat bar | 13" | 1 | 0.45 |
| 6 | Hinge tabs | 1/8" plate | 0.87" × 3.56" blank | 2 | 0.10 ea |

**Total 8.75 lb steel.** Printed PLA ~2.6 lb. Finished ~14 lb with engine and hardware.
(Real M2HB is 84 lb; commercial airsoft M2s run 33–44 lb.)

### ALL STOCK MUST BE IMPERIAL
US steel supply. Never spec a metric size — work backwards from what's on the shelf.
Minimum practical purchase is a **12" length of any stock**.

### SHOPPING LIST (12" minimums, cut to length only — no rip cuts)

| # | Stock | Buy | Yields | For |
|---|---|---|---|---|
| 1 | 2" × 3" × 0.120" wall rect tube | 24" | 22-7/8" | Core tube |
| 2 | 1-1/2" OD × 1.188" ID DOM | 12" | 4" | Barrel socket |
| 3 | 1/2" × 2" flat bar | 12" | 2 × 1.81" | Pintle tabs |
| 4 | 1/4" × 3" flat bar | 12" | 1 × 2" | Barrel plate |
| 5 | 1/8" × 1" flat bar | 24" | 13" + 2 × 3.56" | Hatch spine + hinge tabs |
| 6 | 1/4" round bar | 12" | ~2.5" | Hinge pin |
| 7 | 1/2" round bar | 12" | ~2.5" | Pintle pin |
| 8 | 9/16" round bar *(or 9/16" grade-5 bolt)* | 12" | ~2.5" | Front mount pin |

Item 5 does double duty — spine and both hinge tabs come off one piece; the tab profile
(0.87" × 3.56") fits inside the 1" bar width. Widths are chosen so every part fits the bar with
no rip cut.

9/16" round bar is the least commonly stocked item; a grade-5 bolt substitutes fine. Do **not**
drop the front mount to 1/2" — that's 1.3mm of slop on a pin carrying the gun's weight.

### Pins
| Pin | Model bore | Use |
|---|---|---|
| Hinge | ⌀6.35 | 1/4", exact, ~2.5" long |
| Pintle | ⌀12.0 | open to 1/2" |
| Front mount | ⌀14.0 | 9/16" (14.29mm) |

---

## Core tube

2" × 3" × 0.120" wall, **X −560 … +20** (580mm / 22.83"). Centred at **Z −8**
(spans Z −46.1 … +30.1), Y ±25.4. **Interior 44.70 × 70.10mm.**

Dropped 8mm off-centre so the front mounting bore clears the floor by 3.05mm.
An initial 3"×3" pick was wrong — the receiver necks to 60mm wide in two places.

**Cut length 589.52mm (23.210").** Corner radii modelled: **R0.240" outside, R0.120" inside**.
Without them OSH Cut's profile matcher reads the section as aluminium extrusion — nothing in
their steel catalogue has square corners.

### Cuts in the tube
| Cut | Location |
|---|---|
| Top opening | X −310 … −2, **straight cut at Z +24, full width** |
| Belt slot | X −141 … −2, both walls, Z +18 up to the cut top edge |
| CH shaft slot | X −540 … −348 (192mm), Z −12 … −4, both walls, R4 |
| Air line | ⌀12.7 at X −410, bottom wall |
| Front mounting bore | ⌀14 at X +1, Z −33, both side walls |
| Pintle notches | X −384 … −338, both bottom corners, cut by the tabs themselves |
| Front locating tabs | X +20 … +26.35, top and bottom, 25mm wide |
| Rear locating tabs | X −563.18 … −560, top and bottom, 25mm wide |

The top opening **must** run forward to meet the belt slot at X −2. Stopping it short leaves a
cantilevered tongue ("a diving board").

**The top is one straight cut at Z +24** — the height where the corner radii begin, so it lands
flat on both side walls. No flanges, no R5 corners, no tab notches. The earlier flanged version
(Y ±19 with R5) fouled the hinge tabs and left messy geometry.

**Locating tabs are exactly their plate's thickness** so tab and plate faces finish flush —
nothing protrudes at either end. They pass through through-slots, keeping both the tube and the
plates laser-only. Blind pockets would be a milling op and were rejected.

---

## Weldments

- **Pintle tabs** ×2 — 1/2" plate, X −384…−338, Y ±15.7…28.4, **Z −92…−35**, ⌀12 bore at
  X −361 / Z −79. Tapered profile matching the printed lug (measured Y ±16…28).
  The top 11.1mm sits inside the tube and **cuts its own notch** through the bottom wall and up
  the corner, so the tab drops into a slot instead of balancing on the corner radius.
  Do not move them inboard — that was tried and rejected; it shifts the bore off the lug.
- **Hinge tabs** ×2 — 1/8" plate, **inside the tube** at Y ±19.18…22.35, X −22…0, Z −20…+70.5.
  22 × 40mm weld foot laps the inner side wall; neck tapers to an **r8 round head concentric
  with the pin** at X −9, Z +62.5. Round head = the hatch needs only a circular relief, so
  rotation is free by construction. **Line-drill the pin through both tabs after welding.**
- **Hatch spine** — 1/8" × 25mm × 329.9mm, inlaid into the hatch underside so hinge load never
  passes through plastic.
- **Barrel plate** — 1/4", welded across the tube end at X +20…+26.35, **bore ⌀38.9 (1-17/32")**
  plus two through-slots for the locating tabs. Leaves a 6.0mm web each side in Y.
- **Barrel socket** — 1-1/2" OD × 0.156" wall round tube, **X +13.65 … +113.65 (100mm)**.
  Only 6.35mm sits inside the tube; 87mm runs outside under the shroud.
- **Backplate** — 1/8", X −563.18 … −560, matching the tube's rounded profile, with two
  through-slots for the rear locating tabs. Basis for the trigger mount; bolt pattern TBD.

### Barrel = 1" EMT conduit, passing INSIDE the socket
EMT: OD 1.163" (29.54mm), wall 0.042", ID 1.079".
Socket 1-1/2" × 0.156": OD 38.10mm, **ID 30.18mm** → EMT passes through with **0.64mm**
diametral clearance. Up to **101mm of engagement**.

Printed boss ends at X +24.8, so the **EMT is the visible barrel from X +26.35 forward** and the
socket is hidden behind the skin.

#### Sourcing the socket
It is **round mechanical tubing, NOT pipe**. Pipe is sized by NPS and no pipe size lands near a
1.188" ID — that is exactly why 1" pipe won't take 1" EMT. Ask for it as
**"1-1/2 OD × 1.188 ID DOM"** (DOM is often called out OD × ID rather than by wall).

**Prefer DOM over HREW.** DOM is drawn over a mandrel so the bore is smooth and consistent, which
is what makes a 0.64mm slip fit actually slip. HREW has an internal weld bead that would bind the
EMT and need reaming.

| Spec | ID | EMT slop |
|---|---|---|
| 1.500 × 0.120 | 1.260" | 2.46mm — fallback, stocked everywhere |
| 1.500 × 0.134 | 1.232" | 1.75mm |
| **1.500 × 0.156** | **1.188"** | **0.64mm — spec'd** |
| 1.500 × 0.188 | 1.124" | **WON'T FIT** — EMT OD is 1.163" |

Going *thicker* fails outright. 0.156" (5/32") is a real standard wall but not the most commonly
stocked; 0.120" and 0.188" are more common. If 0.156 isn't available use **1.500 × 0.120** — with
~100mm of engagement the length controls concentricity far more than the clearance does, and the
rest can be taken up with three set screws at the muzzle end or a wrap of shim stock.
**Model change if switching to 0.120: socket ID 30.18 → 32.00; plate bore unchanged (OD is same).**

Rejected alternatives: 1" sch40 pipe of any schedule is **too small** (ID 1.049") — "1 inch" pipe
will not accept "1 inch" EMT. 1-1/4" sch40 has 5.5mm of slop. A 1" EMT set-screw coupling fits by
design but is usually zinc die-cast and won't weld. A 3/4" pipe spigot the EMT slides *over* was
built first (v54–v61) and replaced.

Verified: socket vs tube, cradle, hop-up and barrel all **0.000 cm³**.

Verified clearances: hinge tabs vs barrel, hop-up and tube all **0.000 cm³**.
Hatch rotation **0.000 cm³ through 75°**.

---

## Model landmarks (measured)

| Feature | Location |
|---|---|
| Receiver overall | X −560.6 … +24.8 |
| Floor within tube footprint | Z −50 |
| Belt feeding platform | Z +22.3, X −140.6 … −0.2 |
| Belt aperture, left wall | X −140 … −70, Z +25 … +40 |
| CH guide groove | Y ±24, X −544.2 … −325.8. Right side Z −13.0…+20.1 but **LEFT only Z −13.0…−2.9** — the band common to both is where the shaft slot belongs |
| Recessed side panel | Y ±20.3, X −292.1 … −148.6 |
| Hatch underside | Z +43.6 |
| Hatch hinge bracket | X −4 … +2, Z +59 … +66, Y ±30 — **FRONT of receiver** |
| Hatch central boss | Y −18 … +16 at X −12…−6 (what the pin passes through) |
| Front mounting bore | ⌀14 at X +1, Z −33, transverse (found at both Y ±27) |
| Pintle lug | two tabs Y ±16…±28, bore ⌀12 at X −361, Z −79, bottom Z −92 |

### Source bodies
`Receiver_Lower (1)` rear −560.6…−306.9 · `Receiver_Lower (1) (1) (1)` mid −334.3…−148.6 ·
`Receiver_Lower` front −148.6…+24.8 · `Hatch (1)` −334.3…−4.4

### Installed parts
- **PolarStar F2** X −239.9…−119.4, Y ±12.7, Z −16.0…+12.7
- **FCU** X −281.3…−226.7, Y ±10.8, Z +18…+25
- **HopUp** X −119.9…−89.4, on the barrel axis

### Traps that cost time
- The hatch lug at X −39…−29, Y ±41…45 has **no bore** — it's a latch flange. The hinge is at the front.
- The model contains **no charging handle mechanism** — only the guide groove above.
- `left`/`right` screenshot directions look **down the barrel** (the gun runs along X); use
  `front`/`back` for side views.
- Root `isBodiesFolderLightBulbOn` overrides individual body visibility.

---

## PRINTED SKIN RULES

**"Flat panels" means flat FOR PRINTING, not featureless.** Each piece lies flat on the bed with
its visible face UP so the top surface can be **ironed**. All M2 surface detail must survive.
Clean native plates with no detail were tried and rejected outright.

**Sides are full-height flat panels, cut on the TUBE WALL planes (Y ±25.8).** Left = Y ≤ −25.8,
right = Y ≥ +25.8, top to bottom. **Do not wrap the sides around the bottom.**

**Top and bottom are strips that fit BETWEEN the side panels** — the 51.6mm middle zone, above
the tube top (Z ≥ +30.5) and below the tube bottom (Z ≤ −46.5).

**Two lengthwise sections, not three.** The front boss is a separate part and doesn't count.

**Seam at X −265.** As far forward as the bed allows so the charging-handle geometry (groove ends
X −325.8) is well clear. **Max forward is X −260.6** before Side_1 exceeds the 300mm bed. The
Y ±20.3 recessed panel does get crossed; that's accepted — clearing the CH geometry matters more.

**Bed is 300mm (Creality K1 Max).** The hatch at 329.9mm only fits laid diagonally
(294mm footprint, 5.7mm margin).

### Alignment: interlocking finger seams, NOT dowels
**The panels are a ~3mm shell, not solid.** Dowels were tried and failed — a 3.2mm hole in a 3mm
wall breaks through both faces and is visible from outside. Placement tests must check a full
**envelope** around a hole, not just two points along its axis.

Current scheme: **2 fingers per side per seam, 10mm deep**, on the side panels only, projecting
from section 2 into its neighbours. Alignment lives in the seam plane so nothing shows outside.
The top/bottom strips are too thin (3–8mm) for fingers — they keep plain butt seams and need
clamping during glue-up.

### Pin bores are sized to IMPERIAL bar, not round metric
US bar stock is 6.35 / 12.70 / 14.29 mm — a ⌀12 bore will not take a 1/2" pin. Every pin bore is
cut **0.30 mm over nominal bar**: hinge ⌀6.65 (1/4"), pintle ⌀13.0 (1/2"), front mount ⌀14.6
(9/16"). Do not round these back to 12/14/6.

**When auditing bores, check the face AXIS and AREA, not just the diameter.** The tube's A500
corner radii show up as cylindrical faces at ⌀12.19 (R0.240" outside) and ⌀6.10 (R0.120" inside),
running lengthwise along X with face areas in the thousands of mm². They are fillets, not holes.
Reading them as bores produced a false "three bores are wrong" report; only two actually were.
Real pin bores run along **Y**, are short, and have face areas under ~500 mm².

### Standing subtractions — IN THE GENERATOR, not by hand
Manual deletions "keep coming back" because regenerating from source discards them.
- **Tube clearance envelope `ENV`**: `bx(-26.85, 0, -0.80, 59.1, 5.16, 7.70)` — X −564…+27,
  Y ±25.8, Z −46.5…+30.5. **It must span the WHOLE tube including the locating tabs at both
  ends**, not just the tube body. It was X −561…+21 while the front tabs reached X +26.35, and
  the ~5mm of tab past the envelope drove FrontBoss into the steel by 0.5795 cm³.
  **Whenever the tube's extents change, ENV changes with them** — query
  `tube.boundingBox` and check it rather than assuming.
- **Feed way**: no skin material above the tube in X −334.3 … −13.3. Deletes `Top2` entirely and
  ends `Top1` at X −334.3 — the top deck only exists *behind* the hatch.
- **Pintle lug**: X −395 … −325, everything **below Z −67**. The steel tabs are the lug.
  Cut only below −67, not −50 — the shoulder Z −50…−67 is real side-panel geometry.
- **Front trim**: X 26…41, Y ±14, Z −36…−22 — strands left forward of the barrel plate.
- **Front ring trim**: cylinder r19.8 on the barrel axis, X +19.5…+27.0. Removes two floating
  concentric rings (r15.1 and r19.4) left in FrontBoss when the socket bore went through.
  Socket OD is r19.05, so the trim clears the steel by 0.75mm.
- **Pin bore**: ⌀6.35 at X −9, Z +62.5 cut from **every** skin so one pin passes through
  FrontBoss lug → tab → hatch boss → tab → FrontBoss lug.

**Every piece must be a single shell, and volume must conserve.** Always print
`sum of parts == union volume, LOST 0.00`. A silent bug once dropped the receiver's top shoulders
entirely — the region `{|Y|>25.8, Z>38.5}` belonged to no piece and vanished.

---

## Fusion MCP workflow

- **Never point-probe at high resolution.** `pointContainment` on an 11k-face body hangs Fusion's
  UI thread for 20+ minutes. Budget a few hundred probes. `TemporaryBRepManager` booleans are
  ~0.03s even on faceted bodies — use those freely.
- **Prefer face queries over sampling** to locate features. Iterating `body.faces` filtered by
  `surfaceType == PlaneSurfaceType` plus normal direction is instant and exact. Mesh-node binning
  misled badly twice — put the belt notch 100mm off and reported the receiver floor 7mm high.
- **Fusion rolls back the entire script on an exception.** A late failure discards earlier edits.
- **Verify saves by re-reading geometry.** A save reported success, Fusion crashed, and recovery
  came back *behind* it, silently losing two edits.
- **Sketch on the XZ plane maps sketch-Y to world −Z.** Negate or the part comes out mirrored.
- **`booleanOperation` returns a bool**, not a body. `b = tbm.booleanOperation(b, x, UNION) or b`
  assigns `True` and the next call throws TypeError. Bit me twice.
- **Cutting coincident with a planar face makes zero-thickness shells.** Offset ~0.05mm.
- **Direct-design docs have no `snapshots`** — touching `des.snapshots` throws.
- **The stuck-mouse bug is Deskflow**, not Fusion and not WhisperFlow. It loses the button-up
  event on screen transitions so Fusion orbits forever. Click the button once in the viewport.

---

## Print orientation — a real tension

`tools/stlcheck.js` reports overhang burden per orientation. Standing the pieces **on end**
collapses it, but puts the visible face vertical where it cannot be ironed:

| Piece | Flat (+Z up, ironable) | On end (min support) |
|---|---|---|
| Hatch | 33.6% | 4.2% |
| Bot1 | 31.7% | 3.4% |
| Top1 | 22.0% | 4.6% |
| Bot2 | 21.3% | 0.4% |
| Side_L1 | 11.3% | 2.3% |

Flat-and-ironable is the chosen orientation; the cost is 20–30% of surface needing support on
several pieces. All parts pass watertight with correct normals and 1 shell (except Bot2's two
rails, left deliberately).

## Still open

1. **Skin-to-tube fastening** — no bolt bosses, holes or captive nuts anywhere. Biggest gap.
2. **Rear closure** — tube's back end at X −560 is open. No backplate, grips or trigger.
3. **Verify the three inferred pin positions** against real hardware before drilling steel.
4. **CH slot width** — the 8mm is a guess, not measured. Carrier/handle not modelled.
5. **Torsion cross-strap** over the 139mm U-channel run (top + both walls cut).
6. `Bot2` is 2 shells (two bottom rails) — left as-is deliberately, keeps printing simple.
7. Hatch latch, feed tray detail.
8. Deliverables not produced: 1:1 plotter template (single sheet, not tiled), STL exports.
