"""Generate STATE.md: where things stand right now, on one screen, built from the processed tables and config.

usage: python analysis/build_state.py [--today YYYY-MM-DD]

STATE.md is regenerated after every ingest and never edited by hand. It shows: days to the next races, the last
four weeks (hours, completion, load, gaps, recovery), the latest value of each fitness marker with its date, the
last two occurrences of each benchmark session, upcoming unavailable windows, and the coming week's plan if
plan/ has it. It deliberately holds no conclusions: those live in insights.md.
"""
import sys, os, glob, argparse, datetime as dt
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CFG, repo_path

P = repo_path


def read(path):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()


def fmt(v, suffix=''):
    if v is None or (isinstance(v, float) and np.isnan(v)) or v == '':
        return ''
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f'{v}{suffix}'


def section_races(today):
    lines = []
    for r in CFG['races']:
        d = pd.Timestamp(r['date']).date()
        days = (d - today).days
        if days < 0:
            continue
        where = f" (plan: {r['file']})" if r.get('file') else ''
        lines.append(f"- {r['name']}: {d.isoformat()}, {days} days away, {r['priority']} race{where}")
    return lines


def section_weeks(w):
    if not len(w):
        return ['- weekly.csv not found']
    w = w.copy(); w['week_start'] = pd.to_datetime(w.week_start)
    w = w[w.total_h > 0].tail(4)
    has_well = 'resting_hr_med' in w
    hdr = '| Week of | Total h | Bike / run / swim h | Sessions planned : done | HR load | Gap days |' + (' Resting HR | Sleep h |' if has_well else '')
    sep = '|---|---|---|---|---|---|' + ('---|---|' if has_well else '')
    lines = [hdr, sep]
    for _, r in w.iterrows():
        comp = f"{int(r.planned_sessions)} : {int(r.completed_planned)}" if r.planned_sessions else 'none planned'
        row = f"| {r.week_start.date()} | {r.total_h:.1f} | {r.bike_h:.1f} / {r.run_h:.1f} / {r.swim_h:.1f} | {comp} | {int(r.hr_load)} | {int(r.gap_days)} |"
        if has_well:
            row += f" {fmt(r.get('resting_hr_med'))} | {fmt(r.get('sleep_h_med'))} |"
        lines.append(row)
    lines.append('')
    lines.append('HR load is hours x (average HR / threshold HR)^2 x 100; a steady 1 h ride at threshold HR scores 100. '
                 'A typical good week for Rajat has scored 550 to 800. Gap days is the longest stretch without training touching that week.')
    return lines


def section_markers(c):
    if not len(c):
        return ['- fitness_curves.csv not found']
    items = [
        ('run_pace_at_hr160', 'Outdoor run pace at HR 160', '/km'),
        ('run_pace_at_hr165', 'Outdoor run pace at HR 165', '/km'),
        ('bike_hr_at_106w', 'Bike HR at 106 W (lower is fitter)', ' bpm'),
        ('bike_power_at_hr133', 'Bike power at HR 133 (higher is fitter)', ' W'),
        ('swim_pace_at_hr130_per_100m', 'Swim pace at HR 130', '/100 m'),
        ('long_session_decoupling_pct', 'Drift on sessions of 90 min or more', '%'),
        ('garmin_vo2max', 'Garmin VO2max estimate', ''),
        ('resting_hr', 'Resting HR (monthly median)', ' bpm'),
        ('hrv', 'HRV (monthly median)', ''),
        ('weight_kg', 'Weight', ' kg'),
    ]
    lines = ['| Marker | Latest | Month | Previous | Month |', '|---|---|---|---|---|']
    for col, label, unit in items:
        s = c[['month', col]].dropna() if col in c else pd.DataFrame()
        if not len(s):
            continue
        cur = s.iloc[-1]; prev = s.iloc[-2] if len(s) > 1 else None
        lines.append(f"| {label} | {fmt(cur[col], unit)} | {cur['month']} | {fmt(prev[col], unit) if prev is not None else ''} | {prev['month'] if prev is not None else ''} |")
    lines.append('')
    lines.append('These are monthly medians from the full activity files; they refresh when a full export is reprocessed. For week-to-week movement use the benchmarks below.')
    return lines


