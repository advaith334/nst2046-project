import json,collections,glob,os
R='/Users/advaithkarthikeyan/dev/nst2046-project/runs/'
tot=0
for run in ['smoke','smoke-pinned','smoke-pinned2','pilot-20261027','calibration-20261027','longtail-20261027','calsmall-20261027','main-20261027']:
    rows=[json.loads(l) for l in open(R+run+'/trials.jsonl')]
    cost=sum(float((r.get('usage') or {}).get('cost') or 0) for r in rows)
    tot+=cost
    errs=[r for r in rows if r['auto_score']=='error']
    uniq={r['trial_id'] for r in rows}
    st=[r['started_at'] for r in rows if r.get('started_at')]
    prov=collections.defaultdict(collections.Counter); mr=collections.defaultdict(collections.Counter)
    last={}
    for r in rows: last[r['trial_id']]=r
    for r in last.values():
        prov[r['model_alias']][r.get('provider')]+=1; mr[r['model_alias']][r.get('model_returned')]+=1
    print(f"\n=== {run}: logged rows={len(rows)} unique={len(uniq)} error rows={len(errs)} cost=${cost:.4f} first={min(st)} last={max(st)}")
    ec=collections.Counter(((e.get('error') or '')[:45],e['model_alias']) for e in errs)
    for k,v in ec.most_common(12): print('   err',v,k)
    per=collections.defaultdict(float)
    for r in rows: per[r['model_alias']]+=float((r.get('usage') or {}).get('cost') or 0)
    for m in sorted(prov):
        print(f"   {m}: cost ${per[m]:.4f} hosts={dict(prov[m])} returned={dict(mr[m])}")
    fin=collections.Counter((r['model_alias'],r.get('finish_reason')) for r in last.values())
    print('   finish',{k:v for k,v in fin.items() if k[1]!='stop'})
    sc=collections.Counter((r['model_alias'],r['auto_score']) for r in last.values() if r['auto_score'] in('unparseable','error'))
    print('   unparse/err (final)',dict(sc))
    p=collections.Counter(json.dumps(r.get('params'),sort_keys=True) for r in rows); print('   params',dict(p))
    tk=collections.Counter((r['model_alias'],(r.get('request') or {}).get('max_tokens'),(r.get('request') or {}).get('temperature'),json.dumps((r.get('request') or {}).get('provider'),sort_keys=True)) for r in rows); print('   req',dict(tk))
print('TOTAL',tot)
