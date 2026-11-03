export async function loadRepository(base="../../"){
 const paths={meta:"data/meta.json",actors:"data/actors.json",claims:"data/claims.json",evidence:"data/evidence.json",relations:"data/relations.json",sources:"data/sources.json",taxonomy:"config/taxonomy.json"};
 const d=Object.fromEntries(await Promise.all(Object.entries(paths).map(async([name,path])=>[name,await fetch(base+path).then(r=>{if(!r.ok)throw new Error(path+' HTTP '+r.status);return r.json();})])));
 d.actorById=new Map(d.actors.map(a=>[a.id,a]));d.claimsByActor=new Map();d.claims.forEach(x=>{if(!d.claimsByActor.has(x.subject_id))d.claimsByActor.set(x.subject_id,[]);d.claimsByActor.get(x.subject_id).push(x)});
 d.evidenceById=new Map(d.evidence.map(e=>[e.id,e]));d.sourceById=new Map(d.sources.map(s=>[s.id,s]));return d;
}
export const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
export const norm=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
export const actorClaim=(d,id)=>(d.claimsByActor.get(id)||[]).find(x=>x.claim_type==='position');
export function evidenceHtml(d,ids=[]){if(!ids?.length)return '<p class="muted">Aucune preuve structurée.</p>';return [...new Set(ids)].map(id=>{const e=d.evidenceById.get(id);if(!e)return '';const src=d.sourceById.get(e.source_id);const link=src?.url?`<a target="_blank" rel="noopener noreferrer" href="${esc(src.url)}">${esc(src.title||src.publisher)}</a>${src.status==='aggregator_only'?' (agrégateur : URL éditeur non qualifiée)':''}`:'Source non qualifiée';return `<article class="proof"><div>${esc(e.text)}</div><small>${link}${e.location?` · ${esc(e.location)}`:''}</small></article>`}).join('');}
