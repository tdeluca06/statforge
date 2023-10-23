import cfbd
import os
from config import number

api_key = os.environ.get('API_KEY').strip()
print(f'API Key from environment: {api_key}')
print(f'Number: {number}')

config = cfbd.Configuration()
config.api_key['Authorization'] = api_key
config.api_key_prefix['Authorization'] = 'Bearer'
print(f'API key from config: {config.api_key}')


api = cfbd.StatsApi(cfbd.ApiClient(config))

def get_team_data():
    team_data = api.get_team_season_stats(year=2023, team='Florida State')

    return team_data