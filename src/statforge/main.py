from metrics.havoc import CalculateHavocBottom, CalculateHavocTop
from metrics.ppa import CalculatePPAFactor
from metrics.srs import CalculateSRSLine, print_odds
from src.statforge.data_loader import APIDataFetcher, DataLoader


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
    api_fetcher: APIDataFetcher = APIDataFetcher()

    print("Enter the week you need data for: ")
    current_week: int = int(input())

    loader: DataLoader = DataLoader(api_fetcher, current_week)
    loader.load()

    games = loader.games

    srs_calc = CalculateSRSLine(games, loader.srs_by_team)

    ppa_calc = CalculatePPAFactor(games, loader.ppa_by_team)

    havoc_top_calc = CalculateHavocTop(games, loader.havoc_by_team)

    havoc_bottom_calc = CalculateHavocBottom(games, loader.havoc_by_team)

    srs_lines = srs_calc.calculate_odds()
    print_odds(srs_lines)

    ppa_factors = ppa_calc.calculate_total_factor(current_week)
    havoc_top = havoc_top_calc.calculate_total()
    havoc_bottom = havoc_bottom_calc.calculate_total()

    adjusted_factors = adjust_factor(srs_lines, ppa_factors, havoc_top, havoc_bottom)

    print("Adjusted SRS Odds:")
    for match, adjusted_srs_line in adjusted_factors.items():
        print(f"{match}: {adjusted_srs_line}")
