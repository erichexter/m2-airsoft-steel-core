# RFQ — Laser-cut core tube

**File:** `M2_core_tube_RFQ.stp`
**Quantity:** 1

## Stock

| | |
|---|---|
| Profile | 2" × 3" rectangular tube |
| Wall | 0.120" |
| Material | Mild steel (A500 or equivalent) |
| Cut length | **23.150"** (588.0 mm) |
| Finished mass | 6.39 lb |

Straight tube, both ends square (90° to centerline) — well inside the 45° minimum.

The front end carries **two locating tabs** (one top, one bottom) formed by cutting the wall away
either side of them. They project 8mm past the nominal end, which is why the stock length is
588mm rather than 580mm. The tabs pass **all the way through** matching slots in a 1/4" plate, so
both parts are laser-only — no milled pockets anywhere.

## Features — all cut from the tube

| Feature | Face | Location | Size |
|---|---|---|---|
| Top opening | top | X −310 … −2 | 308 × 38.0mm, R5 corners |
| Belt slot | both sides | X −141 … −2 | open to the top edge, R4 bottom corners |
| CH shaft slot | both sides | X −540 … −348, Z −12…−4 | 192 × 8mm, fully radiused ends |
| Air line hole | bottom | X −410, on centreline | ⌀12.7 (1/2") |
| Front mount bore | both sides | X +1, Z −33 | ⌀14.0 |
| Locating tab, top | top wall | X +20…+28, Y ±12.5 | 25mm wide, 8mm long |
| Locating tab, bottom | bottom wall | X +20…+28, Y ±12.5 | 25mm wide, 8mm long |

The two tabs at the front end are formed by removing the wall either side of them. They pass
**through** slots in a 1/4" plate that welds across the tube end, protruding 1.65mm past its far
face so a weld bead can be run on both sides. The plate self-locates — no jig needed.

**Tab width and position matter more than the tube's overall length.** The tabs set Y and rotation;
the two of them together set Z; the tube end face sets X.

Origin in the STEP is the barrel axis: **X = 0 is 20mm back from the front end**, X runs negative
toward the rear. Z = 0 is the barrel axis; the tube is deliberately offset so it spans
Z −46.1 … +30.1.

Smallest feature is the 8mm-wide CH slot — 67× the 0.120" wall, so nothing is near the
thin-feature limit. Everything else is larger.

## Notes for the vendor

- **The STEP declares centimetres** (`SI_UNIT(.CENTI.,.METRE.)`) — that's Fusion's internal unit
  and it exports that way regardless of display settings. It is valid STEP and any conforming
  reader scales it correctly. Flagging it only so that if a preview ever looks 10× off, the cause
  is obvious. All dimensions quoted in this document are millimetres and inches.

- The top opening and the belt slot **meet** at X −2 and form one continuous aperture. They are
  modelled as a single cut in the STEP; please don't treat them as separate features that leave a
  web between them.
- Over X −141 … −2 the tube is effectively a U-channel (top and both upper side walls removed).
  This is intentional. Expect some relieving; the part is braced by weldments after cutting.
- ±0.005" on overall dimensions is more than adequate here. Feature positions matter more than
  the absolute cut length — the tube length can run ±0.030" without consequence.

## VENDOR — OSH Cut

**Order as: `3" x 2" x 0.12" wall - Rectangular A500 Cold-Formed Carbon Steel`**
(their catalogue: app.oshcut.com/catalog/tube)

That is exactly the section this design is built around — no substitution, no compromise.
**Orient it 2" wide (Y) × 3" tall (Z).** The catalogue calls it 3 × 2; the design uses the 2"
dimension as the width.

OSH Cut accepts STEP directly, along with DXF, SVG, AI, SLDPRT, IPT, IGS, x_t and others.

### Why not RMFG
Checked 2026-09-11: **2 × 3 × 0.120 A500 is not in RMFG's public tube list.** Their A500
rectangular inventory is 1.5×3×.120, 3×1.5×.083, 3×2×.250, 4×2×.120, 4×2×.188, 4×3×.250,
6×3×.3125. The only one that fits is 3×2×**.250**, which doubles the steel to 14.77 lb (vs 7.50)
and leaves the engine cradle 1.05mm of clearance per side. Rejected. They will quote other sizes
on request, but OSH Cut stocks the right one outright.

For reference, what the other candidates would have cost:

| Stock | ID | Verdict | Weight (588mm) |
|---|---|---|---|
| 3 × 2 × .250 | 38.1 × 63.5 | fits, doubles the weight | 14.77 lb |
| 1.5 × 3 × .120 | 32.0 × 70.1 | cradle (36mm) will not fit | 6.71 |
| 4 × 2 × .120 | 44.7 × 95.5 | 101.6mm tall vs 93.6mm available | 9.08 |
| 2 × 2 × .120 sq | 44.7 × 44.7 | fits but 25mm shorter — big redesign | 5.92 |
| 3 × 3 × .120 sq | 70.1 sq | 76.2 wide; receiver necks to 60mm | 9.08 |
| **3 × 2 × .120 — ordered** | **44.7 × 70.1** | — | **7.50** |

## CONFIRMED STOCK SPEC (OSH Cut, 2026-09-11)

| | |
|---|---|
| Outer | 3.000" × 2.000" |
| **Inner** | **2.760" × 1.760" = 70.10 × 44.70 mm** |
| Wall | 0.120" |
| Outside corner radius | **0.118" to 0.360"** (3.00 – 9.14 mm) |
| Weld seam | **Yes** |
| Max length | 235" |
| Alloy | A500, mill finish, in stock |
| Yield / Ultimate | 39 ksi / 45 ksi |

**The inner dimensions match this design exactly** — 70.10 × 44.70 mm is the interior every
clearance was checked against. No adjustment needed.

## TWO RISKS FROM THE REAL PROFILE

### 1. Corner radius is a RANGE, and the pintle tabs sit near it
The spec gives 0.118"–0.360" (3.0–9.14 mm) outside.

**The model now carries A500 radii: R0.240" outside, R0.120" inside** (2× and 1× wall, the
conventional values for 0.120" wall, and mid-range of the published spec). Sharp corners caused
OSH Cut's profile matcher to identify the section as **aluminium extrusion instead of A500 steel**
— aluminium is the closest thing in their catalogue to a sharp-cornered rectangle. Adding the
radii fixes the match.

Consequence for the **bottom face flat**, where the pintle tabs weld:

| Actual corner R | Flat bottom spans | Pintle tab contact |
|---|---|---|
| 0.118" (3.0mm) | Y ±22.4 | 6.7 mm — fine |
| 0.360" (9.14mm) | Y ±16.3 | **0.6 mm — will not seat** |

The pintle tabs run Y 15.7…28.4. At the small end of the radius range they land on flat steel;
at the large end almost the whole tab is over the corner radius and the joint has nothing to sit
on. **Measure the corner radius on the actual tube before welding the pintle tabs.** If it comes
in large, either relieve the tab's top edge to match the radius or move the tabs inboard — but
note that moving them shifts the ⌀12 bore away from the printed lug position.

Everything else is clear: the **hinge tabs** sit at Y ±19.18…22.35, Z 0…+18 on the inner side
wall, and even a 6.1 mm inside radius leaves flat from Z −36.95 to +20.95. No conflict.

For the skins, rounded corners are harmless — they give *more* clearance, not less.

### 2. The tube has an internal weld seam
"Weld Seam: Yes". Position isn't specified and is usually on one flat face. It could interfere
with the hinge tabs lapping the inner wall, or with the engine cradle seating flat.
**Locate the seam on arrival and orient the tube so it falls on an unused face** — the right side
above the CH slot is the least congested.
