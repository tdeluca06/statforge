import cfbd

class APIDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_client = self._create_api_client()
        self.ratings_api = cfbd.RatingsApi(self.api_client)
        self.games_api = cfbd.GamesApi(self.api_client)

    def _create_api_client(self):
        config = cfbd.Configuration()
        config.api_key['Authorization'] = self.api_key
        config.api_key_prefix['Authorization'] = 'Bearer'
        return cfbd.ApiClient(config)
