# Analysis scripts

```
pip install fitdecode pandas numpy --break-system-packages
```

- `load.py`: `load_legs(path)` returns one (records, laps, session) tuple per session, so a multisport race file yields swim, T1, bike, T2, run. `load(path)` parses a .fit or .fit.gz and returns records, laps, session, device info, user profile, zones, events. Timestamps in IST. `hr_source(dev)` returns strap or wrist. `pace(v)` formats m/s as min:sec per km.
- `blocks.py`: `steady_blocks(df, col)` finds near-constant power or speed stretches and reports HR behaviour inside them (slope near 0 = steady state). `decoupling(df, col)` gives first-half vs second-half efficiency loss in percent.
- `build_activities.py`: builds `processed/activities.csv` from a folder of FIT files, flags duplicate uploads (time-window overlap, keeps the file with power), propagates strap HR to both copies, corrects treadmill pace, computes decoupling, pulls Garmin VO2max and recovery time, and optionally joins the TrainingPeaks workouts CSV for planned duration and titles.

- `build_tables.py`: builds `processed/weekly.csv` and `processed/fitness_curves.csv` from the FIT folder, activities.csv, the TrainingPeaks workouts CSV and metrics CSV. See its docstring for the exact definitions.

```
python analysis/build_activities.py <fit_folder> processed/activities.csv --tp-csv workouts.csv
python analysis/build_tables.py <fit_folder> processed/activities.csv workouts.csv metrics.csv processed
```

When two exports overlap (e.g. Sep 2025 to Aug 2026 and Aug to Sep 2026), concatenate the workouts CSVs and metrics CSVs and drop exact duplicate rows before running; copy the FIT files into one folder (duplicate file names are the same file).

Conventions the scripts encode: IST, treadmill correction 12%, duplicate rule = same sport and more than 60% time overlap, keeper priority power > strap > outdoor GPS.
