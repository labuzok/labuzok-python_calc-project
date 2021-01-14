import sys
import nba

if __name__ == '__main__':

  parser = nba.parserFunction()

  # getting names from the command line arguments
  name1 = sys.argv[1] + ' ' + sys.argv[2]
  name2 = sys.argv[3] + ' ' + sys.argv[4]

  # creating two player class objects
  player1, player2 = nba.get_players(name1, name2)

  # plotting and raport creation
  nba.plotting(name1, name2, player1.career_df, player2.career_df)
  nba.report_creation(player1.player_df, player2.player_df, player1.career_df.to_html(index=False), player2.career_df.to_html(index=False))
