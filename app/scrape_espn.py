
import pandas
import requests
import json
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import pytz

import game_fields


class get_data():
    '''
    To Do:
     - team stats?
     - game link?

     - Export to csv/excel/google sheets?
    '''
    def __init__(self, week_num):
        self.week_num = week_num
        return

    def define_url(self, week_num):
        base_url = 'http://www.espn.com/college-football/scoreboard/_/group/80/year/2016/seasontype/2/week/'
        complete_url = '{0}{1}'.format(base_url, week_num)
        return complete_url

    def make_request(self, url):
        r = requests.get(url)
        return r

    def parse_soup(self, request_data):
        soup = bs(request_data.text, "html5lib")
        soup_scripts = soup.select('script')
        score_data = str(soup_scripts[8]).split('=', 1)[1].lstrip(' ').replace(';</script>', '').replace('&#39;', "'").split(';', 1)[0]

        return json.loads(score_data)

    def save_data_to_file(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        return None

    def pull_all_game_data(self, request_data):
        games = request_data['events']

        game_dict = {}
        for i, game in enumerate(games):
            game_info = {'date': game_fields.get_game_date(game),
                         'time': game_fields.get_game_time(game),
                         'networks': str(game_fields.get_game_networks(game)).replace('u','').strip('[]').replace("'","").replace('ABC, ESPN3','ABC'),
                         'home_team': game_fields.get_home_team(game),
                         'home_abbr': game_fields.get_home_abbr(game),
                         'away_team': game_fields.get_away_team(game),
                         'away_abbr': game_fields.get_away_abbr(game),
                         'has_odds': game_fields.has_odds(game),
                         'odds_provider': game_fields.get_game_odds_provider(game),
                         'odds_line': game_fields.get_game_odds_line(game),
                         'odds_line_fav': game_fields.parse_game_odds_line(game_fields.get_game_odds_line(game))[0],
                         'odds_line_spread': game_fields.parse_game_odds_line(game_fields.get_game_odds_line(game))[1],
                         'odds_ou': game_fields.get_game_odds_ou(game),
                         'neutral_site': game_fields.get_neutral_site_ind(game),
                         'weather_conditions': game_fields.get_game_weather_conditions(game),
                         'weather_temp_type': game_fields.get_game_weather_temp(game)[0],
                         'weather_temp_value': game_fields.get_game_weather_temp(game)[1],
                         'venue_name': game_fields.get_venue_name(game),
                         'venue_city': game_fields.get_venue_city(game),
                         'venue_state': game_fields.get_venue_state(game),
                         'home_record': game_fields.get_home_record(game),
                         'away_record': game_fields.get_away_record(game),
                         'conf_game_ind': game_fields.get_conf_game_ind(game),
                         'home_score': game_fields.get_home_score(game),
                         'away_score': game_fields.get_away_score(game),
                         'home_rank': game_fields.get_home_rank(game),
                         'away_rank': game_fields.get_away_rank(game),
                         'game_complete': game_fields.get_game_status(game),
                         'game_quarter': game_fields.get_game_quarter(game),
                         'game_clock': game_fields.get_game_clock(game)
                         }
            game_dict[i] = game_info

        return game_dict

    def insert_game_data_into_df(self, game_dict):
        game_df = pandas.DataFrame.from_dict(game_dict, orient='index')
        return game_df

    def run(self):
        self.game_dict = self.pull_all_game_data(self.parse_soup(self.make_request(self.define_url(self.week_num))))
        self.game_data = self.insert_game_data_into_df(self.game_dict)
        self.game_data = self.game_data[self.game_data['has_odds']]
