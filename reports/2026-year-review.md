# 2026 year in review (17 Sep 2025 to 27 Sep 2026)

Consistency, not fitness, decided the year: only 14 of 43 planned weeks reached 80% of the sessions the coach planned, every fitness marker rose and fell with the training gaps about four to six weeks later, and the half marathon on 2026-09-27 was run on half the run hours and 8 kg more body weight than the February 70.3.

## How to read this report

Written 2026-09-28 from the full TrainingPeaks export: 291 activity files, 592 TrainingPeaks rows and 13 months of Garmin daily metrics (resting heart rate, sleep, heart-rate variability, weight). The tables behind it are `processed/activities.csv`, `weekly.csv` and `fitness_curves.csv`. Rajat's own effort and feel ratings were ignored; only recorded data was used.

Two things sit under every number in this report:

- **Which sensor.** Heart rate came from the watch's wrist sensor on 85 of 89 runs and on every swim, and from a chest strap on 48 of 90 rides. Wrist readings can jump 15 to 25 bpm for no reason and read poorly in water, so every run and swim conclusion carries less trust than the bike ones. Each figure below says wrist or strap.
- **Where.** Indoor means the smart trainer with MyWhoosh (power measured by the trainer) or the treadmill (which reads 10 to 15% faster than reality; every treadmill pace here has been slowed to correct for that). Outdoor means GPS.

Each conclusion carries a confidence: high, medium or low. Medium usually means the direction is clear but the size is blurred by something else that changed at the same time (weight, heat, the move to Bangalore).

Durable facts about Rajat (thresholds, weight history and targets, gear, the training room, fuelling, data quirks) live in `athlete.md` and are pointed to rather than repeated. The conclusions of this review are also listed as dated one-liners in `insights.md`; this report is the evidence behind those lines.

## 1. The year in one paragraph

"Completion" means the share of planned sessions that were actually done. "Real hours" means training time after removing the duplicate copy of every indoor ride (section 11). Real training was 6.5 h/week from Sep to Dec 2025 at 70 to 100% completion; 4.5 h/week from Jan to Mar 2026 (a good January, then a 38-day stop after the 70.3 on 2026-02-14; a 70.3 is a half-distance triathlon of 1.9 km swim, 90 km bike and 21.1 km run); 3.9 h/week from Apr to Jun at 44% completion (the move from Gurgaon to Bangalore, then two more gaps); and 4.8 h/week from Jul to Sep at 41%. Only 14 of 43 planned weeks reached 80% completion. Fitness is measured in this repo by "curves": monthly figures that hold one thing fixed, such as how fast Rajat ran in the moments his heart rate was exactly 160, or what his heart rate was while pushing a fixed 106 W on the bike. A lower heart rate at the same output, or more output at the same heart rate, means fitter. Fitness followed consistency with a four to six week lag: the best month on every curve was January 2026, after the Oct to Jan block; the worst was April, after the 38-day gap; July got back to January's run numbers at 3 kg more body weight; Aug to Sep slipped again after two gaps of 7 and 11 days. Weight went 78 kg (Jan) to 75 (Feb) to 78 (Aug) to 83 (Sep). The half marathon on 2026-09-27 (2:21:30 at an average heart rate of 164) was run on 39% completion and 11.8 run hours in the eight weeks before it; the February 70.3 (5:39) was built on 68% completion and 68 total hours in its eight weeks.

## 2. Central question: how fitness responds to consistency, and how fast it fades

### Evidence

One row per month. "Run pace at HR 160" is the pace Rajat held in the moments his heart rate was 160, from outdoor GPS runs with wrist heart rate; paces are minutes:seconds per km. "Bike HR at 106 W" is his heart rate while the trainer read 106 W, and "Bike W at HR 133" his power while his heart rate was 133, both from indoor MyWhoosh rides with a chest strap. Weight is in kg.

