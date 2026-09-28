# Raw inputs kept in the repo

The activity files (.fit) are large and live in Google Drive (Training/raw). Everything else TrainingPeaks exports is small text and is kept here so every processed table can be rebuilt without the zips:

- `workouts.csv`: every row from every TrainingPeaks workouts export, planned and completed, deduplicated. Seeded on the first ingest; grows each week.
- `metrics.csv`: every row from every TrainingPeaks Metrics Export (resting HR, HRV, sleep, Body Battery, weight), deduplicated.
- `fit_manifest.csv`: name, size and hash of every activity file ever ingested. `analysis/ingest.py` skips files already listed, so re-uploading a week is harmless.

First weekly upload after this restructure: export from 17 Sep 2025 to two weeks ahead once, so `workouts.csv` and `metrics.csv` cover the whole history. After that, one week at a time (last Monday to next Sunday) is enough.
