// Straighten a measured profile: heavy RDP, then snap coordinates onto shared
// values and a clean grid. The M2 is a 1918 sheet-and-plate design - the mesh
// wobble is scan noise, not intent.
const fs=require('fs');
const [file,epsS,gridS,tolS]=process.argv.slice(2);
const EPS=parseFloat(epsS||'0.6'), GRID=parseFloat(gridS||'0.1'), TOL=parseFloat(tolS||'0.7');
const d=JSON.parse(fs.readFileSync(file));
function rdpOpen(p,eps){
  if(p.length<3) return p;
  let dmax=0,idx=-1; const s=p[0],e=p[p.length-1];
  const dx=e[0]-s[0],dy=e[1]-s[1],L=Math.hypot(dx,dy)||1;
  for(let i=1;i<p.length-1;i++){
    // distance to the chord; for a degenerate chord fall back to distance from s
    const q=(L>1e-9)? Math.abs(dy*p[i][0]-dx*p[i][1]+e[0]*s[1]-e[1]*s[0])/L
                    : Math.hypot(p[i][0]-s[0],p[i][1]-s[1]);
    if(q>dmax){dmax=q;idx=i;}}
  // idx must strictly split the chain, else recursion never shrinks it
  if(dmax<=eps || idx<1 || idx>p.length-2) return [s,e];
  return rdpOpen(p.slice(0,idx+1),eps).slice(0,-1).concat(rdpOpen(p.slice(idx),eps));
}
function simplify(pts){
  let i0=0,i1=0;
  for(let i=1;i<pts.length;i++){if(pts[i][0]<pts[i0][0])i0=i;if(pts[i][0]>pts[i1][0])i1=i;}
  const [a,b]=i0<i1?[i0,i1]:[i1,i0];
  const r=(c)=>rdpOpen(c,EPS);
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
// A round hole must not go through RDP - it would come back a triangle. Pull the
// circles out so the build can cut them as real cylinders, and snap only the rest.
const bbox=l=>{const u=l.map(p=>p[0]),v=l.map(p=>p[1]);
  return [Math.min(...u),Math.max(...u),Math.min(...v),Math.max(...v)];};
function isRound(l){
  const [u0,u1,v0,v1]=bbox(l), w=u1-u0, h=v1-v0;
  if(l.length<5 || w<0.3 || Math.abs(w-h)>0.15*Math.max(w,h)) return false;
  const r=(w+h)/4, cu=(u0+u1)/2, cv=(v0+v1)/2;
  // every vertex within 6% of the mean radius
  return l.every(p=>Math.abs(Math.hypot(p[0]-cu,p[1]-cv)-r)<0.09*r+0.03);
}
const circles=[], discs=[];
// a whole region that is just a disc (a raised rivet head) becomes a cylinder too
d.regions = d.regions.filter(r=>{
  if(r.holes.length===0 && isRound(r.outer)){
    const [u0,u1,v0,v1]=bbox(r.outer);
    discs.push({u:+((u0+u1)/2).toFixed(3), v:+((v0+v1)/2).toFixed(3), d:+((u1-u0+v1-v0)/2).toFixed(3)});
    return false;
  }
  return true;
});
d.regions=d.regions.map(r=>{
  const keep=[];
  for(const h of r.holes){
    if(isRound(h)){ const [u0,u1,v0,v1]=bbox(h);
      circles.push({u:+((u0+u1)/2).toFixed(3), v:+((v0+v1)/2).toFixed(3), d:+((u1-u0+v1-v0)/2).toFixed(3)}); }
    else keep.push(h);
  }
  const o=fix(r.outer), h=keep.map(fix);
  return {outer:o, holes:h, net:+(area(o)-h.reduce((s,x)=>s+area(x),0)).toFixed(2)};});
d.circles=circles; d.discs=discs;
d.outer=d.regions[0].outer; d.holes=d.regions[0].holes;
d.areaNet=+d.regions.reduce((s,r)=>s+r.net,0).toFixed(1);
fs.writeFileSync(file.replace('.json','_s.json'), JSON.stringify(d));
console.log(file.padEnd(20)+' -> '+d.regions.length+' region(s) '+d.regions.map(r=>r.outer.length+'pts').join(',')+
  '  net '+d.areaNet+(circles.length?('  + '+circles.length+' circle(s) pulled out: '+
    [...new Set(circles.map(c=>'d'+c.d.toFixed(2)))].join(',')):'')+
  (discs.length?('  + '+discs.length+' disc(s): '+[...new Set(discs.map(c=>'d'+c.d.toFixed(2)))].join(',')):''));
