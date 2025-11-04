"""
Module for computing game-level Havoc factors from CFBD advanced stats.

Projects havoc from both perspectives:
- top = away offense vs. home defense
- bottom = home offense vs. away defense
These two lists can later be merged with SRS/PPA when building an adjusted line.
"""

from typing import TypedDict


class TeamHavocStats(TypedDict):
    offense: float | None
    defense: float | None


class HavocGameTop(TypedDict):
    away_team: str
    home_team: str
    away_offense: float
    home_defense: float
    havoc_factor_top: float


class HavocGameBottom(TypedDict):
    away_team: str
    home_team: str
    home_offense: float
    away_defense: float
    havoc_factor_bottom: float


class CalculateHavocTop:
    """
    Away offense vs. home defense
    """

    def __init__(self, games, team_havoc) -> None:
        self.games = games
        self.team_havoc = team_havoc

    def build_game_data(self) -> list[dict[str, float | str]]:
        rows: list[dict[str, float | str]] = []

        for away_team, home_team in self.games:
            away = self.team_havoc.get(away_team)
            home = self.team_havoc.get(home_team)
            if not away or not home:
                continue

            away_off = away.get("offense")
            home_def = home.get("defense")
            if away_off is None or home_def is None:
                continue

            rows.append(
                {
                    "away_team": away_team,
                    "home_team": home_team,
                    "away_offense": float(away_off),
                    "home_defense": float(home_def),
                }
            )

        return rows

    def calculate_total(self) -> list[dict[str, float | str]]:
        game_data = self.build_game_data()
        out: list[dict[str, float | str]] = []

        for game in game_data:
            offense_havoc = game["away_offense"]
            defense_havoc = game["home_defense"]
            havoc_factor_top = offense_havoc - defense_havoc

            out.append(
                {
                    "away_team": game["away_team"],
                    "home_team": game["home_team"],
                    "away_offense": offense_havoc,
                    "home_defense": defense_havoc,
                    "havoc_factor_top": havoc_factor_top,
                }
            )
        return out

    def print_havoc_factors(self, havoc_factors_top: list[HavocGameTop]) -> None:
        if not havoc_factors_top:
            print("No top havoc factors found.")
            return

        print("Printing havoc factors:")
        for factor in havoc_factors_top:
            home_team = factor["home_team"]
            away_team = factor["away_team"]
            havoc_factor_top = factor["havoc_factor_top"]
            print(f"{home_team} vs. {away_team} Havoc Factor: {havoc_factor_top} top")


def print_havoc_factors(havoc_factors: list[HavocGameBottom]) -> None:
    if not havoc_factors:
        print("No bottom havoc factors found.")
        return

    print("Printing bottom havoc factors:")
    for factor in havoc_factors:
        home_team = factor["home_team"]
        away_team = factor["away_team"]
        havoc_factor_bottom = factor["havoc_factor_bottom"]
        print(
            f"{home_team} vs. {away_team} Havoc Factor: "
            f"{havoc_factor_bottom} bottom calculation"
        )


class CalculateHavocBottom:
    """
    Home offense vs. away defense
    """

    def __init__(self, games, team_havoc) -> None:
        self.games = games
        self.team_havoc = team_havoc

    def build_game_data(self) -> list[dict[str, float | str]]:
        rows: list[dict[str, float | str]] = []

        for away_team, home_team in self.games:
            away = self.team_havoc.get(away_team)
            home = self.team_havoc.get(home_team)
            if not away or not home:
                continue

            home_off = home.get("offense")
            away_def = away.get("defense")
            if home_off is None or away_def is None:
                continue

            rows.append(
                {
                    "away_team": away_team,
                    "home_team": home_team,
                    "home_offense": float(home_off),
                    "away_defense": float(away_def),
                }
            )

        return rows

    def calculate_total(self) -> list[dict[str, float | str]]:
        game_data = self.build_game_data()
        out: list[dict[str, float | str]] = []

        for game in game_data:
            offense_havoc = game["home_offense"]
            defense_havoc = game["away_defense"]
            havoc_factor_bottom = defense_havoc - offense_havoc

            out.append(
                {
                    "away_team": game["away_team"],
                    "home_team": game["home_team"],
                    "home_offense": offense_havoc,
                    "away_defense": defense_havoc,
                    "havoc_factor_bottom": havoc_factor_bottom,
                }
            )
        return out
