import pandas as pd, numpy as np, json, yaml, collections
r='runs/main-20261027/'
raw=pd.read_csv(r+'raw_table.csv'); s=pd.read_csv(r+'summary.csv'); p=pd.read_csv(r+'paired.csv')
piv=s[s.condition.isin(['no_belief','stored_incorrect','stated_incorrect','stored_incorrect_labelled','stored_unrelated','stored_correct'])].pivot(index='model',columns='condition',values='incorrect_rate')[['no_belief','stored_incorrect','stated_incorrect','stored_incorrect_labelled','stored_unrelated','stored_correct']]
print((piv*100).round(1)); print(s.pivot(index='model',columns='condition',values='usable'))
print(s.pivot(index='model',columns='condition',values='unparseable').fillna(0).astype(int))
print(p[['model','comparison','pairs','toward_incorrect','away','mcnemar_p']].to_string())
print('n comparisons',len(p),'bonf',0.05/len(p))
print('bonf survivors'); print(p[p.mcnemar_p<0.05/len(p)][['model','comparison','toward_incorrect','away','mcnemar_p']].to_string())
print('nominal<.05 not bonf'); print(p[(p.mcnemar_p<0.05)&(p.mcnemar_p>=0.05/len(p))][['model','comparison','toward_incorrect','away','mcnemar_p']].to_string())
f=raw[raw.case_kind=='factual']
for m in ['mistral-nemo','mistral-small']:
    g=f[f.model_alias==m].assign(inc=lambda d:d.auto_score=='accepted_incorrect')
    a=g[g.condition=='no_belief'].groupby('case_id').inc.sum(); b=g[g.condition=='stored_incorrect'].groupby('case_id').inc.sum()
    print(m,'items raised',int((b>a).sum()),'lowered',int((b<a).sum()),'same',int((b==a).sum()))
print('other_wrong per model all conds:',raw[raw.auto_score=='other_wrong'].groupby('model_alias').size().to_dict())
print('other_wrong factual only:',f[f.auto_score=='other_wrong'].groupby('model_alias').size().to_dict())
print('unparseable:',raw[raw.auto_score=='unparseable'].groupby(['model_alias','condition']).size().to_dict())
u=raw[raw.case_kind!='factual']; print('useful', u.groupby(['model_alias','condition']).auto_score.value_counts().unstack(fill_value=0)); print(u.groupby(['case_id']).size())
pc=raw[raw.p_incorrect.notna()].groupby('model_alias').size()/raw.groupby('model_alias').size(); print('logprob cov',pc.fillna(0).round(3).to_dict())
pf=f[f.p_incorrect.notna()].groupby('model_alias').size()/f.groupby('model_alias').size(); print('logprob cov factual',pf.fillna(0).round(3).to_dict())
d=yaml.safe_load(open('data/cases/longtail.yaml')); items=d if isinstance(d,list) else d.get('cases',d)
print(len(items)); c=collections.Counter(i['category'] for i in items); print(c)
print('affirms',collections.Counter(i.get('belief_affirms_false') for i in items)); print('sources',sum(1 for i in items if i.get('sources')),'status',collections.Counter(i.get('status','draft') for i in items),'verified_by',sum(1 for i in items if i.get('verified_by')))
print('evidence nonempty',sum(1 for i in items if i.get('evidence')))
print('no source:',[i['id'] for i in items if not i.get('sources')])
for run in ['pilot-20261027','calibration-20261027','calsmall-20261027','longtail-20261027']:
    x=pd.read_csv(f'runs/{run}/summary.csv'); print(run); print(x[x.condition.isin(['no_belief','stored_incorrect','stated_incorrect','stored_incorrect_labelled'])][['model','evidence_mode','condition','usable','correct_rate','incorrect_rate']].round(3).to_string())
    y=pd.read_csv(f'runs/{run}/raw_table.csv'); print(' wrong any (1-correct) per model',(1-(y[y.case_kind=='factual'].auto_score=='correct').groupby(y.model_alias).mean()).round(3).to_dict(), 'useful ok', y[y.case_kind!='factual'].groupby('model_alias').auto_score.apply(lambda s:(s=='correct').mean()).to_dict())
lp=pd.read_csv('runs/longtail-20261027/paired.csv'); print(lp.to_string())
