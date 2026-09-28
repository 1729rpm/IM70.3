# Instructions for Claude

Read this first in every session. It says where things are, what to read for each kind of request, what to write, and how to write it. No athlete facts or numbers live here (they are in athlete.md and config/athlete.yaml), so this file never goes stale.

## Where things are

| Path | Holds | Written by |
|---|---|---|
| `STATE.md` | Where things stand now: days to races, last four weeks, latest markers, benchmark sessions, coming week's plan | `analysis/build_state.py`, never by hand |
| `athlete.md` | Durable facts about Rajat: physiology, gear, fuelling, data quirks | Claude, only when a fact changes |
| `config/athlete.yaml` | Every threshold and cleaning rule, benchmark definitions, race dates, unavailable windows | Claude, when Rajat confirms a change |
| `insights.md` | Conclusions by theme, each dated with evidence and confidence; open questions at the end | Claude, one line per new or changed conclusion |
| `races/` | One file per race (targets, plan, result, lessons) and `pacing-model.md` (the HR-cap method and its evidence) | Claude |
| `plan/` | Coming weeks' planned workouts from TrainingPeaks | `analysis/ingest.py` |
| `reports/` | Weekly reviews and previews, single-session notes, year reviews | Claude |
| `processed/` | Tables: activities, weekly, benchmarks, fitness curves, wellness (see its README) | scripts |
| `raw/` | The small TrainingPeaks CSVs and the activity-file manifest | `analysis/ingest.py` |
| `analysis/` | Scripts (see its README) | Claude |
| `GLOSSARY.md` | Every term used in reports, in plain language | Claude |

## Session start

1. Read `STATE.md` and `athlete.md`. For most requests that is enough.
2. Read `insights.md` when the question asks why, or touches a pattern. Read the relevant `races/` file for race work. Read `config/athlete.yaml` when a threshold matters. Read a `processed/` table only when the question needs numbers STATE.md does not show.
3. Do not read `reports/2026-year-review.md` unless the question is about the year as a whole.

## Request types

### Weekly review (a TrainingPeaks export is attached)
1. `pip install fitdecode pandas numpy pyyaml --break-system-packages`, then `python analysis/ingest.py <zip> --today YYYY-MM-DD`. The script cleans the data, updates every table, writes the plan file and regenerates STATE.md. Read its output for anything it flagged.
2. Read the new STATE.md and the new `plan/` file.
3. Write `reports/YYYY-Www-review.md` using the template below.
4. Add a line to `insights.md` only if a durable conclusion is new or has changed. Edit `athlete.md` only if a fact about Rajat changed. Never edit STATE.md.
5. Commit everything from the session as one commit, message `Week YYYY-Www: review`.
6. In chat: the verdict and the table, then one question if Rajat's input is needed.

### Weekly preview (the coming week's plan, from the same export or pasted)
Write `reports/YYYY-Www-preview.md`: for each session, one sentence on what it trains and why it sits where it does in the block; what to protect so it counts (HR cap, fan, fuel, sleep before it); what would make it a wasted session; and which single session the week cannot afford to lose. Point to `plan/YYYY-Www.md` for the workout text instead of repeating it.

### Single session, already done
Find its row in `processed/activities.csv` (and `benchmarks.csv` if it is a benchmark type), compare with the previous occurrences of the same kind, answer in chat. Write `reports/YYYY-MM-DD-<slug>.md` only if Rajat asks for a file or the session changes a conclusion.

### Single session, upcoming
Purpose, what to ensure, what to watch during it, in chat. No file.

### Race plan (two to three weeks out)
Read `races/pacing-model.md`, the race's file, `athlete.md` and `processed/benchmarks.csv`. Write the plan into the race file under "Plan". Heart rate and feel, never pace. Show the evidence behind every cap and say what is least certain. Commit.

### Race debrief (race activity file attached)
Ingest it like a week. Compare plan against execution in the race file under "Result and lessons". Change `races/pacing-model.md` only if the method itself changed. One line to `insights.md` for anything durable. Commit.

## Writing rules (every report and every file)

1. Write for a smart reader who is not a coach. Explain each term the first time it appears in that document, inside the sentence ("drift, meaning how much heart rate rose while pace stayed the same"). GLOSSARY.md is the reference; it does not excuse a report from explaining itself.
2. One fact lives in one place. The report holds that week's or session's specifics. `insights.md` holds the conclusion as one dated line pointing to the report. `athlete.md` holds the fact about Rajat. Do not restate a report inside insights.md or athlete.md, and do not repeat STATE.md's numbers in a report unless the report is about them.
3. Verdict first. The opening line of every report is the answer in one sentence.
4. Every number carries its trust: wrist or strap HR, indoor or outdoor, how many sessions the claim rests on. Every conclusion carries a confidence (high, medium, low).
5. One session is not a conclusion. Put it under "Open questions" in insights.md and wait.
6. A weekly review fits on one screen: under 600 words plus one table. A preview is shorter. A single-session answer is a few paragraphs.
7. No em dashes. ISO dates, IST times. Plain words, no filler.
8. Before finishing, reread as someone who has never seen this repo: every term explained, nothing said twice, verdict first, numbers trusted correctly.

## Weekly review template

```
# Week YYYY-Www review (DD Mon to DD Mon)

<Verdict in one sentence: ahead, on track or behind for the next race, and why.>

## Planned vs done
| Sport | Planned | Done | Missed sessions |

## What moved
Benchmark sessions compared with their previous occurrence; what improved, what slipped, with the trust of each number.

## Key sessions
Two or three sessions that mattered, each in a few lines: what the coach wanted, what happened, what it says.

## Recovery
Resting HR, sleep, HRV against load, as a trend not a reading.

## Unusual
Anything odd in the data or the week, and one question for Rajat if needed.

## Next week
The session to protect, anything to adjust, anything to raise with the coach.
```

## Rebuilds

- Every week: `ingest.py` with the week's zip. Idempotent; re-uploading a week changes nothing.
- `processed/fitness_curves.csv` needs every activity file, so once a quarter upload the full activity archive from Google Drive and run `ingest.py <archive> --full`.
- If a value in `config/athlete.yaml` changes, rerun `build_benchmarks.py` and `build_state.py`; weekly.csv and the curves need the next full rebuild to reflect it.
