import os
import sys

from dotenv import load_dotenv

from metrics import havoc
from metrics.havoc import CalculateHavocBottom, CalculateHavocTop
from metrics.ppa import CalculatePPAFactor
from metrics.srs import CalculateSRSLine, print_odds
from src.statforge.get_data import APIDataFetcher

load_dotenv()


def get_api_key() -> str:
    """
    Function to get the API_KEY from the environment variable. Modularized into a
    function for unit testing. Exits with error code 1 if API_KEY isn't found.
    :return: API_KEY from .env
    """
    api_key: str | None = os.getenv("API_KEY")
    if not api_key:
        sys.exit("Error: Missing API_KEY environment variable.")
    return api_key


API_KEY: str = get_api_key()


def fetch_srs(api_fetcher: APIDataFetcher, week: int) -> dict[str, float]:
    """
    Function to fetch base SRS ratings from the CFBD API.
    :param api_fetcher: Initialized APIDataFetcher instance to retrieve data from CFBD
    :param week: week to fetch data from
    :return: a dict mapping teams to SRS ratings
    """
    srs_calculator: CalculateSRSLine = CalculateSRSLine(api_fetcher)
    odds: dict[str, float] = srs_calculator.calculate_odds(week)

    print_odds(odds)

    return odds


def calculate_ppa(api_fetcher: APIDataFetcher, week: int) -> list[dict[str, float]]:
    """
    Function to initialize PPA calculator for all matchups in a given week.
    Builds team level PPA data, generates offensive and defensive factors
    to calculate combined factors.
    :param api_fetcher: Initialized APIDataFetcher instance to retrieve data from CFBD
    :param week: week to fetch data from
    :return: A list of dictionaries mapping games (away_team, home_team) to the total
    factor.
    """
    ppa_calculator: CalculatePPAFactor = CalculatePPAFactor(api_fetcher)

    ppa_calculator.build_dict()
    ppa_calculator.build_game_data(week)

    total_factors: list[dict[str, float]] = ppa_calculator.calculate_total_factor(week)
    return total_factors


def calculate_havoc_top(
    api_fetcher: APIDataFetcher, week: int
) -> list[dict[str, float]]:
    """
    Havoc factors are split into top and bottom layers to account for both perspectives
    of the game (top: away offense - home defense, bottom: home offense - away defense)

    Function to initialize a CalculateHavocTop instance (which fetches and caches
    per-team offense and per-team defense havoc totals), builds game-level data for the
    input week and computes the per-matchup havoc factor.

    :param api_fetcher: Initialized APIDataFetcher instance to retrieve data from CFBD
    :param week: week to fetch data from
    :return: A list of dictionaries mapping games (away_team, home_team) to the total
    top factor.
    """
    havoc_calculator: CalculateHavocTop = CalculateHavocTop(api_fetcher)

    havoc.build_dict(api_fetcher)
    havoc_calculator.build_game_data(week)

    total_factors: list[dict[str, float]] = havoc_calculator.calculate_total(week)
    return total_factors


def calculate_havoc_bottom(
    api_fetcher: APIDataFetcher, week: int
) -> list[dict[str, float]]:
    """
    Havoc factors are split into top and bottom layers to account for both perspectives
    of the game (top: away offense - home defense, bottom: home offense - away defense)

    Function to initialize a CalculateHavocBottom instance (which fetches and caches
    per-team offense and per-team defense havoc totals), builds game-level data for the
    input week and computes the per-matchup havoc factor.

    :param api_fetcher: Initialized APIDataFetcher instance to retrieve data from CFBD
    :param week: week to fetch data from
    :return: A list of dictionaries mapping games (away_team, home_team) to the total
    bottom factor.
    """
    havoc_calculator = CalculateHavocBottom(api_fetcher)

    havoc_calculator.build_game_data(week)

    total_factors: list[dict[str, float]] = havoc_calculator.calculate_total(week)
    return total_factors


def adjust_factor(
    srs_lines: dict[str, float],
    ppa_factors: list[dict[str, float]],
    havoc_factors_top: list[dict[str, float]],
    havoc_factors_bottom: list[dict[str, float]],
) -> dict[str, float]:
    """
    Combine SRS, PPA, and Havoc metrics into an adjusted per-matchup line.

    Each matchup is represented as "away_team vs home_team" and adjusted by
    summing all calculated factors.

    :param srs_lines: base SRS odds fetched to operate on
    :param ppa_factors: list of dicts containing total_factors for PPA
    :param havoc_factors_top: list of dicts containing havoc_factor_top per matchup
    :param havoc_factors_bottom: list of dicts containing havoc_factor_bottom per matchup
    :return: dict mapping matchups to adjusted SRS lines
    """
    adjusted: dict[str, float] = {}

    if havoc_factors_top is None:
        print("empty dict")

    for ppa_factor, havoc_factor_top, havoc_factor_bottom in zip(
        ppa_factors, havoc_factors_top, havoc_factors_bottom
    ):
        away_team: float = ppa_factor["away_team"]
        home_team: float = ppa_factor["home_team"]

        # matchup key
        matchup: str = f"{away_team} vs {home_team}"

        if matchup in srs_lines:
            srs_line: float = srs_lines[matchup]
            # Influence is defined as the aggregation of all calculated factors
            total_influence: float = (
                ppa_factor["total_factor"]
                + havoc_factor_top["havoc_factor_top"]
                + havoc_factor_bottom["havoc_factor_bottom"]
            )
            adjusted_srs: float = srs_line + total_influence
            adjusted[matchup] = adjusted_srs

    return adjusted


if __name__ == "__main__":
    data_fetcher: APIDataFetcher = APIDataFetcher(API_KEY)

    print("Enter the week you need data for: ")
    current_week: int = int(input())

    srs_lines: dict[str, float] = fetch_srs(api_fetcher=data_fetcher, week=current_week)
    ppa_odds: list[dict[str, float]] = calculate_ppa(data_fetcher, current_week)
    # handle both top and bottom portions of havoc calculation
    havoc_odds_top: list[dict[str, float]] = calculate_havoc_top(
        data_fetcher, current_week
    )
    havoc_odds_bottom: list[dict[str, float]] = calculate_havoc_bottom(
        data_fetcher, current_week
    )

    adjusted_factors: dict[str, float] = adjust_factor(
        srs_lines, ppa_odds, havoc_odds_top, havoc_odds_bottom
    )

    print("Adjusted SRS Odds:")
    for match, adjusted_srs_line in adjusted_factors.items():
        print(f"{match}: {adjusted_srs_line}")
