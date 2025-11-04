"""
Module for calculating Predicted Points Added (PPA) factors using data from CFBD.

Predicted Points Added is an efficiency metric measuring the expected change in a team's
scoring potential resulting from a singular play.

This module defines the CalculatePPAFactor class, which computes the PPA factors
(offensive, defensive, total) used in the calculation of total influence.
"""


class CalculatePPAFactor:
    """
    Class to handle PPA calculation per-game.

    Attributes:
        games: A list of game tuples for the given week
        team_ppa: Cached dict to map teams to their offensive and defensive PPA metrics
    """

    def __init__(
        self, games: list[tuple], team_ppa: dict[str, dict[str, float]]
    ) -> None:
        """
        Initialize the calculator with a list of games and a dict mapping teams to
        PPA values
        :param games: a list of tuples containing matchups
        :param team_ppa: a dict mapping teams to PPA values
        """
        self.games = games
        self.team_ppa = team_ppa

    def build_game_data(self) -> list[dict[str, float]]:
        """
        Function to construct a list of per-game PPA data for all matchups in a given
        week. Each matchup is represented as:
            {
                "away_team": <team name>,
                "home_team": <team name>,
                "away_team_offense": <float>,
                "away_team_defense": <float>,
                "home_team_offense": <float>,
                "home_team_defense": <float>
            }

        :return: a list of dictionaries containing team PPA data for each matchup
        """
        game_ppa_list: list[dict[str, float]] = []

        for away_team, home_team in self.games:
            if away_team in self.team_ppa and home_team in self.team_ppa:
                away_offense: float = self.team_ppa[away_team].get("offense", 0)
                away_defense: float = self.team_ppa[away_team].get("defense", 0)
                home_offense: float = self.team_ppa[home_team].get("offense", 0)
                home_defense: float = self.team_ppa[home_team].get("defense", 0)

                game_dict: dict[str, float] = {
                    "away_team": away_team,
                    "home_team": home_team,
                    "away_team_offense": away_offense,
                    "away_team_defense": away_defense,
                    "home_team_offense": home_offense,
                    "home_team_defense": home_defense,
                }

                game_ppa_list.append(game_dict)
            else:
                print(
                    f"PPA data not available for the following teams: "
                    f"{away_team} or {home_team}"
                )

        return game_ppa_list

    def calculate_offense_factors(self) -> list[dict[str, float]]:
        """
        Function to calculate total offensive PPA factor per game, and map each game to
        the calculated factor. Each matchup is represented as:
            {
                "away_team": <team name>,
                "home_team": <team name>,
                "offensive_factor": <float>
            }

        :return: a list of dictionaries containing PPA offensive factors per game
        """
        game_data: list[dict[str, float]] = self.build_game_data()
        offense_factors: list[dict[str, float]] = []

        for game in game_data:
            away_team_offense: float = game["away_team_offense"]
            home_team_offense: float = game["home_team_offense"]

            # Perform calculation #1 - Home team offense - away team offense
            offense_factor: float = home_team_offense - away_team_offense

            offense_factors.append(
                {
                    "away_team": game["away_team"],
                    "home_team": game["home_team"],
                    "offense_factor": offense_factor,
                }
            )

        return offense_factors

    def calculate_defense_factors(self) -> list[dict[str, float]]:
        """
        Function to calculate total defensive PPA factor per game, and map each game to
        the calculated factor. Each matchup is represented as:
            {
                "away_team": <team name>,
                "home_team": <team name>,
                "defensive_factor": <float>
            }

        :return: a list of dictionaries containing PPA defensive factors per game
        """

        game_data: list[dict[str, float]] = self.build_game_data()
        defense_factors: list[dict[str, float]] = []

        for game in game_data:
            away_team_defense: float = game["away_team_defense"]
            home_team_defense: float = game["home_team_defense"]

            # Perform calculation #2 - Home team defense - away team defense
            defense_factor: float = home_team_defense - away_team_defense

            defense_factors.append(
                {
                    "away_team": game["away_team"],
                    "home_team": game["home_team"],
                    "defense_factor": defense_factor,
                }
            )

        return defense_factors

    def calculate_total_factor(self, week: int) -> list[dict[str, float]]:
        """
        Function to combine both offensive and defensive PPA factors into a single dict.
        Each matchup is represented as:
            {
                "away_team": <team name>,
                "home_team": <team name>,
                "total_factor": <float>
            }

        The total factor is computed as:
            total_factor = offense_factor - defense_factor

        :param week: week to calculate for
        :return: a list of dictionaries containing PPA total factors per game
        """
        offense_factors: list[dict[str, float]] = self.calculate_offense_factors()
        defense_factors: list[dict[str, float]] = self.calculate_defense_factors()
        total_factors: list[dict[str, float]] = []

        for i in range(min(len(offense_factors), len(defense_factors))):
            offense: dict[str, float] = offense_factors[i]
            defense: dict[str, float] = defense_factors[i]

            total_factor: float = offense["offense_factor"] - defense["defense_factor"]

            total_factors.append(
                {
                    "away_team": offense["away_team"],
                    "home_team": offense["home_team"],
                    "total_factor": total_factor,
                }
            )

        return total_factors
