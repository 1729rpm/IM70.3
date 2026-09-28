# Pacing model

How Rajat's race plans are built. Heart rate and feel, never pace, because pace changes with heat and terrain while heart rate reflects the effort actually being spent. The method below was executed within 2 bpm for 21 km on 27 Sep 2026 and produced a negative split with the fastest kilometre last. Numbers here are the method's; the athlete's thresholds are in `config/athlete.yaml`.

## Open half marathon (cool morning)
- Cap = 155 + km number until km 10 (156 at km 1, 164 at km 9). Sit 2 to 4 bpm under the cap for these kilometres.
- Km 10 to 20: flat cap at 165. Evidence: 70 min at 164 to 167 with 2% drift and no runaway; longest continuous stretch at 165 or above was 17.5 min against 1.7 min in training. Next time the cap can rise to 168 from km 14 (the 5:57 last kilometre says 1 to 2 min were left).
- Km 10 check: if a short sentence is impossible, drop every remaining cap by 3.
- Finish rule: 170 with 3 km to go, 173 with 2, 177 with 1, no cap for the last 500 m.
- Aid stations: carry a soft flask, walk 5 s, two cups, go; stopping fully in crowds cost time.

## 70.3 (heat, off the bike)
- Bike: average heart rate under 150, never above 155. Evidence: true steady state at 156 to 161 for 2 h on the trainer; a 3:15 bike at HR 148 in Feb 2026 left a flat 2:28 run at HR 152.
- Run: 155 to 160 in Goa heat, which is the fresh, cool equivalent of the 165 open-half line after 10 to 12% for the bike and 5 to 8% for heat. Hold the first 2 km off the bike 20 s/km slower than it feels (bricks show a fast start and an 8% fade).
- Fuel and cooling as in athlete.md ("Fuelling that works"); two salt caps an hour in heat.

## Time budget above threshold
Roughly halves per 5 bpm: fresh about 25 min at 175, 12 at 180, 5 at 185; halve those at the end of a half marathon. Low to medium confidence, wrist data at the top end. Used only for the finish rule.

## What each cap depends on
- A working chest strap or arm band; wrist HR cannot be paced against (jumps of 18 bpm seen).
- Temperature: each 5 to 6 C cooler is worth 10 to 15 s/km at the same heart rate, so time targets carry ranges and the caps do not.
- Hydration and salt, which decided the second half on 23 vs 27 Sep 2026.
