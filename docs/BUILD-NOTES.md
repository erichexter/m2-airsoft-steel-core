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

![Everything you cut and weld: the 2×3 tube plus eleven pieces.](img/02-steel-core.png)
*Everything you cut and weld: the 2×3 tube plus eleven pieces.*

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

![The weldments in side view — tab positions along the tube.](img/03-steel-core-side.png)
*The weldments in side view — tab positions along the tube.*

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

> Every part rendered individually, with its catalogue name: **[PARTS.md](PARTS.md)**.

## SKIN FASTENING — 36 × M3 thread-forming into the tube wall

![The nine printed receiver skins that bolt to the tube.](img/04-receiver-skins.png)
*The nine printed receiver skins that bolt to the tube.*
**The panels bed directly on the tube.** Every fastener has a ⌀3.4 clearance hole; the screw pulls
the panel's inner face flat against the steel wall, with no gap to bridge.

> **This used to be a 0.4mm clearance gap** (an artifact of what `ENV` creates) with a **⌀8 boss on
> the panel's inner face** at every fastener to bridge it — the reasoning being that a screw pulled
> across that gap would just flex a 3mm shell.
>
> **The inner face is the face these parts print on**, visible side up so the outside can be ironed.
> So each panel landed on the bed sitting on nothing but those bosses. Measured: `PR-13` rested on
> **2.46 cm² while 216.69 cm² floated 0.45mm above it** — and 2.46 cm² is exactly six bosses,
> 6 × (⌀8 disc − ⌀3.4 hole). 98% of the bed face was held in the air by six pads, and the slicer
> supported all of it.
>
> The gap is now filled instead (`tools/reauthor/flatten_mating.py`). The bosses are absorbed
> flush, the panel beds on the steel across its whole area — a better joint than six pads — and
> `tools/bedcheck.js` reports **92.7–99.9% of every bed face on the bed**. Verified 0.000 mm³ of
> penetration into the tube on all eight skins.
>
> The top and bottom strips had to follow: they ran to |Y| 25.80 to butt against panel faces at
> 25.85, so moving those faces to the tube wall at 25.40 made them overlap by 0.40 each side. They
> are trimmed to **|Y| 25.35**, keeping the original 0.05 clearance. A strip now spans the tube's
> full width and stops just shy of the panel beside it.

Tube gets **⌀2.65 pilot holes**; M3 thread-forming screws cut their own thread in the 0.120" wall.
No tap, no rivnut tool. Heads left proud — they read as the M2's rivet line.

| Panel | X positions | Z or Y |
|---|---|---|
| `PR-12-Side-Rear-R` `PR-11-Side-Rear-L` | −525.1, −460.1, −285.7 | Z −24, +8 |
| `PR-14-Side-Front-R` `PR-13-Side-Front-L` | −242.4, −122.9, −63.1 | Z −24, +8 |
| `PR-15-Top-Deck` | −526.7, −413.5, −356.9 | Y ±18 |
| `PR-18-Bottom-Rear` | −516.3, −442.4, −294.6 | Y ±18 |

Z −24 and +8 miss the CH slot (Z −12…−4) and the belt slot (Z ≥ +18); the X values miss the pivot
pin (X −552), the backplate bosses (X −560…−547), the pintle tabs (X −384…−338), the air line
(X −410) and the hinge tabs (X −22…0).

### Six interferences found while checking the above — now resolved

Pairwise-intersecting the eight skins against all 210 bodies turned these up. All four **predate
the mating-face work** — each was confirmed by checking that the overlap extends outside the
0.45 mm band that work added, so none of them is a consequence of it. They are small, and they are recorded here
because two of them looked like design questions rather than slips:

