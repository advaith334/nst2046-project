import json
real={'pilot-20261027':'dry-pilot','calibration-20261027':'dry-calibration','calsmall-20261027':'dry-calibration_small','longtail-20261027':'dry-longtail','main-20261027':'audit-dry'}
R='/Users/advaithkarthikeyan/dev/nst2046-project/runs/'
def load(p):
    d={}
    for l in open(p):
        r=json.loads(l); d[r['trial_id']]=r
    return d
for a,b in real.items():
    x=load(R+a+'/trials.jsonl'); y=load('dryruns/'+b+'/trials.jsonl')
    same=diffm=diffo=diffr=0; ex=None
    for k in x:
        if k not in y: diffr+=1; continue
        if x[k]['request']==y[k]['request']: same+=1
        else:
            diffm+=1
            if not ex:
                ex=(k,[kk for kk in x[k]['request'] if x[k]['request'].get(kk)!=y[k]['request'].get(kk)])
        if x[k]['option_map']!=y[k]['option_map']: diffo+=1
    print(a,'trials',len(x),'dry',len(y),'identical requests',same,'different',diffm,'missing',diffr,'option_map diffs',diffo,ex)
