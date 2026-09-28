"""Ingest a TrainingPeaks export. This is the only command a weekly session needs to run.

usage: python analysis/ingest.py <export.zip or folder> [more zips or folders...] [--full] [--today YYYY-MM-DD]

What it does, in order:
  1. Unzips everything into a scratch folder and finds the three kinds of file TrainingPeaks exports:
     the workouts CSV (planned and completed sessions), the Metrics CSV (resting HR, HRV, sleep, weight)
     and the activity files (.fit / .fit.gz).
  2. Merges the workouts CSV into raw/workouts.csv and the metrics CSV into raw/metrics.csv, dropping rows
     already there. These two small text files stay in the repo so every table can be rebuilt without the zips.
  3. Records every activity file in raw/fit_manifest.csv (name, size, hash). Files already in the manifest
     are skipped, so re-uploading a week does nothing twice. New files are parsed with build_activities and
     appended to processed/activities.csv; the duplicate-upload check then runs over the whole table.
  4. Rebuilds processed/weekly.csv (for weeks the workouts file covers; older weeks are kept as they were),
     processed/benchmarks.csv, processed/wellness_daily.csv and STATE.md.
     processed/fitness_curves.csv needs record-level data from every activity file, so it is rebuilt only with
     --full (upload the whole activity-file archive for that).
  5. Writes plan/YYYY-Www.md for any planned workouts dated after the last completed session.

The raw activity files are not kept in the repo (they live in Google Drive). Everything else is.
"""
import sys, os, glob, shutil, zipfile, hashlib, argparse, datetime as dt, subprocess
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import repo_path, GAP_DAYS
import build_activities as BA
import build_tables as BT

P = repo_path
SCRATCH = '/tmp/im703_ingest'


def unpack(sources):
    if os.path.exists(SCRATCH): shutil.rmtree(SCRATCH)
    os.makedirs(SCRATCH)
    for i, s in enumerate(sources):
        dest = os.path.join(SCRATCH, f'src{i}')
        if zipfile.is_zipfile(s):
            with zipfile.ZipFile(s) as z: z.extractall(dest)
        else:
            shutil.copytree(s, dest)
    # zips inside zips (TrainingPeaks bundles the activity files as a second zip)
    for inner in glob.glob(os.path.join(SCRATCH, '**', '*.zip'), recursive=True):
        with zipfile.ZipFile(inner) as z: z.extractall(inner[:-4])
    return SCRATCH


def classify(folder):
    csvs = glob.glob(os.path.join(folder, '**', '*.csv'), recursive=True)
    workouts, metrics = [], []
    for c in csvs:
        try:
            head = pd.read_csv(c, nrows=2)
        except Exception:
            continue
        cols = set(head.columns)
        if {'WorkoutDay', 'WorkoutType'} <= cols: workouts.append(c)
        elif {'Timestamp', 'Type', 'Value'} <= cols: metrics.append(c)
    fits = [f for f in glob.glob(os.path.join(folder, '**', '*'), recursive=True) if f.lower().endswith(('.fit', '.fit.gz'))]
    return workouts, metrics, fits


def merge_csv(new_paths, out_path, key_cols):
    frames = [pd.read_csv(p) for p in new_paths]
    if os.path.exists(out_path): frames.insert(0, pd.read_csv(out_path))
    if not frames: return None
    df = pd.concat(frames, ignore_index=True)
    keys = [k for k in key_cols if k in df]
    before = len(df)
    df = df.drop_duplicates(subset=keys if keys else None, keep='last')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f'{os.path.relpath(out_path, P())}: {len(df)} rows ({before - len(df)} duplicates dropped)')
    return df


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()


def update_manifest(fits, today):
    mpath = P('raw', 'fit_manifest.csv')
    man = pd.read_csv(mpath) if os.path.exists(mpath) else pd.DataFrame(columns=['file', 'bytes', 'sha1', 'first_seen'])
    known = set(man.sha1)
    new = []
    for f in fits:
        h = sha1(f)
        if h in known: continue
        new.append({'file': os.path.basename(f), 'bytes': os.path.getsize(f), 'sha1': h, 'first_seen': today.isoformat(), 'path': f})
        known.add(h)
    if new:
        man = pd.concat([man, pd.DataFrame(new).drop(columns=['path'])], ignore_index=True)
        os.makedirs(P('raw'), exist_ok=True); man.to_csv(mpath, index=False)
    print(f'activity files: {len(fits)} in export, {len(new)} new')
    return new


def append_activities(new_files, workouts):
    apath = P('processed', 'activities.csv')
    acts = pd.read_csv(apath) if os.path.exists(apath) else pd.DataFrame()
    rows = [r for nf in new_files for r in (BA.one(nf['path']) or [])]
    if not rows:
        print('no new activities'); return acts
    t = pd.DataFrame(rows)
    if workouts is not None:
        t = BA.attach_plan(t, workouts)
    t = pd.concat([acts, t], ignore_index=True)
    t['date'] = t.date.astype(str)
    t = t.sort_values(['date', 'start_ist']).reset_index(drop=True)
    t = BA.flag_duplicates(t)
    t.to_csv(apath, index=False)
    print(f'activities.csv: +{len(rows)} rows, now {len(t)} ({t.duplicate_of.notna().sum()} duplicates flagged)')
    return t


