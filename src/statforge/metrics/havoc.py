"""
Module for computing game-level Havoc factors from CFBD advanced stats.

Responsibilities:
- pulls per-team offensive and defensive havoc totals for the season,
- builds per-week matchups from the schedule,
- projects havoc from both perspectives:
    - top = away offense vs. home defense
    - bottom = home offense vs. away defense
These two lists can later be merged with SRS/PPA when building an adjusted line.
"""

from typing import TypedDict

from src.utils import build_game_tuples
from src.statforge.config import year


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


def build_dict(api_fetcher) -> dict[str, TeamHavocStats]:
    """
    Build a mapping from team name to offensive/defensive havoc totals for the season.
    """
    conferences: list[str] = [
        "American Athletic",
        "ACC",
        "Big 12",
        "Big Ten",
        "Conference USA",
        "FBS Independents",
        "Mid-American",
        "Mountain West",
        "Pac-12",
        "SEC",
        "Sun Belt",
    ]

    data = api_fetcher.stats_api.get_advanced_season_stats(
        year=year,
        exclude_garbage_time=True,
    )

    team_stats: dict[str, TeamHavocStats] = {}

    # initialize teams
    for entry in data:
        team: str = entry.team
        team_stats[team] = {"offense": None, "defense": None}

    # offense
    for entry in data:
        team: str = entry.team
        if entry.conference in conferences:
            offense_havoc_total: float = entry.offense.havoc.total
            team_stats[team]["offense"] = offense_havoc_total
        else:
            print(entry.conference)
            print(f"No data for team {team}")

    # defense
    for entry in data:
        team: str = entry.team
        if entry.conference in conferences:
            defense_havoc_total: float = entry.defense.havoc.total
            team_stats[team]["defense"] = defense_havoc_total
        else:
            print(entry.conference)
            print(f"No data for team {team} in defense havoc")

    return team_stats


class CalculateHavocTop:
    """
    Away offense vs. home defense
    """

    def __init__(self, api_fetcher) -> None:
        self.api_fetcher = api_fetcher
        self.team_stats: dict[str, TeamHavocStats] = build_dict(api_fetcher)

    def build_game_data(self, week: int) -> list[dict[str, float | str]]:
        """
        Build raw game rows for the given week from the top perspective.
        """
        game_tuples = build_game_tuples(self.api_fetcher, week)
        game_havoc_list: list[dict[str, float | str]] = []

        for away_team, home_team in game_tuples:
            if away_team in self.team_stats and home_team in self.team_stats:
                away_offense = self.team_stats[away_team].get("offense", 0.0)
                home_defense = self.team_stats[home_team].get("defense", 0.0)

                if away_offense is not None and home_defense is not None:
                    game_havoc_list.append(
                        {
                            "away_team": away_team,
                            "home_team": home_team,
                            "away_offense": float(away_offense),
                            "home_defense": float(home_defense),
                        }
                    )
                else:
                    print(
                        f"Havoc data not available for both teams in the game: "
                        f"{away_team} vs {home_team}"
                    )
            else:
                print(
                    f"Havoc data not available for one or both teams in the game: "
                    f"{away_team} vs {home_team}"
                )

        return game_havoc_list

    def calculate_total(self, week: int) -> list[HavocGameTop]:
        """
        Turn raw game rows into final top havoc factors.
        """
        game_data = self.build_game_data(week)
        total_factors: list[HavocGameTop] = []

        for game in game_data:
            offense_havoc = float(game["away_offense"])
            defense_havoc = float(game["home_defense"])

            havoc_factor_top = offense_havoc - defense_havoc
            total_factors.append(
                {
                    "away_team": str(game["away_team"]),
                    "home_team": str(game["home_team"]),
                    "away_offense": offense_havoc,
                    "home_defense": defense_havoc,
                    "havoc_factor_top": havoc_factor_top,
                }
            )

        return total_factors

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

    def __init__(self, api_fetcher) -> None:
        self.api_fetcher = api_fetcher
        self.team_stats: dict[str, TeamHavocStats] = build_dict(api_fetcher)

    def build_game_data(self, week: int) -> list[dict[str, float | str]]:
        """
        Build raw game rows for the given week from the bottom perspective.
        """
        game_tuples = build_game_tuples(self.api_fetcher, week)
        game_havoc_list: list[dict[str, float | str]] = []

        for away_team, home_team in game_tuples:
            if away_team in self.team_stats and home_team in self.team_stats:
                away_defense = self.team_stats[away_team].get("defense", 0.0)
                home_offense = self.team_stats[home_team].get("offense", 0.0)

                if home_offense is not None and away_defense is not None:
                    game_havoc_list.append(
                        {
                            "away_team": away_team,
                            "home_team": home_team,
                            "home_offense": float(home_offense),
                            "away_defense": float(away_defense),
                        }
                    )
                else:
                    print(
                        "Havoc data not available for both teams in the game: "
                        f"{away_team} vs {home_team} in bottom calculation"
                    )
            else:
                print(
                    "Havoc data not available for one or both teams in the game: "
                    f"{away_team} vs {home_team} in bottom calculation"
                )

        return game_havoc_list

    def calculate_total(self, week: int) -> list[HavocGameBottom]:
        """
        Turn raw game rows into final bottom havoc factors.
        """
        game_data = self.build_game_data(week)
        total_factors: list[HavocGameBottom] = []

        for game in game_data:
            offense_havoc = float(game["home_offense"])
            defense_havoc = float(game["away_defense"])

            havoc_factor_bottom = defense_havoc - offense_havoc
            total_factors.append(
                {
                    "away_team": str(game["away_team"]),
                    "home_team": str(game["home_team"]),
                    "home_offense": offense_havoc,
                    "away_defense": defense_havoc,
                    "havoc_factor_bottom": havoc_factor_bottom,
                }
            )

        return total_factors
