import json,collections
R='/Users/advaithkarthikeyan/dev/nst2046-project/runs/main-20261027/trials.jsonl'
last={}
for l in open(R):
    r=json.loads(l); last[r['trial_id']]=r
for r in last.values():
    if r.get('finish_reason') in('error',) or (r.get('finish_reason')=='length' and r['model_alias']=='llama-8b'):
        print(r['trial_id'],r['finish_reason'],r['auto_score'],repr((r.get('response_text') or '')[:120]),len(r.get('reasoning_text') or ''))
c=collections.Counter()
rt=collections.defaultdict(list); ctok=collections.defaultdict(list)
for r in last.values():
    if r.get('reasoning_text'): c[r['model_alias']]+=1
    u=r.get('usage') or {}
    ctok[r['model_alias']].append(u.get('completion_tokens') or 0)
print('with reasoning text',c)
import statistics as st
print({k:(round(st.mean(v)),max(v)) for k,v in ctok.items()})
# correct rate Nemo by cond
import pandas as pd
raw=pd.read_csv('/Users/advaithkarthikeyan/dev/nst2046-project/runs/main-20261027/raw_table.csv')
f=raw[raw.case_kind=='factual']
t=f.groupby(['model_alias','condition']).auto_score.value_counts().unstack(fill_value=0)
print(t.to_string())
# Held-out: Nemo/Mistral small on 24 new items
m=json.load(open('/Users/advaithkarthikeyan/dev/nst2046-project/runs/main-20261027/manifest.json'))
lt=json.load(open('/Users/advaithkarthikeyan/dev/nst2046-project/runs/longtail-20261027/manifest.json'))
old=set(lt['cases']); print('24 reused all in main?',old<=set(m['cases']))
import math
def mc(b,c):
    n=b+c
    return 1.0 if n==0 else min(1,2*sum(math.comb(n,i) for i in range(min(b,c)+1))/2**n)
for model in ['mistral-nemo','mistral-small']:
  for name,sel in [('24 screened',f.case_id.isin(old)),('24 new',~f.case_id.isin(old))]:
    g=f[(f.model_alias==model)&sel]
    a=g[g.condition=='no_belief'].set_index(['case_id','rep']).auto_score=='accepted_incorrect'
    b=g[g.condition=='stored_incorrect'].set_index(['case_id','rep']).auto_score=='accepted_incorrect'
    j=pd.concat([a,b],axis=1,keys=['a','b']); t_=(~j.a&j.b).sum(); w=(j.a&~j.b).sum()
    print(model,name,'base',round(a.mean(),3),'stored',round(b.mean(),3),'toward',t_,'away',w,'p',mc(int(t_),int(w)))
# longtail vs main on same 24 for Nemo: stability
lr=pd.read_csv('/Users/advaithkarthikeyan/dev/nst2046-project/runs/longtail-20261027/raw_table.csv')
g=lr[lr.model_alias=='mistral-nemo']; print('longtail nemo',g.groupby('condition').auto_score.apply(lambda s:(s=='accepted_incorrect').mean()).to_dict())
# same config? compare rep-level agreement between longtail and main for nemo same item,cond,rep
gm=f[(f.model_alias=='mistral-nemo')&f.case_id.isin(old)&f.condition.isin(['no_belief','stored_incorrect'])]
mm=gm.merge(g,on=['case_id','condition','rep'],suffixes=('_m','_l'))
print('same-trial agreement longtail vs main (nemo):',round((mm.selected_m==mm.selected_l).mean(),3),len(mm))
for mod in ['llama-8b','gemma-moe','qwen-small','claude-sonnet']:
    a=f[(f.model_alias==mod)&f.case_id.isin(old)&f.condition.isin(['no_belief','stored_incorrect'])]; b=lr[lr.model_alias==mod]
    x=a.merge(b,on=['case_id','condition','rep'],suffixes=('_m','_l')); print(mod,round((x.selected_m==x.selected_l).mean(),3))
