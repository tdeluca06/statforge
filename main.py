import cfbd
from config import API_KEY_CONFIG
from get_data import APIDataFetcher
from calculate_SRS import CalculateSRSLine
from calculate_PPA import CalculatePPAFactor

def launch():
  api_fetcher = APIDataFetcher(API_KEY_CONFIG)

  srs_calculator = CalculateSRSLine(api_fetcher)
  #ppa_calculator = CalculatePPAFactor(api_fetcher)

  odds = srs_calculator.calculate_odds(10)
  #team_ppa = ppa_calculator.build_dict()
  srs_calculator.print_odds(odds)
  #ppa_calculator.print_dict(team_ppa)
  return 0
      
if __name__ == '__main__':
    launch()