| | | |
|---|---|---|
| `PR-11-Side-Rear-L` ↔ `PR-13-Side-Front-L` | 34.6 mm³ | the lengthwise seam at X −265; the two panels overlap X −275…−265 |
| `PR-12-Side-Rear-R` ↔ `PR-14-Side-Front-R` | 37.6 mm³ | the same seam, other side |
| `PR-12-Side-Rear-R` ↔ `HW-03-Trigger-Pin-4mm` | 20.1 mm³ | the panel fouls the ⌀4 pivot pin — **this one blocks assembly** |
| `PR-15-Top-Deck` ↔ `PR-31-Spade-Grips` | 6.6 mm³ | deck corner into the grip spine |
| `PR-17-Front-Sight-Boss` ↔ `ST-07-Hinge-Tab-L` | 12.6 mm³ | **printed part sits down over welded steel** |
| `PR-17-Front-Sight-Boss` ↔ `ST-07-Hinge-Tab-R` | 2.9 mm³ | the same, other side |

**All four are cleared** by `tools/reauthor/resolve_clashes.py`, at 0.20 mm — deliberately more than
the 0.05 between a strip and a panel, because these are not faces meant to bed together but places
where two parts occupied the same space, and a printed joint wants room to be slid into.

"It is probably an intentional lap" turned out not to be a defence. Two solids cannot share space
whatever the intent; a lap still needs the clearance cut into one side of it. The part that gives
way is the one easier to reprint and less load-bearing — the front panel yields to the rear, the
skin yields to the hardware. Each cut leaves **0.000 mm³** of overlap and a single shell, and the
bed faces are untouched: every relieved area became a pocket deeper than 1 mm, so bed contact stayed
at 92.7–99.9%.

**The last two were only found when the check was widened from the eight skins to all eighteen
printed parts.** The first four came out of checking the parts that had just been edited, which is
the natural thing to do and is why the front sight boss — untouched for days, and previously
reported clear — went unexamined. It runs back to X −13.4 while the hinge tabs run forward to X 0,
so it was sitting down over both of them. Welded steel does not yield; the printed part does.

The check that now stands is the whole matrix: **all 18 printed parts against all 210 bodies, 0
clashing pairs**, deepest penetration into the tube 0.0000 mm³, 18 of 18 single-shell solids.

**`PR-19-Bottom-Front-L` / `-R` cannot be screwed** — two rails over the tube's bottom corner radii with no flat behind
them (tube reads 0.016 cm³ against a ⌀5 probe where the panel is solid). Bond it.

**Probing the top panel: the tube's top is at Z 27.05…30.10 over X −560…−310.** Probing at the
Z +24 cut line reports zero viable positions, because the cut only exists from X −310 forward.

## CLEARANCE: where printed parts meet welded steel

Measured by inflating each steel body until it touches the printed part. **19 interfaces
sit under 0.20 mm.** They are two different things and only one of them is a problem:

**Face bedding — 0.00 mm is correct.** The printed face lies flat *on* steel. Thin in
exactly one axis.

| `PR-11` → tube | 295.00 × 0.60 × 69.28 |
|---|---|
| `PR-15` → cover spine | 0.60 × 25.00 × 3.18 |
| `PR-52` → backplate | 0.60 × 40.00 × 39.50 |

**Enveloping fits — 0.00 mm is unbuildable.** Printed material wraps *around* steel, so
it needs room for FDM tolerance and weld distortion both.

| | extents | clearance |
|---|---|---|
| `PR-11` → pintle tab | 47.20 × 3.55 × 32.50 | ≤ 0.02 mm |
| `PR-18` → pintle tab | 47.20 × 10.30 × 20.85 | ≤ 0.02 mm |
| `PR-16` → cover spine | 329.90 × 26.20 × 3.72 | ≤ 0.10 mm — **fixed, now 0.50** |
| `PR-31` → trigger pin | 1.60 × 40.00 × 4.66 | ≤ 0.02 mm |
| `PR-51` → trigger pin | 5.20 × 12.00 × 5.20 | ≤ 0.15 mm |

Only the spine was corrected in CAD, because a 329.9 mm steel bar will not enter a
printed slot at 0.10 mm by any means. The rest are **hand-fit at assembly**:

- **Pintle pockets** — `PR-11`, `PR-12`, `PR-18` printed unsupported, so the bridge over
  each pocket sagged *into* it. At 0.02 mm nominal any droop fouls the tab. Check with a
  straightedge and dress flat before assembly.
- **Trigger pin bores** — ream to size after printing. An FDM hole comes out undersize
  anyway, so opening the model risks a sloppy pivot instead of a tight one.

**Never put support material in an enveloping fit.** It has no clearance to give up.

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

### DONOR MESHES — check `isSolid`, not just that a boolean returned
`grip.stl` converts to a **surface** body, not a solid, because the mesh is not watertight.
A boolean against an open surface returns "no interference" **no matter what** — there is no
inside for it to find. That silently passed a clash check that was hiding 25.7 cm³ of overlap.
**Always print `body.isSolid` after a mesh convert.**

Repair with `tools/meshrepair.js`. The grip's defect was **T-junctions, not holes**: 8 open edges
whose four "loop" vertices are collinear (same X, same Z, varying Y only) — one side of a seam
used a single 66.6mm edge while the other used three shorter ones. Capping a zero-area loop with a
centroid fan just produces degenerate triangles, which is what a naive hole-filler does. The fix is
to **split the long edge** at the intruding vertices. 4 splits closed it; volume unchanged at
304.6 cm³.

The donor grip **includes its own backplate** — it overlapped the steel `ST-02-Backplate` by
9.04 cm³ over the full height, because on a real M2 the backplate is part of the grip assembly.
The printed grip is relieved around the steel (−25.7 cm³) exactly as the skins are: steel carries
load, plastic is cosmetic. The buffer tube is relieved for the trigger arm's swept envelope
(−1.5 cm³).

**Relieve against the SWEPT envelope of moving parts**, not their rest position — the trigger
envelope over 0…5.5° is 43.0 cm³.

### BACKPLATE IS BOLTED, NOT WELDED
Welding it seals the trigger away for good — the mechanism is at X −580…−526 and the tube's top
opening only runs X −310…−2, so there is no other way in.

**4 × M5 at Y ±16, Z −26 and Z −36**, into two 1/2" bars welded down the inside of the rear walls
(`BP_Boss_L/R_1-2`, X −560…−547.3, Z −39…−17). 12.7mm of thread depth.

**The bars must stop at Z −39.** Running them to −43 clips the tube's interior corner radius,
which begins at Z −39.9 (0.023 cm³ each).

**All four screws are low** — Y ±16 spread 32mm, but only 12mm apart in Z. The switch carrier
occupies Y ±22, Z −16…+26.8 and blocks every upper position. The top of the plate is held by the
rear locating tab instead. Freeing an upper pair would mean trimming the carrier's flange, which
risks disconnecting it from the wall rails at Z 13…23.5.

**The pivot pin cannot retain the backplate** — pin at X −552, backplate at X −563.18…−560, 8mm
apart and never intersecting. What the pin *does* need is drift access: a **⌀6 hole in `PR-11-Side-Rear-L`
at X −552, Z +1**, otherwise the side skin traps it.

Disassembly, each step verified by sweeping the part clear of everything:
1. drift the pin out through the `PR-11-Side-Rear-L` hole
2. draw the trigger straight back, lever sliding out through the backplate slot
3. undo 4 × M5 — the backplate lifts off and brings the switch carrier with it

### TRIGGER — press DOWN, tail rises, switch sits ABOVE the tail

![Butterfly, switch carrier, microswitch and the ⌀4 pin. The switch sits ABOVE the tail.](img/05-trigger-group.png)
*Butterfly, switch carrier, microswitch and the ⌀4 pin. The switch sits ABOVE the tail.*
**Direction matters and I got it backwards once.** Pressing the butterfly down at the rear swings
the tail *up*, because the press point is behind and above the pivot. The switch therefore sits
**above** the tail, not below it. If the switch is under the tail the mechanism can never fire.

