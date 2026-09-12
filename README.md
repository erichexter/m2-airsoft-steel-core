# M2 Airsoft — Steel Core Conversion

A welded steel structural core for a 3D-printed Browning M2 airsoft replica.

Instead of printing the receiver as a structural part, this design puts all the load into a
single piece of **2" × 3" × 0.120" wall rectangular steel tube**. The printed parts become
non-structural cosmetic skins that bolt and glue over it, plus a printed cradle that carries the
airsoft engine and hop-up.

The result is stiffer, survives being carried by the barrel or dropped, and puts the hinge,
pintle and barrel mounts into welded steel rather than plastic.

**~11.2 lb of steel** (including the EMT barrel) and **~3.6 lb of PLA** — call it **~17 lb
finished** with the engine and hardware. The PLA figure assumes a 2mm shell and light infill;
printed solid the same parts would be 8.9 lb.
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

**Charging handle** — slides, spring returns, **150 mm of travel**, and it runs in the
**existing 192 × 8 mm slot**. No extra metal is removed for it and **no guide rod is used** —
three printed parts sandwich the receiver wall and the slot itself is the track:

| Part | Where |
|---|---|
| `CH_Shoe` | inside the tube, Y −22…−14, 16 mm tall behind an 8 mm slot so it can't pull out |
| `CH_Carrier` | 7 mm neck through the slot, pad outside the panel at Y −38…−30 |
| `CH_Handle` | full-length foot bolting to the pad, 1,696 mm² of flat contact |

The shoe and carrier clamp a 7.65 mm stack — skin plus steel wall — across an 8 mm neck, leaving
**0.35 mm of running clearance**. Two M4 bolts hold the sandwich; four **M6** into heat-set
inserts in the handle's own foot carry the pull. Assemble the handle to the carrier off the gun,
then fit the pair and add the shoe.

To install the shoe, turn it 90° about its long axis so its 8 mm edge is vertical, pass it through
the slot, and rotate it home.

**Trigger** — the butterfly and its lever are **one printed part**. It runs through a slot in the
backplate and pivots on a ⌀4.2 pin passing through **both tube side walls** at X −552, so the
pivot is anchored in steel rather than plastic. A tail forward of the pivot works a microswitch
carried on a small printed mount bolted to the backplate's inner face.

The F2 is electronic, so the trigger only has to close a switch — nothing mechanical reaches the
engine, and only the wires run forward. Lever ratio is 51 mm at the thumb against 18 mm at the
tail: **6° of travel gives 5.3 mm at the thumb and 1.9 mm at the tail**, where a typical
microswitch needs about 0.5 mm. Return and resistance come from a torsion spring on the pivot pin;
there's a ⌀3 peg hole in the tail if you'd rather hang a tension spring off it.

Verified clear of the tube, backplate and switch mount through 10°.

Swept in 25 mm steps against the tube, the side panels, the pintle tab, the backplate and the
cradle: 0.0000 cm³ throughout.

The return is **elastic shock cord, not a steel spring** — 150 mm of travel would need a
~350 mm compression spring and there is only 230 mm of clear tube behind the carrier. Anchor the
cord at the barrel plate and route it down the **left side at Y −20, Z −30**: that misses the
cradle (which reaches Y −18), the F2 (Y ±12.7), the hinge tab (Z −20 and up) and the pintle tabs
(Z −35 and down). It is the one path through that is clear end to end.

**The barrel is 1" EMT conduit.** OD 1.163", and the DOM socket's 1.188" ID takes it with 0.64mm
of clearance and the full 100mm of socket engagement. Cut it **39-1/4"** (996mm) measured from
where it bottoms in the socket. Note that 1" *pipe* of any schedule is too small — NPS is
nominal, and 1" sch40 has a 1.049" ID.

**The perforated barrel jacket is printed** and slides over the EMT — it's the M2's signature
feature and the one part of the barrel worth printing. 262mm long, ⌀101.6 at the rear flange,
bored ⌀38.90 over the steel socket and ⌀30.20 for the EMT, with a centring ring at the muzzle end
so it can't flop about on the conduit. Stood on end it fits a 300mm bed with 38mm to spare.
Forward of the jacket the EMT is bare.

It runs back to **X 24.80** so it meets `FrontBoss` flush — its rear is pocketed to clear the 1/4"
barrel plate, which would otherwise show through. **Bond that joint with epoxy; it needs no
fasteners.** The butt gives **1,615 mm² of face-to-face contact**, several times what an epoxy lap
joint requires, and the jacket is already located by the ⌀38.90 bore over the steel socket across
87mm of engagement — so it cannot shift radially and only the axial pull needs carrying. Bolts
were considered and rejected: the joint face is buried under 260mm of jacket from the front and
38mm of FrontBoss from the rear, so no fastener is reachable once assembled.

