# Bundesliga Elo ratings (1993–2018)

A running strength rating for every Bundesliga football club across 25
seasons — enough to read the league's whole history off a single chart,
and accurate enough to genuinely forecast match results.

This uses Elo, the same rating system used for chess rankings, and it's
refreshingly simple: every club starts at the same rating, and after each
match the winner takes rating points from the loser. How many points
change hands depends on how surprising the result was — beating a much
stronger team moves your rating a lot, beating a much weaker one barely
moves it at all. That's the whole idea.

## 25 years in one chart

![Elo trajectory](images/elo_trajectory.png)

Season-average rating for six clubs. The whole story of the league is
visible here:

- **Bayern Munich** are consistently strong, then pull decisively ahead of
  everyone else starting around 2012 — the Pep Guardiola era, peaking at a
  rating of about 1750.
- **Dortmund** dip in the mid-2000s (their near-bankruptcy years), then
  surge back with the Jürgen Klopp title-winning sides around 2011-12.
- **Kaiserslautern** win the title in 1998, then decline and eventually
  drop out of the league entirely (the line stops where they're relegated).
- **Hamburg**'s long, slow decline runs all the way to their first-ever
  relegation from the top division, in 2018.

The six strongest single seasons in the entire 25 years, by rating, are
all Bayern Munich, back to back from 2012-13 through 2017-18 — a way of
putting a number on just how dominant that period was:

| team-season | average rating |
|---|---:|
| Bayern Munich 2013-14 | 1747 |
| Bayern Munich 2014-15 | 1731 |
| Bayern Munich 2015-16 | 1719 |
| Bayern Munich 2016-17 | 1718 |
| Bayern Munich 2017-18 | 1716 |
| Bayern Munich 2012-13 | 1692 |

## Does it actually predict anything?

A rating history is only worth building if the ratings genuinely forecast
real results, not just tell an interesting story after the fact. Checked
directly: grouping every match by what the rating system predicted for the
home team, and comparing that to what actually happened, the two line up
almost perfectly — when the system predicts the home side should get about
65% of the available points, they actually do, on average, get about 65%:

![calibration](images/calibration.png)

And the favourite in any given match wins about as often as you'd expect
in a sport where draws are common (this excludes the very first season,
while ratings are still settling in from everyone starting at the same
value):

| outcome | rate |
|---|---:|
| Rated favourite wins outright | 49.9% |
| Draw | 25.6% |
| Underdog wins (an upset) | 24.5% |
| *(for comparison, always guessing the home team wins)* | *46.8%* |

Roughly half the time the favourite wins, a quarter of the time it's a
draw, and a quarter of the time there's an upset. Football simply isn't
that predictable, and an honest rating system shouldn't pretend otherwise.

### Biggest upsets

The matches with the largest rating gap where the favourite still lost —
almost all of them Bayern Munich defeats, simply because Bayern held by
far the biggest rating advantages of any club, so their rare losses were
mechanically the biggest surprises. Notice how many happened on the very
last matchday of a season, when a team that's already won the title tends
to rest its best players:

- 2013-14: **Augsburg** beat Bayern Munich (a big underdog win)
- 2014-15: **Freiburg** beat Bayern Munich
- 2012-13: **Hoffenheim** beat Dortmund
- 2017-18: **Stuttgart** beat Bayern Munich, on the final day of the season

## A data trap worth knowing about

The match results come from a public source and needed almost no cleaning,
with one important exception that would have quietly broken the ratings if
missed. Three club labels containing the word "Leipzig" appear in the
data, and they are **not** all the same club: one (from the 1993-94 season
only) is VfB Leipzig, a club that was relegated and no longer exists in the
top division; the other, RB Leipzig, is a completely different club that
wasn't even founded until 2009. Merging these by mistake would have given
RB Leipzig a fabricated history built from another club's results
entirely. They were kept separate. (Two genuinely duplicate club names —
just inconsistent spelling of the same club — were correctly merged.)

## How the ratings are built

- Every club starts at the same baseline rating. After each match, rating
  points shift from the loser to the winner, in proportion to how
  surprising the result was.
- The home team gets a fixed advantage added when working out how
  surprising a result was, since home advantage is a well-established
  real effect in football.
- Between seasons, ratings are pulled partway back toward the starting
  baseline, since squads change significantly over the summer transfer
  window, and last season's form is a noisy guide to how a team will
  perform next season.

These are standard, sensible settings, not specially fine-tuned. The point
of this project is the history and the honest checking of whether it
actually works, not squeezing out the very last bit of predictive
accuracy. For a more heavily optimized prediction approach, see the
companion project,
[Bundesliga-Match-Analysis-and-Prediction](https://github.com/SilverKai13/Bundesliga-Match-Analysis-and-Prediction),
which builds a more advanced model and tests it directly against real
bookmaker odds.

## Running it

```bash
pip install -r requirements.txt
pytest tests/                 # 7 automated checks, about 1 second
jupyter lab notebooks/        # 01_elo_ratings, then 02_validation
```

```
src/elo_ratings/
  data.py     # loading and cleaning the data
  elo.py      # the rating system itself
notebooks/
  01_elo_ratings.ipynb   # ratings, the trajectory chart, dominant seasons
  02_validation.ipynb    # checking calibration, favourite win rate, upsets
tests/                   # automated checks
```
