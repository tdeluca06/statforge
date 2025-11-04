"""
Module for computing Simple Rating System (SRS) based game lines using CFBD data.

SRS represents a team's overall strength, adjusted for schedule difficulty, and is used
here to generate a baseline predicted line before incorporating additional efficiency
metrics.

This module defines the CalculateSRSLine class, which calculates matchup-level odds for
each individual FBS game.
"""


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
        games: a list of game tuples representing matchups
        team_srs: a dict mapping teams to SRS ratings
    """

    def __init__(
        self, games: list[tuple[str, str]], team_srs: dict[str, float]
    ) -> None:
        """
        Initialize the class with a data fetcher.
        :param games: a list of tuples representing matchups
        :param team_srs: a dict mapping teams to SRS ratings
        """
        self.games = games
        self.team_srs = team_srs

    def calculate_odds(self) -> dict[str, float]:
        """
        Function to calculate SRS odds per game. Computes the predicted point
        differential between teams based on their SRS ratings.

        A 2.5-point home-field adjustment is applied to the home team before calculating
        the spread.

        Output structure:
            {
                "Away1 vs Home1": <float>,
                "Away2 vs Home2": <float>
            }

        :return: dict mapping away_team vs home_team to the predicted point spread
        """

        odds: dict[str, float] = {}

        for away_team, home_team in self.games:
            away_srs: float = self.team_srs.get(away_team)
            home_srs: float = self.team_srs.get(home_team)
            if home_srs is not None and away_srs is not None:
                calculated_odds: float = (home_srs + 2.5) - away_srs
                odds[f"{away_team} vs {home_team}"] = calculated_odds
            else:
                print(f"Invalid SRS values for {away_team} vs {home_team}")

        return odds
