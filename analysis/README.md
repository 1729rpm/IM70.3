# Analysis scripts

```
pip install fitdecode pandas numpy pyyaml --break-system-packages
python analysis/ingest.py <trainingpeaks_export.zip> --today YYYY-MM-DD        # every week
python analysis/ingest.py <full_activity_archive> --full --today YYYY-MM-DD    # quarterly, rebuilds fitness curves
```

All thresholds and rules come from `config/athlete.yaml` through `config.py`; nothing is hard-coded in a script.

- `ingest.py`: the weekly entry point. Unzips, classifies files, merges the TrainingPeaks CSVs into `raw/`, skips activity files already in the manifest, parses new ones, re-checks duplicates across the whole table, rebuilds the tables, writes `plan/`, regenerates `STATE.md`.
- `build_activities.py`: FIT files to `activities.csv` rows (used by ingest; run directly only for a from-scratch rebuild). Splits multisport files, flags duplicates (same sport, time overlap above the configured fraction; keeps power over strap over GPS), corrects treadmill pace, computes drift.
- `build_tables.py`: `weekly.csv` (every ingest) and `fitness_curves.csv` (full rebuild only). Definitions in the docstring.
- `build_benchmarks.py`: `benchmarks.csv` from `activities.csv` using the benchmark rules in config. No FIT files needed.
- `build_wellness.py`: `wellness_daily.csv` from the metrics export and weekly medians into `weekly.csv`.
- `build_state.py`: `STATE.md` from the tables and config.
- `load.py`: FIT parsing (`load_legs` returns one records/laps/session set per leg; `hr_source` says strap or wrist; timestamps IST).
- `blocks.py`: steady-state detection and drift (`decoupling`) on a session's records.
