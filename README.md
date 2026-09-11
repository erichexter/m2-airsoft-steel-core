# M2 Airsoft — Steel Core Conversion

A welded steel structural core for a 3D-printed Browning M2 airsoft replica.

Instead of printing the receiver as a structural part, this design puts all the load into a
single piece of **2" × 3" × 0.120" wall rectangular steel tube**. The printed parts become
non-structural cosmetic skins that bolt and glue over it, plus a printed cradle that carries the
airsoft engine and hop-up.

The result is stiffer, survives being carried by the barrel or dropped, and puts the hinge,
pintle and barrel mounts into welded steel rather than plastic.

**~8.75 lb of steel, ~2.6 lb of PLA, ~14 lb finished** with engine and hardware.
For scale: a real M2HB is 84 lb; commercial airsoft M2 replicas run 33–44 lb.

---

## What's here

```
cad/M2_core_tube_RFQ.stp   Core tube alone — upload this for a laser-cut quote
cad/M2_steel_core.stp      Full steel assembly + engine cradle
cad/RFQ-core-tube.md       Stock spec, feature table, vendor notes
stl/                       Printed parts, ready to slice
source/                    Fusion 360 archive (.f3d)
tools/stlcheck.js          Printability checker — run it on the STLs
docs/BUILD-NOTES.md        Full build notes: cut list, coordinates, weld plan, gotchas
LICENSE                    CC BY-NC-SA 4.0
```

The STEP and STL files contain **only original work** — the steel design, the printed skins
derived as described under ATTRIBUTION, and the cradle.

### Checking the prints

```
node tools/stlcheck.js stl/*.stl
```

Reports triangle count, watertightness (open and non-manifold edges), degenerate facets,
connected shells, bounding box against the bed, normal orientation, and overhang burden for each
axis-aligned orientation. All current parts pass watertight with correct normals.

**It only tests axis-aligned orientations.** `Hatch.stl` is 329.9mm and reports as not fitting;
it does fit laid diagonally (294mm footprint on a 300mm bed, 5.7mm margin).

---

## Design summary

**Core tube** — 2" × 3" × 0.120" wall, 22-7/8" long, offset 8mm below the barrel axis so the
front mounting bore clears the floor. Cut for a top opening, a belt slot, a charging-handle shaft
slot through both walls, an air-line pass-through, and the front mounting bore.

**Weldments**
- Pintle tabs ×2, 1/2" plate, tapered with a ⌀12 bore
- Hinge tabs ×2, 1/8" plate, mounted **inside** the tube with a round head concentric with the
  pin so the cover's relief is a plain circular pocket and rotation is free by construction
- Hatch spine, 1/8" × 1" flat, inlaid into the cover so hinge load never passes through plastic
- Barrel plate, 1/4", welded across the open tube end
- Barrel socket, 1-1/2" OD × 1.188" ID DOM

**Barrel is 1" EMT conduit.** OD 1.163", and the DOM socket's 1.188" ID takes it with 0.64mm of
clearance and up to 101mm of engagement. Note that 1" *pipe* of any schedule is too small — NPS
is nominal, and 1" sch40 has a 1.049" ID.

**Engine** — PolarStar F2, HPA. No battery bay needed; the air line exits through the tube floor.

See [docs/BUILD-NOTES.md](docs/BUILD-NOTES.md) for the full cut list, every coordinate, the weld
plan, and the fabrication order.

---

## Stock list

All imperial, 12" minimum lengths, cut to length only — no rip cuts.

| # | Stock | Buy | For |
|---|---|---|---|
| 1 | 2" × 3" × 0.120" wall rect tube | 24" | Core tube |
| 2 | 1-1/2" OD × 1.188" ID DOM | 12" | Barrel socket |
| 3 | 1/2" × 2" flat bar | 12" | Pintle tabs |
| 4 | 1/4" × 3" flat bar | 12" | Barrel plate |
| 5 | 1/8" × 1" flat bar | 24" | Hatch spine + hinge tabs |
| 6 | 1/4" round bar | 12" | Hinge pin |
| 7 | 1/2" round bar | 12" | Pintle pin |
| 8 | 9/16" round bar | 12" | Front mount pin |

---

## Status

Working design, not yet fabricated. Known open items:

- No skin-to-tube fastening scheme yet — no bolt bosses or captive nuts
- Rear of the tube is open; no backplate, grips or trigger
- Hinge, pintle and front-mount pin positions are inferred from the printed model rather than
  measured from real hardware — **verify before drilling steel**
- Charging handle slot width is an estimate; the carrier isn't modelled

---

## ATTRIBUTION

The cosmetic skin geometry in this project is **derived from a third-party 3D-printed Browning M2
receiver model** that is not mine and is not redistributed here. Only the steel core design, the
cradle, and the documentation are original work covered by the LICENSE.

If you intend to publish the printed skin STLs, check the original model's license first — a
derivative work cannot be relicensed beyond what the source permits.

The PolarStar F2 engine and FCU CAD models are the property of PolarStar Airsoft and are
referenced for fitment only. They are not included in this repository.

---

## Note

This is an **airsoft replica** — a non-firing recreational replica that launches 6mm plastic BBs
at sub-lethal energies. It has no capability to chamber or fire live ammunition, and nothing here
describes or enables that.

Local law on replica firearms varies. Orange muzzle markings are required in some jurisdictions
and transport rules differ by region — check yours.
