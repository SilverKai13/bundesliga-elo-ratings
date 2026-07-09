import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from elo_ratings import data
from elo_ratings.elo import Elo


@pytest.fixture(scope="module")
def df():
    return data.load_results()


@pytest.fixture(scope="module")
def fitted(df):
    return Elo().run(df)


def test_team_normalization(df):
    teams = set(df.HomeTeam) | set(df.AwayTeam)
    assert "M'Gladbach" not in teams          # merged
    assert "Dusseldorf" not in teams          # merged
    assert "Leipzig" in teams                 # VfB Leipzig kept
    assert "RB Leipzig" in teams              # kept distinct


def test_dates_parse_and_sort(df):
    assert df.Date.isna().sum() == 0
    assert df.Date.is_monotonic_increasing


def test_ratings_are_roughly_zero_sum(fitted):
    # Elo transfers points between teams, so the average across all clubs
    # that ever played should stay near the 1500 base
    avg = sum(fitted.ratings.values()) / len(fitted.ratings)
    assert 1450 < avg < 1550


def test_expected_home_is_a_probability(fitted):
    p = fitted.expected_home("Bayern Munich", "Hamburg")
    assert 0 < p < 1
    # symmetric-ish: swapping venue lowers Bayern's expected result
    p_away = fitted.expected_home("Hamburg", "Bayern Munich")
    assert p > (1 - p_away)  # home advantage helps whoever is at home


def test_strong_team_outrates_weak_team(fitted):
    assert fitted.ratings["Bayern Munich"] > fitted.ratings["Hamburg"]


def test_history_and_predictions_populated(fitted, df):
    hist = fitted.history_frame()
    preds = fitted.predictions_frame()
    assert len(preds) == len(df)          # one forecast per match
    assert len(hist) == 2 * len(df)       # two teams updated per match
    assert set(preds.FTR.unique()) <= {"H", "D", "A"}


def test_elo_beats_coinflip_favourite(fitted):
    # the Elo favourite should win outright well above the ~1/3 you'd get
    # from guessing among three outcomes
    pred = fitted.predictions_frame()
    pred = pred[pred.Season != "1993-94"]
    fav_home = pred.p_home > 0.5
    fav_won = (fav_home & (pred.FTR == "H")) | (~fav_home & (pred.FTR == "A"))
    assert fav_won.mean() > 0.45
