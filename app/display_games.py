@app.route('/')
def display_game_data():
    games = scrape_espn.get_data(1)
    games.run()

    games_data = games.game_data[games.game_data['has_odds']]

    display_cols = ['date',
                    'time',
                    'home_rank',
                    'home_team',
                    'away_team',
                    'away_rank',
                    'odds_line_fav',
                    'odds_line_spread',
                    'odds_ou',
                    'networks',
                    'venue_name',
                    'venue_city',
                    'venue_state'
                    ]
    display_data = pandas.DataFrame()
    for col in display_cols:
        display_data[col] = games_data[col]
    display_data.reset_index(drop=True,inplace=True)

    return display_data.to_html()
