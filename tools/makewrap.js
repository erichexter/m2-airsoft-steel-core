#!/usr/bin/env node
// Build a 1:1 wrap-around cutting template for the 2x3 core tube.
//
//   node tools/makewrap.js <wrap.json> <outdir>
//
// Emits:
//   M2_tube_wrap.svg        one sheet, 1:1, for a plotter or copy shop
//   M2_tube_wrap_tiled.html multi-page letter tiling with registration marks
//
// The tube perimeter is unrolled with the seam on the TOP face centreline,
// running: top(right half) - right - bottom - left - top(left half).

const fs = require('fs');
const path = require('path');

const src = process.argv[2];
const outdir = process.argv[3];
const D = JSON.parse(fs.readFileSync(src, 'utf8'));

const MARGIN = 15;                       // mm of paper around the drawing
const LEN = D.xmax - D.xmin;             // along the tube
const PER = D.perimeter;                 // around the tube
const W = LEN + MARGIN * 2;
const H = PER + MARGIN * 2;

// page geometry -> x grows toward the MUZZLE (+X), u grows down the page
const px = (x) => MARGIN + (x - D.xmin);
const pu = (u) => MARGIN + u;

const FOLD_TOL = 0.35;
const isFold = (pl) => {
  const us = pl.map((p) => p[1]);
  const lo = Math.min(...us), hi = Math.max(...us);
  if (hi - lo > FOLD_TOL) return false;
  const mid = (lo + hi) / 2;
  return D.folds.some((f) => Math.abs(f - mid) < FOLD_TOL) ||
         Math.abs(mid) < FOLD_TOL || Math.abs(mid - PER) < FOLD_TOL;
};

const cuts = [], folds = [];
for (const pl of D.polys) (isFold(pl) ? folds : cuts).push(pl);

const poly = (pl, cls) =>
  `<polyline class="${cls}" points="${pl.map((p) => px(p[0]).toFixed(2) + ',' + pu(p[1]).toFixed(2)).join(' ')}"/>`;

function drawing() {
  let s = '';
  // fold lines full width, drawn from the known u values so they are continuous
  for (const f of D.folds) {
    s += `<line class="fold" x1="${px(D.xmin).toFixed(2)}" y1="${pu(f).toFixed(2)}" x2="${px(D.xmax).toFixed(2)}" y2="${pu(f).toFixed(2)}"/>`;
  }
  // ruler ticks every 50mm from the breech end
  for (let x = Math.ceil(D.xmin / 50) * 50; x <= D.xmax; x += 50) {
    s += `<line class="tick" x1="${px(x).toFixed(2)}" y1="${pu(0).toFixed(2)}" x2="${px(x).toFixed(2)}" y2="${pu(PER).toFixed(2)}"/>`;
    s += `<text class="tick-lbl" x="${(px(x) + 1).toFixed(2)}" y="${(pu(0) - 1.5).toFixed(2)}">${x}</text>`;
  }
  for (const pl of folds) s += poly(pl, 'tangent');
  for (const pl of cuts) s += poly(pl, 'cut');
  // face labels, rotated along the wrap
  for (const [u, label] of D.faceLabels) {
    const y = pu(u), x = px(D.xmin) + 8;
    s += `<text class="face" x="${x.toFixed(2)}" y="${(y - 2).toFixed(2)}">${label}</text>`;
  }
  // border of the wrap area
  s += `<rect class="edge" x="${px(D.xmin).toFixed(2)}" y="${pu(0).toFixed(2)}" width="${LEN.toFixed(2)}" height="${PER.toFixed(2)}"/>`;
  return s;
}

const STYLE = `
  .cut     { fill:none; stroke:#000; stroke-width:0.5; }
  .tangent { fill:none; stroke:#b00; stroke-width:0.25; stroke-dasharray:3 2; }
  .fold    { stroke:#b00; stroke-width:0.25; stroke-dasharray:3 2; }
  .edge    { fill:none; stroke:#888; stroke-width:0.3; stroke-dasharray:6 3; }
  .tick    { stroke:#ccc; stroke-width:0.2; }
  .tick-lbl{ font:2.6px sans-serif; fill:#999; }
  .face    { font:4px sans-serif; fill:#c00; letter-spacing:0.5px; }
  .note    { font:3.4px sans-serif; fill:#000; }
  .cal     { fill:none; stroke:#000; stroke-width:0.4; }
  .cal-lbl { font:3px sans-serif; fill:#000; }
`;

