from get_data import APIDataFetcher
from utils import build_game_tuples

def build_dict(api_fetcher):
    # filter teams that arent in FBS
    conferences = ['American Athletic', 'ACC', 'Big 12', 'Big Ten', 'Conference USA', 'FBS Independents', 'Mid-American', 'Mountain West', 'Pac-12', 'SEC', 'Sun Belt']
    data = api_fetcher.stats_api.get_advanced_team_season_stats(year=2023, exclude_garbage_time=True)
    team_stats = {}   
        
    for entry in data:
        team = entry.team
        team_stats[team] = {'offense': None} 

    # populate team stats with offense data
    for entry in data:
        team = entry.team
        offense_data = entry.offense
        if entry.conference in conferences:
            offense_havoc_total = offense_data.havoc.total
            team_stats[team]['offense'] = offense_havoc_total
        else:
            print(entry.conference)
            print(f"No data for team {team}")

    for entry in data:
        team = entry.team
        defense_data = entry.defense
        if entry.conference in conferences:
            defense_havoc_total = defense_data.havoc.total
            team_stats[team]['defense'] = defense_havoc_total
        else:
            print(entry.conference)
            print(f"No data for team {team} in defense havoc")
    #print(team_stats)
    return team_stats

class CalculateHavocTop:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher
        self.team_stats = build_dict(api_fetcher)

    def build_game_data(self, week):
        game_tuples = build_game_tuples(self.api_fetcher, week)
        game_havoc_list = []

        for away_team, home_team in game_tuples:
            if away_team in self.team_stats and home_team in self.team_stats:
                away_offense = self.team_stats[away_team].get('offense', 0)
                away_defense = self.team_stats[away_team].get('defense', 0) #
                home_defense = self.team_stats[home_team].get('defense', 0)
                home_offense = self.team_stats[home_team].get('offense', 0) #
                # disregard everything else

                if away_offense is not None and home_defense is not None:
                    game_tuple = {
                        'away_team' : away_team,
                        'home_team' : home_team,
                        'away_offense' : away_offense,
                        'home_defense' : home_defense
                    }

                    game_havoc_list.append(game_tuple)
                else:
                    print(f"Havoc data not available for both teams in the game: {away_team} vs {home_team}")
            else:
                print(f"Havoc data not available for one or both teams in the game: {away_team} vs {home_team}")
        #print(game_havoc_list)
        return game_havoc_list

    def calculate_total(self, week):
        game_data = self.build_game_data(week)
        total_factors = []

        for game in game_data:
            offense_havoc = game['away_offense']
            defense_havoc = game['home_defense']

            havoc_factor_top = offense_havoc - defense_havoc
            total_factors.append({
                'away_team': game['away_team'],
                'home_team': game['home_team'],
                'havoc_factor_top': havoc_factor_top
            })

        return total_factors

    def print_havoc_factors(self, havoc_factors_top):
        if not havoc_factors_top:
            print("No top havoc factors found.")
            return

        print("Printing havoc factors:")
        for factor in havoc_factors_top:
            home_team = factor['home_team']
            away_team = factor['away_team']
            havoc_factor_top = factor['havoc_factor_top']
            print(f"{home_team} vs. {away_team} Havoc Factor: {havoc_factor_top} top")

class CalculateHavocBottom:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher
        self.team_stats = build_dict(api_fetcher)

    def build_game_data(self, week):
        game_tuples = build_game_tuples(self.api_fetcher, week)
        game_havoc_list = []

        for away_team, home_team in game_tuples:
            if away_team in self.team_stats and home_team in self.team_stats:
                away_defense = self.team_stats[away_team].get('defense', 0) #
                home_offense = self.team_stats[home_team].get('offense', 0) #
                # disregard everything else

                if home_offense is not None and away_defense is not None:
                    game_tuple = {
                        'away_team' : away_team,
                        'home_team' : home_team,
                        'home_offense' : home_offense,
                        'away_defense' : away_defense
                    }

                    game_havoc_list.append(game_tuple)
                else:
                    print(f"Havoc data not available for both teams in the game: {away_team} vs {home_team} in bottom calculation")
            else:
                print(f"Havoc data not available for one or both teams in the game: {away_team} vs {home_team} in bottom calculation")
        #print(game_havoc_list)
        return game_havoc_list

    def calculate_total(self, week):
        game_data = self.build_game_data(week)
        total_factors = []

        for game in game_data:
            offense_havoc = game['home_offense']
            defense_havoc = game['away_defense']

            havoc_factor_bottom = defense_havoc - offense_havoc
            total_factors.append({
                'away_team': game['away_team'],
                'home_team': game['home_team'],
                'havoc_factor_bottom': havoc_factor_bottom
            })

        return total_factors

    def print_havoc_factors(self, havoc_factors):
        if not havoc_factors:
            print("No bottom havoc factors found.")
            return

        print("Printing bottom havoc factors:")
        for factor in havoc_factors:
            home_team = factor['home_team']
            away_team = factor['away_team']
            havoc_factor_bottom = factor['havoc_factor_bottom']
            print(f"{home_team} vs. {away_team} Havoc Factor: {havoc_factor_bottom} bottom calculation")


        

