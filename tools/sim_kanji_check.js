const { chromium } = require('playwright');const fs=require('fs');const http=require('http');const path=require('path');
(async()=>{const SITE='/home/claude/gakushu-note';const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u==='/')u='/index.html';const p=path.join(SITE,u);if(fs.existsSync(p)&&fs.statSync(p).isFile()){r.setHeader('content-type',u.endsWith('.html')?'text/html;charset=utf8':u.endsWith('.png')?'image/png':'application/json');r.end(fs.readFileSync(p))}else{r.statusCode=404;r.end()}}).listen(8790);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:820,height:1150}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('http://localhost:8790/');await p.waitForTimeout(1000);
const res=await p.evaluate(async()=>{
  const G1='一右雨円王音下火花貝学気九休玉金空月犬見五口校左三山子四糸字耳七車手十出女小上森人水正生青夕石赤千川先早草足村大男竹中虫町天田土二日入年白八百文木本名目立力林六';
  let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};const rn=(a,b)=>a+(b-a)*rnd();
  const refs={};for(const c of G1)refs[c]=await refStrokes(c);
  // make a child's version of a kanji: dense points along each stroke, perturbed
  async function dense(c){const d=await kv(c);const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');document.body.appendChild(svg);const out=d.p.map(dd=>{const q=document.createElementNS('http://www.w3.org/2000/svg','path');q.setAttribute('d',dd);svg.appendChild(q);const L=q.getTotalLength(),a=[];for(let i=0;i<=24;i++){const pt=q.getPointAtLength(L*i/24);a.push([pt.x,pt.y])}return a});svg.remove();return out}
  function perturb(st,lv){const ang=rn(-1,1)*lv.rot*Math.PI/180,sc=rn(lv.s0,lv.s1),ox=rn(100,300),oy=rn(100,300),ca=Math.cos(ang),sa=Math.sin(ang);
    return st.map(s=>{const dx=rn(-1,1)*lv.shift,dy=rn(-1,1)*lv.shift,cut=Math.floor(rn(0,lv.cut)*s.length),ss=s.slice(0,s.length-cut);const ex=1+rn(-1,1)*lv.len;const p0=ss[0];
      return ss.map(q=>{let x=p0[0]+(q[0]-p0[0])*ex,y=p0[1]+(q[1]-p0[1])*ex;x=x-54.5;y=y-54.5;const X=(x*ca-y*sa)*sc*9+ox+ (dx+rn(-1,1)*lv.noise)*9, Y=(x*sa+y*ca)*sc*9+oy+(dy+rn(-1,1)*lv.noise)*9;return [Math.round(X),Math.round(Y)]})})}
  const setInk=(st)=>{S.ink['T__x']={s:st.map(s=>s.flat().join(',')),t:1}};
  const levels={neat:{rot:6,s0:.6,s1:.9,shift:3,cut:0,len:.08,noise:.8},messy:{rot:14,s0:.45,s1:.95,shift:7,cut:.12,len:.2,noise:1.6},verymessy:{rot:20,s0:.4,s1:1,shift:11,cut:.2,len:.3,noise:2.2}};
  const out={};
  for(const [name,lv] of Object.entries(levels)){let ok=0,note=0,ng=0,fails=[];for(const c of G1){const d=await dense(c);for(let k=0;k<5;k++){setInk(perturb(d,lv));const r=await judgeKanji('T__x',c);if(r==='ok')ok++;else if(r==='note')note++;else{ng++;if(fails.length<12)fails.push(c)}}}out[name]={ok,note,ng,fails:fails.join('')}}
  // wrong kanji with the same stroke count
  let pass=[],tot=0;for(const a of G1){const da=await dense(a);for(const b2 of G1){if(a===b2||refs[a].length!==refs[b2].length)continue;tot++;setInk(perturb(da,levels.neat));const r=await judgeKanji('T__x',b2);if(r!=='ng')pass.push(a+'→'+b2+(r==='note'?'*':''))}}
  out.cross={tot,passed:pass.length,list:pass.join(' ')};
  // reversed stroke order & missing stroke
  let rv={ok:0,note:0,ng:0};for(const c of G1){const d=await dense(c);if(d.length<2)continue;setInk(perturb(d.slice().reverse(),levels.neat));rv[await judgeKanji('T__x',c)]++}out.reversedOrder=rv;
  let ms=0,mt=0;for(const c of G1){const d=await dense(c);if(d.length<3)continue;mt++;setInk(perturb(d.slice(0,-1),levels.neat));const r=await judgeKanji('T__x',c);if(r===null)ms++}out.missingStroke_notJudgedYet=ms+'/'+mt;
  return out});
console.log(JSON.stringify(res,null,1),errs);await b.close();srv.close()})();