def section_benchmarks(b):
    if not len(b):
        return ['- benchmarks.csv not found']
    lines = []
    for bid, g in b.groupby('benchmark_id', sort=False):
        g = g.sort_values('date')
        label = g.label.iloc[0]
        last = g.iloc[-1]; prev = g.iloc[-2] if len(g) > 1 else None
        def one(r):
            bits = []
            if fmt(r.pace_min_km): bits.append(f"{r.pace_min_km}/km")
            if fmt(r.pace_per_100m): bits.append(f"{r.pace_per_100m}/100 m")
            if fmt(r.avg_power_w): bits.append(f"{fmt(r.avg_power_w)} W")
            if fmt(r.avg_hr): bits.append(f"HR {fmt(r.avg_hr)}")
            if fmt(r.decoupling_pct): bits.append(f"drift {r.decoupling_pct}%")
            if fmt(r.duration_min): bits.append(f"{fmt(r.duration_min)} min")
            if fmt(r.distance_km): bits.append(f"{r.distance_km} km")
            return f"{r.date}: " + ', '.join(bits) + (f" ({r.hr_source} HR)" if fmt(r.hr_source) else '')
        s = f"- **{label}** ({len(g)} on file). Latest {one(last)}."
        if prev is not None:
            s += f" Before that {one(prev)}."
        lines.append(s)
    return lines


def section_unavailable(today):
    lines = []
    for u in CFG.get('unavailable', []):
        a, z = pd.Timestamp(u['from']).date(), pd.Timestamp(u['to']).date()
        if z >= today and (a - today).days <= 120:
            lines.append(f"- {a.isoformat()} to {z.isoformat()}: {u['reason']} (running and gym only)")
    return lines or ['- none in the next four months']


def section_plan(today):
    files = sorted(f for f in glob.glob(P('plan', '*.md')) if not os.path.basename(f).lower().startswith('readme'))
    if not files:
        return ['- no plan file yet; upcoming workouts appear here once a TrainingPeaks export that includes future dates has been ingested']
    latest = files[-1]
    with open(latest) as f:
        body = f.read().strip().splitlines()
    return [f'- from {os.path.relpath(latest, P())}:'] + ['  ' + l for l in body if l.strip()][:20]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--today')
    a = ap.parse_args()
    today = pd.Timestamp(a.today).date() if a.today else dt.date.today()
    w = read(P('processed', 'weekly.csv')); c = read(P('processed', 'fitness_curves.csv')); b = read(P('processed', 'benchmarks.csv'))
    last_session = None
    acts = read(P('processed', 'activities.csv'))
    if len(acts):
        last_session = acts[acts.duplicate_of.isna()].date.max() if 'duplicate_of' in acts else acts.date.max()
    out = [f'# State on {today.isoformat()}', '',
           'Generated by `analysis/build_state.py`. Do not edit; rerun after every ingest. Conclusions are in insights.md, numbers in config/athlete.yaml, the athlete in athlete.md.', '',
           f'Data covers sessions to {last_session}.' if last_session else '', '',
           '## Races', *section_races(today), '',
           '## Last four training weeks', *section_weeks(w), '',
           '## Fitness markers', *section_markers(c), '',
           '## Benchmark sessions (latest vs previous)', *section_benchmarks(b), '',
           '## Coming week plan', *section_plan(today), '',
           '## Unavailable windows', *section_unavailable(today), '',
           '## Where to look next',
           '- Open questions and what to watch: insights.md, section "Open questions"',
           '- Race plans and debriefs: races/',
           '- Latest weekly review: reports/ (newest file)']
    with open(P('STATE.md'), 'w') as f:
        f.write('\n'.join(l for l in out if l is not None) + '\n')
    print(f"STATE.md written for {today}")


if __name__ == '__main__':
    main()
