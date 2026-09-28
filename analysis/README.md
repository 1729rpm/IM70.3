# Analysis scripts

```
pip install fitdecode pandas numpy --break-system-packages
```

- `load.py`: `load(path)` parses a .fit or .fit.gz and returns records, laps, session, device info, user profile, zones, events. Timestamps in IST. `hr_source(dev)` returns strap or wrist. `pace(v)` formats m/s as min:sec per km.
- `blocks.py`: `steady_blocks(df, col)` finds near-constant power or speed stretches and reports HR behaviour inside them (slope near 0 = steady state). `decoupling(df, col)` gives first-half vs second-half efficiency loss in percent.
- `build_activities.py`: builds `processed/activities.csv` from a folder of FIT files, flags duplicate uploads (time-window overlap, keeps the file with power), propagates strap HR to both copies, corrects treadmill pace, computes decoupling, pulls Garmin VO2max and recovery time, and optionally joins the TrainingPeaks workouts CSV for planned duration and titles.

```
python analysis/build_activities.py <fit_folder> processed/activities.csv --tp-csv workouts.csv
```

Conventions the scripts encode: IST, treadmill correction 12%, duplicate rule = same sport and more than 60% time overlap, keeper priority power > strap > outdoor GPS.
