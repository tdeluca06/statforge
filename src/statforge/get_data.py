import cfbd
import os

from dotenv import load_dotenv


load_dotenv()


class APIDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_client = self._create_api_client()
        self.ratings_api = cfbd.RatingsApi(self.api_client)
        self.games_api = cfbd.GamesApi(self.api_client)
        self.metrics_api = cfbd.MetricsApi(self.api_client)
        self.stats_api = cfbd.StatsApi(self.api_client)

    def _create_api_client(self):
        config = cfbd.Configuration(access_token=os.getenv("API_KEY"))
        # config.api_key['Authorization'] = self.api_key.strip()
        # config.api_key_prefix['Authorization'] = 'Bearer'
        return cfbd.ApiClient(config)
