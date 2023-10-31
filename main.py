import cfbd
from config import API_KEY_CONFIG
from getData import APIDataFetcher
from calculateSRS import CalculateSRSLine

def launch():
  api_fetcher = APIDataFetcher(API_KEY_CONFIG)
  srs_calculater = CalculateSRSLine(api_fetcher)
  odds = srs_calculater.calculate_odds(10)
  srs_calculater.print_odds(odds)
  return 0
      
if __name__ == '__main__':
    launch()