EMT is galvanised. Scuff and etch-prime it before painting or nothing will stick, and **do not
weld or braze it** — heating zinc gives off fumes that will make you ill. It doesn't need welding
here; it's a slip fit into the socket.

The socket runs X 13.65…113.65 and the jacket X 26.75…287, so the steel is completely hidden
inside the printed jacket. Nothing of it shows.

**Engine** — PolarStar F2, HPA. No battery bay needed; the air line exits through the tube floor.

See [docs/BUILD-NOTES.md](docs/BUILD-NOTES.md) for the full cut list, every coordinate, the weld
plan, and the fabrication order.

---

## Stock list

All imperial, 12" minimum lengths, cut to length only — no rip cuts.

| # | Stock | Grade | Buy | For |
|---|---|---|---|---|
| 1 | 2" × 3" × 0.120" wall rect tube | A500 Gr B | — | Core tube — **supplied by the laser vendor, don't buy separately** |
| 2 | 1-1/2" OD × 1.188" ID | **DOM** | 12" | Barrel socket |
| 3 | 1/2" × 2" flat bar | A36 HR | 12" | Pintle tabs ×2 |
| 4 | 1/4" × 3" flat bar | A36 HR | 12" | Barrel plate |
| 5 | 1/8" × 1" flat bar | A36 HR | 24" | Hatch spine + hinge tabs |
| 6 | 1/8" × 3" flat bar | A36 HR | 12" | Backplate |
| 7 | 1/4" round bar | 1018 CRS | 12" | Hinge pin |
| 8 | 1/2" round bar | 1018 CRS | 12" | Pintle pin |
| 9 | 9/16" round bar | 1018 CRS | 12" | Front mount pin |
| 10 | 1" EMT conduit | — | 10 ft | **Barrel** — cut 39-1/4", the rest is spare |

**A36 hot-rolled** is the cheap general-purpose structural grade — fine for tabs and plates that
get welded. **1018 cold-rolled** is used for the three pins only: hot-rolled round bar carries mill
scale and a loose diameter tolerance, so it will not slip-fit a bore.

Pin bores are cut **0.30 mm over** nominal bar (⌀6.65 / ⌀13.0 / ⌀14.6) so imperial stock drops in.
Don't "correct" them to round metric numbers — 1/4", 1/2" and 9/16" bar is 6.35, 12.70 and
14.29 mm, and a 12 mm bore will not accept a 1/2" pin.

**Item 2 is the one place not to substitute.** ERW tubing is cheaper but has an internal weld
bead, and the socket has only 0.64 mm of clearance on the EMT. DOM has a clean ID.

---

## Status

Working design, not yet fabricated. Known open items:

- **No skin-to-tube fastening scheme anywhere** — no bolt bosses or captive nuts on any panel.
  The jacket-to-FrontBoss joint is solved (bonded, see below), but the receiver panels are not.
- Hinge, pintle and front-mount pin positions are inferred from the printed model rather than
  measured from real hardware — **verify before drilling steel**
- Shock cord for the charging handle return is specified by routing, not by rate — pick a cord
  and check the return force by hand before committing to the anchor point
- The barrel jacket's fit on the EMT is set by the centring ring alone; if it rattles, shim it or
  add a second ring partway along
- The steel backplate cannot merge with any printed part — different material and process. The
  grip and buffer tube are already merged into `Grip_Assembly`.

---

## ATTRIBUTION

The cosmetic skin geometry is **derived from**:

> **M2 Browning 0.50 cal Machine Gun (1:1 Scale)** by **HappyBattleSheep**
> https://www.thingiverse.com/thing:7248430
> Licensed **CC BY** (Creative Commons — Attribution)

Specifically, the skins are cut from that model's `corpus` part. The steel core, the engine
cradle, the weldments, the tooling and the documentation are original work.

The source is CC BY, which permits derivatives and redistribution provided the original author is
credited. That credit is the line above — **keep it if you fork this.** CC BY is not share-alike,
so this derivative may carry the more restrictive CC BY-NC-SA in [LICENSE](LICENSE); that applies
to the original contributions here and cannot revoke anyone's rights to HappyBattleSheep's work,
which remains available under CC BY from the link above.

The upstream model pack is not vendored into this repo — download it from Thingiverse.

The PolarStar F2 engine and FCU CAD models are the property of PolarStar Airsoft and are
referenced for fitment only. They are not included in this repository.

---

## Note

This is an **airsoft replica** — a non-firing recreational replica that launches 6mm plastic BBs
at sub-lethal energies. It has no capability to chamber or fire live ammunition, and nothing here
describes or enables that.

Local law on replica firearms varies. Orange muzzle markings are required in some jurisdictions
and transport rules differ by region — check yours.