function calibration(x, y) {
  return `<g><line class="cal" x1="${x}" y1="${y}" x2="${x + 100}" y2="${y}"/>` +
    `<line class="cal" x1="${x}" y1="${y - 2}" x2="${x}" y2="${y + 2}"/>` +
    `<line class="cal" x1="${x + 100}" y1="${y - 2}" x2="${x + 100}" y2="${y + 2}"/>` +
    `<text class="cal-lbl" x="${x + 34}" y="${y - 3}">100 mm — measure me</text></g>`;
}

// ---------- single sheet ----------
const single =
`<svg xmlns="http://www.w3.org/2000/svg" width="${W.toFixed(2)}mm" height="${H.toFixed(2)}mm" viewBox="0 0 ${W.toFixed(2)} ${H.toFixed(2)}">
<style>${STYLE}</style>
<rect width="${W.toFixed(2)}" height="${H.toFixed(2)}" fill="#fff"/>
${drawing()}
<text class="note" x="${MARGIN}" y="${(H - 8).toFixed(2)}">M2 core tube — 2x3x0.120 wall. Wrap 1:1. Seam on TOP centreline. Red dashed = corner tangents (fold lines), NOT cuts. Ticks are X in mm from the model origin.</text>
<text class="note" x="${MARGIN}" y="${(H - 3.5).toFixed(2)}">Tube length ${LEN.toFixed(2)} mm, wrap ${PER.toFixed(2)} mm. Breech at left, muzzle at right.</text>
${calibration(MARGIN, MARGIN - 6)}
</svg>`;
fs.writeFileSync(path.join(outdir, 'M2_tube_wrap.svg'), single);

// ---------- tiled for letter ----------
const PW = 279.4, PH = 215.9;            // letter, landscape
const PM = 8;                            // printer margin
const OVER = 12;                         // overlap between tiles
const TW = PW - PM * 2, TH = PH - PM * 2;
const cols = Math.ceil((W - OVER) / (TW - OVER));
const rows = Math.ceil((H - OVER) / (TH - OVER));

let pages = '';
for (let r = 0; r < rows; r++) {
  for (let c = 0; c < cols; c++) {
    const ox = c * (TW - OVER), oy = r * (TH - OVER);
    pages += `<div class="page"><svg xmlns="http://www.w3.org/2000/svg" width="${TW}mm" height="${TH}mm" viewBox="${ox} ${oy} ${TW} ${TH}">
<style>${STYLE}</style>
<g>${drawing()}</g>
<text class="note" x="${ox + 3}" y="${oy + 5}">sheet r${r + 1}c${c + 1} of ${rows}x${cols} — overlap ${OVER}mm, trim on the grey crop marks and tape</text>
</svg>
<div class="crop tl"></div><div class="crop tr"></div><div class="crop bl"></div><div class="crop br"></div>
</div>`;
  }
}

const html = `<!doctype html><meta charset="utf-8"><title>M2 tube wrap — tiled</title>
<style>
  @page { size: letter landscape; margin: ${PM}mm; }
  body { margin:0; font-family:sans-serif; }
  .page { position:relative; width:${TW}mm; height:${TH}mm; page-break-after:always; overflow:hidden; }
  .crop { position:absolute; width:6mm; height:6mm; border:0.3mm solid #999; }
  .tl{left:0;top:0;border-right:none;border-bottom:none}
  .tr{right:0;top:0;border-left:none;border-bottom:none}
  .bl{left:0;bottom:0;border-right:none;border-top:none}
  .br{right:0;bottom:0;border-left:none;border-top:none}
  @media screen { body{background:#666;padding:10mm} .page{background:#fff;margin-bottom:8mm} }
</style>
${pages}`;
fs.writeFileSync(path.join(outdir, 'M2_tube_wrap_tiled.html'), html);

console.log('wrap        ' + LEN.toFixed(2) + ' mm long x ' + PER.toFixed(2) + ' mm around');
console.log('sheet       ' + W.toFixed(2) + ' x ' + H.toFixed(2) + ' mm (incl. ' + MARGIN + 'mm margin)');
console.log('cut lines   ' + cuts.length);
console.log('fold/tangent' + String(folds.length).padStart(4));
console.log('tiled       ' + rows + ' x ' + cols + ' = ' + rows * cols + ' letter pages');
