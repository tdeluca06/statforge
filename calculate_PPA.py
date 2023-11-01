from get_data import APIDataFetcher

class CalculatePPAFactor:
    def __init__(self, api_fetcher):
        self.api_fetcher = api_fetcher

    def build_dict(self):
        team_ppa = {}
        conferences = ['AAC', 'acc', 'B12', 'B1G', 'CUSA', 'Ind', 'MAC', 'MWC', 'PAC', 'SEC', 'SBC']

        for conference in conferences:
            print(f"Fetching data for conference: {conference}")
            try:
                ppa_list = self.api_fetcher.metrics_api.get_team_ppa(year=2023, conference=conference)
                for entry in ppa_list:
                    team_ppa[entry.team] = entry.offense.overall
            except Exception as e:
                print(f"Error fetching data for conference {conference}: {e}")

        return team_ppa
        
    def print_dict(self, team_ppa):
        for team,value in team_ppa.items():
            print(f"{team}: {value}")