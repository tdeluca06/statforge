import cfbd
from config import API_KEY_CONFIG

api_key = API_KEY_CONFIG

config = cfbd.Configuration()
config.api_key['Authorization'] = api_key
config.api_key_prefix['Authorization'] = 'Bearer'

games_api = cfbd.GamesApi(cfbd.ApiClient(config))
ratings_api = cfbd.RatingsApi(cfbd.ApiClient(config))
teams_api = cfbd.TeamsApi(cfbd.ApiClient(config))

def build_list():
   """
   Function to build a list 'total_srs' of FBS teams and their SRS ratings. 

   Returns: a formatted list of SRS ratings by team
   """
   total_srs_strings = []
   american_srs = ratings_api.get_srs_ratings(year=2023, conference='AAC')
   acc_srs = ratings_api.get_srs_ratings(year=2023, conference='acc')
   big12_srs = ratings_api.get_srs_ratings(year=2023, conference='B12')
   bigten_srs = ratings_api.get_srs_ratings(year=2023, conference='B1G')
   conf_usa_srs = ratings_api.get_srs_ratings(year=2023, conference='CUSA')
   independents_srs = ratings_api.get_srs_ratings(year=2023, conference='Ind')
   mid_srs = ratings_api.get_srs_ratings(year=2023, conference='MAC')
   mountain_srs = ratings_api.get_srs_ratings(year=2023, conference='MWC')
   pac12_srs = ratings_api.get_srs_ratings(year=2023, conference='PAC')
   sec_srs = ratings_api.get_srs_ratings(year=2023, conference='SEC')
   sunbelt_srs= ratings_api.get_srs_ratings(year=2023, conference='SBC')

   total_srs = [
      american_srs, acc_srs, big12_srs, sec_srs,
      bigten_srs, conf_usa_srs, independents_srs,
      mid_srs, mountain_srs, pac12_srs, sunbelt_srs ]
   
   for srs_list in total_srs:
      for entry in srs_list:
         total_srs_strings.append("{}: {}".format(entry.team, entry.rating))
   
   return total_srs_strings

def controller():
   print(build_list())

def get_data(week):
   request = "https://api.collegefootballdata.com/games/media?year=2023&week=9&classification=fbs"