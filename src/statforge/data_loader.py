import sys
import cfbd
import os

from typing import TypedDict
from dotenv import load_dotenv
from cfbd import TeamSeasonPredictedPointsAdded, DivisionClassification
from src.statforge.config import year


load_dotenv()

conferences: list[str] = [
    "FBS Independents",
    "American Athletic",
    "ACC",
    "Big 12",
    "Big Ten",
    "Conference USA",
    "Mid-American",
    "Mountain West",
    "Pac-12",
    "SEC",
    "Sun Belt",
]


def get_api_key() -> str:
    """
    Function to get the API_KEY from the environment variable. Modularized into a
    function for unit testing. Exits with error code 1 if API_KEY isn't found.

    :return: API_KEY from .env
    """
    api_key: str | None = os.getenv("CFBD_API_KEY")
    if not api_key:
        sys.exit("Error: Missing API_KEY environment variable.")
    return api_key


class APIDataFetcher:
    def __init__(self):
        self.api_key = get_api_key()
        self.api_client = self._create_api_client()
        self.ratings_api = cfbd.RatingsApi(self.api_client)
        self.games_api = cfbd.GamesApi(self.api_client)
        self.metrics_api = cfbd.MetricsApi(self.api_client)
        self.stats_api = cfbd.StatsApi(self.api_client)

    def _create_api_client(self):
        config = cfbd.Configuration(access_token=get_api_key())
        return cfbd.ApiClient(config)


def build_game_tuples(api_fetcher: APIDataFetcher, current_week: int) -> list[tuple]:
    games = api_fetcher.games_api.get_games(
        year=year, week=current_week, classification=DivisionClassification.FBS
    )

    out = []

    for game in games:
        away_team = game.away_team
        home_team = game.home_team
        game_tuple = (away_team, home_team)
        out.append(game_tuple)

    return out


class TeamHavocStats(TypedDict):
    offense: float | None
    defense: float | None


class DataLoader:
    """
    To handle all API work. Goal is to load in and shape the data accordingly, while
    allowing calculators to just calculate.
    """

    def __init__(self, api_fetcher: APIDataFetcher, week: int) -> None:
        self.api_fetcher = api_fetcher
        self.week = week

        self.games: list[tuple[str, str]] = []
        self.srs_by_team: dict[str, float] = {}
        self.ppa_by_team: dict[str, dict[str, float]] = {}
        self.havoc_by_team: dict[str, TeamHavocStats] = {}

    def load(self) -> None:
        self.games = build_game_tuples(self.api_fetcher, self.week)
        self.srs_by_team = self._load_srs()
        self.ppa_by_team = self._load_ppa()
        self.havoc_by_team = self._load_havoc()

    def _load_srs(self) -> dict[str, float]:
        print("Loading srs..")
        team_ratings: dict[str, float] = {}
        # SRS endpoint uses abbreviations - will NOT work with the globally defined list
        srs_conferences: list = [
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

        for conference in srs_conferences:
            try:
                rows = self.api_fetcher.ratings_api.get_srs(
                    year=year, conference=conference
                )

                for entry in rows:
                    team_ratings[entry.team] = entry.rating

            except Exception as e:
                print(f"Error getting SRS data for: {conference}. Exception: {e}")

        return team_ratings

    def _load_ppa(self) -> dict[str, dict[str, float]]:
        print("Loading ppa...")
        team_ppa: dict[str, dict[str, float]] = {}

        for conference in conferences:
            try:
                rows: list[TeamSeasonPredictedPointsAdded] = (
                    self.api_fetcher.metrics_api.get_predicted_points_added_by_team(
                        year=year, conference=conference, exclude_garbage_time=True
                    )
                )

                for entry in rows:
                    team: str = entry.team

                    if team not in team_ppa:
                        team_ppa[team] = {}

                    if entry.offense:
                        team_ppa[team]["offense"] = entry.offense.overall
                    else:
                        print(f"Offense PPA value not found for {team}")
                    if entry.defense:
                        team_ppa[team]["defense"] = entry.defense.overall
                    else:
                        print(f"Defense PPA value not found for {team}")

            except Exception as e:
                print(f"Error fetching data for {conference}: {e}")

        return team_ppa

    def _load_havoc(self) -> dict[str, TeamHavocStats]:
        print("Loading havoc..")
        team_havoc: dict[str, TeamHavocStats] = {}

        try:
            rows = self.api_fetcher.stats_api.get_advanced_season_stats(
                year=year,
                exclude_garbage_time=True,
            )

            for entry in rows:
                if entry.conference not in conferences:
                    continue

                team = entry.team

                team_havoc[team] = {"offense": None, "defense": None}

                if entry.offense and entry.offense.havoc:
                    team_havoc[team]["offense"] = entry.offense.havoc.total
                if entry.defense and entry.defense.havoc:
                    team_havoc[team]["defense"] = entry.defense.havoc.total

        except Exception as e:
            print(f"Error fetching data for havoc: {e}")

        return team_havoc
