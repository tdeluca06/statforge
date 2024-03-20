from get_data import APIDataFetcher
from utils import build_game_tuples

class CalculateSRSLine:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher

    def build_dict(self) :
        team_ratings = {}
        conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'Ind', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC']

        for conference in conferences:
            try:
                srs_list = self.api_fetcher.ratings_api.get_srs_ratings(year=2023, conference=conference)
                for entry in srs_list:
                    team_ratings[entry.team] = entry.rating
            except Exception as e:
                print(f"Error getting SRS data for: {conference}")
        #print(team_ratings)
        return team_ratings
    
    def calculate_odds (self, current_week):
        teams_srs = self.build_dict()
        games_data = build_game_tuples(self.api_fetcher, current_week)

        odds = {}

        for away_team, home_team in games_data:
            away_srs = teams_srs.get(away_team)
            home_srs = teams_srs.get(home_team)
            if home_srs is not None and away_srs is not None:
                calculated_odds = (home_srs + 2.5) - away_srs
                odds[f"{away_team} vs {home_team}"] = calculated_odds
            else:
                print(f"Invalid SRS values for {away_team} vs {home_team}")
        return odds
    
    def print_odds(self, odds):
        for game, calculated_odds in odds.items():
            formatted_odds = "{}, {:.1f}".format(game, calculated_odds)
            print(formatted_odds)