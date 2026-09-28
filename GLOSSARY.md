# Glossary

Plain-language meanings of the terms used in this repo, and how each is used here. Reports still explain a term the first time they use it; this is the reference.

**Threshold heart rate (LTHR).** The highest heart rate you can hold for about an hour of hard, steady effort. Above it, effort gets unsustainable fast. Each sport has its own value (running highest, cycling lower) in `config/athlete.yaml`. It anchors everything else here: zones, load, race caps.

**Cap.** A heart-rate ceiling for part of a race or session. Rajat races to caps, not paces, because pace changes with heat and terrain while heart rate reflects actual effort.

**Drift (decoupling).** How much heart rate rises while pace or power stays the same, comparing the second half of a session with the first, in percent. Low drift (under 5%) means the effort was well within aerobic fitness and the athlete was fuelled and cool. High drift (over 10%) means heat, dehydration, going too hard, or simply not enough endurance for that duration yet. Indoor rides without a fan drift a lot for everyone.

**HR load.** The measure of how hard a week was, replacing TrainingPeaks' broken TSS number. Hours multiplied by (average heart rate divided by threshold heart rate) squared, times 100. One steady hour at threshold scores 100. Rajat's good weeks score 550 to 800.

**TSS, IF (TrainingPeaks).** TrainingPeaks' own load and intensity numbers. Wrong for Rajat's runs and swims all year because the thresholds in his TrainingPeaks profile are misconfigured. Ignored here.

**Completion.** Planned sessions that were actually done, as a count or percent. The single biggest driver of Rajat's fitness in the data.

**Gap.** Seven or more consecutive days without training. Each one has cost weeks of fitness.

**Benchmark session.** A kind of session that repeats often enough to compare over time (an outdoor easy run, an indoor ride with power and chest strap, a swim of 1,500 m or more). Definitions live in `config/athlete.yaml`; occurrences in `processed/benchmarks.csv`. The right way to see week-to-week change.

**Fitness curve.** A monthly figure that holds one thing fixed to reveal fitness: run pace at a fixed heart rate, bike heart rate at a fixed power, swim pace at a fixed heart rate. Lower heart rate at the same output, or more output at the same heart rate, means fitter. Needs a whole month of second-by-second data, so it refreshes only on a full rebuild.

**Brick.** A run started within 45 minutes of finishing a ride. Trains the legs for the run leg of a triathlon. Rajat runs faster, hotter and fades more in bricks than in standalone runs.

**Negative split.** Second half faster than the first. The sign of a well-paced race.

**Steady state.** Heart rate levelling off at a constant pace or power. Above threshold it never levels off; it keeps climbing (runaway).

**Easy, moderate, hard.** Heart-rate bands used for the intensity mix: below 140, 140 to 159, 160 and above, across all sports. The best training block of the year was 55% easy, 40% moderate, 5% hard.

**FTP.** The bike equivalent of threshold: the highest power holdable for about an hour, in watts. Estimated 150 to 160 W for Rajat; no formal test yet.

**Normalized power.** A ride's power averaged in a way that weights hard surges more, so a variable ride compares with a steady one.

**Resting HR, HRV.** Morning heart rate and heart-rate variability from the watch. Trends over weeks matter, single days do not. Rajat's resting HR is normally mid-40s; a rise of 10 bpm or more over weeks is the most important recovery signal in his data.

**Body Battery.** Garmin's 0 to 100 recovery estimate. Used only as a rough flag.

**VO2max estimate.** Garmin's guess at aerobic capacity per kilogram of body weight. It falls when weight rises even if fitness has not changed, so read it with the weight column.

**Cadence, ground contact time, vertical ratio.** Running form numbers: steps per minute, how long each foot stays on the ground (milliseconds), and how much of each stride goes up rather than forward (percent). Higher cadence, shorter contact and lower vertical ratio are more economical.

**Wrist HR vs strap HR.** The watch's optical sensor versus a chest strap. Wrist readings can jump by 15 to 25 bpm for no reason, so any conclusion built on wrist data says so and carries lower confidence.

**Treadmill correction.** The treadmill reports pace 10 to 15% faster than reality; all treadmill paces here are slowed by 12%.

**Duplicate upload.** Every indoor ride on MyWhoosh reaches TrainingPeaks twice (MyWhoosh file plus watch file). The scripts keep the copy with power and flag the other, so hours and load are not double-counted.

**Multisport file.** A race recorded as one file with five parts: swim, transition 1, bike, transition 2, run. Split into one row per part in the tables.

**A race, B race.** A race is the target the season is built around; a B race is a test on the way.
