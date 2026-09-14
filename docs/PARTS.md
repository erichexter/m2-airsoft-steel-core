# Parts catalogue

Every part in the model has one name, and that name is the same in Fusion, in
`stl/`, and in the build notes.

```
<class>-<NN>-<Descriptive-Name>[-L|-R]
```

| class | meaning |
|---|---|
| `ST` | **steel** — you cut it and weld it |
| `HW` | **hardware** — you buy it (conduit, pins, switch, fasteners) |
| `PR` | **printed** — you print it |
| `RF` | **reference** — never built; donor meshes and bought-in models |

The number groups by subassembly: `0x` structure, `1x` receiver skins, `2x` barrel,
`3x` grips, `4x` charging handle, `5x` trigger, `6x` engine.

## Which side is L and which is R

**Standing behind the gun, firing forward.** The muzzle is +X, up is +Z.

The charging handle on a real M2 is on the **right**, and in this model it sits at
**negative Y** — so negative Y is the right-hand side. Everything below follows the
physical side.

> **The donor mesh names have this backwards.** Its `Side_L1` / `Side_L2` /
> `CH_Handle` are all at negative Y, which is physically the **right** of the gun.
> If you are cross-referencing the original Thingiverse files, swap L and R.

---

## Fusion browser

| component | holds |
|---|---|
| `00_Ref_PolarStar_F2` | the engine, bought-in model — shown, because it has to fit |
| `00_Ref_FCU` | FCU model |
| `00_Ref_Donor_Skins` | the original faceted skins, superseded |
| `00_Ref_Donor_Jacket` / `_Grip` / `_Meshes` | the rest of the donor geometry |
| `00_Ref_Import_Scrap` | dead duplicates left by the original import — safe to delete |
| `10_Steel_Core` | the tube |
| `11_Steel_Weldments` | everything welded to it, plus the EMT barrel |
| `20_Print_Receiver` | the receiver skins |
| `30_Print_Barrel` | jacket |
| `40_Print_Grip` | spade grips |
| `50_Print_Charging` | charging handle group |
| `60_Print_Trigger` | trigger group |
| `70_Print_Engine` | engine cradle |

Everything under `00_Ref` is hidden by default except the PolarStar, which stays
visible because the engine has to fit.

### Getting the browser into this order

**Fusion lists components in creation order, not alphabetically**, and there is no
API to reorder them — `Occurrence` has no index setter, and neither does anything
else. Numbering the names does nothing on its own; the `00_Ref` components were the
original ones and stayed scattered through the list at indices 0, 1, 4, 6, 8, 10 and 14
while the newer ones piled up at the bottom.

The only lever is creation order itself. `tools/reauthor/reorder.py` uses it:

1. rename every component out of the way (`~old~…`) to free the real names
2. create fresh components **in the order you want** — new ones append
3. `moveToComponent` the bodies across
4. delete the empties

It refuses to run if any component it would empty is not at an identity transform,
because moving a body out of a transformed component moves the geometry with it.
`00_Ref_FCU` *is* transformed and holds child occurrences rather than bodies, so it
is skipped and simply stays at the top.

Re-run it any time the order drifts. 58 bodies moved, 22 spot-checked for volume,
shell count and solidity afterwards — nothing shifted.

---

## Steel — cut and weld

Blue in the renders. Eleven pieces plus the tube.

| | part | cm³ | was called |
|:-:|---|---:|---|
| <img src="img/part-ST-01-Core-Tube.png" width="150"> | `ST-01-Core-Tube` | 344.50 | `CoreBox_cut` |
| <img src="img/part-ST-02-Backplate.png" width="150"> | `ST-02-Backplate` | 9.64 | `Backplate_1-8` |
| <img src="img/part-ST-03-Backplate-Boss-L.png" width="150"> | `ST-03-Backplate-Boss-L` | 3.24 | `BP_Boss_R_1-2` |
| <img src="img/part-ST-03-Backplate-Boss-R.png" width="150"> | `ST-03-Backplate-Boss-R` | 3.24 | `BP_Boss_L_1-2` |
| <img src="img/part-ST-04-Barrel-Plate.png" width="150"> | `ST-04-Barrel-Plate` | 16.04 | `Barrel_Plate_1-4` |
| <img src="img/part-ST-05-Barrel-Socket.png" width="150"> | `ST-05-Barrel-Socket` | 42.39 | `Barrel_Socket_1-5x156` |
| <img src="img/part-ST-06-Cover-Spine.png" width="150"> | `ST-06-Cover-Spine` | 26.19 | `Hatch_Spine_1-8` |
| <img src="img/part-ST-07-Hinge-Tab-L.png" width="150"> | `ST-07-Hinge-Tab-L` | 5.55 | `Hinge_Tab_R_1-8` |
| <img src="img/part-ST-07-Hinge-Tab-R.png" width="150"> | `ST-07-Hinge-Tab-R` | 5.55 | `Hinge_Tab_L_1-8` |
| <img src="img/part-ST-08-Pintle-Tab-L.png" width="150"> | `ST-08-Pintle-Tab-L` | 26.25 | `Pintle_Tab_R_1-2` |
| <img src="img/part-ST-08-Pintle-Tab-R.png" width="150"> | `ST-08-Pintle-Tab-R` | 26.25 | `Pintle_Tab_L_1-2` |

