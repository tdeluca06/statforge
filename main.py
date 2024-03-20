import cfbd
from config import API_KEY_CONFIG
from get_data import APIDataFetcher
from calculate_SRS import CalculateSRSLine
from calculate_PPA import CalculatePPAFactor
from calculate_havoc import CalculateHavoc

def calculate_srs(api_fetcher, week):
   # Create class instance
   srs_calculator = CalculateSRSLine(api_fetcher)
   odds = srs_calculator.calculate_odds(week)
   # Debugging - print SRS lines
   #srs_calculator.print_odds(odds)
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

def calculate_havoc(api_fetcher, week):
    havoc_calculator = CalculateHavoc(api_fetcher)
    data = havoc_calculator.build_dict()
    print(data)

def adjust_factor(srs_lines, ppa_factors):
    adjusted_factors = {}

    for ppa_factor in ppa_factors:
        away_team = ppa_factor['away_team']
        home_team = ppa_factor['home_team']

        # matchup key
        matchup = f"{away_team} vs {home_team}"

        if matchup in srs_lines:
            # get original SRS line by matchup
            srs_line = srs_lines[matchup]
            # perform calculation on SRS line
            adjusted_srs_line = srs_line - ppa_factor['total_factor']
            adjusted_factors[matchup] = adjusted_srs_line
    
    return adjusted_factors

def launch():
  api_fetcher = APIDataFetcher(API_KEY_CONFIG)
  ppa_calculator = CalculatePPAFactor(api_fetcher)
  # Get week
  print("Enter the week you need data for: ")
  week = int(input())
  # Handle SRS calculation
  srs_lines = calculate_srs(api_fetcher, week)
  # Handle PPA calculation
  ppa_odds = calculate_ppa(api_fetcher, week)
  # Adjust SRS odds
  adjusted_factors = adjust_factor(srs_lines, ppa_odds)
  # figure out how my own code works
  """
  if isinstance(srs_lines, list):
    print("srs lines as list")
  elif isinstance(srs_lines, dict):
    print("srs lines as dict:\n", srs_lines)
  elif isinstance(srs_lines, set):
    print("srs lines as set")
  elif isinstance(srs_lines, tuple):
    print("srs lines as tuple?? wtf")

  if isinstance(ppa_odds, list):
    print("ppa lines as list\n", ppa_odds)
  elif isinstance(ppa_odds, dict):
    print("ppa lines as dict")
  elif isinstance(ppa_odds, set):
    print("ppa lines as set")
  elif isinstance(ppa_odds, tuple):
    print("ppa lines as tuple?? wtf")

  """

  # Print adjusted SRS odds
  print("Adjusted SRS Odds:")
  #for matchup, adjusted_srs_line in adjusted_factors.items():
      #print(f"{matchup}: {adjusted_srs_line}")

  havoc_factor = calculate_havoc(api_fetcher, week)

  return 0
      
if __name__ == '__main__':
    launch()