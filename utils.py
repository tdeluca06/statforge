# Common functions used across different files

def build_game_tuples(api_fetcher, current_week):
    games = api_fetcher.games_api.get_game_media(year=2023, week=current_week, classification='fbs')
    game_tuples = []

    for game in games:
        away_team = game.away_team
        home_team = game.home_team
        game_tuple = (away_team, home_team)
        game_tuples.append(game_tuple)

    return game_tuples