def rebuild_weekly(acts, workouts):
    wpath = P('processed', 'weekly.csv')
    if workouts is None or not len(acts): return
    fresh = BT.weekly(acts, workouts).reset_index()
    fresh['week_start'] = fresh.week_start.astype(str)
    if os.path.exists(wpath):
        old = pd.read_csv(wpath); old['week_start'] = old.week_start.astype(str)
        cutoff = str(pd.to_datetime(workouts.WorkoutDay).min().date())
        keep = old[old.week_start < cutoff]
        extra = [c for c in old.columns if c not in fresh.columns]   # wellness medians etc.
        fresh = pd.concat([keep, fresh[fresh.week_start >= cutoff]], ignore_index=True)
        for c in extra:
            fresh[c] = fresh[c] if c in fresh else np.nan
    fresh.to_csv(wpath, index=False)
    print(f'weekly.csv: {len(fresh)} weeks')


def write_plan(workouts, acts, today):
    if workouts is None: return
    w = workouts.copy(); w['date'] = pd.to_datetime(w.WorkoutDay).dt.date
    last_done = pd.to_datetime(acts.date).max().date() if len(acts) else today
    fut = w[(w.date > last_done) & w.PlannedDuration.notna()].sort_values('date')
    if not len(fut): print('no planned workouts after the last completed session'); return
    desc_col = next((c for c in ('WorkoutDescription', 'Description') if c in w), None)
    cc_col = 'CoachComments' if 'CoachComments' in w else None
    os.makedirs(P('plan'), exist_ok=True)
    for (year, week), g in fut.groupby([pd.to_datetime(fut.date).dt.isocalendar().year, pd.to_datetime(fut.date).dt.isocalendar().week]):
        path = P('plan', f'{year}-W{int(week):02d}.md')
        lines = [f'# Plan for week {year}-W{int(week):02d}', '', 'Exported from TrainingPeaks; the coach wrote these. One line per session: day, sport, planned time, title, then the description.', '']
        for _, r in g.iterrows():
            mins = int(round(float(r.PlannedDuration) * 60)) if pd.notna(r.PlannedDuration) else ''
            lines.append(f"## {r.date} ({pd.Timestamp(r.date).strftime('%a')}) {r.WorkoutType}, {mins} min: {r.Title}")
            if desc_col and pd.notna(r.get(desc_col)): lines.append(str(r[desc_col]).strip())
            if cc_col and pd.notna(r.get(cc_col)): lines.append(f'Coach: {str(r[cc_col]).strip()}')
            lines.append('')
        with open(path, 'w') as f: f.write('\n'.join(lines))
        print(f'plan: {os.path.relpath(path, P())} ({len(g)} sessions)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sources', nargs='+'); ap.add_argument('--full', action='store_true'); ap.add_argument('--today')
    a = ap.parse_args()
    today = pd.Timestamp(a.today).date() if a.today else dt.date.today()
    folder = unpack(a.sources)
    wk_csvs, met_csvs, fits = classify(folder)
    print(f'found {len(wk_csvs)} workouts csv, {len(met_csvs)} metrics csv, {len(fits)} activity files')
    workouts = merge_csv(wk_csvs, P('raw', 'workouts.csv'), ['WorkoutDay', 'WorkoutType', 'Title', 'TimeTotalInHours', 'PlannedDuration'])
    metrics = merge_csv(met_csvs, P('raw', 'metrics.csv'), ['Timestamp', 'Type'])
    new_files = update_manifest(fits, today)
    acts = append_activities(new_files, workouts)
    rebuild_weekly(acts, workouts)
    if a.full and os.path.exists(P('raw', 'metrics.csv')):
        m = pd.read_csv(P('raw', 'metrics.csv')); m['Timestamp'] = pd.to_datetime(m.Timestamp)
        c = BT.curves(folder, acts, m); c.to_csv(P('processed', 'fitness_curves.csv'), index=False)
        print(f'fitness_curves.csv rebuilt: {len(c)} months')
    if os.path.exists(P('raw', 'metrics.csv')):
        subprocess.run([sys.executable, P('analysis', 'build_wellness.py'), P('raw', 'metrics.csv')], check=False)
    subprocess.run([sys.executable, P('analysis', 'build_benchmarks.py')], check=False)
    write_plan(workouts, acts, today)
    subprocess.run([sys.executable, P('analysis', 'build_state.py'), '--today', today.isoformat()], check=False)
    print('ingest complete; check STATE.md, then write the review')


if __name__ == '__main__':
    main()