Switch is an **Omron SS-5GL13** — subminiature, simulated roller lever. Body 19.8 × 10.2 × 6.4mm,
mounting holes ⌀1.6 at 9.5mm pitch, **OT min 1.0mm, OF 50gf**. The lever type was chosen
deliberately: a bare plunger only tolerates a few tenths of overtravel and the striker would
bottom on the switch body.

Geometry: pivot X −552 **Z +1**, lever run Z −6…+8, striker on top of the lever at X −540 rising
to Z +10.0, switch actuator free at Z +10.4 (**0.4mm gap**), body Z +10.4…+20.6.

  5.0 deg -> presses 0.65mm   FIRES
  5.5 deg -> presses 0.75mm   hard stop engages, inside the 1.0mm OT

**`PR-52-Trigger-Switch-Carrier` registers off the tube itself**, so the switch lands in the right place
without measuring: a narrow ceiling pad at Y ±18 bearing on the interior roof (**measured at
Z +27.0**, not the +20.95 I first assumed — the rear of the tube is uncut), and wide rails at
Y ±22.0 on the flat part of the side walls. **The pad must be narrower than the rails** — the
interior corner radii pull the width in to ±20.38 by Z +26.8, so a full-width roof clashes.

Slides in from the rear before the backplate is welded; also bolts through 2 × M4 at Y ±16, Z −8.

**Fusion joints are not available here** — `AsBuiltJointInput is only supported in parametric`,
and this document is direct-modelling with no timeline. Motion has to be verified by transforming
a copy and running boolean intersections, which is what every check above does.

### Superseded trigger designs — do not revisit
The F2 is electronic, so the trigger only has to close a microswitch. **The switch does not need
to be inside the tube — only its wires do.**

**Pivot is a ⌀4.2 pin through BOTH tube side walls at X −552, Z +6.** Anchoring in the steel beats
any bracket, and it puts the spring inside where there is room.

- `PR-51-Trigger-Butterfly` — the donor butterfly plus an integral lever: a drop behind the backplate
  (X −578…−569, Z +2…+30) then a run forward through the backplate (X −572…−534, Z +2…+10).
  Pivot bore at X −552 Z +6, ⌀3 peg hole in the tail at X −534 for the return spring.
- `Trigger_Switch_Mount` — printed, bolts to the backplate's inner face with the 2 × M4 at
  Y ±16 Z +8. Holds a microswitch under the tail at X −540, Z −6, plunger up.
- Backplate carries a **16 × 15mm lever slot** at Y 0, Z −2…+13.

Lever ratio: thumb radius 51mm, tail radius 18mm. **6° of trigger travel = 5.33mm at the thumb
and 1.88mm at the tail** — a D2F needs ~0.5mm, so 2–3° is enough to fire. Return is a torsion
spring on the pivot pin; the ⌀3 tail peg is the alternative anchor for a tension spring.

Verified clear of tube, backplate and switch mount through 10°.

**Two rejected versions, do not go back to them:**
1. A 27mm slab arm hanging off the trigger with a ⌀7 boss poking through the backplate into the
   tube, plus two welded steel ears for the pivot. Clunky, and the boss bound in its hole as it
   tilted through the arc.
2. Pivoting on a printed bracket bolted behind the backplate, switch outside. Tidier, but the
   pivot was in plastic and there was nowhere good for a spring.

**The switch mount's flange must be split either side of the lever's Y ±6 channel** or it fouls
the lever at rest (0.096 cm³).

### BARREL — EMT is the barrel, only the jacket is printed
**Do not print the barrel.** 1" EMT conduit (⌀29.54) *is* the barrel, running X 13.65 (bottomed
in the socket) to X 1010.5 — 996.9mm / 39-1/4", 2.49 lb. Socket ID 30.18 gives 0.64mm diametral
clearance over the full 100mm of engagement.