| Month | Completion | Real h/wk | Run pace at HR 160 | Run pace at HR 165 | Bike HR at 106 W | Bike W at HR 133 | Weight |
|---|---|---|---|---|---|---|---|
| Oct 25 | 88% | 9.0 | (treadmill only) | | | | 81? |
| Nov 25 | 67% | 5.9 | | | | | |
| Dec 25 | 48% | 4.1 | | | | | |
| Jan 26 | 80% | 10.4 | 6:12 | 5:56 | | 134 | 78 |
| Feb 26 | 40% | 5.8 | 6:24 | 6:28 | 116 | 134 | 75 |
| Mar 26 | 24% | 1.0 | | | | | |
| Apr 26 | 29% | 3.1 | | | 139 | 75 | |
| May 26 | 7% | 0.7 | | | | 80 | |
| Jun 26 | 49% | 6.5 | | | 132 | 79 | |
| Jul 26 | 46% | 7.3 | 6:06 | 5:58 | 134 | 104 | |
| Aug 26 | 37% | 4.0 | 7:17 | 6:41 | 119 | 126 | 78 |
| Sep 26 | 35% | 5.3 | 6:59 | 6:31 | 138 | 110 | 83 |

A blank run cell means the month had fewer than 300 outdoor heart-rate readings in that band, too few to trust (Oct to Dec 2025 was almost all treadmill). The January run figures include the duathlon on 2026-01-11 (5 km run, 40 km bike, 10 km run); a race run at a steady heart rate belongs in the curve, but it lifts January a little.

### Conclusions

- **It takes about four to six weeks for consistency to show in the curves.** January's numbers follow the Oct to Jan block; July's follow the 49% and 46% months of June and early July; the Aug to Sep drop follows the low stretch from 2026-07-20 to 2026-09-07 (two gaps, weeks at 11 to 43% completion). Medium confidence: 13 monthly points, with two other things changing at the same time (weight and the Bangalore heat).

- **The 38-day gap (2026-02-14 to 2026-03-24) cost a lot, and more on the bike than the run.** Run pace at heart rate 150 went from 6:59/km in February to 8:23 in late March, about 20% slower (outdoor, wrist). Bike heart rate at 106 W went from 116 to 139 bpm, and power at heart rate 133 from 134 W to 75 W, about 45% less power at the same heart rate (indoor, strap). Swim pace at heart rate 130 barely moved (2:31 to 2:25 per 100 m), but wrist heart rate in water is weak evidence. Medium-high confidence on the direction, medium on the size: the February bike numbers were taken fresh after the race taper (the easy fortnight before a race), and the April ones are the first hot Bangalore rides after the trainer left the air-conditioned Gurgaon room (`athlete.md`, gear), so the two are not a clean pair.

- **The run took 12 to 14 weeks of interrupted training to come back; the bike has not.** Run pace at heart rate 160 and 165 was back to January's values by July (6:06 and 5:58 against 6:12 and 5:56; outdoor, wrist) at about 78 kg. Bike power at heart rate 133 was still 110 W in September against 134 W in January (indoor, strap). Part of that gap is heat (section 4), part is lost fitness, and the September number sits between the two. Medium confidence.

- **Shorter gaps cost less, but they add up.** The 7-day gap ending 2026-08-06 and the 11-day gap ending 2026-09-07 each pushed heart rate at 106 W up (119 in August to 138 in September across the second gap; strap) and run pace at heart rate 165 out by 30 to 45 s/km (5:58 in July to 6:41 in August; wrist). After the 11-day gap, the race on 2026-09-27 (6:41/km at heart rate 165 in 22 C) shows a return to near-August form within three weeks. Medium confidence.

- **Each kilogram is worth roughly 6 to 8 s/km at a fixed heart rate on this data.** Between July (about 78 kg, 6:06 at heart rate 160) and September (83 kg, 6:59 at heart rate 160, in hotter evening sessions) the change in pace is too large to be weight alone; the race (6:41 at 165 on a cool morning) is the cleaner point and gives the smaller figure. Low-medium confidence, because heat, time of day and the gaps all overlap with the weight change.

### What the data cannot answer

Whether the bike responds to consistency faster than the run. The bike curve is muddied by the change of training room in March 2026, and there is no bike test or race with power to anchor it.

## 3. Behaviour: what gets skipped and when

From 561 planned TrainingPeaks sessions between Sep 2025 and Sep 2026. These are session counts, so no sensor question applies.

