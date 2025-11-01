"""
Module for computing Simple Rating System (SRS) based game lines using CFBD data.

SRS represents a team's overall strength, adjusted for schedule difficulty, and is used
here to generate a baseline predicted line before incorporating additional efficiency
metrics.

This module defines the CalculateSRSLine class, which retrieves per-team SRS ratings
for a given season and calculates matchup-level odds for each individual FBS game.
"""

from cfbd import TeamSRS

from src.utils import build_game_tuples
from src.statforge.config import year
from src.statforge.get_data import APIDataFetcher


def print_odds(odds: dict[str, float]) -> None:
    """
    Print each game and its calculated SRS odds in a readable format. Temporary before
    eventual move to logging.

    :param odds: dict mapping "away_team vs home_team" to predicted point spread
    """
    for game, calculated_odds in odds.items():
        formatted_odds = "{}, {:.1f}".format(game, calculated_odds)
        print(formatted_odds)


class CalculateSRSLine:
    """
    Class to handle SRS data retrieval and per-game aggregation.

    Attributes:
        api_fetcher: An initialized APIDataFetcher instance for CFBD API calls
    """

    def __init__(self, api_fetcher: APIDataFetcher) -> None:
        """
        Initialize the class with a data fetcher.
        :param api_fetcher:  An initialized APIDataFetcher instance for CFBD API calls
        """
        self.api_fetcher = api_fetcher

    def build_dict(self) -> dict[str, float]:
        """
        Function to build a dictionary mapping teams to their SRS ratings. Fetches and
        stores values in the form:
            {
                "team_name": <float>
            }

        :return: a dict mapping teams to their SRS rating
        """
        team_ratings: dict[str, float] = {}
        conferences: list[str] = [
            "AAC",
            "acc",
            "B12",
            "B1G",
            "CUSA",
            "Ind",
            "MAC",
            "MWC",
            "PAC",
            "SEC",
            "SBC",
        ]

        for conference in conferences:
            try:
                srs_list: list[TeamSRS] = self.api_fetcher.ratings_api.get_srs(
                    year=year, conference=conference
                )
                for entry in srs_list:
                    team_ratings[entry.team] = entry.rating
            except Exception as e:
                print(f"Error getting SRS data for: {conference}. Exception: {e}")

        return team_ratings

    def calculate_odds(self, week: int) -> dict[str, float]:
        """
        Function to calculate SRS odds per game. Builds matchup tuples for the specified
        week using CFBD schedule data, then computes the predicted point differential
        between teams based on their SRS ratings.

        A 2.5-point home-field adjustment is applied to the home team before calculating
        the spread.

        Output structure:
            {
                "Away1 vs Home1": <float>,
                "Away2 vs Home2": <float>
            }

        :param week: week to fetch data from
        :return: dict mapping away_team vs home_team to the predicted point spread
        """
        teams_srs: dict[str, float] = self.build_dict()
        games_data: list[tuple] = build_game_tuples(self.api_fetcher, week)

        odds: dict[str, float] = {}

        for away_team, home_team in games_data:
            away_srs: float = teams_srs.get(away_team)
            home_srs: float = teams_srs.get(home_team)
            if home_srs is not None and away_srs is not None:
                calculated_odds: float = (home_srs + 2.5) - away_srs
                odds[f"{away_team} vs {home_team}"] = calculated_odds
            else:
                print(f"Invalid SRS values for {away_team} vs {home_team}")

        return odds
