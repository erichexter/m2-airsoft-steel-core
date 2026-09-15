#!/usr/bin/env node
// Printability check for binary STL files.
//
//   node stlcheck.js <file.stl> [...]
//   node stlcheck.js ../stl/*.stl
//
// Reports: triangle count, watertightness (open + non-manifold edges),
// degenerate facets, connected shells, bounding box vs bed, normal
// consistency, and overhang burden for each axis-aligned print orientation.

const fs = require('fs');
const path = require('path');

const BED = [300, 300, 300];      // Creality K1 Max
const OVERHANG_DEG = 45;          // steeper than this off vertical needs support
const QUANT = 1e4;                // vertex weld tolerance -> 0.0001mm

function readBinarySTL(file) {
  const buf = fs.readFileSync(file);
  // An LFS pointer is a 131-byte text file, and it is what you get from "Download ZIP",
  // from raw.githubusercontent.com, or from cloning without git-lfs installed. Left to
  // the generic path it reports "truncated: header claims 828596793 triangles", which
  // sends you looking for a broken export instead of a missing download.
  if (buf.subarray(0, 40).toString('latin1').startsWith('version https://git-lfs')) {
    throw new Error('this is a Git LFS pointer, not an STL — ' +
                    'run "git lfs install && git lfs pull", or download the file ' +
                    'from the GitHub file page rather than from Download ZIP');
  }
  if (buf.length < 84) throw new Error('too short to be a binary STL');
  const n = buf.readUInt32LE(80);
  if (buf.length < 84 + n * 50) throw new Error('truncated: header claims ' + n + ' triangles');
  const tri = new Float32Array(n * 9);
  const nor = new Float32Array(n * 3);
  let o = 84;
  for (let i = 0; i < n; i++) {
    nor[i * 3] = buf.readFloatLE(o);
    nor[i * 3 + 1] = buf.readFloatLE(o + 4);
    nor[i * 3 + 2] = buf.readFloatLE(o + 8);
    for (let k = 0; k < 9; k++) tri[i * 9 + k] = buf.readFloatLE(o + 12 + k * 4);
    o += 50;
  }
  return { n, tri, nor };
}

function key(x, y, z) {
  return Math.round(x * QUANT) + ',' + Math.round(y * QUANT) + ',' + Math.round(z * QUANT);
}

function analyse(file) {
  const { n, tri } = readBinarySTL(file);

  // weld vertices
  const vmap = new Map();
  const idx = new Int32Array(n * 3);
  const lo = [Infinity, Infinity, Infinity];
  const hi = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < n * 3; i++) {
    const x = tri[i * 3], y = tri[i * 3 + 1], z = tri[i * 3 + 2];
    if (x < lo[0]) lo[0] = x; if (x > hi[0]) hi[0] = x;
    if (y < lo[1]) lo[1] = y; if (y > hi[1]) hi[1] = y;
    if (z < lo[2]) lo[2] = z; if (z > hi[2]) hi[2] = z;
    const k = key(x, y, z);
    let id = vmap.get(k);
    if (id === undefined) { id = vmap.size; vmap.set(k, id); }
    idx[i] = id;
  }

  // edges, degenerate facets, area, volume
  const edges = new Map();
  let degenerate = 0, area = 0, vol = 0;
  const faceArea = new Float64Array(n);
  const faceNz = new Float64Array(n * 3);
  for (let t = 0; t < n; t++) {
    const a = idx[t * 3], b = idx[t * 3 + 1], c = idx[t * 3 + 2];
    if (a === b || b === c || a === c) { degenerate++; continue; }
    const p = t * 9;
    const ux = tri[p + 3] - tri[p], uy = tri[p + 4] - tri[p + 1], uz = tri[p + 5] - tri[p + 2];
    const vx = tri[p + 6] - tri[p], vy = tri[p + 7] - tri[p + 1], vz = tri[p + 8] - tri[p + 2];
    const cx = uy * vz - uz * vy, cy = uz * vx - ux * vz, cz = ux * vy - uy * vx;
    const mag = Math.hypot(cx, cy, cz);
    if (mag < 1e-12) { degenerate++; continue; }
    const ar = mag / 2;
    faceArea[t] = ar;
    area += ar;
    faceNz[t * 3] = cx / mag; faceNz[t * 3 + 1] = cy / mag; faceNz[t * 3 + 2] = cz / mag;
    vol += (tri[p] * (tri[p + 4] * tri[p + 8] - tri[p + 5] * tri[p + 7])
          - tri[p + 1] * (tri[p + 3] * tri[p + 8] - tri[p + 5] * tri[p + 6])
          + tri[p + 2] * (tri[p + 3] * tri[p + 7] - tri[p + 4] * tri[p + 6])) / 6;
    for (const [u, v] of [[a, b], [b, c], [c, a]]) {
      const ek = u < v ? u + '_' + v : v + '_' + u;
      edges.set(ek, (edges.get(ek) || 0) + 1);
    }
  }
  let open = 0, nonmanifold = 0;
  for (const cnt of edges.values()) {
    if (cnt === 1) open++;
    else if (cnt > 2) nonmanifold++;
  }

  // connected components over shared vertices
  const parent = new Int32Array(vmap.size);
  for (let i = 0; i < parent.length; i++) parent[i] = i;
  const find = (x) => { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; };
  const union = (a, b) => { a = find(a); b = find(b); if (a !== b) parent[b] = a; };
  for (let t = 0; t < n; t++) {
    union(idx[t * 3], idx[t * 3 + 1]);
    union(idx[t * 3 + 1], idx[t * 3 + 2]);
  }
  const roots = new Set();
  for (let i = 0; i < parent.length; i++) roots.add(find(i));

  // overhang burden per axis-aligned orientation
  const cutoff = Math.cos((90 - OVERHANG_DEG) * Math.PI / 180);
  const dirs = [
    ['+Z up', [0, 0, 1]], ['-Z up', [0, 0, -1]],
    ['+Y up', [0, 1, 0]], ['-Y up', [0, -1, 0]],
    ['+X up', [1, 0, 0]], ['-X up', [-1, 0, 0]],
  ];
  const over = dirs.map(([name, d]) => {
    let a = 0;
    for (let t = 0; t < n; t++) {
      if (!faceArea[t]) continue;
      const dot = faceNz[t * 3] * d[0] + faceNz[t * 3 + 1] * d[1] + faceNz[t * 3 + 2] * d[2];
      if (dot < -cutoff) a += faceArea[t];   // faces pointing down steeply
    }
    const size = [hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]];
    const upAxis = d.findIndex(v => v !== 0);
    const foot = size.filter((_, i) => i !== upAxis);
    const fits = size[upAxis] <= BED[2] && foot[0] <= BED[0] && foot[1] <= BED[1];
    return { name, area: a, pct: 100 * a / area, height: size[upAxis], fits };
  });
  over.sort((p, q) => p.area - q.area);

  return {
    file: path.basename(file), n, degenerate, open, nonmanifold,
    shells: roots.size ? countShells(idx, n, find) : 0,
    verts: vmap.size, area, vol, lo, hi, over,
  };
}