**The perforated jacket IS printed** — it is the M2's identifying feature. X 26.75…287 (260.2mm),
bored ⌀38.90 over the socket and ⌀30.20 for the EMT, with a centring ring at X 274…284 so it
can't flop on the conduit. Fits a 300mm bed stood on end (+X up, 9.3% overhang).

The jacket-to-thin-barrel step is at **X ≈ 285**; X 285…298 is a smooth prismatic zone with no
vertices, which is why it cuts cleanly there.

**The jacket's rear runs to X 24.80, not 26.75.** Trimming it to the barrel plate's front face
(26.35) + 0.4 left a **1.95mm gap** to `PR-17-Front-Sight-Boss`, which ends at X 24.80 — the 1/4" plate showed
through all the way round. **Trim the jacket to PR-17-Front-Sight-Boss, not to the plate.**

To extend it: the jacket's section is **constant over X 26.75…29.00** (2.235 cm³ at every slice),
so take a 1.95mm slice and translate it back — an exact extrusion without needing a sketch. Then
pocket it Y ±25.8, Z −46.5…30.5 to clear the plate. Adds 4.47 cm³.

**Bond the joint, don't bolt it.** The butt gives **1,615 mm² of contact** (70% of the jacket's
2,295 mm² rear face — `PR-17-Front-Sight-Boss` is only Y ±30 against the jacket's Y ±39.6, so they don't fully
overlap). That is several times what epoxy needs, and the ⌀38.90 bore over the socket already
locates it radially across 87mm. 23 bolt positions were found viable in the top band, but **every
one is unreachable once assembled** — 260mm of jacket in front, 38mm of PR-17-Front-Sight-Boss behind.

EMT is galvanised: etch-prime before paint, and never weld or braze it (zinc fumes). It doesn't
need welding — it's a slip fit.

The socket leaves **88.8mm exposed** ahead of the front skin. It was positioned forward when a
full-length printed shroud was going to hide it; the jacket now covers it, so that is moot.

### CHARGING HANDLE — slide + spring return, 150mm travel, IN THE EXISTING SLOT

![Handle, carrier and shoe. The carrier sandwiches the tube wall through the existing slot.](img/06-charging-handle.png)
*Handle, carrier and shoe. The carrier sandwiches the tube wall through the existing slot.*
**Design the carrier to fit the slot; do not enlarge the slot to fit the donor part.** The
upstream `charging.stl` has a shoe 17.6mm tall, and I once cut a 214 × 19mm aperture in the left
wall to pass it. That was wrong — the donor shoe is discarded anyway (the handle bolts to a
carrier we make), so the neck can be any size we like. It removed 4066mm² where 2032mm² does, and
forced an RFQ change for nothing. Reverted.

Track = **the existing 192 × 8mm slot**, X −540…−348, Z −12…−4, both walls, R4 ends. Straight
section is X −536…−352 = 184mm. Neck 34mm + 150mm travel = 184mm, an exact fit.

**No guide rod. No shaft. Three printed parts sandwich the wall and the slot is the track.**
An earlier version had a 1/4" rod on two welded tabs — deleted, it was a complicated part for no
benefit and cost 0.128 lb of steel and two weldments.

- `PR-43-CH-Shoe`    X −386…−352, **Y −22…−14**, Z −16…0 — inside the tube, 16mm tall behind an 8mm
               slot so it cannot pull out. 2 × M4 heat-set inserts.
- `PR-42-CH-Carrier` neck Y −30…−22, **Z −11.5…−4.5 (7mm in an 8mm slot)**; pad X −386…**−280**,
               Y −38…−30, Z −13…+3. 2 × M4 clearance to the shoe, 4 × M6 clearance to the handle.
- `PR-41-CH-Handle`  donor arm outboard of Y −48, unioned to a **full-length foot** X −386…−280,
               Y −48…−38, Z −13…+3. **4 × M6 heat-set inserts in the foot.**

