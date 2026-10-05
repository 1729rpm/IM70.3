# Upcoming workouts

One file per ISO week, `YYYY-Www.md`, written by `analysis/ingest.py` from the planned rows of the TrainingPeaks export (any planned workout dated on or after the ingest date and not yet done). Each entry carries the day, sport, planned minutes, the coach's title and description.

The weekly preview (`reports/YYYY-Www-preview.md`) explains what each session is for and what to protect; the following week's review then judges the week against this file. Files are kept after the week passes so the plan-versus-done history stays complete.
