import cfbd
import calculate_havoc
from config import API_KEY_CONFIG
from get_data import APIDataFetcher
from calculate_SRS import CalculateSRSLine
from calculate_PPA import CalculatePPAFactor
from calculate_havoc import CalculateHavocTop
from calculate_havoc import CalculateHavocBottom

year = 2024

def calculate_srs(api_fetcher, week):
   # Create class instance
   srs_calculator = CalculateSRSLine(api_fetcher)
   odds = srs_calculator.calculate_odds(week)
   # Debugging - print SRS lines
   srs_calculator.print_odds(odds)
   return odds

def calculate_ppa(api_fetcher, week):
   # Create class instance
   ppa_calculator = CalculatePPAFactor(api_fetcher)
   team_ppa = ppa_calculator.build_dict()
   ppa_data = ppa_calculator.build_game_data(week)
   offense_factors = ppa_calculator.calculate_offense_factors(week)
   defense_factors = ppa_calculator.calculate_defense_factors(week)
   total_factors = ppa_calculator.calculate_total_factor(week, offense_factors, defense_factors)
   # Debugging - print PPA stats
   #ppa_calculator.print_dict(team_ppa)
   #ppa_calculator.print_game_data(ppa_data)
   #ppa_calculator.print_total_factors(total_factors)
   return total_factors

def calculate_havoc_top(api_fetcher, week):
    havoc_calculator = CalculateHavocTop(api_fetcher)
    team_havoc = calculate_havoc.build_dict(api_fetcher)
    havoc_data = havoc_calculator.build_game_data(week)
    total_factors = havoc_calculator.calculate_total(week)
    #havoc_calculator.print_havoc_factors(total_factors)
    return total_factors

def calculate_havoc_bottom(api_fetcher, week):
    havoc_calculator = CalculateHavocBottom(api_fetcher)
    team_havoc = calculate_havoc.build_dict(api_fetcher)
    havoc_data = havoc_calculator.build_game_data(week)
    total_factors = havoc_calculator.calculate_total(week)
    #havoc_calculator.print_havoc_factors(total_factors)
    return total_factors

def adjust_factor(srs_lines, ppa_factors, 
                  havoc_factors_top, havoc_factors_bottom):
    adjusted_factors = {}

    if havoc_factors_top is None:
        print("empty dict")

    for ppa_factor,havoc_factor_top, havoc_factor_bottom in zip(ppa_factors, havoc_factors_top, 
                                       havoc_factors_bottom):
        away_team = ppa_factor['away_team']
        home_team = ppa_factor['home_team']

        # matchup key
        matchup = f"{away_team} vs {home_team}"

        if matchup in srs_lines:
            # get original SRS line by matchup
            srs_line = srs_lines[matchup]
            # perform calculation
            total_factor = ppa_factor['total_factor'] + havoc_factor_top['havoc_factor_top'] + havoc_factor_bottom['havoc_factor_bottom']
            adjusted_srs_line = srs_line + total_factor
            adjusted_factors[matchup] = adjusted_srs_line
    
    return adjusted_factors

def launch():
  api_fetcher = APIDataFetcher(API_KEY_CONFIG)
  #ppa_calculator = CalculatePPAFactor(api_fetcher)
  # Get week
  print("Enter the week you need data for: ")
  week = int(input())
  # Handle SRS calculation
  srs_lines = calculate_srs(api_fetcher, week)
  # Handle PPA calculation
  ppa_odds = calculate_ppa(api_fetcher, week)
  # Handle havoc calculation top
  havoc_odds_top = calculate_havoc_top(api_fetcher, week)
  # Handle havoc calculation bottom
  havoc_odds_bottom = calculate_havoc_bottom(api_fetcher, week)
  # Adjust SRS odds
  adjusted_factors = adjust_factor(srs_lines, ppa_odds, 
                                   havoc_odds_top, havoc_odds_bottom)
  
  # Print adjusted SRS odds
  print("Adjusted SRS Odds:")
  for matchup, adjusted_srs_line in adjusted_factors.items():
      print(f"{matchup}: {adjusted_srs_line}")
  
 
  return 0
      
if __name__ == '__main__':
    launch()