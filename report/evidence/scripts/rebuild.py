import sys,json,shutil,math
from pathlib import Path
import pandas as pd, numpy as np
from memsyco import report as R, screen as Sc
from memsyco.config import load_config, load_cases
from memsyco.conditions import option_map
from memsyco.parse import selected_letter, auto_score
clone=Path('.')
RUNS={'pilot-20261027':'pilot','calibration-20261027':'calibration','calsmall-20261027':'calibration_small','longtail-20261027':'longtail','main-20261027':'main'}
def cmp(a,b,keys):
    a=a.sort_values(keys).reset_index(drop=True); b=b.sort_values(keys).reset_index(drop=True)
    if a.shape!=b.shape: return f'SHAPE {a.shape} vs {b.shape}'
    bad=[]
    for c in a.columns:
        if c not in b.columns: bad.append('nocol '+c); continue
        if pd.api.types.is_numeric_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c]):
            if not np.allclose(a[c].astype(float),b[c].astype(float),equal_nan=True,atol=1e-9): bad.append(c)
        elif not (a[c].astype(str)==b[c].astype(str)).all(): bad.append(c)
    return 'MATCH' if not bad else 'DIFF '+','.join(bad)
for run,cfgname in RUNS.items():
    d=clone/'runs'/run
    cfg=load_config(clone/f'config/{cfgname}.yaml')
    cases={c.id:c for c in load_cases(cfg.case_files+cfg.useful_memory_files)}
    raw=pd.read_csv(d/'raw_table.csv',keep_default_na=True)
    # A: reparse from committed csv using seed-derived option maps
    mism_letter=mism_sel=mism_score=0; n=0; errs=(raw.auto_score=='error').sum()
    for r in raw.itertuples():
        if r.auto_score=='error': continue
        case=cases[r.case_id]
        omap=option_map(case,f'{cfg.seed}:{case.id}:r{r.rep}')
        txt=r.response_text if isinstance(r.response_text,str) else ''
        L=selected_letter(txt,list(omap),False); sel=omap.get(L) if L else None
        n+=1
        exp_L=None if pd.isna(r.selected_display) else r.selected_display
        exp_s=None if pd.isna(r.selected) else r.selected
        mism_letter+=(L!=exp_L); mism_sel+=(sel!=exp_s); mism_score+=(auto_score(case,sel)!=r.auto_score)
    s_new=R.summarise(raw); p_new=R.paired(raw)
    s_old=pd.read_csv(d/'summary.csv')
    print(f'--- {run}: rows={len(raw)} errors={errs} reparse n={n} letter_mism={mism_letter} selected_mism={mism_sel} score_mism={mism_score}')
    print('  summary.csv from raw_table:',cmp(s_new,s_old,['model','evidence_mode','condition']))
    if (d/'paired.csv').exists():
        print('  paired.csv from raw_table:',cmp(p_new,pd.read_csv(d/'paired.csv'),['model','comparison']))
    else: print('  paired.csv not committed; recomputed rows',len(p_new))
    if (d/'screen.csv').exists():
        sc=Sc.screen(raw); print('  screen.csv from raw_table:',cmp(sc,pd.read_csv(d/'screen.csv'),['case_id','evidence_mode','model']))
