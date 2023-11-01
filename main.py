import cfbd
from config import API_KEY_CONFIG
from get_data import APIDataFetcher
from calculate_SRS import CalculateSRSLine
from calculate_PPA import CalculatePPAFactor

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
   ppa_calculator.print_total_factors(total_factors)

def launch():
  api_fetcher = APIDataFetcher(API_KEY_CONFIG)
  ppa_calculator = CalculatePPAFactor(api_fetcher)
  # Get week
  week = input("Enter the week you need data for: ")
  week = int(week) # convert string to usable int
  # Handle SRS calculation
  srs_odds = calculate_srs(api_fetcher, week)
  # Handle PPA calculation
  ppa_odds = calculate_ppa(api_fetcher, week)
  return 0
      
if __name__ == '__main__':
    launch()