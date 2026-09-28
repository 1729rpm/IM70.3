# Prompts and project instructions

## Claude project instructions (paste into the project settings)

Rajat is a triathlete in Bangalore (30, 83 kg, target 76). Coach on TrainingPeaks. Races: IRONMAN 70.3 Goa 1 Nov 2026 (target 7:00), IRONMAN 70.3 Venice-Jesolo 24 Apr 2027 (target 5:45 to 6:00), open half marathon 1:45 by late 2027. Plans are heart-rate and feel based, never pace. Ignore his logged RPE and feel ratings. Run LTHR 170, max HR about 200, resting HR mid-40s (the 69 in Garmin files is a placeholder). Trust chest-strap HR over wrist. Treadmill pace is 10 to 15% inflated. MyWhoosh rides are often uploaded twice; deduplicate. All processed data, reports and scripts live in the GitHub repo 1729rpm/IM70.3; raw TrainingPeaks exports live in Google Drive and are uploaded in the chat when needed. Before any analysis, read athlete.md and insights.md from the repo and use analysis/load.py and analysis/build_activities.py. Write outputs back to the repo in one commit per session; Rajat makes no manual edits to the repo. Conclude from data, state confidence, flag anomalies and ask about them before concluding. No em dashes.

## Prompt 1: year in review (full export attached)

Attached is my complete TrainingPeaks export from September 2025 to today (workouts CSV plus all activity files). The repo 1729rpm/IM70.3 is connected; read README.md, athlete.md, insights.md and analysis/ first, and commit everything you produce there.

Work in this order and check in with me between steps 2 and 3.

1. Data audit. Run analysis/build_activities.py, then identify duplicate uploads (same ride from MyWhoosh and the watch), wrist vs chest-strap HR, treadmill runs (correct pace by 10 to 15%), indoor vs outdoor, and misconfigured thresholds or TSS. Tell me which sessions are trustworthy for each kind of analysis and exclude the rest. Ignore my RPE and feel ratings.

2. Build processed/activities.csv (one row per session), processed/weekly.csv (hours and km by sport, planned vs completed, corrected load) and processed/fitness_curves.csv (monthly outdoor run pace at HR 150, 155, 160, 165; bike watts per heartbeat at fixed power and fixed HR; swim pace per 100 m at fixed HR; decoupling on long sessions). Commit them. Then list every unusual data point or pattern and ask me about them before drawing conclusions.

3. Analyse. Central question: how does my fitness respond to consistency and how fast does it fade when I stop? Measure the lag between completion rate and the fitness curves, and recovery time after every gap of 7 or more days. Then go wide: detraining curves per sport, cardiac drift by temperature, time of day and indoor vs outdoor, evidence of heat acclimation, intensity distribution vs improvement, load spikes vs the gaps that followed, brick runs vs standalone runs, run economy trends (cadence, ground contact, vertical ratio) vs pace, swim stroke and SWOLF trends, power-duration changes, the eight weeks before each race (Feb 70.3, 27 Sep half) compared, and anything else the data supports that I have not asked for. Behavioural patterns too: which workouts I skip by sport, type, day of week and time of day, and what precedes a skipped week.

4. Deliver: reports/2026-year-review.md with every conclusion tied to evidence and a confidence level, a ranked list of the five changes that would move my fitness most before Venice-Jesolo, and updates to athlete.md, races.md and insights.md. Where the data cannot answer something, say so.

## Prompt 2: weekly check-in (week's export attached)

Attached is this week's TrainingPeaks export. Read athlete.md, insights.md and processed/ from 1729rpm/IM70.3 before starting.

1. Audit the week's files (duplicates, HR source, treadmill), append to processed/activities.csv and weekly.csv, update fitness_curves.csv.
2. Give me the week on one screen: planned vs completed by sport, what moved on the fitness curves, drift and decoupling on key sessions, anything unusual, and one question if you need my input.
3. Compare against the Venice plan and say plainly whether we are ahead, on track or behind, and what next week should protect.
4. Commit the processed files and reports/YYYY-Www.md in one commit. If anything belongs in athlete.md or insights.md, make those edits in the same commit.

Conclude from data, state confidence, flag anomalies. No em dashes.

## Prompt 3: race plan (two weeks out)

Build my race plan for [race, date] from processed/ and athlete.md in 1729rpm/IM70.3. HR and feel based, never pace. I want HR caps for the bike and a km by km line for the run using the same cap logic as my 27 Sep half, a time-based nutrition and hydration schedule, expected splits with ranges and what each depends on, race week and race morning checklists, and the finish rule for when to push. Show the evidence behind each cap, say what you are least sure of, and commit the plan to reports/.

## Prompt 4: race debrief (race file attached)

Attached is the race activity file for [race]. Read races.md and the plan in reports/. Compare plan vs execution km by km (HR, pace, drift, decoupling, fuel timing if logged), state what worked and what to change, update races.md with the result and lessons, add anything durable to athlete.md and insights.md, and commit.