Clamped stack is skin-outer-face (Y −30.0) to tube-inner-face (Y −22.35) = **7.65mm**, neck spans
8.0mm → **0.35mm running clearance**. Do not "fix" the neck to 7.65.

Mating area handle-to-carrier is **1696 mm²** of flat contact. The earlier 2 × ⌀14 boss joint was
replaced because it only touched at two spots and M4 was too small.

**Assembly order:** bolt handle to carrier off the gun (M6 heads sit in counterbores on the pad's
inner face and are unreachable once fitted) → offer the pair to the slot → turn the shoe 90° about
X so its 8mm edge is vertical, pass it through the slot, rotate home → 2 × M4.

### The pad must cantilever forward — the slot and the handle do not line up
Two measured facts that force the design:
- **`PR-12-Side-Rear-R` is open only over X −540…−350.** Forward of that the panel is solid, so the neck
  cannot go forward — it has to stay inside that window.
- **The donor handle only has material to bolt into over X −320…−262** (probe Y −70…−46). Its
  arm root is forward of the panel opening entirely.

So the neck sits at X −386…−352 and the **pad cantilevers 106mm forward to X −280** to reach the
handle. Do not try to move the slot forward to meet the handle: moving it 28mm forward put the
neck into solid panel (0.466 cm³) and the bolts still had nothing to bite. Reverted.

Joint: **2 × M6** through the handle into heat-set inserts (⌀8.0 × 9mm) in ⌀14 bosses on the pad
at **X −306 and −286**, the bosses registering in ⌀14.4 pockets in the handle so the joint is
located as well as clamped. M4 was too small. Confirmed 0.92 and 1.14 cm³ of handle material
behind each boss — check this, because most of the pad's length has nothing behind it.

Trimming the donor at Y −38 leaves a **0.286 cm³ loose fragment** at X −360…−351; delete it or the
STL exports as two shells.

**The pad's top must not exceed Z +3.** The left skin's outer surface steps outboard above
Z ≈ +3.3; a pad reaching Z +4 buries 0.7mm into the panel at every stroke position.

**The skin already has the slot.** `PR-12-Side-Rear-R` is open over the slot footprint — the corpus models
it as a through-feature, so no channel needs cutting. Verify rather than assume: a cut that
removes 0.00 cm³ means either it was already open or the boolean silently failed.

**Sweep against the SKINS too, not just tube + weldments.** The first travel check omitted them
and missed a standing 0.071 cm³ interference at every position.

**The return is shock cord, not a steel spring.** 150mm of travel needs a ~350mm compression
spring; there is only 230mm of clear tube behind the carrier. Route the cord at **Y −20, Z −30**:
clear of the cradle (reaches Y −18), the F2 (Y ±12.7), the hinge tab (Z −20 up) and the pintle
tabs (Z −35 down). That is the only end-to-end clear path.

### THE DONOR PARTS ARE STILL FACETED — and cannot be converted automatically
11 bodies are faceted STL conversions totalling **67,497 faces**. Everything designed
from scratch is native: the tube is 135 faces with 73 real cylinders, the weldments are
4-32 faces each. So **the STEP a fabricator receives is clean** — only the cosmetic
printed parts are faceted, and those ship as STL anyway.

| | bodies | faces |
|---|---|---|
| faceted (donor-derived) | 11 | 67,497 |
| native (designed here) | 26 | ~900 |

**Do not waste time on `PrismaticMeshConvertMethodType`.** Tested exhaustively against
`FacetedMeshConvertMethodType`:

- Prismatic with no face groups -> identical output
- Prismatic + `meshGenerateFaceGroupsFeatures`, Fast (29 groups) -> identical output
- Prismatic + face groups, **Accurate** (36 groups) -> identical output

592 faces, all planar, zero cylinders, every time — on both a 592-face trigger and a
20,730-face barrel. Fusion generates the face groups correctly and the convert ignores
them. Prismatic almost certainly requires the **Product Design Extension**, which the
docs only flag for Organic.

