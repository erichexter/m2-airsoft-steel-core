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

- The top opening and the belt slot **meet** at X −2 and form one continuous aperture. They are
  modelled as a single cut in the STEP; please don't treat them as separate features that leave a
  web between them.
- Over X −141 … −2 the tube is effectively a U-channel (top and both upper side walls removed).
  This is intentional. Expect some relieving; the part is braced by weldments after cutting.
- ±0.005" on overall dimensions is more than adequate here. Feature positions matter more than
  the absolute cut length — the tube length can run ±0.030" without consequence.

## Confirm before ordering

2" × 3" × 0.120" wall may or may not be in the vendor's public tube inventory. If it isn't, the
nearest substitute is **2" × 3" × 0.125"** — the 0.005" of extra wall changes nothing in this
design, since all interior clearances were checked with ≥2mm of margin.
