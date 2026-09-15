#!/usr/bin/env node
// How flat is the face this part gets printed on?
//
//   node tools/bedcheck.js <file.stl> [axis] [min|max]
//
// The printed skins bed on the face that mates with the steel tube, visible side up
// so it can be ironed. Anything protruding from that face is what the slicer has to
// support, and anything sitting just above it is a gap the part rocks on.
//
// Reports the plane-parallel facet area at each distinct height above the bed plane.
// A part that prints cleanly has ~all of its bed-facing area in the 0.00 bucket.
//
// Axis and side are guessed from the bounding box - a skin wraps the tube, so its
// mating face is the one nearest the tube axis - but can be given explicitly.

const fs = require('fs');

const file = process.argv[2];
if (!file) { console.error('usage: node bedcheck.js <file.stl> [x|y|z] [min|max]'); process.exit(1); }

const buf = fs.readFileSync(file);
if (buf.subarray(0, 23).toString('latin1') === 'version https://git-lfs') {
  console.error(`${file}: Git LFS pointer, not an STL — run "git lfs pull"`); process.exit(1);
}
const n = buf.readUInt32LE(80);
const tri = [];
for (let i = 0, o = 84; i < n; i++, o += 50) {
  const nor = [buf.readFloatLE(o), buf.readFloatLE(o + 4), buf.readFloatLE(o + 8)];
  const v = [];
  for (let k = 0; k < 3; k++) {
    const b = o + 12 + k * 12;
    v.push([buf.readFloatLE(b), buf.readFloatLE(b + 4), buf.readFloatLE(b + 8)]);
  }
  tri.push({ nor, v });
}

const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
for (const t of tri) for (const p of t.v) for (let a = 0; a < 3; a++) {
  if (p[a] < lo[a]) lo[a] = p[a];
  if (p[a] > hi[a]) hi[a] = p[a];
}

// Guess: the skin's mating face is the bbox face nearest the tube centreline. The tube
// runs along X, so only Y and Z are candidates; pick whichever the part is thinnest in,
// then the end of that axis closest to zero.
let axis = process.argv[3];
let side = process.argv[4];
if (!axis) {
  const spanY = hi[1] - lo[1], spanZ = hi[2] - lo[2];
  axis = spanY < spanZ ? 'y' : 'z';
}
const ax = { x: 0, y: 1, z: 2 }[axis];
if (!side) side = Math.abs(lo[ax]) < Math.abs(hi[ax]) ? 'min' : 'max';

const plane = side === 'min' ? lo[ax] : hi[ax];
const sign = side === 'min' ? -1 : 1;   // outward normal direction of the bed face

// Facets lying in a plane perpendicular to the axis and facing the bed.
const NORMAL_TOL = 0.999;
const area3 = (a, b, c) => {
  const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
  const w = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const x = u[1] * w[2] - u[2] * w[1], y = u[2] * w[0] - u[0] * w[2], z = u[0] * w[1] - u[1] * w[0];
  return Math.sqrt(x * x + y * y + z * z) / 2;
};

const buckets = new Map();   // height above bed plane (0.01mm) -> area
let bedFacing = 0;
for (const t of tri) {
  if (t.nor[ax] * sign < NORMAL_TOL) continue;        // not facing the bed
  const h = Math.abs(t.v[0][ax] - plane);
  if (Math.abs(t.v[1][ax] - t.v[0][ax]) > 1e-4) continue;  // not planar in this axis
  if (Math.abs(t.v[2][ax] - t.v[0][ax]) > 1e-4) continue;
  const a = area3(t.v[0], t.v[1], t.v[2]);
  bedFacing += a;
  const key = Math.round(h * 100) / 100;
  buckets.set(key, (buckets.get(key) || 0) + a);
}

const rows = [...buckets.entries()].sort((a, b) => a[0] - b[0]);
const name = file.replace(/\\/g, '/').split('/').pop();
const footprint = ax === 1 ? (hi[0] - lo[0]) * (hi[2] - lo[2]) : (hi[0] - lo[0]) * (hi[1] - lo[1]);

console.log(`\n=== ${name} ===`);
console.log(`  bbox        X ${lo[0].toFixed(1)}…${hi[0].toFixed(1)}  ` +
            `Y ${lo[1].toFixed(1)}…${hi[1].toFixed(1)}  Z ${lo[2].toFixed(1)}…${hi[2].toFixed(1)}`);
console.log(`  bed face    ${axis.toUpperCase()} ${side} = ${plane.toFixed(3)}`);
console.log(`  height above bed      area        of bed-facing`);
for (const [h, a] of rows) {
  if (a < 0.5) continue;
  const pct = (a / bedFacing * 100);
  const bar = '#'.repeat(Math.max(0, Math.round(pct / 3)));
  console.log(`    ${h.toFixed(2).padStart(6)} mm   ${(a / 100).toFixed(2).padStart(8)} cm2   ` +
              `${pct.toFixed(1).padStart(5)}%  ${bar}`);
}
const atBed = buckets.get(0) || 0;
const proud = bedFacing - atBed;
console.log(`  ---`);
console.log(`  ON the bed plane      ${(atBed / 100).toFixed(2)} cm2  (${(atBed / bedFacing * 100).toFixed(1)}% of bed-facing)`);
console.log(`  standing off it       ${(proud / 100).toFixed(2)} cm2  in ${rows.length - (atBed ? 1 : 0)} level(s)`);
console.log(`  bbox footprint        ${(footprint / 100).toFixed(2)} cm2`);
// A shallow step is the thing that ruins the print: the part lands on whatever is
// lowest and the rest is held in the air, so the slicer supports all of it. A deep one
// is just a pocket in the part — it starts higher up and costs nothing. Only the first
// kind is a defect, and reporting both as "not flat" buries the signal.
const STANDOFF_MAX = 1.0;   // mm
const standoff = rows.filter(([h, a]) => h > 0 && h <= STANDOFF_MAX && a > 0.5);
const pockets  = rows.filter(([h]) => h > STANDOFF_MAX);
const pct = atBed / bedFacing * 100;

if (standoff.length) {
  const held = standoff.reduce((s, [, a]) => s + a, 0);
  console.log(`  VERDICT  NOT FLAT — ${(held / 100).toFixed(2)} cm2 held ` +
              `${standoff.map(([h]) => h.toFixed(2)).join('/')} mm off the bed, ` +
              `resting on ${(atBed / 100).toFixed(2)} cm2`);
} else {
  console.log(`  VERDICT  flat — ${pct.toFixed(1)}% of the bed face is on the bed` +
              (pockets.length ? `, plus ${pockets.length} pocket(s) deeper than ${STANDOFF_MAX} mm` : ''));
}
