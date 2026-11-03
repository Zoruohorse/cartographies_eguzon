#!/usr/bin/env python3
"""Cohérence statique du référentiel Éguzon–Marmagne (stdlib uniquement)."""
import json, re, sys
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
a,c,e,r,s,m,t=(load(x) for x in ['data/actors.json','data/claims.json','data/evidence.json','data/relations.json','data/sources.json','data/meta.json','config/taxonomy.json'])
errors=[];warnings=[]
def unique(items,label):
 ids=[v.get('id') for v in items]
 if len(ids)!=len(set(ids)):errors.append(f'Identifiants {label} dupliqués')
unique(a,'acteurs');unique(c,'positions');unique(e,'preuves');unique(r,'relations');unique(s,'sources')
A={x['id'] for x in a};E={x['id'] for x in e};S={x['id'] for x in s};T=set(t['relation_types']);K=set(t['categories']);ST=set(t['stances']);CERT=set(t['certainty_levels'])
if m['id'] not in A:errors.append('Projet central absent')
for x in a:
 if not x.get('categories') or any(z not in K for z in x['categories']): errors.append(f'Catégorie acteur {x["id"]}')
 if not set(x.get('evidence_ids',[]))<=E:errors.append(f'Preuves acteur {x["id"]}')
for x in c:
 if x['subject_id'] not in A or x.get('project_id')!=m['id']:errors.append(f'Position {x["id"]} : sujet/projet absent')
 if x['value'] not in ST or x['value']=='all' or x['certainty'] not in CERT:errors.append(f'Taxonomie position {x["id"]}')
 if not set(x.get('evidence_ids',[]))<=E:errors.append(f'Preuve manquante position {x["id"]}')
 if not x.get('evidence_ids'):errors.append(f'Position sans preuve {x["id"]}')
for x in r:
 if x['source_id'] not in A or x['target_id'] not in A:errors.append(f'Entité manquante relation {x["id"]}')
 if x['type'] not in T or x['certainty'] not in CERT:errors.append(f'Taxonomie relation {x["id"]}')
 if not set(x.get('evidence_ids',[]))<=E:errors.append(f'Preuve manquante relation {x["id"]}')
 if not x.get('evidence_ids'):errors.append(f'Relation sans preuve {x["id"]}')
for x in e:
 if x['source_id'] not in S: errors.append(f'Source manquante preuve {x["id"]}')
 if not x.get('location') or not x.get('text'):errors.append(f'Preuve incomplète {x["id"]}')
for x in s:
 if not re.fullmatch(r'https://[^\s]+',x.get('url','')):errors.append(f'URL invalide {x["id"]}')
 if x.get('status')=='aggregator_only':warnings.append(f'URL agrégateur à qualifier: {x["id"]}')
for x in m.get('griefs',[]):
 if not set(x.get('evidence_ids',[]))<=E:errors.append(f'Grief référence cassée: {x.get("title")}')
if len(m.get('vigilance',[]))!=len(m.get('vigilance_evidence_ids',[])):errors.append('Désalignement des vigilances et preuves')
for ids in m.get('vigilance_evidence_ids',[]):
 if not set(ids)<=E:errors.append('Preuve manquante vigilance')
audit=load('audit/corpus-review.json')
if len(audit)!=37 or len({x['xlsx_row'] for x in audit})!=37:errors.append('Inventaire Excel incomplet')
refs={i for x in a for i in x.get('evidence_ids',[])}|{i for x in c for i in x.get('evidence_ids',[])}|{i for x in r for i in x.get('evidence_ids',[])}|{i for g in m['griefs'] for i in g.get('evidence_ids',[])}|{i for ids in m.get('vigilance_evidence_ids',[]) for i in ids}
orphans=E-refs
if orphans:errors.append('Preuves orphelines: '+', '.join(sorted(orphans)))
result={'status':'PASS' if not errors else 'FAIL','counts':{'actors':len(a),'claims':len(c),'evidence':len(e),'relations':len(r),'sources':len(s),'griefs':len(m['griefs']),'vigilance':len(m['vigilance']),'resources_examined':len(audit)},'sources_aggregator_only':len([z for z in s if z.get('status')=='aggregator_only']),'positions_unqualified':len([x for x in a if x['id']!=m['id'] and x['categories'][0] not in ('context','griefs','sources') and not any(y['subject_id']==x['id'] for y in c)]),'errors':errors,'warnings':warnings}
(root/'audit'/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
