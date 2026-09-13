// Sample the local diameter of a raised feature along its axis, so a dome can be
// told from a cylinder. Slices the mesh and measures the loop nearest (u,v).
const fs=require('fs');
const [file,axisName,uc,vc,y0,y1,n]=process.argv.slice(2);
const AX={x:0,y:1,z:2}[axisName], U=(AX+1)%3, V=(AX+2)%3;
const UC=+uc, VC=+vc;
const b=fs.readFileSync(file), N=b.readUInt32LE(80);
let o=84; const T=[];
for(let i=0;i<N;i++){const v=[];for(let k=0;k<9;k++)v.push(b.readFloatLE(o+12+k*4));o+=50;
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
  for(const [p,q] of segs) for(const [x,y] of [[p,q],[q,p]]){if(!m.has(K(x)))m.set(K(x),[]);m.get(K(x)).push(y);}
  const seen=new Set(), loops=[];
  for(const [p] of segs){
    if(seen.has(K(p)))continue;
    const loop=[p];seen.add(K(p));let prev=p,cur=(m.get(K(p))||[])[0];
    while(cur&&!seen.has(K(cur))){loop.push(cur);seen.add(K(cur));
      const nb=(m.get(K(cur))||[]).filter(z=>K(z)!==K(prev)&&!seen.has(K(z)));prev=cur;cur=nb[0];}
    if(loop.length>=4)loops.push(loop);
  }
  return loops;
}
const rows=[];
for(let i=0;i<+n;i++){
  const s=+y0+(+y1-+y0)*i/(+n-1);
  let best=null,bd=1e9;
  for(const l of loopsAt(s)){
    const u=l.map(p=>p[0]),v=l.map(p=>p[1]);
    const cu=(Math.min(...u)+Math.max(...u))/2, cv=(Math.min(...v)+Math.max(...v))/2;
    const w=Math.max(...u)-Math.min(...u), h=Math.max(...v)-Math.min(...v);
    if(w>25||h>25) continue;                    // ignore the big outline loops
    const dist=Math.hypot(cu-UC,cv-VC);
    if(dist<bd){bd=dist;best={d:(w+h)/2,w,h,cu,cv,dist};}
  }
  rows.push([s,best]);
}
console.log('  station    dia     (w x h)        offset');
for(const [s,r] of rows){
  if(!r||r.dist>4){console.log('  '+s.toFixed(2).padStart(7)+'   --  none within 4 mm');continue;}
  console.log('  '+s.toFixed(2).padStart(7)+'  '+r.d.toFixed(2).padStart(6)+'   ('+r.w.toFixed(2)+' x '+r.h.toFixed(2)+')   '+r.dist.toFixed(2));
}
// fit a sphere r^2 = R^2 - (s-c)^2 through the first and last valid rows
const ok=rows.filter(([s,r])=>r&&r.dist<=4);
if(ok.length>=2){
  const [s1,r1]=ok[0], [s2,r2]=ok[ok.length-1];
  const a1=(r1.d/2)**2, a2=(r2.d/2)**2;
  const c=((s2*s2-s1*s1)-(a1-a2))/(2*(s2-s1));
  const R=Math.sqrt(a1+(s1-c)**2);
  console.log('  sphere fit -> centre '+c.toFixed(3)+'  R '+R.toFixed(3)+'  tip at '+(c+R).toFixed(3)+' / '+(c-R).toFixed(3));
  let err=0;
  for(const [s,r] of ok){ const pred=Math.sqrt(Math.max(0,R*R-(s-c)**2))*2; err=Math.max(err,Math.abs(pred-r.d)); }
  console.log('  max deviation from a true sphere: '+err.toFixed(3)+' mm'+(err<0.35?'   -> DOME':'   -> not a sphere'));
}
