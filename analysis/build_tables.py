"""Build processed/weekly.csv and processed/fitness_curves.csv.

usage: python build_tables.py <fit_folder> <activities.csv> <workouts.csv> <metrics.csv> <out_dir>

Normally called through analysis/ingest.py (weekly.csv every time, fitness_curves.csv only with --full).
Thresholds (LTHR per sport, interval title words, gap length) come from config/athlete.yaml.

weekly.csv (weeks start Monday, IST):
  hours and km per sport excluding duplicate uploads; tp_shows_h is what TrainingPeaks displayed
  (inflated by the double uploads); planned vs completed sessions from the TrainingPeaks CSV;
  hr_load is a corrected training load: sum over sessions of hours * (avgHR / sport LTHR)^2 * 100
  (the TrainingPeaks TSS column is unusable, see athlete.md);
  gap_days is the longest run of days without any session that touches the week.
  build_wellness.py adds resting_hr_med, hrv_med, sleep_h_med, wellness_days.

fitness_curves.csv (one row per month), all from record-level data after the first 10 minutes:
  run_pace_at_hr150..165: outdoor GPS runs only, median pace of samples within 3 bpm of the target HR,
    needs at least 300 samples in the month, else blank
  bike_hr_at_106w / bike_w_per_beat_at_106w: chest-strap rides with power, samples at 100 to 112 W
  bike_power_at_hr133: chest-strap rides with power, median power at HR 130 to 136
  swim_pace_at_hr130_per_100m: per-lap pace (pool files have no per-record speed) for laps with average HR 128 to 134,
    needs at least 400 m of such laps in the month
  run curves skip interval, rep, stride, fartlek, hill and time-trial sessions (title match), where HR lags pace
  long_session_decoupling_pct: median decoupling of kept sessions of 90 minutes or more
  resting_hr, hrv, sleep_h: monthly medians from the Garmin daily metrics
  weight_kg: last logged weight in the month
"""
import sys, os, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import load_legs
from config import LTHR, GAP_DAYS, is_interval_title

MIN_SAMPLES = 300


def fmt_pace(v):
    if not v or v <= 0 or np.isnan(v): return None
    p = 1000 / v / 60; m = int(p); s = int(round((p - m) * 60))
    if s == 60: m += 1; s = 0
    return f'{m}:{s:02d}'


def fmt_pace100(v):
    if not v or v <= 0 or np.isnan(v): return None
    p = 100 / v / 60; m = int(p); s = int(round((p - m) * 60))
    if s == 60: m += 1; s = 0
    return f'{m}:{s:02d}'


def weekly(acts, tp):
    a = acts[acts.duplicate_of.isna() & ~acts.sport.eq('transition')].copy()
    a['date'] = pd.to_datetime(a.date)
    a['week'] = (a.date - pd.to_timedelta(a.date.dt.weekday, unit='D')).dt.date
    a['h'] = a.duration_min / 60
    a['lthr'] = a.sport.map(LTHR)
    a['hr_load'] = np.where(a.avg_hr.notna() & a.lthr.notna(), a.h * (a.avg_hr / a.lthr) ** 2 * 100, np.nan)
    piv = a.pivot_table(index='week', columns='sport', values=['h', 'distance_km'], aggfunc='sum').fillna(0)
    w = pd.DataFrame({
        'bike_h': piv.get(('h', 'cycling'), 0), 'run_h': piv.get(('h', 'running'), 0), 'swim_h': piv.get(('h', 'swimming'), 0),
        'bike_km': piv.get(('distance_km', 'cycling'), 0), 'run_km': piv.get(('distance_km', 'running'), 0), 'swim_km': piv.get(('distance_km', 'swimming'), 0),
    })
    w['other_h'] = a[~a.sport.isin(LTHR)].groupby('week').h.sum()
    w['total_h'] = a.groupby('week').h.sum()
    w['hr_load'] = a.groupby('week').hr_load.sum()
    w['sessions'] = a.groupby('week').size()
    tp = tp.copy(); tp['date'] = pd.to_datetime(tp.WorkoutDay)
    tp['week'] = (tp.date - pd.to_timedelta(tp.date.dt.weekday, unit='D')).dt.date
    # a week with a plan but no completed session must keep its planned counts (0% done, not "none planned"),
    # so widen the index to the plan's weeks before the plan columns are attached
    w = w.reindex(sorted(set(w.index) | set(tp.week)))
    tp['done'] = tp.TimeTotalInHours.fillna(0) > 0
    tp['planned'] = tp.PlannedDuration.notna()
    g = tp.groupby('week')
    w['tp_shows_h'] = g.TimeTotalInHours.sum()
    w['planned_sessions'] = g.planned.sum()
    w['completed_planned'] = tp[tp.planned].groupby('week').done.sum()
    w['unplanned_sessions'] = tp[~tp.planned].groupby('week').done.sum()
    w['planned_h'] = g.PlannedDuration.sum()
    allw = pd.date_range(min(w.index.min(), tp.week.min()), max(w.index.max(), tp.week.max()), freq='W-MON').date
    w = w.reindex(sorted(set(allw) | set(w.index) | set(tp.week)))
    w = w.fillna(0)
    w['completion_pct'] = np.where(w.planned_sessions > 0, 100 * w.completed_planned / w.planned_sessions, np.nan)
    days = sorted(a.date.dt.normalize().unique())
    gaps = [(x, y, (y - x).days) for x, y in zip(days, days[1:]) if (y - x).days >= GAP_DAYS]
    def gap_for(week):
        ws = pd.Timestamp(week); we = ws + pd.Timedelta(days=6)
        return max([d for x, y, d in gaps if x <= we and y >= ws], default=0)
    w['gap_days'] = [gap_for(k) for k in w.index]
    w.index.name = 'week_start'
    cols = ['bike_h', 'run_h', 'swim_h', 'other_h', 'total_h', 'tp_shows_h', 'bike_km', 'run_km', 'swim_km',
            'sessions', 'planned_sessions', 'completed_planned', 'unplanned_sessions', 'completion_pct', 'planned_h', 'hr_load', 'gap_days']
    return w[cols].round(1)


