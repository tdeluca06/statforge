from get_data import APIDataFetcher

class CalculateSRSLine:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher

    def build_dict(self) :
        team_ratings = {}
        conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'Ind', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC']

        for conference in conferences:
            srs_list = self.api_fetcher.ratings_api.get_srs_ratings(year=2023, conference=conference)
            for entry in srs_list:
                team_ratings[entry.team] = entry.rating

            return team_ratings
    
    def get_data(self, current_week):
        games = self.api_fetcher.games_api.get_game_media(year=2023, week=current_week, classification='fbs')
        game_tuples = []

        for game in games:
            away_team = game.away_team
            home_team = game.home_team
            game_tuple = (away_team, home_team)
            game_tuples.append(game_tuple)

        return game_tuples
    
    def calculate_odds (self, current_week):
        teams_srs = self.build_dict()
        games_data = self.get_data(current_week)

        odds = {}

        for away_team, home_team in games_data:
            away_srs = teams_srs.get(away_team, 0)
            home_srs = teams_srs.get(home_team, 0)

            calculated_odds = (home_srs + 2.5) - away_srs

            odds[f"{away_team} vs {home_team}"] = calculated_odds

        return odds
    
    def print_odds(self, odds):
        for game, calculated_odds in odds.items():
            formatted_odds = "{}, {:.1f}".format(game, calculated_odds)
            print(formatted_odds)