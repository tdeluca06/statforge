from get_data import APIDataFetcher
from utils import build_game_tuples

class CalculateHavoc:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher

    def build_dict(self):
        # filter teams that arent in FBS
        conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'Ind', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC']

        data = self.api_fetcher.stats_api.get_advanced_team_stats(exclude_garbage_time=true)
        print(data)