function countShells(idx, n, find) {
  const s = new Set();
  for (let t = 0; t < n; t++) s.add(find(idx[t * 3]));
  return s.size;
}

const files = process.argv.slice(2);
if (!files.length) { console.error('usage: node stlcheck.js <file.stl> [...]'); process.exit(1); }

let problems = 0;
// Kept separate from `problems`: a file that cannot be read at all is a different
// thing from a part that merely needs turning on the bed. Two of the 18 printed parts
// raise advisory conditions that are understood and documented in the README, so
// exiting non-zero on those would cry wolf every single run.
let unreadable = 0;
for (const f of files) {
  let r;
  try { r = analyse(f); } catch (e) { console.log(`\n${path.basename(f)}\n  FAILED: ${e.message}`); problems++; unreadable++; continue; }
  const size = [r.hi[0] - r.lo[0], r.hi[1] - r.lo[1], r.hi[2] - r.lo[2]];
  const watertight = r.open === 0 && r.nonmanifold === 0;
  const best = r.over[0];
  const asModelled = r.over.find(o => o.name === '+Z up');

  console.log('');
  console.log('=== ' + r.file + ' ===');
  console.log('  triangles      ' + r.n.toLocaleString() + '   vertices ' + r.verts.toLocaleString());
  console.log('  size           ' + size.map(v => v.toFixed(1)).join(' x ') + ' mm');
  console.log('  volume         ' + (r.vol / 1000).toFixed(1) + ' cm3' + (r.vol < 0 ? '   ** NEGATIVE - normals inverted **' : ''));
  console.log('  watertight     ' + (watertight ? 'yes' : 'NO'));
  if (r.open) console.log('     open edges      ' + r.open + '   <-- holes in the mesh');
  if (r.nonmanifold) console.log('     non-manifold    ' + r.nonmanifold + '   <-- edges shared by >2 faces');
  if (r.degenerate) console.log('  degenerate     ' + r.degenerate + ' zero-area facets');
  console.log('  shells         ' + r.shells + (r.shells > 1 ? '   <-- separate pieces' : ''));
  console.log('  best orient    ' + best.name + '   overhang ' + best.pct.toFixed(1) + '% of surface, ' + best.height.toFixed(0) + 'mm tall' + (best.fits ? '' : '   DOES NOT FIT BED'));
  if (asModelled && asModelled.name !== best.name) {
    console.log('  as modelled    +Z up  overhang ' + asModelled.pct.toFixed(1) + '%');
  }
  const anyFits = r.over.some(o => o.fits);
  if (!anyFits) console.log('  ** NO ORIENTATION FITS THE ' + BED.join('x') + ' BED **');
  if (!watertight || r.vol < 0 || !anyFits) problems++;
}
console.log('');
console.log(files.length + ' file(s), ' + problems + ' with problems' +
            (unreadable ? ', ' + unreadable + ' could not be read at all' : ''));
// Exit non-zero only when a file could not be read - an LFS pointer, a truncated
// export, something that is not an STL. It used to exit 0 even then, so a script
// calling it passed while holding 131 bytes of text.
if (unreadable) process.exit(1);
