// Compare the hole inventory of two solids, section by section, on one axis.
//   node holediff.js <donor> <mine> <axis> <s0> <s1> <step>
const {execSync} = require('child_process');
const fs = require('fs');
const [DON, MINE, axis, s0, s1, step] = process.argv.slice(2);
function holes(f, s) {
  try { execSync(`node profile.js "${f}" ${axis} ${s} 0.15 --json _hd.json`, {stdio:['pipe','pipe','pipe']}); }
  catch (e) { return null; }
  const d = JSON.parse(fs.readFileSync('_hd.json'));
  const out = [];
  for (const g of d.regions) for (const h of (g.holes || [])) {
    const u = h.map(p => p[0]), v = h.map(p => p[1]);
    out.push({cu:(Math.min(...u)+Math.max(...u))/2, cv:(Math.min(...v)+Math.max(...v))/2,
              w:Math.max(...u)-Math.min(...u), h:Math.max(...v)-Math.min(...v)});
  }
  return out;
}
const LBL = {x:['Y','Z'], y:['Z','X'], z:['X','Y']}[axis];
let diffs = 0, checked = 0;
for (let s = +s0; s <= +s1 + 1e-9; s += +step) {
  const a = holes(DON, s.toFixed(2)), b = holes(MINE, s.toFixed(2));
  if (a === null || b === null) continue;
  checked++;
  const used = new Array(b.length).fill(false);
  const missing = [], extra = [], wrong = [];
  for (const q of a) {
    let best = -1, bd = 1e9;
    b.forEach((r, i) => { if (used[i]) return;
      const dd = Math.hypot(r.cu-q.cu, r.cv-q.cv); if (dd < bd) { bd = dd; best = i; } });
    if (best < 0 || bd > 2.0) { missing.push(q); continue; }
    used[best] = true;
    const r = b[best];
    if (Math.abs(r.w-q.w) > 0.6 || Math.abs(r.h-q.h) > 0.6) wrong.push([q, r]);
  }
  b.forEach((r, i) => { if (!used[i]) extra.push(r); });
  if (missing.length || extra.length || wrong.length) {
    diffs++;
    console.log(`${axis}=${s.toFixed(2)}`);
    for (const q of missing) console.log(`   MISSING  ${LBL[0]} ${q.cu.toFixed(2)} ${LBL[1]} ${q.cv.toFixed(2)}  ${q.w.toFixed(2)}x${q.h.toFixed(2)}`);
    for (const r of extra)   console.log(`   EXTRA    ${LBL[0]} ${r.cu.toFixed(2)} ${LBL[1]} ${r.cv.toFixed(2)}  ${r.w.toFixed(2)}x${r.h.toFixed(2)}`);
    for (const [q,r] of wrong) console.log(`   SIZE     ${LBL[0]} ${q.cu.toFixed(2)} ${LBL[1]} ${q.cv.toFixed(2)}  donor ${q.w.toFixed(2)}x${q.h.toFixed(2)}  mine ${r.w.toFixed(2)}x${r.h.toFixed(2)}`);
  }
}
console.log(`-- ${axis}: ${checked} sections checked, ${diffs} with differences`);
