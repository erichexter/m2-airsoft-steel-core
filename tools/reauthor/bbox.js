const fs=require('fs');
for(const f of process.argv.slice(2)){
  const b=fs.readFileSync(f), n=b.readUInt32LE(80);
  let o=84; const lo=[1e9,1e9,1e9], hi=[-1e9,-1e9,-1e9];
  // also tally facet normals to find the dominant plate direction
  const nx={x:0,y:0,z:0};
  for(let i=0;i<n;i++){
    const nv=[b.readFloatLE(o),b.readFloatLE(o+4),b.readFloatLE(o+8)];
    const ax=Math.abs(nv[0]),ay=Math.abs(nv[1]),az=Math.abs(nv[2]);
    if(ax>=ay&&ax>=az)nx.x++; else if(ay>=az)nx.y++; else nx.z++;
    for(let k=0;k<3;k++){for(let c=0;c<3;c++){const v=b.readFloatLE(o+12+k*12+c*4);
      if(v<lo[c])lo[c]=v; if(v>hi[c])hi[c]=v;}}
    o+=50;
  }
  const nm=f.split(/[\/]/).pop().replace('.stl','');
  console.log('%s  tris=%d  X %.1f..%.1f (%.1f)  Y %.1f..%.1f (%.1f)  Z %.1f..%.1f (%.1f)  normals x%d y%d z%d',
    nm.padEnd(22), n, lo[0],hi[0],hi[0]-lo[0], lo[1],hi[1],hi[1]-lo[1], lo[2],hi[2],hi[2]-lo[2], nx.x,nx.y,nx.z);
}
