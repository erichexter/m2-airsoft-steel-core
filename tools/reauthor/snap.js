// Straighten a measured profile: heavy RDP, then snap coordinates onto shared
// values and a clean grid. The M2 is a 1918 sheet-and-plate design - the mesh
// wobble is scan noise, not intent.
const fs=require('fs');
const [file,epsS,gridS,tolS]=process.argv.slice(2);
const EPS=parseFloat(epsS||'0.6'), GRID=parseFloat(gridS||'0.1'), TOL=parseFloat(tolS||'0.7');
const d=JSON.parse(fs.readFileSync(file));
function rdpOpen(p,eps){
  if(p.length<3) return p;
  let dmax=0,idx=0; const s=p[0],e=p[p.length-1];
  const dx=e[0]-s[0],dy=e[1]-s[1],L=Math.hypot(dx,dy)||1;
  for(let i=1;i<p.length-1;i++){
    const q=Math.abs(dy*p[i][0]-dx*p[i][1]+e[0]*s[1]-e[1]*s[0])/L;
    if(q>dmax){dmax=q;idx=i;}}
  return dmax<=eps?[s,e]:rdpOpen(p.slice(0,idx+1)).slice(0,-1).concat(rdpOpen(p.slice(idx)));
}
function simplify(pts){
  let i0=0,i1=0;
  for(let i=1;i<pts.length;i++){if(pts[i][0]<pts[i0][0])i0=i;if(pts[i][0]>pts[i1][0])i1=i;}
  const [a,b]=i0<i1?[i0,i1]:[i1,i0];
  const r=(c)=>{const o=rdpOpen(c,EPS);return o;};
  const c1=r(pts.slice(a,b+1)), c2=r(pts.slice(b).concat(pts.slice(0,a+1)));
  return c1.slice(0,-1).concat(c2.slice(0,-1));
}
// cluster values within TOL and replace each with the cluster mean, snapped to GRID
function cluster(vals){
  const s=[...new Set(vals)].sort((x,y)=>x-y), map=new Map();
  let i=0;
  while(i<s.length){
    let j=i; while(j+1<s.length && s[j+1]-s[j]<=TOL) j++;
    const grp=s.slice(i,j+1);
    let m=grp.reduce((p,q)=>p+q,0)/grp.length;
    m=Math.round(m/GRID)*GRID;
    // prefer a round number only if it is already within a whisker - interface
    // dimensions like 12.70 (half an inch) and 43.625 must survive untouched
    for(const cand of [Math.round(m), Math.round(m*2)/2])
      if(Math.abs(cand-m)<=0.06) { m=cand; break; }
    for(const g of grp) map.set(g, +m.toFixed(3));
    i=j+1;
  }
  return map;
}
const all=[];
for(const r of d.regions){ all.push(...r.outer); for(const h of r.holes) all.push(...h); }
const mu=cluster(all.map(p=>p[0])), mv=cluster(all.map(p=>p[1]));
const fix=l=>{
  const s=simplify(l).map(p=>[mu.get(p[0]), mv.get(p[1])]);
  const out=[];
  for(const p of s){ const q=out[out.length-1]; if(!q||q[0]!==p[0]||q[1]!==p[1]) out.push(p); }
  if(out.length>1 && out[0][0]===out[out.length-1][0] && out[0][1]===out[out.length-1][1]) out.pop();
  // drop points that are collinear with their neighbours after snapping
  const keep=[];
  for(let i=0;i<out.length;i++){
    const a=out[(i-1+out.length)%out.length], b=out[i], c=out[(i+1)%out.length];
    const cr=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
    if(Math.abs(cr)>1e-6) keep.push(b);
  }
  return keep.length>=3?keep:out;
};
const area=l=>{let a=0;for(let i=0;i<l.length;i++){const j=(i+1)%l.length;a+=l[i][0]*l[j][1]-l[j][0]*l[i][1];}return Math.abs(a/2);};
d.regions=d.regions.map(r=>{const o=fix(r.outer), h=r.holes.map(fix);
  return {outer:o, holes:h, net:+(area(o)-h.reduce((s,x)=>s+area(x),0)).toFixed(2)};});
d.outer=d.regions[0].outer; d.holes=d.regions[0].holes;
d.areaNet=+d.regions.reduce((s,r)=>s+r.net,0).toFixed(1);
fs.writeFileSync(file.replace('.json','_s.json'), JSON.stringify(d));
console.log(file.padEnd(20)+' -> '+d.regions.map(r=>r.outer.length+'pts').join(',')+
  '  net '+d.areaNet+'  (was '+d.areaOuter+')');
