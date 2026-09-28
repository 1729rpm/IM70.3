# Processed tables

- `activities.csv`: one row per activity file, built by `analysis/build_activities.py`. Rows with `duplicate_of` set are the second copy of a session and are excluded from all totals.
- `weekly.csv`: weeks start Monday. Hours and km exclude duplicates. `tp_shows_h` is what TrainingPeaks displayed, kept to show the inflation.
- `fitness_curves.csv`: one row per month. Run paces are outdoor only, GPS, within a 3 bpm band of the stated HR, after the first 10 minutes. Bike watts per beat uses chest-strap rides at 100 to 112 W steady. Swim pace at HR 128 to 134.

`activities.csv` currently covers 6 Aug to 27 Sep 2026 and will be rebuilt from the full export in the year review. The seed rows in `weekly.csv` and `fitness_curves.csv` come from the 21 to 28 Sep 2026 analysis.
