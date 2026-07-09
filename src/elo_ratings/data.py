"""Load and clean 25 seasons of Bundesliga results.

Two teams appear under more than one label and are merged. One pair is
deliberately kept apart: "Leipzig" (VfB Leipzig, relegated after 1993-94)
and "RB Leipzig" (founded 2009, promoted 2016) are unrelated clubs --
merging them on the shared word would give RB Leipzig a rating history
built from another club's results.
"""

import os

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "data"))

TEAM_RENAMES = {
    "M'Gladbach": "M'gladbach",          # capitalisation variant
    "Dusseldorf": "Fortuna Dusseldorf",  # same club, two labels
}


def _parse_dates(series):
    """football-data mixes 4-digit and 2-digit years, both day-first."""
    d = pd.to_datetime(series, format="%d/%m/%Y", errors="coerce")
    return d.fillna(pd.to_datetime(series, format="%d/%m/%y", errors="coerce"))


def load_results(path=None):
    path = path or os.path.join(DATA_DIR, "Bundesliga_Results.csv")
    df = pd.read_csv(path)
    df["Date"] = _parse_dates(df["Date"])
    df["HomeTeam"] = df["HomeTeam"].replace(TEAM_RENAMES)
    df["AwayTeam"] = df["AwayTeam"].replace(TEAM_RENAMES)
    df = df.sort_values("Date").reset_index(drop=True)
    df["SeasonStart"] = df["Season"].str.slice(0, 4).astype(int)
    return df
