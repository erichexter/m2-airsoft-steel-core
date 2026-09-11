# RFQ — Laser-cut core tube

**File:** `M2_core_tube_RFQ.stp`
**Quantity:** 1

## Vendor — OSH Cut

**Order as: `3" x 2" x 0.12" wall - Rectangular A500 Cold-Formed Carbon Steel`**
(catalogue: app.oshcut.com/catalog/tube — in stock)

**Orient it 2" wide (Y) × 3" tall (Z).** The catalogue calls it 3 × 2; this design uses the 2"
dimension as the width. They accept STEP directly.

### Confirmed stock spec

| | |
|---|---|
| Outer | 3.000" × 2.000" |
| **Inner** | **2.760" × 1.760" = 70.10 × 44.70 mm** |
| Wall | 0.120" |
| Outside corner radius | 0.118" to 0.360" |
| Weld seam | Yes |
| Max length | 235" |
| Yield / Ultimate | 39 / 45 ksi |

The inner dimensions match this design exactly — every clearance was checked against
70.10 × 44.70 mm.

## Part

| | |
|---|---|
| Cut length | **23.210"** (589.52 mm) |
| Finished mass | 5.97 lb |
| Modelled corner radii | R0.240" outside, R0.120" inside |

Straight tube, both ends square. **The STEP carries A500 corner radii** — without them OSH Cut's
profile matcher identifies the section as aluminium extrusion, since nothing in their steel
catalogue has square corners.

## Features

| Feature | Face | Location | Size |
|---|---|---|---|
| Top opening | top | X −310 … −2 | **straight cut at Z +24, full width** |
| Belt slot | both sides | X −141 … −2 | open to the cut top edge, R4 bottom |
| CH shaft slot | both sides | X −540 … −348, Z −12…−4 | 192 × 8mm, radiused ends |
| Air line | bottom | X −410, centreline | ⌀12.7 (1/2") |
| Front mount bore | both sides | X +1, Z −33 | ⌀14.6 |
| Pintle notches | bottom corners | X −384 … −338 | for the 1/2" pintle tabs |
| Front locating tabs | top + bottom | X +20 … +26.35 | 25mm wide |
| Rear locating tabs | top + bottom | X −563.18 … −560 | 25mm wide |

The top cut is **one plane at Z +24** — the height where the corner radii begin, so it lands flat
on both side walls with no leftover arc, no flanges and no notches. Everything above goes.

Locating tabs at both ends are **exactly their plate's thickness** (1/4" front, 1/8" rear) so the
tab and plate faces finish flush — nothing protrudes. They pass through matching through-slots,
so the plates and the tube are both laser-only with no milled pockets anywhere.

Smallest feature is the 8mm CH slot — 67× the 0.120" wall.

## Notes for the vendor

- **The STEP declares centimetres** (`SI_UNIT(.CENTI.,.METRE.)`). That's Fusion's internal unit and
  it exports that way regardless of display settings. Valid STEP; any conforming reader scales it
  correctly. Flagged only so a 10× preview doesn't cause alarm. All dimensions here are mm and in.
- The top opening and belt slot **meet** at X −2 and form one continuous aperture. Modelled as a
  single cut — please don't leave a web between them.
- Over X −310 … −2 the tube is a U-channel by design. It is braced by weldments after cutting.
- ±0.005" is more than adequate. Feature positions matter more than overall length; the tube can
  run ±0.030" long without consequence.

## Two risks from the real profile

### Corner radius is a range
Spec is 0.118"–0.360". The model uses R0.240" outside (2× wall, conventional for 0.120"). If the
delivered tube lands at the large end, the flat bottom narrows and the **pintle tab notches** shift
relative to the corner. Measure the corner radius on arrival before welding those tabs.

### Internal weld seam
Position isn't specified and is usually on one flat face. It could foul the hinge tabs lapping the
inner wall or stop the cradle seating flat. **Locate the seam on arrival and orient the tube so it
falls on an unused face** — the right side above the CH slot is the least congested.
