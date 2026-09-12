#!/usr/bin/env node
// Make a binary STL watertight so it converts to a SOLID rather than a surface.
//
//   node tools/meshrepair.js <in.stl> <out.stl>
//
// Handles the two things that actually break these donor meshes:
//
//   1. T-junctions - one side of a seam uses a single long edge while the other
//      side uses several short ones, so the edges never pair up. The boundary
//      "loop" is a set of COLLINEAR points enclosing zero area, and capping it
//      with a fan just produces degenerate triangles. The fix is to split the
//      long edge at the intruding vertices.
//   2. Genuine holes - capped with a centroid fan, wound to match the shell.
//
// Reports before/after so the repair is verifiable rather than assumed.

const fs = require('fs');

const QUANT = 1e4;          // 0.0001 mm vertex weld
const ON_SEG = 1e-3;        // mm, tolerance for "this vertex lies on that edge"
const inFile = process.argv[2];
const outFile = process.argv[3];
if (!inFile || !outFile) {
  console.error('usage: node meshrepair.js <in.stl> <out.stl>');
  process.exit(1);
}

function readSTL(file) {
  const buf = fs.readFileSync(file);
  const n = buf.readUInt32LE(80);
  const tris = [];
  let o = 84;
  for (let i = 0; i < n; i++) {
    const v = [];
    for (let k = 0; k < 9; k++) v.push(buf.readFloatLE(o + 12 + k * 4));
    o += 50;
    tris.push([[v[0], v[1], v[2]], [v[3], v[4], v[5]], [v[6], v[7], v[8]]]);
  }
  return tris;
}

function writeSTL(file, tris) {
  const buf = Buffer.alloc(84 + tris.length * 50);
  buf.write('repaired by meshrepair.js', 0, 'ascii');
  buf.writeUInt32LE(tris.length, 80);
  let o = 84;
  for (const t of tris) {
    const ux = t[1][0] - t[0][0], uy = t[1][1] - t[0][1], uz = t[1][2] - t[0][2];
    const vx = t[2][0] - t[0][0], vy = t[2][1] - t[0][1], vz = t[2][2] - t[0][2];
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const m = Math.hypot(nx, ny, nz) || 1;
    buf.writeFloatLE(nx / m, o); buf.writeFloatLE(ny / m, o + 4); buf.writeFloatLE(nz / m, o + 8);
    let p = o + 12;
    for (const v of t) for (const c of v) { buf.writeFloatLE(c, p); p += 4; }
    buf.writeUInt16LE(0, o + 48);
    o += 50;
  }
  fs.writeFileSync(file, buf);
}

const key = (v) => Math.round(v[0] * QUANT) + ',' + Math.round(v[1] * QUANT) + ',' + Math.round(v[2] * QUANT);

const raw = readSTL(inFile);
const vmap = new Map(), verts = [];
const id = (v) => {
  const k = key(v);
  let i = vmap.get(k);
  if (i === undefined) { i = verts.length; vmap.set(k, i); verts.push(v); }
  return i;
};

let faces = [];
let degenerate = 0;
const area2 = (a, b, c) => {
  const p = verts[a], q = verts[b], r = verts[c];
  const ux = q[0] - p[0], uy = q[1] - p[1], uz = q[2] - p[2];
  const vx = r[0] - p[0], vy = r[1] - p[1], vz = r[2] - p[2];
  return Math.hypot(uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx);
};
for (const t of raw) {
  const a = id(t[0]), b = id(t[1]), c = id(t[2]);
  if (a === b || b === c || a === c || area2(a, b, c) < 1e-12) { degenerate++; continue; }
  faces.push([a, b, c]);
}

function openEdges(fs_) {
  const dir = new Map();
  for (const [a, b, c] of fs_)
    for (const [u, v] of [[a, b], [b, c], [c, a]])
      dir.set(u + '_' + v, (dir.get(u + '_' + v) || 0) + 1);
  const out = [];
  for (const [k, cnt] of dir) {
    const [u, v] = k.split('_').map(Number);
    const back = dir.get(v + '_' + u) || 0;
    for (let i = 0; i < cnt - back; i++) out.push([u, v]);
  }
  return out;
}

console.log(inFile.split(/[\\/]/).pop());
console.log('  triangles in       ' + raw.length.toLocaleString());
console.log('  degenerate dropped ' + degenerate);
console.log('  open edges         ' + openEdges(faces).length);