- **By sport:** bike 62% completed, run 49%, swim 42%, cross-training 54%. Long sessions were not skipped more than short ones (bike 61% long against 63% short, run 52% against 49%).
- **By day and sport:** Monday runs 23%, Sunday swims 4%, Saturday bikes 41%, Friday swims 32%. Everything on Monday and Sunday except the bike is weak. Tuesday to Thursday sit at 60 to 70%. High confidence, large sample.
- **Time of day actually trained** (IST): 88% of swims started after 17:00. Rides and runs split roughly 40% before 09:00, 25% midday and 30% after 17:00. The evening runs in Bangalore had the worst drift, meaning how much heart rate rose while pace stayed the same, comparing the second half of a session with the first: 7.5% on 2026-09-07 at 30 C and 5.5% on 2026-09-23 (outdoor, wrist).
- **What comes before a skipped week** (a week under 40% completion): the week before it averaged 51% completion and an HR load of 233, against 59% and 338 for the year as a whole. HR load is the repo's measure of how hard a week was: hours multiplied by the square of (average heart rate divided by threshold heart rate), times 100, where threshold heart rate is the highest heart rate holdable for about an hour; one steady hour at threshold scores 100. Low weeks follow low weeks; the pattern is a slide, not a crash after a spike. The only gap that followed a jump in load was 2026-04-17 to 2026-04-28, when the previous week was 2.2 times the four-week average (the first full week back in Bangalore). The 38-day gap followed the race with no spike before it. High confidence on the pattern, medium on the cause.

## 4. Drift, heat and adapting to it

Drift (defined in section 3; TrainingPeaks calls it decoupling) is the main heat signal in the data.

- **Indoor rides drift 12% (the median of 36 rides longer than 60 minutes; strap); outdoor rides 12%; outdoor runs 3%; treadmill runs 2.5% (wrist).** The bike drift did not start in Bangalore: Oct 2025 rides in the air-conditioned Gurgaon room show 20% (three rides), January 2026 10%, the Bangalore months 11 to 18%. So a large part of the bike drift is Rajat's physiology at 2 to 3 hours, not only the room. Medium-high confidence.
- **Time of day:** indoor rides before 09:00 drift 12%, midday 9%, after 13:00 10%; no clean heat-of-day signal indoors (strap). Outdoors, the three cool early runs at 27 C (2026-07-22, 2026-07-30, 2026-09-27) drifted 0.9 to 2%; the evening runs at 28 to 30 C drifted 5.5 to 7.5%; the 08:00 runs at 27 to 30 C sat at 4 to 6% (2026-08-19, which had intervals, and 2026-09-16). The watch only records temperature from June 2026, so the Gurgaon winter runs have no reading. Medium confidence, wrist.
- **Heat adaptation:** indoor ride drift by month in Bangalore went 18.5% (Apr), 13.5% (Jun), 11.3% (Jul), 12.4% (Aug), 10.6% (Sep). Bike heart rate at 106 W did not follow a clean line (139, 132, 134, 119, 138). The drift trend fits partial adaptation over the summer; the heart-rate-at-power series says any adaptation is smaller than the effect of the gaps. Low-medium confidence, strap.

The training room itself is described in `athlete.md` (gear); what to change in it is change 5 in section 12.

## 5. Intensity mix

Share of all heart-rate readings across all sports, weighted by time, in three bands: easy below 140 bpm, moderate 140 to 159, hard 160 and above. Mixed wrist and strap.

| Period | Easy | Moderate | Hard |
|---|---|---|---|
| Sep to Nov 2025 | 70% | 24% | 5% |
| Dec 2025 to Feb 2026 | 55% | 41% | 5% |
| Mar to May 2026 | 52% | 36% | 11% |
| Jun to Aug 2026 | 50% | 37% | 13% |
| Sep 2026 | 39% | 37% | 24% (includes the race) |

The block that produced the best curves (Dec to Feb) was 55/41/5: lots of steady moderate work and very little above 160. The Bangalore months doubled the hard share while cutting total hours by a third. At 4 to 5 h/week with a quarter of it above heart rate 160, that is a high-intensity, low-volume pattern, and the curves did not reward it. Medium confidence: the bands use the same cut-offs for every sport, and bike heart rate runs 5 to 8 bpm lower than run heart rate at the same effort.

## 6. Running off the bike