Two API traps found on the way: `meshGenerateFaceGroupsFeatures.createInput()` takes a
**single MeshBody, not a list**, and the method property is
`meshGenerateFaceGroupsMethodType` (0 = Fast, 1 = Accurate) — a wrong name silently
swallowed by a bare `except` leaves it on Fast.

**Rebuilding these means re-authoring the M2's panel and rivet detail by hand.** That is
not a conversion, it is modelling a new part, and the result would no longer be
HappyBattleSheep's artwork — which is the whole point of the skins. Worth doing only to
change the surface detail or to drive the panels parametrically.

### Fusion gotchas learned here
- **An exception anywhere in a script rolls back everything that script did.** A mesh convert that
  succeeded was silently undone by a trailing `isLightBulbOn` error on the consumed mesh. Wrap
  `main()` in try/except and print the traceback instead of letting it propagate.
- **`exportManager` body-level STL export can report `execute=True` and write nothing.** It failed
  on the 20k-face barrel at every refinement level. Export the **occurrence or component** with
  everything else hidden instead, and always stat the file afterwards.
- Mesh → BRep: `component.features.meshConvertFeatures` with
  `FacetedMeshConvertMethodType`. ~5s for 20k triangles. In a direct-design doc `add()` returns
  null but the conversion still happens; find the new body by name.

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
  the ~5mm of tab past the envelope drove PR-17-Front-Sight-Boss into the steel by 0.5795 cm³.
  **Whenever the tube's extents change, ENV changes with them** — query
  `tube.boundingBox` and check it rather than assuming.
- **Feed way**: no skin material above the tube in X −334.3 … −13.3. Deletes `Top2` entirely and
  ends `PR-15-Top-Deck` at X −334.3 — the top deck only exists *behind* the hatch.
- **Pintle lug**: X −395 … −325, everything **below Z −67**. The steel tabs are the lug.
  Cut only below −67, not −50 — the shoulder Z −50…−67 is real side-panel geometry.
- **Front trim**: X 26…41, Y ±14, Z −36…−22 — strands left forward of the barrel plate.
- **Front ring trim**: cylinder r19.8 on the barrel axis, X +19.5…+27.0. Removes two floating
  concentric rings (r15.1 and r19.4) left in PR-17-Front-Sight-Boss when the socket bore went through.
  Socket OD is r19.05, so the trim clears the steel by 0.75mm.
- **Pin bore**: ⌀6.35 at X −9, Z +62.5 cut from **every** skin so one pin passes through
  PR-17-Front-Sight-Boss lug → tab → hatch boss → tab → PR-17-Front-Sight-Boss lug.

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
| PR-18-Bottom-Rear | 31.7% | 3.4% |
| PR-15-Top-Deck | 22.0% | 4.6% |
| PR-19-Bottom-Front | 21.3% | 0.4% |
| PR-12-Side-Rear-R | 11.3% | 2.3% |

Flat-and-ironable is the chosen orientation; the cost is 20–30% of surface needing support on
several pieces. All parts pass watertight with correct normals and 1 shell (PR-19-Bottom-Front's two
rails, left deliberately).

## Still open

1. **Skin-to-tube fastening** — no bolt bosses, holes or captive nuts anywhere. Biggest gap.
2. **Rear closure** — tube's back end at X −560 is open. No backplate, grips or trigger.
3. **Verify the three inferred pin positions** against real hardware before drilling steel.
4. **CH slot width** — the 8mm is a guess, not measured. Carrier/handle not modelled.
5. **Torsion cross-strap** over the 139mm U-channel run (top + both walls cut).
6. `PR-19-Bottom-Front` was 2 shells (two bottom rails) and is now split into `-L` and `-R`.
7. Hatch latch, feed tray detail.
8. Deliverables not produced: 1:1 plotter template (single sheet, not tiled), STL exports.

