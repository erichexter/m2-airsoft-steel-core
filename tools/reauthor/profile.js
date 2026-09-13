// Exact cross-section at one station, chained and corner-preserving (RDP), for extrusion.
//   node profile.js <stl> <axis> <station> [eps] [--json out]
const fs=require('fs');
const A=process.argv.slice(2);
const file=A[0], axisName=A[1], S=parseFloat(A[2]), EPS=parseFloat(A[3]||'0.15');
const outArg=(A.includes('--json')?A[A.indexOf('--json')+1]:null);
const AX={x:0,y:1,z:2}[axisName], U=(AX+1)%3, V=(AX+2)%3;
const b=fs.readFileSync(file), n=b.readUInt32LE(80);
let o=84; const T=[];
for(let i=0;i<n;i++){const v=[];for(let k=0;k<9;k++)v.push(b.readFloatLE(o+12+k*4));o+=50;
  T.push([[v[0],v[1],v[2]],[v[3],v[4],v[5]],[v[6],v[7],v[8]]]);}
const segs=[];
for(const t of T){
  const d=t.map(p=>p[AX]-S), pts=[];
  for(let i=0;i<3;i++){const j=(i+1)%3;
    if((d[i]>0)!==(d[j]>0)){const f=d[i]/(d[i]-d[j]);
      pts.push([t[i][U]+f*(t[j][U]-t[i][U]), t[i][V]+f*(t[j][V]-t[i][V])]);}}
  if(pts.length===2 && (pts[0][0]!==pts[1][0]||pts[0][1]!==pts[1][1])) segs.push(pts);
}
const K=p=>Math.round(p[0]*1e4)+','+Math.round(p[1]*1e4);
const m=new Map(), pos=new Map();
for(const [p,q] of segs) for(const [x,y] of [[p,q],[q,p]]){
  const k=K(x); if(!m.has(k)){m.set(k,[]); pos.set(k,x);} m.get(k).push(y); }
const seen=new Set(), loops=[];
for(const [p] of segs){
  if(seen.has(K(p))) continue;
  const loop=[p]; seen.add(K(p)); let prev=p, cur=(m.get(K(p))||[])[0];
  while(cur && !seen.has(K(cur))){ loop.push(cur); seen.add(K(cur));
    const nb=(m.get(K(cur))||[]).filter(z=>K(z)!==K(prev)&&!seen.has(K(z)));
    prev=cur; cur=nb[0]; }
  if(loop.length>=4) loops.push(loop);
}
const area=l=>{let a=0;for(let i=0;i<l.length;i++){const j=(i+1)%l.length;a+=l[i][0]*l[j][1]-l[j][0]*l[i][1];}return a/2;};
function rdpClosed(pts,eps){
  // split the closed loop at its two extreme points so RDP sees open chains
  let i0=0,i1=0;
  for(let i=1;i<pts.length;i++){ if(pts[i][0]<pts[i0][0])i0=i; if(pts[i][0]>pts[i1][0])i1=i; }
  const [a,b2]=i0<i1?[i0,i1]:[i1,i0];
  const c1=pts.slice(a,b2+1), c2=pts.slice(b2).concat(pts.slice(0,a+1));
  const r=(p)=>{
    if(p.length<3) return p;
    let dmax=0,idx=0; const s=p[0],e=p[p.length-1];
    const dx=e[0]-s[0], dy=e[1]-s[1], L=Math.hypot(dx,dy)||1;
    for(let i=1;i<p.length-1;i++){
      const d=Math.abs(dy*p[i][0]-dx*p[i][1]+e[0]*s[1]-e[1]*s[0])/L;
      if(d>dmax){dmax=d;idx=i;} }
    return dmax<=eps ? [s,e] : r(p.slice(0,idx+1)).slice(0,-1).concat(r(p.slice(idx)));
  };
  const out=r(c1).slice(0,-1).concat(r(c2).slice(0,-1));
  return out.map(p=>[+p[0].toFixed(3),+p[1].toFixed(3)]);
}
let L=loops.map(l=>({a:area(l), raw:l.length, pts:rdpClosed(l,EPS)}));
L.sort((p,q)=>Math.abs(q.a)-Math.abs(p.a));
// containment: a loop nested inside an odd number of others is a hole
const inPoly=(pt,poly)=>{let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){
  if((poly[i][1]>pt[1])!==(poly[j][1]>pt[1]) &&
     pt[0]<(poly[j][0]-poly[i][0])*(pt[1]-poly[i][1])/(poly[j][1]-poly[i][1])+poly[i][0]) c=!c;}return c;};
const depth=L.map((l,i)=>L.filter((o,j)=>j!==i && Math.abs(o.a)>Math.abs(l.a) && inPoly(l.pts[0],o.pts)).length);
const regions=[];
L.forEach((l,i)=>{ if(depth[i]%2===0) regions.push({outer:l.pts, aOuter:Math.abs(l.a), holes:[], idx:i}); });
L.forEach((l,i)=>{
  if(depth[i]%2===0) return;
  // attach to the smallest enclosing even-depth loop
  let best=null;
  for(const r of regions) if(depth[r.idx]===depth[i]-1 && inPoly(l.pts[0], r.outer))
    if(!best || r.aOuter<best.aOuter) best=r;
  if(best) best.holes.push(l.pts);
});
for(const r of regions){ r.net = +(r.aOuter - r.holes.reduce((s,h)=>{
  let a=0;for(let i=0;i<h.length;i++){const j=(i+1)%h.length;a+=h[i][0]*h[j][1]-h[j][0]*h[i][1];}
  return s+Math.abs(a/2);},0)).toFixed(2); delete r.idx; }
const netAll = regions.reduce((s,r)=>s+r.net,0);
const res={axis:axisName, station:S, regions,
  outer:regions[0].outer, holes:regions[0].holes,
  areaOuter:+regions[0].aOuter.toFixed(1), areaNet:+netAll.toFixed(1)};
if(outArg) fs.writeFileSync(outArg, JSON.stringify(res));
console.error(`${file.split(/[\/]/).pop()} @${axisName}=${S}: loops ${L.length} -> ${regions.length} region(s)  ` +
  regions.map(r=>`[${r.outer.length}pts net ${r.net}${r.holes.length?' holes '+r.holes.length:''}]`).join(' ') +
  `  total ${res.areaNet}`);
if(!outArg) console.log(JSON.stringify(res));
