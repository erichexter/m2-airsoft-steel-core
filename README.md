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
- Backplate bosses ×2, 1/2" bar, welded down the inside of the rear walls, tapped 4 × M5

**The backplate is bolted, not welded** — 4 × M5 into those bosses. Welding it shut would seal the
trigger away permanently: the mechanism sits at X −580…−526, well behind the tube's top opening
(X −310…−2), so there would be no access to it at all.

Disassembly, verified by sweeping each part clear:

1. Drift the ⌀4 pivot pin out through the **⌀6 hole in `Side_R1`** at X −552, Z +1
2. Draw the trigger straight back — the lever slides out through the backplate slot
3. Undo 4 × M5 and the backplate lifts off, **bringing the switch carrier with it**

The pin cannot retain the backplate, in case it looks like it should: the pin is at X −552 and
the backplate at X −563.18…−560, so they never intersect.

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

### The barrel comes off without disturbing the jacket

**2 × M5 set screws tapped into the socket** at X 55 and X 75, entering from underneath and
bearing on the EMT. The socket wall is 3.96mm, so an M5 gets full thread depth. They close a
0.32mm radial gap (socket ID r15.09 against EMT OD r14.77) — dimple the EMT at both positions so
the screws locate positively rather than relying on friction.

The screws sit under the jacket, so the jacket carries **2 × ⌀7 access channels** straight up from
its underside. A 2.5mm hex key reaches both screws with the barrel fully assembled — verified
clear through jacket, socket and EMT. Slacken both and the barrel slides straight out forward;
swept 150mm with no catch.

X 55 and 75 were chosen because X 95 lands on one of the jacket's cooling holes.

EMT is galvanised. Scuff and etch-prime it before painting or nothing will stick, and **do not
weld or braze it** — heating zinc gives off fumes that will make you ill. It doesn't need welding
here; it's a slip fit into the socket.

The socket runs X 13.65…113.65 and the jacket X 26.75…287, so the steel is completely hidden
inside the printed jacket. Nothing of it shows.

**Engine** — PolarStar F2, HPA. No battery bay needed; the air line exits through the tube floor.

**Panels screw on — 36 × M3.** Thread-forming button-head screws through the panel into ⌀2.65
pilot holes drilled in the tube wall. No tapping and no rivnut tool; the wall is 0.120" so a
thread-former cuts a full-depth thread on the way in. Heads sit proud, reading as the M2's rivet
line rather than being hidden.

| Panel | Screws | Where |
|---|---|---|
| `Side_L1`, `Side_R1` | 6 each | X −525.1 / −460.1 / −285.7, at Z −24 and +8 |
| `Side_L2`, `Side_R2` | 6 each | X −242.4 / −122.9 / −63.1, at Z −24 and +8 |
| `Top1` | 6 | X −526.7 / −413.5 / −356.9, at Y ±18 |
| `Bot1` | 6 | X −516.3 / −442.4 / −294.6, at Y ±18 |

Every panel carries a **⌀8 boss on its inner face at each screw**, bridging the 0.4 mm clearance
gap to the tube so the screw clamps against solid material instead of flexing a 3 mm shell.

**`Bot2` is bonded, not screwed.** It is two thin rails sitting over the tube's bottom corner
radii — there is no flat there to pull against. `FrontBoss` is bonded too, to the barrel jacket.
The pilot holes are on the wrap template in `templates/`.

See [docs/BUILD-NOTES.md](docs/BUILD-NOTES.md) for the full cut list, every coordinate, the weld
plan, and the fabrication order.

---

## Stock list

All imperial, 12" minimum lengths, cut to length only — no rip cuts.

| # | Stock | Grade | Buy | For |
|---|---|---|---|---|
| 1 | 2" × 3" × 0.120" wall rect tube | A500 Gr B | — | Core tube — **supplied by the laser vendor, don't buy separately** |
| 2 | 1-1/2" OD × 1.188" ID | **DOM** | 12" | Barrel socket |
| 3 | 1/2" × 2" flat bar | A36 HR | 12" | Pintle tabs ×2 + backplate bosses ×2 |
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

Working design, not yet fabricated. The geometry is resolved — every part has been checked against
every other part with no interference, and every mechanism has been swept through its full range.

Open items, all of which need hardware in hand rather than more CAD:

- Shock cord for the charging handle return is specified by routing, not by rate — pick a cord
  and check the return force by hand before committing to the anchor point
- The barrel jacket's fit on the EMT is set by the centring ring alone; if it rattles, shim it or
  add a second ring partway along
- Print tolerance on the ⌀38.90 jacket bore over the ⌀38.10 socket: FDM holes come out undersized,
  so print a short test ring before committing 260 mm of filament

Decided, not open:

- **Pin positions stand as designed.** Hinge, pintle and front-mount pins are inferred from the
  donor model rather than measured off real hardware, and that is accepted — the mounts are
  tolerant enough that a few millimetres either way does not matter.
- `Bot2` is 2 shells by design — two thin rails in the bottom corners, printed as one file
- `Hatch` is 329.9 mm and only fits the bed laid diagonally (294 mm footprint, 5.7 mm margin)
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
