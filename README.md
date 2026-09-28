# IM70.3: training data and analysis

Everything Claude produces from Rajat's TrainingPeaks and Garmin data lives here. Raw exports live in Google Drive (Training/raw) and are uploaded in the chat when an analysis needs them.

## Layout

| Path | What | Who writes it |
|---|---|---|
| `athlete.md` | thresholds, weights, zones, gear, data quirks | Claude, when something durable changes |
| `races.md` | every race: targets, actuals, splits, lessons | Claude, after each race |
| `insights.md` | dated conclusions with evidence and confidence; superseded lines struck through, never deleted | Claude |
| `prompts.md` | the prompts used to start each kind of chat, plus the Claude project instructions | Claude |
| `analysis/` | FIT parsing, steady-state detection, activities builder | Claude |
| `processed/activities.csv` | one row per session | `analysis/build_activities.py` |
| `processed/weekly.csv` | hours, km, planned vs completed, HR-based load, gaps, by week | `analysis/build_tables.py` |
| `processed/fitness_curves.csv` | monthly fitness proxies: run pace at fixed HR, bike watts per beat, swim pace at fixed HR, resting HR, HRV, sleep, weight | `analysis/build_tables.py` |
| `reports/` | one markdown per analysis or week, `YYYY-Www.md` or `YYYY-MM-DD-<race>.md` | Claude |

## Weekly loop

1. Rajat exports the week from TrainingPeaks (workouts CSV plus Workout File Export) and uploads the zips in a new chat using the weekly prompt in `prompts.md`.
2. Claude audits the files (duplicates, HR source, treadmill), appends to `processed/`, writes `reports/YYYY-Www.md`, updates `athlete.md` or `insights.md` if warranted, and pushes one commit.
3. Rajat makes no manual edits here.

## Conventions

- Times are IST. Dates are ISO.
- Plans are heart-rate and feel based, never pace. Logged RPE and feel ratings are ignored.
- Chest-strap HR is trusted; wrist HR is used with caution (see `athlete.md`).
- Treadmill pace is inflated 10 to 15%; corrected by 12% in `build_activities.py`.
- MyWhoosh rides are often uploaded twice (MyWhoosh file plus watch file). The MyWhoosh file (has power) is kept, the watch copy is flagged `duplicate_of`.
- No em dashes in any document.

## Setup for analysis (Claude's container)

```
pip install fitdecode pandas numpy --break-system-packages
python analysis/build_activities.py <folder of FIT files> processed/activities.csv --tp-csv <workouts.csv>
python analysis/build_tables.py <folder of FIT files> processed/activities.csv <workouts.csv> <metrics.csv> processed
```