A brick is a run started within 45 minutes of finishing a ride; it trains the legs for the run leg of a triathlon. Of 89 runs, 15 were bricks. Outdoor bricks averaged heart rate 153 at 6:48/km with 8.4% drift; outdoor standalone runs averaged heart rate 148 at 7:30/km with 2% drift (wrist). Rajat runs faster off the bike, at a higher heart rate, and fades more. The 7 indoor bricks show heart rate 138 at 8:12/km after the treadmill correction, so the treadmill bricks were run truly easy. For Goa the outdoor pattern (fast start, 8% fade) is the one to reverse: hold the first 2 km off the bike 20 s/km slower than it feels. Medium confidence, small sample.

## 7. Running form

Three form numbers from the watch: cadence (steps per minute), ground contact (how long each foot stays on the ground, in milliseconds) and vertical ratio (how much of each stride goes up rather than forward, in percent). Higher cadence, shorter contact and lower vertical ratio are more economical. Taking outdoor runs at 6:30 to 7:00/km and the median for each month: cadence 164, contact 282 ms and vertical ratio 9.4% in Jan to Feb 2026 (at 75 to 78 kg, heart rate 150); cadence 168 to 170, contact 274 to 277 ms and vertical ratio 9.2 to 9.3% in Jun to Sep 2026 (heart rate 147 to 163). Form at a fixed pace improved slightly over the year while heart rate at that pace has gone up 10 to 13 bpm since July. So the lost economy is metabolic (weight, heat, less training), not mechanical. Medium confidence: wrist heart rate, and the September runs were hotter.

## 8. Bike power over different durations

For each month, the best average power Rajat held for 5, 20 and 60 minutes in any MyWhoosh ride, in watts (indoor, trainer power). FTP, functional threshold power, is the bike equivalent of threshold heart rate: the highest power holdable for about an hour.

| Month | 5 | 20 | 60 |
|---|---|---|---|
| Oct 25 | 199 | 148 | 110 |
| Jan 26 | 182 | 149 | 134 |
| Feb 26 | 164 | 143 | 126 |
| Apr 26 | 200 | 160 | 121 |
| Jul 26 | 168 | 148 | 130 |
| Aug 26 | 188 | 166 | 139 |
| Sep 26 | 148 | 133 | 114 |

Best 20 min effort of the year is 166 W (Aug 2026); best 60 min is 139 W (Aug). These came from training sessions, not tests, so they understate what he can do. An FTP of 150 to 160 W fits them. The August peak came from the 3 h 70.3 Build rides and the threshold work on 2026-08-22; September fell with the 11-day gap. Medium confidence, no test protocol.

## 9. Swim

