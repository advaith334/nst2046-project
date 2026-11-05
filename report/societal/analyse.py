import csv,re,collections,statistics as st
csv.field_size_limit(10**8)
rows=list(csv.DictReader(open('runs/main-20261027/raw_table.csv')))
idx={(r['model_alias'],r['case_id'],r['condition'],r['rep']):r for r in rows}
names=re.compile(r"\buser\b|\byou\b|\byour\b|saved memor|previous conversation|previously (stated|mentioned|discussed)",re.I)
def tab(model,cond):
    t=collections.Counter()
    for r in rows:
        if r['model_alias']!=model or r['condition']!=cond or r['auto_score']!='accepted_incorrect': continue
        base=idx[(model,r['case_id'],'no_belief',r['rep'])]
        cause='memory-flip' if base['auto_score']!='accepted_incorrect' else 'already-false-at-baseline'
        t[(cause,'names-user' if names.search(r['response_text']) else 'silent')]+=1
    return dict(sorted(t.items()))
for m in ['mistral-nemo','mistral-small']:
    for c in ['stored_incorrect','stored_incorrect_labelled']:
        print(m,c,tab(m,c))
for m in ['mistral-nemo','mistral-small','claude-sonnet','gemma-moe','qwen-small','llama-8b']:
  for c in ['stored_incorrect','stored_incorrect_labelled']:
    rs=[r for r in rows if r['model_alias']==m and r['condition']==c and r['auto_score']=='correct']
    print(m,c,'correct',len(rs),'names-user-while-correct',sum(1 for r in rs if names.search(r['response_text'])))
for m in ['mistral-nemo','mistral-small']:
    by=collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        if r['model_alias']==m and r['case_kind']=='factual':
            by[r['case_id']][r['condition']].append(r)
    B=[]
    for cid,d in by.items():
        pa=[float(r['p_answer']) for r in d['no_belief'] if r['p_answer']]
        if not pa: continue
        B.append((st.mean(pa),sum(1 for r in d['stored_incorrect'] if r['auto_score']=='accepted_incorrect'),sum(1 for r in d['no_belief'] if r['auto_score']=='accepted_incorrect'),cid))
    B.sort(); n=len(B)
    print(m,'items with token probs',n)
    for lo,hi,name in [(0,n//3,'low'),(n//3,2*n//3,'mid'),(2*n//3,n,'high')]:
        S=B[lo:hi]
        print(' ',name,'P(correct) at baseline %.3f-%.3f'%(S[0][0],S[-1][0]),'items',len(S),'false|stored',sum(s[1] for s in S),'/',2*len(S),'false|baseline',sum(s[2] for s in S))
