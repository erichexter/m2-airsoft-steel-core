const fs=require('fs');
const CW=parseInt(process.env.CW||'104',10);
for(const f of process.argv.slice(2)){
  const d=JSON.parse(fs.readFileSync(f));
  const all=[d.outer,...(d.holes||[])].flat();
  const u0=Math.min(...all.map(p=>p[0])), u1=Math.max(...all.map(p=>p[0]));
  const v0=Math.min(...all.map(p=>p[1])), v1=Math.max(...all.map(p=>p[1]));
  const CH=Math.max(3,Math.round(CW*(v1-v0)/(u1-u0)/2.1));
  const inside=(pt,poly)=>{let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){
    if((poly[i][1]>pt[1])!==(poly[j][1]>pt[1]) &&
       pt[0]<(poly[j][0]-poly[i][0])*(pt[1]-poly[i][1])/(poly[j][1]-poly[i][1])+poly[i][0]) c=!c;}return c;};
  console.log(`=== ${f}  ${d.outer.length} pts  net ${d.areaNet} mm2   u ${u0.toFixed(1)}..${u1.toFixed(1)}  v ${v0.toFixed(1)}..${v1.toFixed(1)}`);
  for(let r=0;r<CH;r++){let line='';
    for(let q=0;q<CW;q++){
      const u=u0+(u1-u0)*(q+0.5)/CW, v=v1-(v1-v0)*(r+0.5)/CH;
      let on=inside([u,v],d.outer); for(const h of (d.holes||[])) if(inside([u,v],h)) on=false;
      line+= on?'#':'.';}
    console.log(line);}
  console.log('');
}