## REMOVABLE BARREL — M5 set screws in the socket

![Socket welded to the front plate; the 1" EMT drops in and is held by two set screws.](img/07-barrel-mount.png)
*Socket welded to the front plate; the 1" EMT drops in and is held by two set screws.*
The socket is **welded to the barrel plate**, so it is fixed and can be tapped. Wall is
(38.10 − 30.18)/2 = **3.96mm**, enough for full M5 thread.

- 2 × M5 tapped **at X 55 and X 75**, entering from underneath (tap drill ⌀4.2, Z −21…−15.05)
- **Stop the tap hole at Z −15.05.** The socket ID is r15.09 and the EMT OD r14.77; drilling past
  −15.05 cuts the EMT instead of leaving the screw to press on it.
- The screws close a **0.32mm radial gap**. Dimple the EMT at both positions so they locate
  positively instead of relying on friction.

**X 95 lands on one of the jacket's cooling holes** — the jacket has no material underneath there.
X 55 and 75 are solid.

The screws are buried under the jacket, so the jacket gets **2 × ⌀7 access channels** straight up
from its underside at the same X. Verified a 3.0mm driver shaft runs clear through jacket, socket
and EMT to reach both screws with everything assembled. Barrel then slides straight out forward —
swept 150mm, no catch.

The jacket itself stays bonded to `PR-17-Front-Sight-Boss`; it never has to come off to change the barrel.

## NATIVE REAUTHORING — proven on the barrel jacket
`PR-21-Barrel-Jacket` is authored from primitives, not converted from mesh.

| | faceted | native |
|---|---|---|
| faces | 17,422 | **57** (13 planar, 39 cylindrical, 5 conical) |
| STEP | ~1 MB | 382 KB |
| editable | no | hole count, diameter, pitch and profile are all variables |

**305x fewer faces**, and it is real analytic geometry — the holes are true cylinders, the
flanges true cones.

### How the pattern was measured
Vertex-occupancy does not work: a smooth cylindrical band has vertices only at its edges, so
empty bins read as holes. Two wrong answers came out of that before ray-casting gave the truth.

**Ray-cast inward from r=60 on an (x, theta) grid and record the FIRST-hit radius.** Hit near
r=39.6 means wall; anything deeper means a hole. Counting hits alone is useless — every ray
crosses the far wall, so everything reads as material.

Measured result: **4 holes per row at 90 degrees, alternate rows offset 45 degrees**, pitch
25.5mm, 7 rows from X 88, d26. Staggered, not aligned — an earlier read said 8 aligned rows of
d20 and looked visibly wrong against the donor.

### Profile, measured off the donor
Rear flange r50.80 to X 38, taper to r41.35 by X 41, r41.35 to X 82, taper to r39.60 by X 90,
main tube r39.60 to X 272, muzzle flange r41.40 X 272..284. Bore r19.45 over the socket to X 46,
then r29.13; centring ring r15.10 at X 273..285.

**Do not forget the barrel-plate pocket** (Y +/-25.8, Z -46.5..30.5 over X 24.3..26.75). Without
it the native jacket fouls `ST-04-Barrel-Plate` by 3.9 cm3.

### What is NOT worth reauthoring
The jacket worked because it is a body of revolution with a regular hole pattern. The rest are
not:

- `PR-31-Spade-Grips` (17,621), `PR-41-CH-Handle` (10,134) - organic knurled handles. Primitives would
  look worse than the donor.
- `PR-12-Side-Rear-R` (6,631), `PR-11-Side-Rear-L`, `PR-15-Top-Deck`, `PR-16-Top-Cover`, `PR-17-Front-Sight-Boss` - flat panels carrying the M2's
  rivet and rib detail. The rivets are a trivial pattern; the panel outlines and raised detail
  are freeform and would take days to approximate badly.

Reauthoring those means re-drawing HappyBattleSheep's artwork, which is the thing worth keeping.
