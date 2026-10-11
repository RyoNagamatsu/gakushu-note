/* Offline support. Network first for the app and weekly files (so an update is never held back), saved copy when there is no connection.
   Stroke-order data and web fonts do not change, so they are served from the saved copy. Requests to api.github.com and api.anthropic.com are not touched. */
const C='gk-offline-1';
const CORE=['./','manifest.webmanifest','icon-180.png','icon-512.png','weeks/index.json'];
const KV='30 4e 4f 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f 80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f'.split(' ');
const key=u=>{const x=new URL(u);x.search='';x.hash='';return x.href};
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(CORE.map(p=>fetch(p,{cache:'reload'}).then(r=>{if(r.ok)return c.put(key(new URL(p,self.registration.scope).href),r)}).catch(()=>{})))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k!==C&&k.startsWith('gk-offline-'))await caches.delete(k);await self.clients.claim();
  const c=await caches.open(C);for(const k of KV){const u=new URL('kv/'+k+'.json',self.registration.scope).href;try{if(!(await c.match(u))){const r=await fetch(u);if(r.ok)await c.put(u,r)}}catch(err){break}}})())});
async function cacheFirst(req,k){const c=await caches.open(C);const hit=await c.match(k);if(hit)return hit;const r=await fetch(req);if(r.ok||r.type==='opaque')c.put(k,r.clone()).catch(()=>{});return r}
async function staleWhileRevalidate(req,k){const c=await caches.open(C);const hit=await c.match(k);const net=fetch(req).then(r=>{if(r.ok||r.type==='opaque')c.put(k,r.clone()).catch(()=>{});return r});if(hit){net.catch(()=>{});return hit}return net}
async function networkFirst(req,k,nav){const c=await caches.open(C);
  const saved=async()=>(await c.match(k))||(nav?await c.match(key(new URL('./',req.url).href)):undefined);
  const net=fetch(req).then(r=>{if(r.ok)c.put(k,r.clone()).catch(()=>{});return r});
  const slow=new Promise(res=>setTimeout(async()=>res(await saved()),4000));
  try{const r=await Promise.race([net,slow.then(x=>x||net)]);return r}catch(err){const hit=await saved();if(hit)return hit;throw err}}
self.addEventListener('fetch',e=>{const req=e.request;if(req.method!=='GET')return;const u=new URL(req.url);
  if(u.hostname==='fonts.gstatic.com'){e.respondWith(cacheFirst(req,req.url));return}
  if(u.hostname==='fonts.googleapis.com'){e.respondWith(staleWhileRevalidate(req,req.url));return}
  if(u.origin!==location.origin||!u.href.startsWith(self.registration.scope))return;
  if(/\/version\.json$/.test(u.pathname))return;
  if(/\/kv\/[0-9a-f]+\.json$/.test(u.pathname)){e.respondWith(cacheFirst(req,key(req.url)));return}
  e.respondWith(networkFirst(req,key(req.url),req.mode==='navigate'))});
