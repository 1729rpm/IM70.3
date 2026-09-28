# Athlete profile: Rajat

Durable facts. Update a line only when the fact changes; keep the old value in brackets with its date. Numbers the scripts use (thresholds, corrections, race dates) live in `config/athlete.yaml`; this file describes, that file computes. Current form and recent weeks are in `STATE.md`, not here.

## Basics
- Age 30, Bangalore. Triathlete, coached on TrainingPeaks (coach builds the plan; Claude analyses and advises).
- Weight 83 kg (Sep 2026). Logged: 78 (Jan 2026), 75 (Feb 2026, stated), 78 (Aug 2026), 83 (Sep 2026); the 81 logged in Oct 2025 is unverified, Rajat says 76 was constant before 2026. Gained about 5 kg between Aug and Sep 2026 after leaving a job. Targets: 78 by mid-Dec 2026, 76 by Feb 2027, 75 for Venice-Jesolo. No calorie deficit until after Goa (1 Nov 2026).
- Runs hot: large drift, most training indoors without a fan or around midday.

## Heart rate
- Run threshold 170 (coach set 168; data brackets 168 to 172; Garmin's 178 is a formula off max HR and is ignored).
- Max HR about 200 (197 seen on a fast 800 m, wrist; the watch profile has crept to 199 to 203 from wrist artefacts and should be set manually).
- Resting HR mid-40s (the 69 in Garmin activity files is a profile placeholder).
- Running: heart rate levels off at constant pace up to about 168 to 172. Above that it climbs 1 to 2.5 bpm per minute at constant speed (treadmill, 20 Sep 2026). Held 164 to 167 for 70 min in the 27 Sep half with no runaway.
- Bike (chest strap): true steady state at 156 to 161 for 2 h (8 Aug 2026); threshold reps top out at 163 to 167; 2 min hard reps peak 172 to 175; the same power indoors at 2 PM creeps 163, 165, 169 (22 Aug). Race bike cap: 150, never above 155.
- Run HR sits about 5 to 8 bpm above bike HR at the same effort.
- Above 170, sustainable time roughly halves per 5 bpm: fresh about 25 min at 175, 12 at 180, 5 at 185; halve those at the end of a half marathon.
- HR recovers well: 26 to 34 bpm drop in 60 s after 2 min hard reps; 12 to 14 bpm in 30 s at run stops.
- The race pacing method built on these numbers is in `races/pacing-model.md`.

## Drift and heat
- Indoor rides lose 9 to 21% efficiency over 2 to 3 h without a fan (HR 134 to 153 at constant power).
- Outdoor runs: 5% drift in evening heat while under-hydrated (23 Sep 2026), 2% in a cool morning race with water at every station (27 Sep). About 11 bpm rise at constant pace over 100 min.
- Cooler by 5 to 6 C is worth 10 to 15 s/km at the same HR.
- Water over head and neck at every aid station is the main cooling tool.

## Fitness markers (Sep 2026)
- Open half marathon 2:21:30 (27 Sep 2026, avg HR 164). Pace at HR 165 about 6:41/km at 22 C.
- Estimated 5K about 28:30 (19 Aug 2026 intervals at 5:40 to 6:03/km, HR reaching 185 to 190).
- Bike: holds about 145 W for 15 to 20 min at HR 156 to 165; FTP estimated 150 to 160 W. Cadence-work efficiency: 106 W at HR 131 (25 Aug) vs 140 (8 Sep, after a 10 day gap).
- Swim: 1,525 m continuous at 2:36/100 m at HR 132 (Aug 2026).
- Run form: cadence 155 to 162 and ground contact about 300 ms at easy pace (8:10/km), 168 to 171 and about 258 ms at 5:45 to 6:45/km. Vertical ratio 10.3% easy, 8.3% fast.
- Garmin VO2max estimate 49.6 (6 Aug) to 45.8 (23 Sep); most of the drop is the weight gain (49.6 x 76/83 = 45.4).

## Gear and devices
- Garmin watch with wrist optical HR; wrist readings have jumped 18 bpm in 20 s and read 25 bpm low on a rep. Garmin HRM-Dual chest strap: slides and is uncomfortable, one 15 s dropout seen. To fix (tighter, electrode gel) or replace with an optical arm band before Goa. Test on two bricks first.
- Indoor rides on a Tacx smart trainer with MyWhoosh (power from the trainer, same setup all year); the watch also records them, hence duplicate uploads. Until Mar 2026 the trainer was in an air-conditioned room in Gurgaon; since Mar 2026 it stands in the Bangalore flat's hall by an east-facing balcony door, ceiling fan only, morning sun on the trainer. Bike HR-at-power numbers before and after Mar 2026 are not directly comparable.
- Swims: Bangalore pool is 25 m (from Mar 2026). Gurgaon pool length unknown.
- Treadmill pace reads 10 to 15% faster than actual.
- Headphones: Sony WH-CH720N, not sweat rated; decided not to race with them (heat over ears).
- Visor preferred over cap (runs hot).

## Fuelling that works
- Bike: about 90 g carbs/h (Unived large gel 180 kcal, 45 g carbs, 228 to 280 mg sodium, plus carb mix), 750 ml to 1 L fluid/h in heat.
- Run: gel every 35 min, salt cap (Unived, 214 mg sodium) 20 min after each gel, water at every station; two caps/h in heat. Small gel 10 to 15 min before the start.
- Race week: maintenance calories (about 2,600 to 2,800), Saturday 450 to 500 g carbs, low fibre, low fat, mild; dinner by 8 PM. Breakfast 2 to 2.5 h before: 100 to 150 g carbs, 500 ml water, 1 salt cap.
- Aid stations cost time when stopping fully in crowds. Carry a 250 to 500 ml soft flask; walk 5 s, two cups, go.

## Calendar
Race dates, targets and unavailable windows: `config/athlete.yaml` (dates) and `races/` (targets and plans).

## TrainingPeaks and Garmin data quirks
- Every MyWhoosh ride uploads twice (11 of 34 ride rows in Aug to Sep 2026). Fix the upload path.
- Run TSS is wrong for the whole year, in two regimes. Sep 2025 to 6 Feb 2026: outdoor runs show IF 1.4 to 1.9 and TSS 200 to 340, which back-solves to a run threshold pace of about 4:35/km. From 7 Feb 2026: IF 2.5 to 3.5 and TSS 500 to 2,800, back-solving to about 2:10/km, so the threshold field was edited on or just before 7 Feb 2026 and made worse. Treadmill runs without GPS fall back to HR-based TSS and look sane. Swim threshold changed on the same date, from about 8:00 to 9:00 per 100 m to about 2:50 to 3:00. Bike FTP in TrainingPeaks has been about 140 W all year. Ask the coach to set run threshold pace about 6:15/km, run LTHR 170, swim threshold about 2:40/100 m; until then the repo uses its own HR load.
- Wellness data (resting HR, HRV, sleep, Body Battery, weight) comes from the TrainingPeaks Metrics Export, not the activity files. Weight is logged only a few times a year.
- The Feb 2026 70.3 is one multisport file with five parts; the scripts split it into one row per part.
