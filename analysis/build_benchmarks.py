"""Build processed/benchmarks.csv from processed/activities.csv.

usage: python analysis/build_benchmarks.py [activities.csv] [out.csv]

A benchmark is a kind of session that repeats often enough to compare week to week (an outdoor easy run,
an indoor ride with power, a long swim). The rules live in config/athlete.yaml under `benchmarks`. Each
matching session becomes one row here, so the weekly review can ask "same kind of session, how did it move?"
without touching the FIT files. Duplicate uploads and race transitions are excluded.

Columns: benchmark_id, label, date, title, and the reported metrics (pace_min_km, avg_hr, avg_power_w,
decoupling_pct, avg_cadence, duration_min, distance_km, pace_per_100m), plus hr_source and indoor so a reader
can judge how much to trust the row.
"""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CFG, is_interval_title, repo_path

REPORT_COLS = ['pace_min_km', 'avg_hr', 'avg_power_w', 'decoupling_pct', 'avg_cadence', 'duration_min', 'distance_km', 'pace_per_100m']


def swim_pace_per_100m(row):
    if not row.distance_km or row.distance_km <= 0:
        return None
    secs = row.duration_min * 60 / (row.distance_km * 10)
    m, s = divmod(int(round(secs)), 60)
    return f'{m}:{s:02d}'


def mark_bricks(a):
    """A run is a brick if it starts within 45 minutes of a ride ending on the same day."""
    a = a.copy()
    a['_start'] = pd.to_datetime(a.date.astype(str) + ' ' + a.start_ist.astype(str), errors='coerce')
    a['_end'] = a._start + pd.to_timedelta(a.duration_min, unit='m')
    a['brick'] = False
    rides = a[a.sport == 'cycling']
    for i, r in a[a.sport == 'running'].iterrows():
        same_day = rides[rides.date == r.date]
        if any((r._start - e).total_seconds() / 60 <= 45 and (r._start - e).total_seconds() >= -60 for e in same_day._end):
            a.loc[i, 'brick'] = True
    return a.drop(columns=['_start', '_end'])


def match(rule, a):
    m = (a.sport == rule['sport'])
    if 'indoor' in rule:
        m &= a.indoor.astype(str).str.lower().eq(str(rule['indoor']).lower())
    if 'hr_source' in rule:
        m &= a.hr_source.eq(rule['hr_source'])
    if rule.get('requires_power'):
        m &= a.avg_power_w.notna()
    if 'min_minutes' in rule:
        m &= a.duration_min >= rule['min_minutes']
    if 'min_km' in rule:
        m &= a.distance_km >= rule['min_km']
    if 'avg_hr_between' in rule:
        lo, hi = rule['avg_hr_between']
        m &= a.avg_hr.between(lo, hi)
    if rule.get('exclude_interval_titles'):
        m &= ~a.title.map(is_interval_title)
    if 'exclude_title_words' in rule:
        words = [str(w).lower() for w in rule['exclude_title_words']]
        m &= ~a.title.str.lower().apply(lambda t: any(w in t for w in words))
    if 'brick' in rule:
        m &= a.brick if rule['brick'] else ~a.brick
    return a[m]


def main():
    acts = sys.argv[1] if len(sys.argv) > 1 else repo_path('processed', 'activities.csv')
    out = sys.argv[2] if len(sys.argv) > 2 else repo_path('processed', 'benchmarks.csv')
    a = pd.read_csv(acts)
    if 'duplicate_of' not in a: a['duplicate_of'] = None
    a = a[a.duplicate_of.isna() & ~a.sport.eq('transition')].copy()
    a['title'] = a.title.fillna('')
    a = mark_bricks(a)
    a['pace_min_km'] = a.pace_corrected_min_km.where(a.pace_corrected_min_km.notna(), a.pace_min_km)
    a['pace_per_100m'] = a.apply(lambda r: swim_pace_per_100m(r) if r.sport == 'swimming' else None, axis=1)
    rows = []
    for rule in CFG['benchmarks']:
        hits = match(rule, a)
        for _, r in hits.iterrows():
            row = {'benchmark_id': rule['id'], 'label': rule['label'], 'date': r.date, 'title': r.title,
                   'hr_source': r.hr_source, 'indoor': r.indoor, 'file': r.file}
            for c in REPORT_COLS:
                row[c] = r.get(c) if c in rule['report'] else None
            rows.append(row)
    b = pd.DataFrame(rows).sort_values(['benchmark_id', 'date']).reset_index(drop=True)
    cols = ['benchmark_id', 'label', 'date', 'title'] + REPORT_COLS + ['hr_source', 'indoor', 'file']
    b = b.reindex(columns=cols)
    b.to_csv(out, index=False)
    print(f'{len(b)} benchmark rows across {b.benchmark_id.nunique()} benchmarks -> {out}')
    print(b.groupby('benchmark_id').size().to_string())


if __name__ == '__main__':
    main()
