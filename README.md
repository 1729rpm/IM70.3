# IM70.3: Rajat's training hub

Everything Claude produces from Rajat's TrainingPeaks and Garmin data lives here: cleaned tables, weekly reviews, race plans and the conclusions drawn from them. Rajat's coach plans in TrainingPeaks; this repo is the analysis layer alongside.

Start with `INSTRUCTIONS.md` (how sessions work and where everything is) and `STATE.md` (where things stand right now). Terms are in `GLOSSARY.md`.

## Layout

| Path | What |
|---|---|
| `INSTRUCTIONS.md` | Operating rules for Claude, per request type |
| `STATE.md` | Generated snapshot: races, last four weeks, latest markers, benchmark sessions, coming plan |
| `athlete.md` | Durable facts about Rajat |
| `config/athlete.yaml` | Every threshold and rule the scripts use |
| `insights.md` | Conclusions by theme, dated, with confidence |
| `races/` | One file per race plus the pacing method |
| `plan/` | Upcoming workouts, one file per week |
| `reports/` | Weekly reviews and previews, session notes, year reviews |
| `processed/` | Cleaned tables |
| `raw/` | Small TrainingPeaks CSVs and the activity-file manifest (the .fit files stay in Google Drive) |
| `analysis/` | Scripts |

## Weekly loop

1. Rajat exports from TrainingPeaks: date range from last Monday to next Sunday, workouts CSV plus the workout file export (and the Metrics export). One zip.
2. In a new chat he attaches it and says what he wants ("here's last week", "what is Thursday's session for", "review Saturday's ride").
3. Claude runs `analysis/ingest.py`, which cleans the data once (duplicates, treadmill pace, HR source), updates every table, writes the plan file and regenerates STATE.md. Then Claude writes the review or answer and commits once.
4. Rajat makes no manual edits here.

## Conventions

IST, ISO dates, heart rate and feel rather than pace, chest strap trusted over wrist, no em dashes. The numbers behind these live in `config/athlete.yaml`, not in prose.
