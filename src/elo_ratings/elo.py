"""Sequential Elo ratings for football.

Ratings start at 1500 and update after every match. A draw counts as half
a win for each side. A fixed home-field bonus is added to the home team's
rating when computing the expected result. Between seasons, ratings are
pulled part-way back toward the mean (regression), because squads change
and last May's form is a noisy guide to August.
"""

import numpy as np
import pandas as pd


class Elo:
    def __init__(self, k=20, home_adv=65, base=1500, season_regression=0.25):
        self.k = k
        self.home_adv = home_adv
        self.base = base
        self.season_regression = season_regression
        self.ratings = {}
        self.history = []          # (date, season, team, rating_after)
        self.predictions = []      # (date, season, home, away, p_home_win, ftr)

    def _get(self, team):
        return self.ratings.get(team, self.base)

    def expected_home(self, home, away):
        """Probability the home team takes the points (win = 1, draw = 0.5)."""
        diff = (self._get(home) + self.home_adv) - self._get(away)
        return 1.0 / (1.0 + 10 ** (-diff / 400))

    def _regress_to_mean(self):
        for t in self.ratings:
            self.ratings[t] = (
                self.base + (1 - self.season_regression) * (self.ratings[t] - self.base)
            )

    def run(self, matches):
        """Feed a chronologically-sorted match frame through the ratings,
        recording each match's pre-match forecast and each team's rating
        after every game."""
        current_season = None
        for r in matches.itertuples():
            if current_season is not None and r.Season != current_season:
                self._regress_to_mean()
            current_season = r.Season

            exp_h = self.expected_home(r.HomeTeam, r.AwayTeam)
            self.predictions.append(
                (r.Date, r.Season, r.HomeTeam, r.AwayTeam, exp_h, r.FTR)
            )

            score_h = {"H": 1.0, "D": 0.5, "A": 0.0}[r.FTR]
            delta = self.k * (score_h - exp_h)
            self.ratings[r.HomeTeam] = self._get(r.HomeTeam) + delta
            self.ratings[r.AwayTeam] = self._get(r.AwayTeam) - delta

            self.history.append((r.Date, r.Season, r.HomeTeam, self.ratings[r.HomeTeam]))
            self.history.append((r.Date, r.Season, r.AwayTeam, self.ratings[r.AwayTeam]))
        return self

    def history_frame(self):
        return pd.DataFrame(self.history, columns=["Date", "Season", "Team", "Rating"])

    def predictions_frame(self):
        return pd.DataFrame(
            self.predictions,
            columns=["Date", "Season", "HomeTeam", "AwayTeam", "p_home", "FTR"],
        )
