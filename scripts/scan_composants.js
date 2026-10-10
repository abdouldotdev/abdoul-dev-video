const {chromium}=require('playwright');const fs=require('fs');(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:300,height:400}});
 const files=fs.readdirSync('.').filter(f=>f.endsWith('.html')).sort();const rep={};
 for(const f of files){await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(120);
  const r=await p.evaluate(()=>{const out=[];const sc=document.querySelector('.ad-scene');if(!sc)return out;const R0=sc.getBoundingClientRect(),k=R0.width/360;
   const U=x=>+(x/k).toFixed(1);const rect=e=>{const q=e.getBoundingClientRect();return {l:(q.left-R0.left)/k,t:(q.top-R0.top)/k,r:(q.right-R0.left)/k,b:(q.bottom-R0.top)/k,w:q.width/k,h:q.height/k}};
   const isBox=e=>{const s=getComputedStyle(e);return parseFloat(s.borderLeftWidth)>=2||e.classList.contains('phone')||e.classList.contains('scr')};
   const lab=e=>(e.className&&e.className.baseVal===undefined?e.className:'')+':'+(e.textContent||'').trim().slice(0,18);
   // 1 débordement : un descendant sort de sa boîte (hors ombre)
   sc.querySelectorAll('*').forEach(e=>{if(e.closest('svg')&&e.tagName!=='svg')return;const box=e.parentElement&&e.parentElement.closest('.bx,.phone,.scr,.tg,.btn,.row[style*="border"]');if(!box||!sc.contains(box)||box===e)return;
     const a=rect(e),c=rect(box);if(!a.w||!a.h)return;const ov=Math.max(c.l-a.l,a.r-c.r,c.t-a.t,a.b-c.b);
     if(ov>1.5&&getComputedStyle(box).overflow!=='hidden')out.push({k:'déborde',el:lab(e),box:lab(box),px:U(ov*k)});});
   // 2 texte coupé
   sc.querySelectorAll('*').forEach(e=>{if(e.children.length||!(e.textContent||'').trim())return;if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')out.push({k:'texte coupé',el:lab(e)})});
   // 3 marge texte / bord
   const w=document.createTreeWalker(sc,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(t.length<2)continue;const el=n.parentElement;if(el.closest('.cap,.t,.big,svg'))continue;
     let c=el;while(c&&c!==sc&&!isBox(c))c=c.parentElement;if(!c||c===sc)continue;const rg=document.createRange();rg.selectNodeContents(n);const q=rg.getBoundingClientRect();if(!q.width)continue;const cr=c.getBoundingClientRect(),s=getComputedStyle(c);
     const L=(q.left-cr.left-parseFloat(s.borderLeftWidth))/k,Rr=(cr.right-parseFloat(s.borderRightWidth)-q.right)/k;if(Math.min(L,Rr)<6)out.push({k:'marge',el:lab(el),L:+L.toFixed(1),R:+Rr.toFixed(1)})}
   // 4 chevauchement entre blocs frères à contour
   const boxes=[...sc.querySelectorAll('.bx,.tg,.btn,.phone')].filter(e=>getComputedStyle(e).opacity!=='0');
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const A=boxes[i],B=boxes[j];if(A.contains(B)||B.contains(A))continue;const a=rect(A),c=rect(B);
     const x=Math.min(a.r,c.r)-Math.max(a.l,c.l),y=Math.min(a.b,c.b)-Math.max(a.t,c.t);if(x>2&&y>2)out.push({k:'chevauche',a:lab(A),b:lab(B),x:+x.toFixed(1),y:+y.toFixed(1)})}
   // 5 centrage horizontal du groupe
   const st=sc.querySelector('.ad-stage')||sc;let l=1e9,r=-1e9;[...st.children].forEach(c=>{if(c.classList.contains('cap')||c.classList.contains('t')||c.classList.contains('big'))return;const q=rect(c);if(!q.w)return;l=Math.min(l,q.l);r=Math.max(r,q.r)});
   if(r>l){const cx=(l+r)/2;if(Math.abs(cx-180)>4)out.push({k:'décentré',dx:+(180-cx).toFixed(1)})}
   // 6 tailles par famille
   sc.querySelectorAll('.tg,.btn,.inp').forEach(e=>{const h=rect(e).h;const ok=e.classList.contains('tg')?[22,28,32]:[28];if(!ok.some(v=>Math.abs(v-h)<1.5))out.push({k:'taille',el:lab(e),h:+h.toFixed(1)})});
   return out});
  if(r.length)rep[f.replace('.html','')]=r}
 fs.writeFileSync('scan.json',JSON.stringify(rep,null,1));
 const cnt={};Object.values(rep).flat().forEach(x=>cnt[x.k]=(cnt[x.k]||0)+1);console.log(JSON.stringify(cnt),Object.keys(rep).length,'composants');
 for(const [k,v] of Object.entries(rep))console.log(k,'→',v.map(x=>x.k+' '+(x.el||x.a||'')+(x.box?' ⊄ '+x.box:'')+(x.b?' ∩ '+x.b:'')+(x.px!==undefined?' '+x.px:'')+(x.h?' h'+x.h:'')+(x.dx!==undefined?' dx'+x.dx:'')+(x.L!==undefined?` L${x.L}/R${x.R}`:'')).join(' | ').slice(0,600));
 await b.close()})()
