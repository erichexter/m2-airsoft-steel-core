// Cross-section loops resampled at FIXED ANGLES about each loop's centroid, so
// point i of every section corresponds -> lofts without twisting.
const fs=require('fs');
const a=process.argv.slice(2);
const file=a[0], axisName=a[1], S0=+a[2], S1=+a[3], N=+a[4], P=+a[5];
const AX={x:0,y:1,z:2}[axisName], U=(AX+1)%3, V=(AX+2)%3;
const b=fs.readFileSync(file), n=b.readUInt32LE(80);
let o=84; const T=[];
for(let i=0;i<n;i++){const v=[];for(let k=0;k<9;k++)v.push(b.readFloatLE(o+12+k*4));o+=50;
  T.push([[v[0],v[1],v[2]],[v[3],v[4],v[5]],[v[6],v[7],v[8]]]);}
function loopsAt(s){
  const segs=[];
  for(const t of T){
    const d=t.map(p=>p[AX]-s), pts=[];
    for(let i=0;i<3;i++){const j=(i+1)%3;
      if((d[i]>0)!==(d[j]>0)){const f=d[i]/(d[i]-d[j]);
        pts.push([t[i][U]+f*(t[j][U]-t[i][U]), t[i][V]+f*(t[j][V]-t[i][V])]);}}
    if(pts.length===2) segs.push(pts);
  }
  const K=p=>Math.round(p[0]*1e3)+','+Math.round(p[1]*1e3);
  const m=new Map();
  for(const [p,q] of segs) for(const [x,y] of [[p,q],[q,p]]){ if(!m.has(K(x)))m.set(K(x),[]); m.get(K(x)).push(y); }
  const seen=new Set(), loops=[];
  for(const [p] of segs){
    if(seen.has(K(p))) continue;
    const loop=[p]; seen.add(K(p)); let prev=p, cur=(m.get(K(p))||[])[0];
    while(cur && !seen.has(K(cur))){ loop.push(cur); seen.add(K(cur));
      const nb=(m.get(K(cur))||[]).filter(z=>K(z)!==K(prev)&&!seen.has(K(z))); prev=cur; cur=nb[0]; }
    if(loop.length>=6) loops.push(loop);
  }
  return loops;
}
const area=l=>{let A=0;for(let i=0;i<l.length;i++){const j=(i+1)%l.length;A+=l[i][0]*l[j][1]-l[j][0]*l[i][1];}return A/2;};
function areaCentroid(l){
  let A=0,cx=0,cy=0;
  for(let i=0;i<l.length;i++){const j=(i+1)%l.length;
    const f=l[i][0]*l[j][1]-l[j][0]*l[i][1];A+=f;cx+=(l[i][0]+l[j][0])*f;cy+=(l[i][1]+l[j][1])*f;}
  A/=2; return A?[cx/(6*A),cy/(6*A)]:[0,0];
}
// farthest intersection of ray (c, dir) with the polygon
function rayR(loop,c,ux,uy){
  let best=null;
  for(let i=0;i<loop.length;i++){
    const p=loop[i], q=loop[(i+1)%loop.length];
    const ex=q[0]-p[0], ey=q[1]-p[1];
    const den=ux*ey-uy*ex;
    if(Math.abs(den)<1e-12) continue;
    const wx=p[0]-c[0], wy=p[1]-c[1];
    const t=(wx*ey-wy*ex)/den;       // along ray
    const u=(wx*uy-wy*ux)/den;       // along edge
    if(t>1e-9 && u>=-1e-9 && u<=1+1e-9 && (best===null||t>best)) best=t;
  }
  return best;
}
function angResample(loop,k,phase){
  if(area(loop)<0) loop=loop.slice().reverse();
  const c=areaCentroid(loop);
  const r=[];
  for(let i=0;i<k;i++){
    const th=phase+2*Math.PI*i/k;
    r.push(rayR(loop,c,Math.cos(th),Math.sin(th)));
  }
  // fill any misses from neighbours, then 3-tap smooth
  for(let i=0;i<k;i++) if(r[i]===null){
    let a=null,bv=null;
    for(let d=1;d<k;d++){ if(r[(i-d+k)%k]!==null){a=r[(i-d+k)%k];break;} }
    for(let d=1;d<k;d++){ if(r[(i+d)%k]!==null){bv=r[(i+d)%k];break;} }
    r[i]=(a??bv??1);
  }
  const s=r.map((_,i)=>0.25*r[(i-1+k)%k]+0.5*r[i]+0.25*r[(i+1)%k]);
  return s.map((rr,i)=>{const th=phase+2*Math.PI*i/k;
    return [+(c[0]+rr*Math.cos(th)).toFixed(3), +(c[1]+rr*Math.sin(th)).toFixed(3)];});
}
// arc-length resample, re-indexed so point 0 is the top-most vertex (canonical
// start) and winding is CCW -> point i corresponds across sections.
function arcResample(loop,k){
  if(area(loop)<0) loop=loop.slice().reverse();
  // canonical start: highest V, tie-break lowest U
  let bi=0;
  for(let i=1;i<loop.length;i++){
    if(loop[i][1]>loop[bi][1]+1e-9 || (Math.abs(loop[i][1]-loop[bi][1])<1e-9 && loop[i][0]<loop[bi][0])) bi=i;
  }
  loop=loop.slice(bi).concat(loop.slice(0,bi));
  let L=0; const d=[0];
  for(let i=1;i<=loop.length;i++){const q=loop[i%loop.length];
    L+=Math.hypot(q[0]-loop[i-1][0],q[1]-loop[i-1][1]); d.push(L);}
  const out=[];
  for(let i=0;i<k;i++){
    const t=L*i/k; let j=1; while(j<d.length-1&&d[j]<t)j++;
    const p0=loop[j-1], p1=loop[j%loop.length];
    const f=(t-d[j-1])/((d[j]-d[j-1])||1);
    out.push([p0[0]+f*(p1[0]-p0[0]), p0[1]+f*(p1[1]-p0[1])]);
  }
  // gentle 3-tap smoothing to take the facet noise off
  const sm=out.map((_,i)=>{
    const a=out[(i-1+k)%k], b=out[i], c2=out[(i+1)%k];
    return [+(0.25*a[0]+0.5*b[0]+0.25*c2[0]).toFixed(3), +(0.25*a[1]+0.5*b[1]+0.25*c2[1]).toFixed(3)];});
  return sm;
}
const MODE = process.env.SAMPLE || 'arc';
const PHASE = Math.PI/2/ P;
const out=[];
for(let i=0;i<N;i++){
  const s=+(S0+(S1-S0)*i/(N-1)).toFixed(3);
  const ls=loopsAt(s).map(l=>({a:Math.abs(area(l)),c:areaCentroid(l),pts:(MODE==='ang'?angResample(l,P,PHASE):arcResample(l,P)),
    raw:l.length}));
  ls.sort((x,y)=>y.a-x.a);
  out.push({s,loops:ls});
}
console.log(JSON.stringify(out));
