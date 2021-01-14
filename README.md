# <div align="center"> Python in Engineering Calculations - NBA players statistics
  <img src = "img/agh.jpg"> </div>
  <div align="center">
  <br><b>Author:</b> Michał Kozubal
  <br><b>Country:</b> Poland
  <br><b>Faculty:</b> Department of Applied Informatics and Computational Physics
  <br><b>Field of study:</b> Computational Physics
</div >

___

## Project description

The goal of this <b>Python></b> project is to create an html report comparing statistisc of two given NBA players (current or historical). The user writes the names in the command line when he wants to run the script. It then takes these names and gets information about them using `nba_api`, which is an API Client for `www.nba.com`. More about the client [here](https://github.com/swar/nba_api/blob/master/README.md). It gathers general information like birthdate, height, weight etc. as well as whole career statistics which include games played in each season, field goals percentage etc. The script also plots three bar plots. First is for both players points per game in every season they played, second for assists per game and third for rebound per game.

## Running the script

- open the terminal and enter the directory which contains the project
- run the script:
```console
python script.py FirstName1 LastName1 FirstName2 LastName2
```
where the names are obviously of players we want to get information about
- if everything goes well the report should appear in the same directory as the script




