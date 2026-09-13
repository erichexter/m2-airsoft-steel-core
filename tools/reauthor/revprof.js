// Radius profile of a body of revolution: cast rays inward from outside on an
// (axis, theta) grid and take the first-hit radius, then report min/median/max
// per station. Identical method to the barrel jacket.
const fs=require('fs');
const [file,axisName,ac,bc,s0,s1,n,nth]=process.argv.slice(2);
const AX={x:0,y:1,z:2}[axisName], U=(AX+1)%3, V=(AX+2)%3;
const CU=+ac, CV=+bc, N=+n, NTH=+(nth||48);
const buf=fs.readFileSync(file), NT=buf.readUInt32LE(80);
let o=84; const T=[];
for(let i=0;i<NT;i++){const v=[];for(let k=0;k<9;k++)v.push(buf.readFloatLE(o+12+k*4));o+=50;
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
  return segs;
}
console.log(' station   rmin    rmed    rmax    spread');
for(let i=0;i<N;i++){
  const s=+s0+(+s1-+s0)*i/(N-1);
  const segs=loopsAt(s);
  const rs=[];
  for(let k=0;k<NTH;k++){
    const th=2*Math.PI*k/NTH, ux=Math.cos(th), uy=Math.sin(th);
    let best=null;
    for(const [p,q] of segs){
      const ex=q[0]-p[0], ey=q[1]-p[1];
      const den=ux*ey-uy*ex; if(Math.abs(den)<1e-12) continue;
      const wx=p[0]-CU, wy=p[1]-CV;
      const t=(wx*ey-wy*ex)/den, u=(wx*uy-wy*ux)/den;
      if(t>1e-9 && u>=-1e-9 && u<=1+1e-9 && (best===null||t>best)) best=t;
    }
    if(best!==null) rs.push(best);
  }
  if(!rs.length){console.log('  '+s.toFixed(2).padStart(7)+'   (empty)');continue;}
  rs.sort((a,b)=>a-b);
  const med=rs[Math.floor(rs.length/2)];
  console.log('  '+s.toFixed(2).padStart(7)+'  '+rs[0].toFixed(3).padStart(6)+'  '+med.toFixed(3).padStart(6)+
    '  '+rs[rs.length-1].toFixed(3).padStart(6)+'   '+(rs[rs.length-1]-rs[0]).toFixed(3));
}
