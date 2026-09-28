"""Build processed/activities.csv from a folder of FIT files (TrainingPeaks 'Workout File Export').

usage: python build_activities.py <fit_folder> <out_csv> [--tp-csv workouts.csv]

Normally run through analysis/ingest.py, which handles new files only. Run this directly to rebuild from scratch.

What it does:
  * one row per activity file (one per leg for multisport race files, see `leg`): date, start time (IST), sport,
    indoor flag, HR source (strap/wrist), duration, distance, avg/max HR, power, pace (and treadmill-corrected
    pace), cadence, temperature, decoupling (first half vs second half), Garmin VO2max estimate, training effect
  * flags duplicate uploads: same sport and time windows overlapping by more than the configured fraction of the
    shorter one -> the richer file is kept (power > strap HR > outdoor GPS), the other gets duplicate_of
  * optionally joins the TrainingPeaks workouts CSV to attach planned duration and coach titles
All thresholds come from config/athlete.yaml.
"""
import sys, os, glob, argparse
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import load, load_legs, hr_source, pace
from blocks import decoupling
from config import TREADMILL_FACTOR, DUP_OVERLAP


def garmin_extras(path):
    import fitdecode
    from load import _open
    vo2 = None; rec = None
    with fitdecode.FitReader(_open(path), check_crc=fitdecode.CrcCheck.DISABLED) as fr:
        for m in fr:
            if isinstance(m, fitdecode.FitDataMessage) and getattr(m, 'global_mesg_num', None) == 140:
                for fd in m.fields:
                    if fd.def_num == 7 and fd.value: vo2 = round(fd.value * 3.5 / 65536, 1)
                    if fd.def_num == 9 and fd.value is not None: rec = round(fd.value / 60, 1)
    return vo2, rec


def one(path):
    """One row per session in the file. Single-sport files give one row; a multisport race file gives one
    row per leg (swim, T1, bike, T2, run) sharing the same file name, with `leg` set to n/total."""
    legs, dev, user, zones, events = load_legs(path)
    rows = []
    for i, (df, laps, sess) in enumerate(legs):
        r = _row(df, laps, sess, dev, path)
        if r:
            r['leg'] = f'{i+1}/{len(legs)}' if len(legs) > 1 else None
            rows.append(r)
    return rows


def _row(df, laps, sess, dev, path):
    if not sess: return None
    sport = str(sess.get('sport')); sub = str(sess.get('sub_sport'))
    indoor = sub in ('treadmill', 'indoor_cycling', 'virtual_activity', 'indoor_rowing', 'lap_swimming') or ('lat' in df and df.lat.notna().sum() == 0)
    start = (pd.to_datetime(sess['start_time']).tz_localize(None) + pd.Timedelta(hours=5, minutes=30)) if sess.get('start_time') is not None else None
    dist = (sess.get('total_distance') or 0) / 1000; timer = (sess.get('total_timer_time') or 0) / 60
    v = (dist * 1000 / (timer * 60)) if timer else 0
    row = dict(date=start.date() if start is not None else None, start_ist=start.strftime('%H:%M') if start is not None else None,
               sport=sport, sub_sport=sub, indoor=indoor, hr_source=hr_source(dev),
               duration_min=round(timer, 1), distance_km=round(dist, 2),
               avg_hr=sess.get('avg_heart_rate'), max_hr=sess.get('max_heart_rate'),
               avg_power_w=sess.get('avg_power'), np_w=sess.get('normalized_power'),
               pace_min_km=pace(v) if sport == 'running' else None,
               pace_corrected_min_km=pace(v * TREADMILL_FACTOR) if (sport == 'running' and sub == 'treadmill') else (pace(v) if sport == 'running' else None),
               avg_cadence=(sess.get('avg_running_cadence') or sess.get('avg_cadence')),
               avg_temp_c=sess.get('avg_temperature'), ascent_m=sess.get('total_ascent'),
               training_effect=sess.get('total_training_effect'), calories=sess.get('total_calories'),
               file=os.path.basename(path))
    try:
        row['decoupling_pct'] = decoupling(df, col='pw' if sport == 'cycling' and 'pw' in df and df.pw.notna().any() else 'v') if sport in ('running', 'cycling') else None
    except Exception: row['decoupling_pct'] = None
    try: row['garmin_vo2max'], row['garmin_recovery_h'] = garmin_extras(path)
    except Exception: row['garmin_vo2max'], row['garmin_recovery_h'] = None, None
    # keeper priority when two files describe one session: power (4) > strap HR (2) > outdoor GPS (1)
    row['channels'] = 4 * int('pw' in df and df.pw.notna().any()) + 2 * int(row['hr_source'] == 'strap') + int(not indoor)
    return row


def flag_duplicates(t):
    """Two files of the same sport whose time windows overlap by more than DUP_OVERLAP of the shorter one are
    the same session recorded twice (typically MyWhoosh + watch). The richer file is kept; the other gets
    duplicate_of. If either copy has strap HR, both are marked strap (same sensor broadcast to both)."""
    t = t.copy()
    t['duplicate_of'] = None
    t['_start'] = pd.to_datetime(t.date.astype(str) + ' ' + t.start_ist.astype(str), errors='coerce')
    t['_end'] = t._start + pd.to_timedelta(t.duration_min, unit='m')
    for i, a in t.iterrows():
        for j, b in t.iterrows():
            if j <= i or a.sport != b.sport or pd.isna(a._start) or pd.isna(b._start): continue
            overlap = (min(a._end, b._end) - max(a._start, b._start)).total_seconds() / 60
            if overlap > DUP_OVERLAP * min(a.duration_min, b.duration_min):
                loser, keeper = (i, j) if a.channels < b.channels else (j, i)
                t.loc[loser, 'duplicate_of'] = t.loc[keeper, 'file']
                if 'strap' in (a.hr_source, b.hr_source): t.loc[[i, j], 'hr_source'] = 'strap'
    return t.drop(columns=['_start', '_end'])


def attach_plan(t, tp):
    """Join planned duration and coach titles from the TrainingPeaks workouts CSV by date and sport."""
    tp = tp.copy(); tp['date'] = pd.to_datetime(tp.WorkoutDay).dt.date
    tp['sport'] = tp.WorkoutType.map({'Run': 'running', 'Bike': 'cycling', 'Swim': 'swimming'})
    plan = tp.groupby(['date', 'sport']).agg(planned_min=('PlannedDuration', lambda s: round(s.sum() * 60, 0)),
                                             title=('Title', lambda s: ' | '.join(s.dropna().astype(str)))).reset_index()
    t = t.copy(); t['date'] = pd.to_datetime(t.date).dt.date
    t = t.drop(columns=[c for c in ('planned_min', 'title') if c in t])
    return t.merge(plan, on=['date', 'sport'], how='left')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('out'); ap.add_argument('--tp-csv')
    a = ap.parse_args()
    files = [f for f in glob.glob(os.path.join(a.folder, '**', '*'), recursive=True) if f.lower().endswith(('.fit', '.fit.gz'))]
    rows = [r for f in sorted(files) for r in (one(f) or [])]
    t = pd.DataFrame(rows).sort_values(['date', 'start_ist']).reset_index(drop=True)
    t = flag_duplicates(t)
    if a.tp_csv:
        t = attach_plan(t, pd.read_csv(a.tp_csv))
    t.to_csv(a.out, index=False)
    print(f'{len(t)} activities, {t.duplicate_of.notna().sum()} duplicates flagged -> {a.out}')


if __name__ == '__main__': main()
