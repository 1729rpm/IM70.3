# Processed tables

All built by scripts in `analysis/`; never edited by hand. Duplicate uploads (`duplicate_of` set) and race transitions are excluded from every total.

- `activities.csv`: one row per session (one per leg for a multisport race file). Date and start time in IST, sport, indoor flag, HR source (strap or wrist), duration, distance, heart rate, power, pace (treadmill pace already slowed by the configured factor), cadence, temperature, drift (`decoupling_pct`), Garmin VO2max estimate, plus the coach's planned minutes and title from TrainingPeaks. Grows each week through `ingest.py`.
- `weekly.csv`: weeks start Monday. Hours and km per sport, what TrainingPeaks displayed (`tp_shows_h`, inflated by duplicates), planned vs completed sessions, `hr_load` (hours x (average HR / threshold HR)^2 x 100), `gap_days` (longest no-training gap of 7 days or more touching the week), and once metrics are ingested the weekly medians of resting HR, HRV and sleep with the count of days that had a reading.
- `benchmarks.csv`: one row per occurrence of each repeatable session type defined in `config/athlete.yaml` (outdoor easy run, outdoor steady run, indoor ride with power and strap, long ride, swim of 1,500 m or more, brick run) with the metrics that matter for that type and the trust of the HR source. The week-to-week view of fitness.
- `fitness_curves.csv`: one row per month of pace at fixed heart rate, heart rate at fixed power, swim pace at fixed heart rate, drift on long sessions, VO2max estimate and wellness medians. Built from second-by-second data, so it refreshes only on a full rebuild (`ingest.py --full` with the whole activity archive).
- `wellness_daily.csv`: one row per day of resting HR, HRV, sleep hours, Body Battery peak and weight from the TrainingPeaks Metrics Export. Appears after the first ingest that includes that export.

Coverage: 17 Sep 2025 onward (291 activity files at the 28 Sep 2026 rebuild, 39 duplicates flagged, one multisport race split into five legs).
