// mesure l'emprise de chaque scène (tout visible, sans animation) et écrit le décalage de centrage
const {chromium}=require('playwright');const fs=require('fs');(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+process.cwd()+'/proj/index.html');await p.waitForTimeout(600);
 const out=await p.evaluate(()=>{const res={};document.querySelectorAll('.clip .ad-stage').forEach(st=>{
   const clip=st.closest('.clip');clip.style.visibility='visible';st.style.transform='none';
   st.querySelectorAll('*').forEach(e=>{e.style.opacity='1';e.style.transform='none'});
   const r0=st.parentElement.getBoundingClientRect(),k=r0.width/360;let t=1e9,bo=-1e9,l=1e9,r=-1e9;
   [...st.children].forEach(c=>{const q=c.getBoundingClientRect();if(!q.height)return;t=Math.min(t,q.top);bo=Math.max(bo,q.bottom);l=Math.min(l,q.left);r=Math.max(r,q.right)});
   const cy=((t+bo)/2-r0.top)/k,cx=((l+r)/2-r0.left)/k;res[clip.id]=[+(180-cx).toFixed(1),+(+st.dataset.cy-cy).toFixed(1)];});return res});
 fs.writeFileSync('center.json',JSON.stringify(out,null,1));console.log(out);await b.close()})()