// ---- pass 1: split T-junctions ----
function distToSeg(w, u, v) {
  const p = verts[w], a = verts[u], b = verts[v];
  const ab = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
  const ap = [p[0] - a[0], p[1] - a[1], p[2] - a[2]];
  const L2 = ab[0] * ab[0] + ab[1] * ab[1] + ab[2] * ab[2];
  if (L2 < 1e-18) return Infinity;
  let t = (ap[0] * ab[0] + ap[1] * ab[1] + ap[2] * ab[2]) / L2;
  if (t <= 1e-6 || t >= 1 - 1e-6) return Infinity;        // must be strictly interior
  const c = [a[0] + ab[0] * t, a[1] + ab[1] * t, a[2] + ab[2] * t];
  return { d: Math.hypot(p[0] - c[0], p[1] - c[1], p[2] - c[2]), t };
}

let splits = 0;
for (let pass = 0; pass < 12; pass++) {
  const open = openEdges(faces);
  if (!open.length) break;
  const openVerts = new Set();
  for (const [u, v] of open) { openVerts.add(u); openVerts.add(v); }
  let didSplit = false;
  for (const [u, v] of open) {
    const hits = [];
    for (const w of openVerts) {
      if (w === u || w === v) continue;
      const r = distToSeg(w, u, v);
      if (r !== Infinity && r.d < ON_SEG) hits.push([r.t, w]);
    }
    if (!hits.length) continue;
    hits.sort((a, b) => a[0] - b[0]);
    const chain = [u, ...hits.map((h) => h[1]), v];
    // find the face carrying directed edge (u,v) and fan it
    let fi = -1, rot = 0;
    for (let i = 0; i < faces.length && fi < 0; i++) {
      const f = faces[i];
      for (let r = 0; r < 3; r++) {
        if (f[r] === u && f[(r + 1) % 3] === v) { fi = i; rot = r; break; }
      }
    }
    if (fi < 0) continue;
    const third = faces[fi][(rot + 2) % 3];
    const repl = [];
    for (let i = 0; i < chain.length - 1; i++) {
      if (area2(chain[i], chain[i + 1], third) > 1e-12) repl.push([chain[i], chain[i + 1], third]);
    }
    if (!repl.length) continue;
    faces.splice(fi, 1, ...repl);
    splits += repl.length - 1;
    didSplit = true;
  }
  if (!didSplit) break;
}
console.log('  T-junction splits  ' + splits + '   open now ' + openEdges(faces).length);

// ---- pass 2: cap any genuine holes that remain ----
const remaining = openEdges(faces);
let capped = 0;
if (remaining.length) {
  const next = new Map();
  for (const [u, v] of remaining) {
    if (!next.has(u)) next.set(u, []);
    next.get(u).push(v);
  }
  const used = new Set();
  for (const [u0, vs] of next) {
    for (const v0 of vs) {
      if (used.has(u0 + '_' + v0)) continue;
      const loop = [u0];
      let cur = v0;
      used.add(u0 + '_' + v0);
      let guard = 0;
      while (cur !== u0 && guard++ < 100000) {
        loop.push(cur);
        const outs = (next.get(cur) || []).filter((w) => !used.has(cur + '_' + w));
        if (!outs.length) break;
        used.add(cur + '_' + outs[0]);
        cur = outs[0];
      }
      if (cur !== u0 || loop.length < 3) continue;
      const c = [0, 0, 0];
      for (const i of loop) { c[0] += verts[i][0]; c[1] += verts[i][1]; c[2] += verts[i][2]; }
      c[0] /= loop.length; c[1] /= loop.length; c[2] /= loop.length;
      const ci = id(c);
      for (let i = 0; i < loop.length; i++) {
        const a = loop[i], b = loop[(i + 1) % loop.length];
        if (area2(b, a, ci) > 1e-12) { faces.push([b, a, ci]); capped++; }
      }
    }
  }
  console.log('  hole cap triangles ' + capped);
}

const after = openEdges(faces);
console.log('  open edges after   ' + after.length + (after.length ? '   ** STILL OPEN **' : '   watertight'));

let vol = 0;
for (const [a, b, c] of faces) {
  const p = verts[a], q = verts[b], r = verts[c];
  vol += (p[0] * (q[1] * r[2] - q[2] * r[1])
        - p[1] * (q[0] * r[2] - q[2] * r[0])
        + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6;
}
console.log('  signed volume      ' + (vol / 1000).toFixed(1) + ' cm3' +
  (vol < 0 ? '   (normals inverted)' : ''));

writeSTL(outFile, faces.map(([a, b, c]) => [verts[a], verts[b], verts[c]]));
console.log('  wrote              ' + outFile.split(/[\\/]/).pop() +
  '  (' + faces.length.toLocaleString() + ' triangles)');
