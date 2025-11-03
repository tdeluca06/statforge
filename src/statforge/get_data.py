import sys

import cfbd
import os

from dotenv import load_dotenv

from src.statforge.main import get_api_key

load_dotenv()


class APIDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_client = self._create_api_client()
        self.ratings_api = cfbd.RatingsApi(self.api_client)
        self.games_api = cfbd.GamesApi(self.api_client)
        self.metrics_api = cfbd.MetricsApi(self.api_client)
        self.stats_api = cfbd.StatsApi(self.api_client)

    def get_api_key(self) -> str:
        """
        Function to get the API_KEY from the environment variable. Modularized into a
        function for unit testing. Exits with error code 1 if API_KEY isn't found.

        :return: API_KEY from .env
        """
        api_key: str | None = os.getenv("CFBD_API_KEY")
        if not api_key:
            sys.exit("Error: Missing API_KEY environment variable.")
        return api_key

    def _create_api_client(self):
        config = cfbd.Configuration(access_token=get_api_key())
        # config.api_key['Authorization'] = self.api_key.strip()
        # config.api_key_prefix['Authorization'] = 'Bearer'
        return cfbd.ApiClient(config)
