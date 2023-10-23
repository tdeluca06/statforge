import cfbd
from config import API_KEY_CONFIG

api_key = API_KEY_CONFIG

config = cfbd.Configuration()
config.api_key['Authorization'] = api_key
config.api_key_prefix['Authorization'] = 'Bearer'

games_api = cfbd.GamesApi(cfbd.ApiClient(config))
ratings_api = cfbd.RatingsApi(cfbd.ApiClient(config))
teams_api = cfbd.TeamsApi(cfbd.ApiClient(config))

def build_dict():
    """
    Function to build a dictionary 'team_ratings' of FBS teams and their SRS ratings.

    Returns: a dictionary of team SRS ratings
    """
    team_ratings = {}
    conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'Ind', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC']

    for conference in conferences:
        srs_list = ratings_api.get_srs_ratings(year=2023, conference=conference)
        for entry in srs_list:
            team_ratings[entry.team] = entry.rating

    return team_ratings


def get_data(current):
   """
   Function to get data on college football games in the current week, and create a list
   of tuples in the format "away_team vs home_team".

   Parameters:
   current - integer value specifying which calender week of the CFB regular season to 
   pull data from.

   Returns - a list of tuples in the format "away_team vs home_team" of the current week.
   """
   games = games_api.get_game_media(year=2023, week=current, classification='fbs')
   #print(games)
   game_tuples = []

   for game in games:
      away_team = game.away_team
      home_team = game.home_team
      game_tuple = (away_team, home_team)
      game_tuples.append(game_tuple)
   
   return game_tuples

def calculate_odds(current_week):
    teams_srs = build_dict()
    games_data = get_data(current_week)

    odds = {}

    for away_team, home_team in games_data:
        away_srs = teams_srs.get(away_team, 0)  
        home_srs = teams_srs.get(home_team, 0)  
        
        calculated_odds = (home_srs + 2.5) - away_srs

        odds[f"{away_team} vs {home_team}"] = calculated_odds

    return odds

def print_odds(odds):
    for game, calculated_odds in odds.items():
        formatted_odds = "{}, {:.1f}".format(game, calculated_odds)
        print(formatted_odds)

def launch():
  odds = calculate_odds(9)
  print_odds(odds)
  return 0
      
launch()