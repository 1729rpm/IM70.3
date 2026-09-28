# Prompts

## Claude project instructions (paste into the project settings, nothing else)

Read INSTRUCTIONS.md in the GitHub repo 1729rpm/IM70.3 before doing anything, then follow it.

## Then just say what you want

- "Here's last week." (with the TrainingPeaks zip attached) -> weekly review
- "What's next week for?" -> weekly preview, from the same zip's planned rows
- "Review Saturday's long ride." -> single session, done
- "What is Thursday's session for and what should I make sure of?" -> single session, upcoming
- "Plan Goa." -> race plan
- "Here's the race file." -> race debrief
- "Why has my resting HR gone up?" -> question; Claude reads insights.md and the tables

## Twice a year or when starting fresh

"Here is the full activity archive from Drive. Rebuild everything." -> `ingest.py <archive> --full`, which regenerates the monthly fitness curves that need every file.