## Hardware — buy

Brass in the renders.

| | part | what | was called |
|:-:|---|---|---|
| <img src="img/part-HW-01-Barrel-EMT-1in.png" width="150"> | `HW-01-Barrel-EMT-1in` | 1" EMT conduit, the barrel | `Barrel_EMT_1in` |
| <img src="img/part-HW-02-Switch-SS5GL13.png" width="150"> | `HW-02-Switch-SS5GL13` | trigger microswitch | `REF_Switch_SS5GL13` |
| <img src="img/part-HW-03-Trigger-Pin-4mm.png" width="150"> | `HW-03-Trigger-Pin-4mm` | ⌀4 trigger pivot pin | `REF_PivotPin_4mm` |

## Printed

Light grey in the renders.

| | part | faces | cm³ | was called |
|:-:|---|---:|---:|---|
| <img src="img/part-PR-11-Side-Rear-L.png" width="150"> | `PR-11-Side-Rear-L` | 162 | 201.43 | `Side_R1` |
| <img src="img/part-PR-12-Side-Rear-R.png" width="150"> | `PR-12-Side-Rear-R` | 262 | 328.35 | `Side_L1` |
| <img src="img/part-PR-13-Side-Front-L.png" width="150"> | `PR-13-Side-Front-L` | 75 | 122.16 | `Side_R2` |
| <img src="img/part-PR-14-Side-Front-R.png" width="150"> | `PR-14-Side-Front-R` | 84 | 133.95 | `Side_L2` |
| <img src="img/part-PR-15-Top-Deck.png" width="150"> | `PR-15-Top-Deck` | 61 | 468.72 | `Top1` |
| <img src="img/part-PR-16-Top-Cover.png" width="150"> | `PR-16-Top-Cover` | 138 | 510.84 | `Hatch` |
| <img src="img/part-PR-17-Front-Sight-Boss.png" width="150"> | `PR-17-Front-Sight-Boss` | 250 | 106.67 | `FrontBoss` |
| <img src="img/part-PR-18-Bottom-Rear.png" width="150"> | `PR-18-Bottom-Rear` | 181 | 279.13 | `Bot1` |
| <img src="img/part-PR-19-Bottom-Front-L.png" width="150"> | `PR-19-Bottom-Front-L` | 30 | 3.65 | half of `Bot2` |
| <img src="img/part-PR-19-Bottom-Front-R.png" width="150"> | `PR-19-Bottom-Front-R` | 30 | 3.65 | half of `Bot2` |
| <img src="img/part-PR-21-Barrel-Jacket.png" width="150"> | `PR-21-Barrel-Jacket` | 60 | 638.00 | `Barrel_Jacket` |
| <img src="img/part-PR-31-Spade-Grips.png" width="150"> | `PR-31-Spade-Grips` | 1,549 | 330.82 | `Grip_Assembly` |
| <img src="img/part-PR-41-CH-Handle.png" width="150"> | `PR-41-CH-Handle` | 73 | 116.82 | `CH_Handle` |
| <img src="img/part-PR-42-CH-Carrier.png" width="150"> | `PR-42-CH-Carrier` | 33 | 13.27 | `CH_Carrier` |
| <img src="img/part-PR-43-CH-Shoe.png" width="150"> | `PR-43-CH-Shoe` | 8 | 3.96 | `CH_Shoe` |
| <img src="img/part-PR-51-Trigger-Butterfly.png" width="150"> | `PR-51-Trigger-Butterfly` | 611 | 32.78 | `Trigger` |
| <img src="img/part-PR-52-Trigger-Switch-Carrier.png" width="150"> | `PR-52-Trigger-Switch-Carrier` | 52 | 23.10 | `Trigger_Switch_Carrier` |
| <img src="img/part-PR-61-Engine-Cradle.png" width="150"> | `PR-61-Engine-Cradle` | 30 | 181.08 | `Cradle_F2_HopUp` |

**18 printed parts, 2,724 cm³** — about 3.4 kg in PLA at 100% infill, less in practice.

`Bot2` was one body containing two disconnected rails; it is now two parts, which is
what a slicer would have made of it anyway.

---

## Files

```
stl/        one STL per part, named exactly as above — print straight from here
stl/donor/  the original donor meshes, kept for reference and attribution
cad/        one STEP per component group
```

Steel parts have STLs too. They are not for printing — they are for checking the
cut list and for anyone quoting the fabrication.

---

## Keeping it consistent

The build scripts in `tools/reauthor/` write directly into these components under
these names, so re-running a part does not undo the organisation. Two traps that
cost time when the model was reorganised:

- **`feature.bodies.item(0)` is wrong in a direct-design document.** It returns the
  component's *first* body, not the one the feature just made. That looks correct
  only while each part sits alone in its own component. Take the last body in the
  component instead.
- **Fusion hands back a fresh wrapper object on every access**, so `occurrence is
  target` is always False. Comparing identity instead of names silently hid every
  body and exported 29 empty STLs. Compare names.
- **Anything that looks a body up by name breaks on a rename.** The grip's relief
  cuts against the steel and the trigger were still searching for `CoreBox_cut` and
  `Trigger_Group`; they found nothing and quietly did nothing. Count what you match
  and print it.