Pace per 100 m in the moments heart rate was 128 to 134 (wrist, which reads poorly in water): 2:13 to 2:15 in Sep to Oct 2025 (Gurgaon pool, length unknown); 2:41 to 2:43 in Nov to Dec; 2:31 to 2:34 in Jan to Feb (February includes the race's open-water swim at 2:23 for 1.8 km); 2:25 to 2:30 in Mar to Jun in the Bangalore 25 m pool; 2:38 in August. The Sep to Oct 2025 figure is probably an artefact of pool length (the watch counting lengths in a longer pool as if they were shorter), so the usable series starts in November and is roughly flat at 2:25 to 2:40. With 67 swims in the year, 42% completion and 4% of Sunday swims done, there was never a block long enough to move the swim. Stroke count and SWOLF (strokes plus seconds for one length, a single efficiency score) are in the per-length records and have not been extracted yet. Low-medium confidence throughout.

## 10. The eight weeks before each race

| | Feb 70.3 (2026-02-14) | Bengaluru half (2026-09-27) |
|---|---|---|
| Total real hours | 67.9 | 38.3 |
| Bike / run / swim hours | 37.9 / 17.6 / 12.7 | 23.0 / 11.8 / 3.5 |
| Sessions | 58 | 31 |
| Planned completion | 68% | 39% |
| HR load per week | 600 | 344 |
| Longest run before race | 11.1 km (plus the 2026-01-11 10 km) | 13.0 km (4 days out) |
| Longest ride | 3.2 h | 3.2 h |
| Runs | 17 | 11 |
| Weight | 75 | 83 |
| Race run | 21.0 km in 2:28:30 at HR 152, 1.4% drift | 21.1 km in 2:21:30 at HR 164, 2% drift |

The February run, off a 3:15 bike in the sun at heart rate 148, was 7:03/km at heart rate 152. The September open half (a standalone running race, not the run leg of a triathlon) was 6:41/km at heart rate 164, 8 kg heavier, on half the run hours. Rajat's pace at a given heart rate was probably 30 to 40 s/km better in February than in September once the bike fatigue is removed; that matches the curves (6:24 at heart rate 160 in February, 6:59 in September). High confidence on the comparison, medium on the 30 to 40 s figure.

## 11. Data-quality findings that change how the year should be read

- The run load number TrainingPeaks computes (TSS) is unusable all year because the run threshold pace in Rajat's TrainingPeaks profile is wrong, in two different ways before and after 2026-02-06 (the mechanics are in `athlete.md`, data quirks). `weekly.csv` carries the HR load from section 3 instead. High confidence.
- 39 of the 291 files are duplicate uploads: every MyWhoosh ride is also recorded by the watch. TrainingPeaks weekly hours were inflated 30 to 90% in bike-heavy weeks. The scripts keep the copy with power. High confidence.
- The two highest wrist readings of the year, 197 and 199 bpm (2026-08-19 and 2026-09-20), rose gradually (no jump above 6 bpm per second), came at 5:04 to 5:35/km, and stayed above 185 for 7 and 3.6 minutes. That fits real values near a true maximum of about 200, not sensor spikes. Medium confidence, wrist.
- Garmin resting heart rate medians sat at 47 to 51 for ten months, then 56.5 in Aug 2026 and 62 in Sep. Rajat attributes the rise to alcohol with no other change. Weight (plus 5 kg since August) and fewer nights with the watch on (16 to 19 readings a month against 25 to 31) also contribute. Whatever the cause, a 10 to 15 bpm rise in resting heart rate is the largest change in any wellness series this year, and it began before the poor Aug to Sep training. Worth tracking weekly. Medium confidence on the size, low on the cause.
- Sleep medians 6.4 to 7.0 h except Apr to May 2026 (5.2 to 5.6 h, late-night TV, few readings). HRV (heart-rate variability, the variation between beats measured overnight; higher usually means better recovered) drifted from 43 to 48 in Sep 2025 to Jan 2026 down to 38 to 41 in Jun to Sep 2026. Low-medium confidence, sparse recent data.

## 12. Ranked: the five changes that would move fitness most before Venice-Jesolo (2027-04-24)

1. **Make Monday, Friday and Sunday sessions survivable, or move them.** Monday runs 23% done, Sunday swims 4%, Friday swims 32%. Ask the coach to put the week's two hardest sessions on Tuesday to Thursday (60 to 70% completion) and make the Monday and Sunday slots short and easy, or move the swim to a weekday morning. Completion is the single biggest lever in the data, and the losses sit on three days.
2. **No gap longer than 4 days between now and Venice**, including the three windows already marked unavailable in `config/athlete.yaml` (Diwali, December, the wedding week). Every gap of 7 or more days cost 3 to 6 weeks; the 38-day one cost a quarter of the year. Running and gym are possible in all three windows. A 30-minute run every third day through them keeps the run curve where it is.
3. **Return to 76 kg by February.** Independent of training, each kilogram is worth several s/km at a fixed heart rate (section 2), and it moves the watch's VO2max estimate (its guess at aerobic capacity per kilogram of body weight, which falls when weight rises even if fitness has not) back to 49 to 50. The staged targets and the no-deficit rule before Goa are in `athlete.md`.
4. **Rebalance intensity toward the Dec to Feb pattern:** 55% easy, 40% moderate, 5% hard, at 8 to 10 h/week. The current 40/37/24 at 5 h/week produced the worst curves of the year. Mostly the coach's call; the evidence is section 5.
5. **Fix the bike environment and get a real FTP number.** Fan on the torso, curtain closed, ride before 08:00. Then a 20-minute test in October so the Venice bike target (185 to 195 W) has a baseline; the best training 20 minutes this year is 166 W.

Not in the top five but cheap: a chest strap or arm band on every run (85 of 89 were wrist), fix the run threshold in TrainingPeaks, stop the double upload.

## 13. Open questions

The questions this data cannot settle (the true FTP, whether April's bike loss was mostly heat, the cause of the resting heart rate rise, the Gurgaon pool length, the 2026-01-11 duathlon result) are tracked under "Open questions" in `insights.md` and are not repeated here.
