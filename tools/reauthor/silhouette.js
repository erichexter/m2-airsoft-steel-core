// Project an STL onto a plane, rasterise, and extract simplified boundary contours.
//   node silhouette.js <stl> <plane xy|xz|yz> <cell_mm> [--slab a,b] [--json out]
// Outputs {outer:[[u,v]...], holes:[[...]]} in mm, plus the projection bbox.
const fs=require('fs');
const A=process.argv.slice(2);
const file=A[0], plane=A[1], CELL=parseFloat(A[2]||'0.5');
const slabArg=(A.includes('--slab')?A[A.indexOf('--slab')+1]:null);
const outArg=(A.includes('--json')?A[A.indexOf('--json')+1]:null);
const AXES={xy:[0,1,2],xz:[0,2,1],yz:[1,2,0]}[plane];
const [U,V,W]=AXES;
const buf=fs.readFileSync(file), n=buf.readUInt32LE(80);
let o=84; const tris=[];
for(let i=0;i<n;i++){const v=[];for(let k=0;k<9;k++)v.push(buf.readFloatLE(o+12+k*4));o+=50;
  tris.push([[v[0],v[1],v[2]],[v[3],v[4],v[5]],[v[6],v[7],v[8]]]);}
let T=tris;
if(slabArg){const [a,b]=slabArg.split(',').map(Number);
  T=tris.filter(t=>t.some(p=>p[W]>=a&&p[W]<=b));}
let u0=1e9,u1=-1e9,v0=1e9,v1=-1e9;
for(const t of T) for(const p of t){
  if(p[U]<u0)u0=p[U]; if(p[U]>u1)u1=p[U]; if(p[V]<v0)v0=p[V]; if(p[V]>v1)v1=p[V];}
const PAD=2*CELL;
u0-=PAD;v0-=PAD;u1+=PAD;v1+=PAD;
const NU=Math.ceil((u1-u0)/CELL)+1, NV=Math.ceil((v1-v0)/CELL)+1;
const grid=new Uint8Array(NU*NV);
// scanline-fill each projected triangle
for(const t of T){
  const p=t.map(q=>[(q[U]-u0)/CELL,(q[V]-v0)/CELL]);
  let jmin=Math.max(0,Math.floor(Math.min(p[0][1],p[1][1],p[2][1])));
  let jmax=Math.min(NV-1,Math.ceil(Math.max(p[0][1],p[1][1],p[2][1])));
  for(let j=jmin;j<=jmax;j++){
    const y=j+0.5, xs=[];
    for(let e=0;e<3;e++){
      const a=p[e], b=p[(e+1)%3];
      if((a[1]>y)!==(b[1]>y)) xs.push(a[0]+(y-a[1])/(b[1]-a[1])*(b[0]-a[0]));
    }
    if(xs.length<2) continue;
    xs.sort((x,y2)=>x-y2);
    for(let k=0;k+1<xs.length;k+=2){
      const s=Math.max(0,Math.ceil(xs[k]-0.5)), e=Math.min(NU-1,Math.floor(xs[k+1]-0.5));
      for(let i=s;i<=e;i++) grid[j*NU+i]=1;
    }
  }
}
// close 1-cell gaps: dilate then erode
function morph(g,val){
  const out=new Uint8Array(g.length);
  for(let j=0;j<NV;j++)for(let i=0;i<NU;i++){
    let hit=0;
    for(let dj=-1;dj<=1&&!hit;dj++)for(let di=-1;di<=1;di++){
      const jj=j+dj, ii=i+di;
      if(jj<0||jj>=NV||ii<0||ii>=NU) continue;
      if(g[jj*NU+ii]===val){hit=1;break;}
    }
    out[j*NU+i]= val? (hit?1:g[j*NU+i]) : (hit?0:g[j*NU+i]);
  }
  return out;
}
let G=morph(morph(grid,1),0);
const at=(i,j)=>(i<0||j<0||i>=NU||j>=NV)?0:G[j*NU+i];
// Oriented boundary-edge walk: every filled cell contributes its edges whose
// neighbour is empty, wound CCW around material. Chaining them gives closed loops.
const key=(i,j)=>i+','+j;
const outMap=new Map();
function addEdge(a,b){ const k=key(...a); if(!outMap.has(k)) outMap.set(k,[]); outMap.get(k).push(b); }
for(let j=0;j<NV;j++) for(let i=0;i<NU;i++){
  if(!at(i,j)) continue;
  if(!at(i,j-1)) addEdge([i,j],   [i+1,j]);     // bottom
  if(!at(i+1,j)) addEdge([i+1,j], [i+1,j+1]);   // right
  if(!at(i,j+1)) addEdge([i+1,j+1],[i,j+1]);    // top
  if(!at(i-1,j)) addEdge([i,j+1], [i,j]);       // left
}
const loops=[];
const remaining=new Map();
for(const [k,v] of outMap) remaining.set(k, v.slice());
for(const [startK] of outMap){
  while((remaining.get(startK)||[]).length){
    const loop=[];
    let curK=startK;
    for(let guard=0; guard<2000000; guard++){
      const outs=remaining.get(curK);
      if(!outs || !outs.length) break;
      const nxt=outs.shift();
      loop.push(curK.split(',').map(Number));
      curK=key(...nxt);
      if(curK===startK) break;
    }
    if(loop.length>=8) loops.push(loop);
  }
}

function toMM(l){ return l.map(([i,j])=>[+(u0+i*CELL).toFixed(3), +(v0+j*CELL).toFixed(3)]); }
function areaOf(l){let A2=0;for(let i=0;i<l.length;i++){const j=(i+1)%l.length;A2+=l[i][0]*l[j][1]-l[j][0]*l[i][1];}return A2/2;}
function rdp(pts,eps){
  if(pts.length<3) return pts;
  let dmax=0,idx=0;
  const [a,b]=[pts[0],pts[pts.length-1]];
  const dx=b[0]-a[0], dy=b[1]-a[1], L=Math.hypot(dx,dy)||1;
  for(let i=1;i<pts.length-1;i++){
    const d=Math.abs(dy*pts[i][0]-dx*pts[i][1]+b[0]*a[1]-b[1]*a[0])/L;
    if(d>dmax){dmax=d;idx=i;}
  }
  if(dmax<=eps) return [a,b];
  return rdp(pts.slice(0,idx+1),eps).slice(0,-1).concat(rdp(pts.slice(idx),eps));
}
let L2=loops.map(l=>{const m=toMM(l); return {a:areaOf(m), pts:m};});
L2.sort((p,q)=>Math.abs(q.a)-Math.abs(p.a));
const EPS=CELL*0.9;
const simp=l=>{ const s=rdp(l.pts,EPS); if(s.length>2 && s[0][0]===s[s.length-1][0] && s[0][1]===s[s.length-1][1]) s.pop(); return s; };
const outer=simp(L2[0]);
const holes=L2.slice(1).filter(l=>Math.abs(l.a)>CELL*CELL*25).map(simp);
const res={plane, cell:CELL, bbox:{u:[+u0.toFixed(3),+u1.toFixed(3)],v:[+v0.toFixed(3),+v1.toFixed(3)]},
  outer, holes, area:+Math.abs(L2[0].a).toFixed(1)};
if(outArg) fs.writeFileSync(outArg, JSON.stringify(res));
console.error(`${plane}  grid ${NU}x${NV}  loops ${L2.length}  outer ${L2[0].pts.length}->${outer.length} pts  area ${res.area} mm2  holes ${holes.length} [${holes.map(h=>h.length).join(',')}]`);
if(!outArg) console.log(JSON.stringify(res));
