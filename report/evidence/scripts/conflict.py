import json,re,sys
sys.path.insert(0,'clone/src')
_A=re.compile(r"(?i:\banswer\s*(?:is)?\s*[:\-]?)\s*\**\s*\(?([A-H])\)?(?![A-Za-z])")
R='/Users/advaithkarthikeyan/dev/nst2046-project/runs/'
for run in ['pilot-20261027','calibration-20261027','calsmall-20261027','longtail-20261027','main-20261027']:
    last={}
    for l in open(R+run+'/trials.jsonl'):
        r=json.loads(l); last[r['trial_id']]=r
    c=[]
    for r in last.values():
        t=r.get('response_text') or ''
        vals=[m.group(1) for m in _A.finditer(t) if m.group(1) in r['option_map']]
        if len(set(vals))>1: c.append((r['trial_id'],vals,r['auto_score']))
    print(run,len(last),'conflicting-letter responses',len(c)); 
    for x in c[:12]: print('   ',x)
