"""FIT file loader used across the IM70.3 repo.

load(path) -> (records_df, laps_df, session_dict, device_info_list, user_profile_dict, time_in_zone_list, events_list)
load_legs(path) -> ([(records_df, laps_df, session_dict) per session], device_info_list, user_profile_dict, time_in_zone_list, events_list)
  A multisport race file has one session per leg (swim, transition, bike, transition, run); load() returns only the last.
Timestamps in records_df['t'] are converted to IST. Accepts .fit or .fit.gz / .FIT.gz.
pace(v) formats a speed in m/s as min:sec per km.
"""
import gzip, io, datetime as dt
import fitdecode, pandas as pd, numpy as np

IST = dt.timedelta(hours=5, minutes=30)

def _open(path):
    if str(path).lower().endswith('.gz'):
        return io.BytesIO(gzip.open(path, 'rb').read())
    return path

def load(path):
    recs=[]; laps=[]; sess=None; dev=[]; zones=[]; user=None; events=[]; sessions=[]
    with fitdecode.FitReader(_open(path), check_crc=fitdecode.CrcCheck.DISABLED) as fr:
        for m in fr:
            if not isinstance(m, fitdecode.FitDataMessage): continue
            g=lambda k: m.get_value(k, fallback=None)
            if m.name=='record':
                recs.append(dict(t=g('timestamp'), d=g('distance'), hr=g('heart_rate'), cad=g('cadence'), fcad=g('fractional_cadence'),
                                 v=g('enhanced_speed') if g('enhanced_speed') is not None else g('speed'), alt=g('enhanced_altitude'),
                                 temp=g('temperature'), pw=g('power'), lat=g('position_lat'),
                                 gct=g('stance_time'), vo=g('vertical_oscillation'), vr=g('vertical_ratio'), sl=g('step_length')))
            elif m.name=='lap':
                laps.append(dict(start=g('start_time'), dist=g('total_distance'), timer=g('total_timer_time'), hr=g('avg_heart_rate'),
                                 mhr=g('max_heart_rate'), cad=g('avg_running_cadence'), trig=g('lap_trigger'), intensity=g('intensity'),
                                 v=g('enhanced_avg_speed') or g('avg_speed'), wkt_step=g('wkt_step_index')))
            elif m.name=='session':
                sess={fd.name: fd.value for fd in m.fields}; sessions.append(sess)
            elif m.name=='device_info': dev.append({fd.name: fd.value for fd in m.fields})
            elif m.name=='user_profile': user={fd.name: fd.value for fd in m.fields}
            elif m.name=='time_in_zone': zones.append({fd.name: fd.value for fd in m.fields})
            elif m.name=='event': events.append({fd.name: fd.value for fd in m.fields})
    df=pd.DataFrame(recs)
    if len(df):
        df['t']=pd.to_datetime(df['t']).dt.tz_localize(None)+IST
    lp=pd.DataFrame(laps)
    if len(lp): lp['start']=pd.to_datetime(lp['start']).dt.tz_localize(None)+IST
    load.last_sessions=sessions   # all session messages; multisport files (a race) have one per leg plus transitions
    return df, lp, sess, dev, user, zones, events

def load_legs(path):
    """Multisport support. Returns a list of (records_df, laps_df, session_dict) with one entry per session
    message, records and laps sliced to that session's time window. Single-sport files give a one-item list."""
    df, lp, sess, dev, user, zones, events = load(path)
    out=[]
    for s in load.last_sessions:
        st=pd.to_datetime(s['start_time']).tz_localize(None)+IST
        en=st+pd.Timedelta(seconds=float(s.get('total_elapsed_time') or 0))
        d=df[(df.t>=st)&(df.t<=en)] if len(df) else df
        l=lp[(lp.start>=st)&(lp.start<en)] if len(lp) else lp
        out.append((d,l,s))
    return out, dev, user, zones, events

def hr_source(dev):
    """'strap' if a heart-rate sensor device is listed, else 'wrist'."""
    for d in dev:
        for k in ('device_type','antplus_device_type','local_device_type'):
            if d.get(k) is not None and 'heart_rate' in str(d.get(k)): return 'strap'
    return 'wrist'

def pace(v):
    if v is None or (isinstance(v,float) and np.isnan(v)) or not v or v<=0: return '--'
    p=1000/v/60; m=int(p); s=int(round((p-m)*60))
    if s==60: m+=1; s=0
    return f"{m}:{s:02d}"
