from get_data import APIDataFetcher
from utils import build_game_tuples

class CalculatePPAFactor:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher
        self.team_ppa = {}
    
    def build_dict(self):
        conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC'] # Missing Ind

        for conference in conferences:
            print(f"Fetching PPA data for {conference}...")
            try:
                offense_list = self.api_fetcher.metrics_api.get_team_ppa(year=2023, conference=conference, exclude_garbage_time=True)
                defense_list = self.api_fetcher.metrics_api.get_team_ppa(year=2023, conference=conference, exclude_garbage_time=True)

                for entry in offense_list:
                    team = entry.team
                    offense_value = entry.offense.overall

                    if team not in self.team_ppa:
                        self.team_ppa[team] = {}

                    self.team_ppa[team]['offense'] = offense_value

                for entry in defense_list:
                    team = entry.team
                    defense_value = entry.defense.overall

                    if team not in self.team_ppa:
                        self.team_ppa[team] = {}

                    self.team_ppa[team]['defense'] = defense_value
                    
            except Exception as e:
                print(f"Error fetching data for {conference}: {e}")

        return self.team_ppa
    
    def build_game_data(self, week):
        game_tuples = build_game_tuples(self.api_fetcher, week)
        game_ppa_list = []

        for away_team, home_team in game_tuples:
            # Ensure PPA data exists for teams
            if away_team in self.team_ppa and home_team in self.team_ppa:
                away_offense = self.team_ppa[away_team].get('offense', 0)
                away_defense = self.team_ppa[away_team].get('defense', 0)
                home_offense = self.team_ppa[home_team].get('offense', 0)
                home_defense = self.team_ppa[home_team].get('defense', 0)

                game_tuple = {
                    'away_team': away_team,
                    'home_team': home_team,
                    'away_team_offense': away_offense,
                    'away_team_defense': away_defense,
                    'home_team_offense': home_offense,
                    'home_team_defense': home_defense,
                }

                game_ppa_list.append(game_tuple)
            else:
                print(f"PPA data not available for the following teams: {away_team} or {home_team}")

        return game_ppa_list

    def print_dict(self, team_ppa):
        for team, data in team_ppa.items():
            offense_value = data.get('offense', 'no data found')
            defense_value = data.get('defense', 'no data found')
            print(f"{team} [OFFENSE PPA: ] {offense_value} [DEFENSE PPA: ] {defense_value}")

    def print_game_data(self, game_data):
        for game in game_data:
            away_team = game['away_team']
            home_team = game['home_team']
            away_offense = game['away_team_offense']
            away_defense = game['away_team_defense']
            home_offense = game['home_team_offense']
            home_defense = game['home_team_defense']

            print(f"{away_team} [OFFENSE]: {away_offense} [DEFENSE]: {away_defense}")
            print(f"{home_team} [OFFENSE]: {home_offense} [DEFENSE]: {home_defense}")
            print()  # Add an empty line between games for better readability

    def calculate_offense_factors(self, week):
        game_data = self.build_game_data(week)
        offense_factors = []

        for game in game_data:
            away_team_offense = game['away_team_offense']
            home_team_offense = game['home_team_offense']

            # Perform calculation #1 - Home team offense - away team offense
            offense_factor = home_team_offense - away_team_offense

            offense_factors.append({
                'away_team' : game['away_team'],
                'home_team' : game['home_team'],
                'offense_factor' : offense_factor
            })

        return offense_factors
    
    def calculate_defense_factors(self,week):
        game_data = self.build_game_data(week)
        defense_factors = []

        for game in game_data:
            away_team_defense = game['away_team_defense']
            home_team_defense = game['home_team_defense']

            # Perform calculation #2 - Home team defense - away team defense
            defense_factor = home_team_defense - away_team_defense

            defense_factors.append({
                'away_team' : game['away_team'],
                'home_team' : game['home_team'],
                'defense_factor' : defense_factor
            })

        return defense_factors
        
    def calculate_total_factor(self, week, offense_factors, defense_factors):
            offense_factors = self.calculate_offense_factors(week)
            defense_factors = self.calculate_defense_factors(week)
            total_factors = []

            for i in range(min(len(offense_factors), len(defense_factors))):
                offense = offense_factors[i]
                defense = defense_factors[i]

                total_factor = offense['offense_factor'] - defense['defense_factor']

                total_factors.append({
                    'away_team' : offense['away_team'],
                    'home_team' : offense['home_team'],
                    'total_factor' : offense['offense_factor'] - defense['defense_factor']
                })

            return total_factors
    
    def print_total_factors(self, total_factors):
        for factor in total_factors:
            home_team = factor['home_team']
            away_team = factor['away_team']
            total_factor = factor['total_factor']
            print(f"{home_team} vs. {away_team} Factor: {total_factor}")
