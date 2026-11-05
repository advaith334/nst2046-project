import json,re,collections,yaml
_A=re.compile(r"(?i:\banswer\s*(?:is)?\s*[:\-]?)\s*\**\s*\(?([A-H])\)?(?![A-Za-z])")
R='/Users/advaithkarthikeyan/dev/nst2046-project/'
items={}
for f in ['longtail','useful_memory']:
    d=yaml.safe_load(open(R+f'data/cases/{f}.yaml')); L=d if isinstance(d,list) else d.get('cases')
    for i in L: items[i['id']]=i
last={}
for l in open(R+'runs/main-20261027/trials.jsonl'):
    r=json.loads(l); last[r['trial_id']]=r
t=collections.defaultdict(lambda:[0,0,0,0])
ex=[]
for r in last.values():
    if r['case_kind']!='factual' or r['auto_score'] in('error','unparseable'): continue
    txt=r.get('response_text') or ''
    v=[m.group(1) for m in _A.finditer(txt) if m.group(1) in r['option_map']]
    if not v: continue
    first=r['option_map'][v[0]]; lastv=r['option_map'][v[-1]]
    inc=items[r['case_id']]['incorrect_option']
    k=(r['model_alias'],r['condition'])
    t[k][0]+=1; t[k][1]+=first==inc; t[k][2]+=lastv==inc; t[k][3]+=first!=lastv
    if first!=lastv and first==inc: ex.append((r['trial_id'],txt[:60].replace('\n',' | '),'...',txt[-130:].replace('\n',' | ')))
for k in sorted(t):
    a=t[k]
    if a[1]!=a[2] or a[3]: print(k,'n',a[0],'first-answer false',a[1],'last-answer false',a[2],'changed',a[3])
print(len(ex)); 
for e in ex: print(e)
# parsing path used: how many had no Answer match (fallback leading)
c=collections.Counter()
for r in last.values():
    txt=r.get('response_text') or ''
    v=[m.group(1) for m in _A.finditer(txt) if m.group(1) in r['option_map']]
    c[(r['model_alias'],len(v)>0)]+=1
print({k:v for k,v in c.items() if not k[1]})
