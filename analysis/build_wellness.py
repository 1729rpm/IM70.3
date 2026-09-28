"""Build processed/wellness_daily.csv from the TrainingPeaks Metrics Export (long format: Timestamp, Type, Value)
and add weekly medians to processed/weekly.csv.

usage: python analysis/build_wellness.py <metrics.csv> [weekly.csv]

wellness_daily.csv: one row per day with resting_hr, hrv, sleep_h, body_battery_max, weight_kg (blank when not
recorded). Recovery signals matter as trends against training load, not as single readings, so weekly.csv gets
resting_hr_med, hrv_med, sleep_h_med and wellness_days (how many days had a reading; fewer than 4 means the week's
medians are thin).

The Garmin "Pulse" type is resting HR. Weight is logged only a handful of times a year and carries forward here
only within the day it was logged (no interpolation).
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import repo_path

TYPES = {'Pulse': 'resting_hr', 'HRV': 'hrv', 'Sleep Hours': 'sleep_h', 'Body Battery': 'body_battery_max',
         'Weight Kilograms': 'weight_kg'}


def daily(metrics):
    m = metrics.copy()
    m['Timestamp'] = pd.to_datetime(m.Timestamp, errors='coerce')
    m = m.dropna(subset=['Timestamp'])
    m['date'] = m.Timestamp.dt.date
    m['Value'] = pd.to_numeric(m.Value, errors='coerce')
    m = m[m.Type.isin(TYPES)]
    agg = {'Pulse': 'min', 'HRV': 'median', 'Sleep Hours': 'max', 'Body Battery': 'max', 'Weight Kilograms': 'last'}
    rows = []
    for (d, t), g in m.groupby(['date', 'Type']):
        v = getattr(g.Value, agg[t])() if agg[t] != 'last' else g.sort_values('Timestamp').Value.iloc[-1]
        rows.append({'date': d, 'metric': TYPES[t], 'value': v})
    if not rows:
        return pd.DataFrame(columns=['date'] + list(TYPES.values()))
    w = pd.DataFrame(rows).pivot_table(index='date', columns='metric', values='value', aggfunc='first')
    return w.reindex(columns=list(TYPES.values())).round(1).reset_index()


def add_weekly(daily_df, weekly_path):
    if not os.path.exists(weekly_path):
        print(f'{weekly_path} not found; skipping weekly medians'); return
    w = pd.read_csv(weekly_path)
    d = daily_df.copy(); d['date'] = pd.to_datetime(d.date)
    d['week_start'] = (d.date - pd.to_timedelta(d.date.dt.weekday, unit='D')).dt.date.astype(str)
    g = d.groupby('week_start')
    med = pd.DataFrame({'resting_hr_med': g.resting_hr.median(), 'hrv_med': g.hrv.median(),
                        'sleep_h_med': g.sleep_h.median(), 'wellness_days': g.resting_hr.count()}).round(1)
    w = w.drop(columns=[c for c in med.columns if c in w], errors='ignore')
    w = w.merge(med, left_on='week_start', right_index=True, how='left')
    w.to_csv(weekly_path, index=False)
    print(f'weekly medians added for {med.index.nunique()} weeks -> {weekly_path}')


def main():
    metrics_csv = sys.argv[1]
    weekly_path = sys.argv[2] if len(sys.argv) > 2 else repo_path('processed', 'weekly.csv')
    out = repo_path('processed', 'wellness_daily.csv')
    metrics = pd.read_csv(metrics_csv)
    d = daily(metrics)
    if os.path.exists(out):   # merge with what is already there; new readings win
        old = pd.read_csv(out); old['date'] = pd.to_datetime(old.date).dt.date
        d = pd.concat([old, d]).drop_duplicates('date', keep='last').sort_values('date')
    d.to_csv(out, index=False)
    print(f'{len(d)} days -> {out}')
    add_weekly(d, weekly_path)


if __name__ == '__main__':
    main()
