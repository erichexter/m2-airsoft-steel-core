# M2 Airsoft — Steel Core Conversion

> **Part names.** Every part has one name, used identically in Fusion, in `stl/`, and in
> these notes — `ST-` you weld, `HW-` you buy, `PR-` you print. See **[docs/PARTS.md](docs/PARTS.md)**
> for the full catalogue and the old-name mapping. Note that **L and R are the physical
> sides of the gun**, and the donor mesh names had them backwards.


A welded steel structural core for a 3D-printed Browning M2 airsoft replica.

![The assembled replica](docs/img/01-assembly.png)

*Blue is steel you weld, brass is hardware you buy, grey is 3D printed.*

**▶ [Three-minute walkthrough video](https://github.com/erichexter/m2-airsoft-steel-core/releases/tag/v1.0)**
— cross-sections, what is steel, how it goes together.

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
docs/PARTS.md              Parts catalogue — every name, in one place. START HERE
docs/PRINTING.md           Orientation per part, settings, and why the long panels warp
docs/SLICER-AGENT-PROMPT.md  Self-contained brief to hand an agent on the slicer machine
docs/BUILD-NOTES.md        Full build notes: cut list, coordinates, weld plan, gotchas
docs/NATIVE-REBUILD.md     How the donor meshes were reauthored as native geometry

stl/PR-*.stl               The 18 printed parts, ready to slice
stl/print-aids/            PR-11/PR-12 with snap-off corner pads — print THESE two
stl/ST-*.stl               Steel parts — for checking the cut list, not for printing
stl/donor/                 Original donor meshes, kept for reference and attribution

cad/10_Steel_Core.stp      One STEP per component group
cad/20_Print_Receiver.stp    …
cad/M2_core_tube_RFQ.stp   Core tube alone — upload this for a laser-cut quote
cad/M2_steel_core.stp      Full steel assembly + engine cradle
cad/RFQ-core-tube.md       Stock spec, feature table, vendor notes

source/                    Fusion 360 archive (.f3d)
tools/stlcheck.js          Printability checker — run it on the STLs
tools/reauthor/            Mesh-to-native toolchain and the per-part build scripts
LICENSE                    CC BY-NC-SA 4.0
```

The STEP and STL files contain **only original work** — the steel design, the printed skins
derived as described under ATTRIBUTION, and the cradle.

### Getting the STLs

**Easiest: grab the print pack from the
[latest release](https://github.com/erichexter/m2-airsoft-steel-core/releases/latest).**
The print pack ZIP there has the 18 printed parts and both tube templates in one
download — no clone, no git-lfs, nothing to configure. Always take the **latest**
release; earlier packs are left up for reference but are superseded.

That matters because **the STLs, STEPs and renders are stored in Git LFS, and two of
the obvious ways to download them silently give you 131-byte text pointers instead of
models.** Release assets are served directly and sidestep it entirely. Verified
against this repo:

| how | what you get |
|---|---|
| **Code → Download ZIP** | ❌ pointers — all 40 STLs come to **5 KB total** |
| `raw.githubusercontent.com/…` | ❌ pointer |
| **Download button on the file's page** | ✅ the real STL |
| `github.com/erichexter/m2-airsoft-steel-core/raw/main/stl/<name>.stl` | ✅ the real STL |
| `git clone` **with git-lfs installed** | ✅ everything |

A pointer file is 131 bytes of text beginning `version https://git-lfs…`. If a
download is that size, that is what happened.

To get the whole set at once, install [git-lfs](https://git-lfs.com) *first*, then:

```
git lfs install
git clone https://github.com/erichexter/m2-airsoft-steel-core.git
```

Cloning **without** git-lfs installed also gives you pointers. If that has already
happened, `git lfs install && git lfs pull` fixes it in place. Either way, check
before slicing:

```
node tools/stlcheck.js stl/PR-*.stl
```

which fails loudly on a pointer file rather than letting a slicer choke on it.

### Checking the prints

```
node tools/stlcheck.js stl/PR-*.stl
```

Reports triangle count, watertightness (open and non-manifold edges), degenerate facets,
connected shells, bounding box against the bed, normal orientation, and overhang burden for each
axis-aligned orientation. All 18 printed parts are closed — **zero open edges** — with correct
normals and a single shell.

Two reported conditions, both understood and both fine:

- **`PR-16-Top-Cover.stl` "does not fit the bed".** The checker only tests axis-aligned
  orientations. The cover is 329.9 mm long and does fit laid diagonally — measured by rotating
  its actual first-layer point set, the best angle is **45°, giving 272.7 × 272.4 mm — 13.6 mm
  of margin per side**, which is room for a 10 mm brim. An earlier note here said 294 mm and
  5.7 mm; that was an estimate, not a measurement, and it was wrong.
- **`PR-31-Spade-Grips.stl` reports 3 non-manifold edges.** They are three 2 mm verticals at
  X ≈ −583, Y ≈ ±10, where the trigger's clearance slot cuts through the spine and the cut
  surface meets itself. The part has **no holes** and is one closed shell; slicers handle
  touching edges without complaint.

---

## What it looks like

| | |
|---|---|
| ![Steel core](docs/img/02-steel-core.png) | **The steel.** One 2×3 tube plus eleven welded pieces. Everything else hangs off this. |
| ![Receiver skins](docs/img/04-receiver-skins.png) | **The printed receiver skins.** Nine parts that clothe the tube and carry no load. |
| ![Trigger group](docs/img/05-trigger-group.png) | **Trigger.** Butterfly on a ⌀4 pin through both tube walls; the switch sits *above* the tail, so pressing down closes it. |
| ![Charging handle](docs/img/06-charging-handle.png) | **Charging handle.** The carrier sandwiches the tube wall through the existing slot; four ⌀8 nut pockets in the arm. |
| ![Barrel mount](docs/img/07-barrel-mount.png) | **Barrel.** 1" EMT in a welded socket, two set screws, reachable through the jacket perforations. |
| ![Grips and backplate](docs/img/08-grip-backplate.png) | **Grips.** Bolted, not welded — the backplate comes off to service the trigger. |
| ![Engine cradle](docs/img/09-engine-cradle.png) | **Engine.** PolarStar F2 with the direct-attach combo, in a printed cradle. |

Every image above is rendered straight from the model by `tools/reauthor/render_docs.py`,
so they cannot drift from the geometry.

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

1. Drift the ⌀4 pivot pin out through the **⌀6 hole in `PR-11-Side-Rear-L`** at X −552, Z +1
2. Draw the trigger straight back — the lever slides out through the backplate slot
3. Undo 4 × M5 and the backplate lifts off, **bringing the switch carrier with it**

The pin cannot retain the backplate, in case it looks like it should: the pin is at X −552 and
the backplate at X −563.18…−560, so they never intersect.

**Charging handle** — slides, spring returns, **150 mm of travel**, and it runs in the
**existing 192 × 8 mm slot**. No extra metal is removed for it and **no guide rod is used** —
three printed parts sandwich the receiver wall and the slot itself is the track:

| Part | Where |
|---|---|
| `PR-43-CH-Shoe` | inside the tube, Y −22…−14, 16 mm tall behind an 8 mm slot so it can't pull out |
| `PR-42-CH-Carrier` | 7 mm neck through the slot, pad outside the panel at Y −38…−30 |
| `PR-41-CH-Handle` | full-length foot bolting to the pad, 1,696 mm² of flat contact |

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

It runs back to **X 24.80** so it meets `PR-17-Front-Sight-Boss` flush — its rear is pocketed to clear the 1/4"
barrel plate, which would otherwise show through. **Bond that joint with epoxy; it needs no
fasteners.** The butt gives **1,615 mm² of face-to-face contact**, several times what an epoxy lap
joint requires, and the jacket is already located by the ⌀38.90 bore over the steel socket across
87mm of engagement — so it cannot shift radially and only the axial pull needs carrying. Bolts
were considered and rejected: the joint face is buried under 260mm of jacket from the front and
38mm of PR-17-Front-Sight-Boss from the rear, so no fastener is reachable once assembled.

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
| `PR-12-Side-Rear-R`, `PR-11-Side-Rear-L` | 6 each | X −525.1 / −460.1 / −285.7, at Z −24 and +8 |
| `PR-14-Side-Front-R`, `PR-13-Side-Front-L` | 6 each | X −242.4 / −122.9 / −63.1, at Z −24 and +8 |
| `PR-15-Top-Deck` | 6 | X −526.7 / −413.5 / −356.9, at Y ±18 |
| `PR-18-Bottom-Rear` | 6 | X −516.3 / −442.4 / −294.6, at Y ±18 |

Every panel carries a **⌀8 boss on its inner face at each screw**, bridging the 0.4 mm clearance
gap to the tube so the screw clamps against solid material instead of flexing a 3 mm shell.

**`PR-19-Bottom-Front-L` / `-R` are bonded, not screwed.** They are two thin rails sitting over the tube's bottom corner
radii — there is no flat there to pull against. `PR-17-Front-Sight-Boss` is bonded too, to the barrel jacket.
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

Working design, not yet fabricated. Every part has been checked against every other part with no
interference, and every mechanism swept through its full range.

**The donor-derived parts are faceted STL conversions.** Everything designed here is native
geometry, so the tube STEP a fabricator receives is clean (135 faces, 73 real cylinders). The
barrel jacket has been reauthored natively — **17,422 faces down to 60** — and the rest are
tracked in [docs/NATIVE-REBUILD.md](docs/NATIVE-REBUILD.md). Fusion cannot convert them
automatically; see the build notes.

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
- `PR-19-Bottom-Front` used to be one body containing two disconnected rails; it is now
  two parts, `-L` and `-R`, which is what a slicer made of it anyway
- `PR-16-Top-Cover` is 329.9 mm and only fits the bed laid diagonally (294 mm footprint, 5.7 mm margin)
- The steel backplate cannot merge with any printed part — different material and process. The
  grip and buffer tube are already merged into `PR-31-Spade-Grips`.

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