def curves(fit_folder, acts, metrics):
    a = acts[acts.duplicate_of.isna()].copy(); a['date'] = pd.to_datetime(a.date)
    files = {os.path.basename(f): f for f in glob.glob(os.path.join(fit_folder, '**', '*'), recursive=True)}
    runs = {}; bikes = {}; swims = {}
    for _, r in a.iterrows():
        path = files.get(r.file)
        if not path: continue
        if r.sport == 'running' and not r.indoor:
            if is_interval_title(r.get('title')): continue   # intervals break the pace-at-HR relation (HR lag)
            bucket = runs
        elif r.sport == 'cycling' and r.hr_source == 'strap': bucket = bikes
        elif r.sport == 'swimming': bucket = swims
        else: continue
        legs, dev, user, zones, events = load_legs(path)
        for df, laps, sess in legs:
            if str(sess.get('sport')) != r.sport or not len(df): continue
            m = r.date.to_period('M')
            if bucket is swims:
                if len(laps):
                    l = laps[(laps.dist > 0) & (laps.timer > 0) & laps.hr.notna()].copy()
                    l['v'] = l.dist / l.timer
                    bucket.setdefault(m, []).append(l[['v', 'hr', 'dist']])
                continue
            df = df[df.t >= df.t.min() + pd.Timedelta(minutes=10)].dropna(subset=['hr'])
            if not len(df): continue
            bucket.setdefault(m, []).append(df)
    months = sorted(set(a.date.dt.to_period('M')))
    rows = []
    for m in months:
        row = {'month': str(m)}
        R = pd.concat(runs[m]) if m in runs else pd.DataFrame()
        for hr in (150, 155, 160, 165):
            v = None
            if len(R):
                s = R[(R.hr >= hr - 3) & (R.hr <= hr + 3) & (R.v > 1.0)]
                if len(s) >= MIN_SAMPLES: v = s.v.median()
            row[f'run_pace_at_hr{hr}'] = fmt_pace(v) if v else None
        row['run_outdoor_samples'] = int(len(R))
        B = pd.concat(bikes[m]) if m in bikes else pd.DataFrame()
        if len(B) and 'pw' in B and B.pw.notna().any():
            s = B[(B.pw >= 100) & (B.pw <= 112)]
            if len(s) >= MIN_SAMPLES:
                row['bike_hr_at_106w'] = round(s.hr.median()); row['bike_w_per_beat_at_106w'] = round(106 / s.hr.median(), 2)
            s2 = B[(B.hr >= 130) & (B.hr <= 136) & (B.pw > 0)]
            if len(s2) >= MIN_SAMPLES: row['bike_power_at_hr133'] = round(s2.pw.median())
        S = pd.concat(swims[m]) if m in swims else pd.DataFrame()
        if len(S) and 'v' in S:
            s = S[(S.hr >= 128) & (S.hr <= 134) & (S.v > 0.3)]
            if s.dist.sum() >= 400: row['swim_pace_at_hr130_per_100m'] = fmt_pace100(s.v.median())
        long_ = a[(a.date.dt.to_period('M') == m) & (a.duration_min >= 90) & a.decoupling_pct.notna() & a.sport.isin(['running', 'cycling'])]
        row['long_session_decoupling_pct'] = round(long_.decoupling_pct.median(), 1) if len(long_) else None
        row['long_sessions_n'] = int(len(long_))
        mm = metrics[metrics.Timestamp.dt.to_period('M') == m]
        def med(t):
            x = pd.to_numeric(mm[mm.Type == t].Value, errors='coerce').dropna()
            return round(x.median(), 1) if len(x) else None
        row['resting_hr'] = med('Pulse'); row['hrv'] = med('HRV'); row['sleep_h'] = med('Sleep Hours')
        wt = mm[mm.Type == 'Weight Kilograms']
        row['weight_kg'] = float(wt.sort_values('Timestamp').Value.iloc[-1]) if len(wt) else None
        row['garmin_vo2max'] = a[(a.date.dt.to_period('M') == m)].garmin_vo2max.dropna().median()
        rows.append(row)
    cols = ['month', 'run_pace_at_hr150', 'run_pace_at_hr155', 'run_pace_at_hr160', 'run_pace_at_hr165', 'run_outdoor_samples',
            'bike_hr_at_106w', 'bike_w_per_beat_at_106w', 'bike_power_at_hr133', 'swim_pace_at_hr130_per_100m',
            'long_session_decoupling_pct', 'long_sessions_n', 'garmin_vo2max', 'resting_hr', 'hrv', 'sleep_h', 'weight_kg']
    return pd.DataFrame(rows).reindex(columns=cols)


def main():
    fit_folder, acts_csv, tp_csv, metrics_csv, out = sys.argv[1:6]
    acts = pd.read_csv(acts_csv); tp = pd.read_csv(tp_csv)
    metrics = pd.read_csv(metrics_csv); metrics['Timestamp'] = pd.to_datetime(metrics.Timestamp)
    if 'leg' not in acts: acts['leg'] = None
    w = weekly(acts, tp); w.to_csv(os.path.join(out, 'weekly.csv'))
    c = curves(fit_folder, acts, metrics); c.to_csv(os.path.join(out, 'fitness_curves.csv'), index=False)
    print(f'{len(w)} weeks, {len(c)} months -> {out}')


if __name__ == '__main__': main()
