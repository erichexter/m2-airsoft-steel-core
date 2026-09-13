// Report cross-sectional area vs station to locate prismatic runs and breakpoints.
const fs=require('fs');
const [file,axisName,s0,s1,step]=process.argv.slice(2);
const AX={x:0,y:1,z:2}[axisName], U=(AX+1)%3, V=(AX+2)%3;
const b=fs.readFileSync(file), n=b.readUInt32LE(80);
let o=84; const T=[];
for(let i=0;i<n;i++){const v=[];for(let k=0;k<9;k++)v.push(b.readFloatLE(o+12+k*4));o+=50;
  T.push([[v[0],v[1],v[2]],[v[3],v[4],v[5]],[v[6],v[7],v[8]]]);}
function areaAt(s){
  const segs=[];
  for(const t of T){
    const d=t.map(p=>p[AX]-s), pts=[];
    for(let i=0;i<3;i++){const j=(i+1)%3;
      if((d[i]>0)!==(d[j]>0)){const f=d[i]/(d[i]-d[j]);
        pts.push([t[i][U]+f*(t[j][U]-t[i][U]), t[i][V]+f*(t[j][V]-t[i][V])]);}}
    if(pts.length===2) segs.push(pts);
  }
  // signed area via the divergence theorem over all segments (orientation from the facet normal is
  // unavailable here, so use |sum| of the shoelace over chained loops); chain first
  const K=p=>Math.round(p[0]*1e3)+','+Math.round(p[1]*1e3);
  const m=new Map();
  for(const [p,q] of segs) for(const [x,y] of [[p,q],[q,p]]){if(!m.has(K(x)))m.set(K(x),[]);m.get(K(x)).push(y);}
  const seen=new Set(); let A=0,nl=0; const bb=[1e9,-1e9,1e9,-1e9];
  for(const [p] of segs){
    if(seen.has(K(p)))continue;
    const loop=[p]; seen.add(K(p)); let prev=p,cur=(m.get(K(p))||[])[0];
    while(cur&&!seen.has(K(cur))){loop.push(cur);seen.add(K(cur));
      const nb=(m.get(K(cur))||[]).filter(z=>K(z)!==K(prev)&&!seen.has(K(z)));prev=cur;cur=nb[0];}
    if(loop.length<4)continue;
    let a=0;for(let i=0;i<loop.length;i++){const j=(i+1)%loop.length;a+=loop[i][0]*loop[j][1]-loop[j][0]*loop[i][1];}
    A+=Math.abs(a/2); nl++;
    for(const q of loop){bb[0]=Math.min(bb[0],q[0]);bb[1]=Math.max(bb[1],q[0]);bb[2]=Math.min(bb[2],q[1]);bb[3]=Math.max(bb[3],q[1]);}
  }
  return {A,nl,bb};
}
let prev=null;
for(let s=+s0; s<=+s1+1e-9; s+=+step){
  const r=areaAt(+s.toFixed(4));
  const mark = (prev===null||Math.abs(r.A-prev)>1.0) ? '  <<<' : '';
  console.log('%s  A=%s  loops=%d  u %s..%s  v %s..%s%s',
    s.toFixed(2).padStart(9), r.A.toFixed(1).padStart(8), r.nl,
    r.bb[0].toFixed(2).padStart(7), r.bb[1].toFixed(2).padStart(7),
    r.bb[2].toFixed(2).padStart(7), r.bb[3].toFixed(2).padStart(7), mark);
  prev=r.A;
}
