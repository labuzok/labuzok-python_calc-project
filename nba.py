from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import jinja2
import sys


#-------------------------------
# script description

help = '''
This script compares statistics of two given NBA players.
Enter players' names to obtain information about them.
The required format is this: script.py FirstName1 LastName1 FirstName2 LastName2
'''

#-------------------------------
# function parsing command line arguments

def parserFunction():

    parser = argparse.ArgumentParser(description = help)

    # adding arguments
    parser.add_argument('first player\'s first name', help=u'''Full first name of the first player''')
    parser.add_argument('first player\'s last name', help=u'''Full last name of the first player''')
    parser.add_argument('second player\'s first name', help=u'''Full first name of the second player''')
    parser.add_argument('second player\'s last name', help=u'''Full last name of the second player''')
    args = parser.parse_args()

    return args


#-------------------------------
# class which generates and stores all the data for one player

class player:

    def __init__(self, name):
        self.name = name
        self.id = self.get_player_id()
        self.player_df = self.get_player_info()
        self.career_df = self.get_player_stats()

    # function which gets the player id (which as an argument for other functions) based on name given by the user
    def get_player_id(self):
        nba_players = players.get_players()
        df = pd.DataFrame(nba_players)
        id = df.loc[df['full_name'] == self.name]['id']
        return id

    # function which gets basic player info based on his id
    def get_player_info(self):

        # downlading information about the player from the NBA Stats API
        player_info = commonplayerinfo.CommonPlayerInfo(player_id = self.id)
        player_df = player_info.get_data_frames()[0]
        # choosing columns which are interesting to us
        player_columns = ['DISPLAY_FIRST_LAST', 'BIRTHDATE', 'SCHOOL', 'COUNTRY', 'HEIGHT', 'WEIGHT', 'POSITION', 'TEAM_NAME', 'FROM_YEAR', 'TO_YEAR']
        player_df = player_df[player_columns]
        # changing these columns' names
        col = ['Name', 'Birthdate', 'School', 'Country', 'Height', 'Weight', 'Position', 'Team', 'Played from', 'Played to']
        player_df.columns = col
        # formatting player's birthdate
        player_df['Birthdate'] = player_df['Birthdate'][0][:10]
        # changing data format to dictionary so it's easier to handle with jinja2
        player_df = player_df.to_dict()

        return player_df

    # function which gets player's statistics throughout his career based on his id
    def get_player_stats(self):

        # downloading data about the player from the NBA Stats API
        career = playercareerstats.PlayerCareerStats(player_id=self.id)
        career_df = career.get_data_frames()[0]
        # adding 3 additional columns: points per game, assists per game and rebound per game
        career_df['PPG'] = round(career_df['PTS']/career_df['GP'], 1)
        career_df['APG'] = round(career_df['AST']/career_df['GP'], 1)
        career_df['RPG'] = round(career_df['REB']/career_df['GP'], 1)
        # choosing columns which are interesting to us
        col_career = ['SEASON_ID', 'TEAM_ABBREVIATION', 'GP', 'GS', 'FG_PCT','FG3_PCT','FT_PCT', 'PPG', 'APG', 'RPG']
        career_df = career_df[col_career]
        # changing these columns' names
        col_career_final = ['Season', 'Team', 'Games played', 'Games started', 'FG percentage', '3PTS percentage', 'FT percentage', 'PPG', 'APG', 'RPG']
        career_df.columns = col_career_final

        return career_df


#-------------------------------
# function which generates two objects of the player class
# it handles an exception if one or both of the players are not in the database

def get_players(name1, name2):
    try:
        player1 = player(name1)
        player2 = player(name2)
        return player1, player2
    except:
        print('One or both players are not in the database. Try Again.')
        sys.exit(1)


#-------------------------------
# function which plots three barplots (points per game, assists per game, rebound per game) based on both objects of the player class

def plotting(name1, name2, df1, df2):

    plt.figure(figsize = (20, 22))
    df = pd.merge(df1, df2, how = 'outer', on = 'Season')
    df = df.sort_values('Season')
    df.plot(x = 'Season', y = ['PPG_x', 'PPG_y'], kind='bar', label = ['PPG {}'.format(name1), 'PPG {}'.format(name2)], color = ['red', 'royalblue'])
    plt.grid()
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig('./img/ppg.png')

    plt.figure(figsize = (20, 22))
    df.plot(x = 'Season', y = ['APG_x', 'APG_y'], kind='bar', label = ['APG {}'.format(name1), 'APG {}'.format(name2)], color = ['red', 'royalblue'])
    plt.grid()
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig('./img/apg.png')

    plt.figure(figsize = (20, 22))
    df.plot(x = 'Season', y = ['RPG_x', 'RPG_y'], kind='bar', label = ['RPG {}'.format(name1), 'RPG {}'.format(name2)], color = ['red', 'royalblue'])
    plt.grid()
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig('./img/rpg.png')





# function which creates a html file with prepared data

def report_creation(player1_info, player2_info, table1, table2):

    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "templatka.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    output = template.render(dict=player1_info, dict2 = player2_info, career_table = table1, career2_table = table2)

    with open('./{} and {} report.html'.format(player1_info['Name'][0], player2_info['Name'][0]), 'w') as f:
        f.write(output)
