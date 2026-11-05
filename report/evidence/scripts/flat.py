import json,re
T="/Users/advaithkarthikeyan/.claude/projects/-Users-advaithkarthikeyan-dev-nst2046-project/98985bb9-4618-4e6d-8e36-81eadc66d0da.jsonl"
red=re.compile(r'sk-[A-Za-z0-9_\-]{16,}|Bearer\s+[A-Za-z0-9._\-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|OPENROUTER_API_KEY=\S+')
def R(s): return red.sub('[REDACTED]',s)
hits=0
out=open('flat.txt','w');users=open('users.txt','w')
for n,l in enumerate(open(T)):
    d=json.loads(l)
    t=d.get('type')
    if t not in('user','assistant'): continue
    ts=d.get('timestamp','')
    m=d.get('message',{})
    c=m.get('content')
    if isinstance(c,str): c=[{'type':'text','text':c}]
    for b in c or []:
        if not isinstance(b,dict): continue
        k=b.get('type')
        if k=='text':
            s=b['text']
            hits+=len(red.findall(s))
            hdr=f"\n### L{n} {ts} {t.upper()} TEXT\n"
            out.write(hdr+R(s)+"\n")
            if t=='user' and not d.get('isMeta'):
                users.write(hdr+R(s)+"\n")
        elif k=='tool_use':
            s=json.dumps(b.get('input'))
            hits+=len(red.findall(s))
            out.write(f"\n### L{n} {ts} TOOL_USE {b.get('name')}\n"+R(s)[:1500]+"\n")
        elif k=='tool_result':
            cc=b.get('content')
            if isinstance(cc,list):
                cc=' '.join(x.get('text','') for x in cc if isinstance(x,dict))
            s=str(cc)
            hits+=len(red.findall(s))
            out.write(f"\n### L{n} {ts} TOOL_RESULT\n"+R(s)[:2500]+"\n")
print('secret-like matches redacted',hits)
