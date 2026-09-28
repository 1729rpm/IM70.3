"""Steady-state block detection: find stretches of near-constant power (or speed) and report
how HR behaved inside them. HR slope near zero = steady state; a sustained positive slope at
constant output = above the sustainable ceiling (or heat/dehydration drift)."""
import numpy as np, pandas as pd

def steady_blocks(df, col='pw', min_len=360, tol=0.10, smooth=30):
    s=df.dropna(subset=['t']).drop_duplicates('t').set_index('t')[[col,'hr']].astype(float).resample('1s').mean().interpolate(limit=10)
    p=s[col].rolling(smooth,center=True,min_periods=5).mean()
    blocks=[]; i=0; n=len(p); vals=p.values
    while i<n-min_len:
        if np.isnan(vals[i]) or vals[i]<=0: i+=1; continue
        ref=np.nanmedian(vals[i:i+60]); j=i+60
        if ref<=0 or np.isnan(ref): i+=30; continue
        while j<n and not np.isnan(vals[j]) and abs(vals[j]-ref)/ref<=tol:
            j+=1
            if (j-i)%60==0: ref=np.nanmedian(vals[i:j])
        if j-i>=min_len: blocks.append((i,j)); i=j
        else: i+=15
    out=[]
    for (i,j) in blocks:
        seg=s.iloc[i:j]; dur=(j-i)/60; hr=seg.hr; t=np.arange(len(hr))/60.0
        k=int(len(hr)*0.4)  # skip HR kinetics at block start
        m=~np.isnan(hr.values[k:])
        slope=np.polyfit(t[k:][m],hr.values[k:][m],1)[0] if m.sum()>60 else np.nan
        out.append(dict(start=seg.index[0].strftime('%Y-%m-%d %H:%M'),dur_min=round(dur,1),val=round(seg[col].mean(),1),
                        hr_3min=round(hr.iloc[150:210].mean()) if len(hr)>210 else None,
                        hr_mid=round(hr.iloc[len(hr)//2-30:len(hr)//2+30].mean()),hr_last=round(hr.iloc[-60:].mean()),
                        hr_max=round(hr.max()),slope_bpm_per_min=round(slope,2)))
    return pd.DataFrame(out)

def decoupling(df, moving_speed=1.2, skip_start_min=10, skip_end_min=2, col='v'):
    """Efficiency loss (%) first half vs second half of moving time. col='v' for runs, 'pw' for rides."""
    cols=list(dict.fromkeys([col,'hr','v']))
    s=df.dropna(subset=['t']).drop_duplicates('t').set_index('t')[cols].astype(float).resample('1s').mean().interpolate(limit=5)
    s=s[s.v>moving_speed] if col=='v' else s[s[col]>0]
    s=s.iloc[skip_start_min*60: len(s)-skip_end_min*60]
    if len(s)<1200: return np.nan
    h=len(s)//2; a,b=s.iloc[:h],s.iloc[h:]
    ef_a=a[col].mean()/a.hr.mean(); ef_b=b[col].mean()/b.hr.mean()
    return round((ef_a/ef_b-1)*100,1)
