import urllib3
import certifi
import re
import glob
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_card_data(soup, game_dict):
    """This function returns cards for both the home- and awaytime from a 
    soup object and writes those information in the according matchday 
    dataframe. I record card color, player name, and minute of foul."""
    
    # Find container with card information.
    cards_soup = soup.find(
        "table", {"class": "content_table_std spielerstrafen"})
    cards_soup = cards_soup.find_all("td", {"valign": "top"})
    
    for i, team in enumerate(["home", "away"]):
        # Get cards soup for every team.
        team_cards = cards_soup[i].findAll("div", {"class": "tn_item"})
        
        # Initalize values for card counting.
        game_dict["{}_card_yllw".format(team)] = 0
        game_dict["{}_card_red".format(team)] = 0
        
        # Loop through all cards of respective team. 
        minmax = min(len(team_cards), 11)
        for j in range(minmax):
            try:
                # Get player name and minute of card.
                player = team_cards[j].a.text
                minute = team_cards[j].find(
                    "span", {"class": "klammerzahl"}).text[:-1]

                game_dict["{}_card_plyr_{}".format(team, j)] = player
                game_dict["{}_card_min_{}".format(team, j)] = int(minute)

                # Scrape card colors and contiuously count cards.
                if team_cards[j].div["style"] == "color:#FBDB04;":
                    game_dict["{}_card_clr_{}".format(team, j)] = 1  # yellow = 1
                    game_dict["{}_card_yllw".format(team)] += 1
                    
                elif team_cards[j].div["style"] == "color:#D7110C;":
                    game_dict["{}_card_clr_{}".format(team, j)] = 2  # red = 2
                    game_dict["{}_card_red".format(team)] += 1
                    
                elif team_cards[j].div["class"][0] == "icon_gelbrot":
                    game_dict["{}_card_clr_{}".format(team, j)] = 3 # yellow / red = 3
                    game_dict["{}_card_yllw".format(team)] += 2 # count as two yellow cards
                    
                else:
                    game_dict["{}_card_clr_{}".format(team, j)] = np.nan
                    
            except:
                pass
            
    return game_dict

# def get_goal_data(soup, game_dict):
#     """This function returns goals for both the home- and awaytime from a
#     soup object and writes those information in the according matchday
#     dataframe. I record player name, scoreline, and minute of play."""
#     try:
#         # Find location where goal informations are stored.
#         goals_soup = soup.find(
#             "table", {"class": "content_table_std torschuetzen"})
#         goals = goals_soup.findAll(
#             "div", {"class": "tn_item torschuetzen_ausgabe"})

#         # Enumerate goal html objects.
#         for j, goal in enumerate(goals):
#             scoreline = goal.find("span", {"class": "spielstand"}).text
#             scorer = goal.img["title"]
#             scoretime = goal.find("span", {"class": "klammerzahl"}).text[:-1]

#             # Save relevant infromation to dataframe.
#             game_dict["goal_" + str(j)] = scoreline
#             game_dict["goal_plyr_" + str(j)] = scorer
#             game_dict["goal_min" + str(j)] = scoretime
#     except:
#         pass

#     return game_dict


# def get_coach_data(soup, game_dict, i):
#     """Given an url this function returns the soup object, i.e., it gets
#     the page request and pulls the data out of HTML code, needed to
#     start the actual web scraping process."""
#     try:
#         coach_home = soup.findAll(
#             "div", {"class": "aufstellung_ausgabe_block homeside"})[2]
#         game_dict["coach_home"] = coach_home.a.text
#         coach_away = soup.findAll(
#             "div", {"class": "aufstellung_ausgabe_block awayside"})[2]
#         game_dict["coach_away"] = coach_away.a.text
#     except:
#         pass

#     return game_dict


def get_player_data(soup, game_dict):
    """This function returns player data for both the home- and awayteam
    from a  soup object and writes those information in the according 
    matchday dataframe. Besides player names, also corresponding player
    urls are retrieved."""
    
    # Loop through teams to store information by team.
    for i, team in enumerate(["home", "away"]):
        plyrs_soup = soup.findAll("div", {"class": "aufstellung_ausgabe_block {}side".format(team)})[0]
        plyrs = plyrs_soup.findAll("a", {"class": "spieler_linkurl"})
        
        # Loop through players.
        for j in range(min(len(plyrs), 11)):
            try:
                game_dict["{}_plyr_{}".format(team, j)] = plyrs[j].text
                game_dict["{}_plyr_url_{}".format(team, j)] = plyrs[j]["href"]
            except:
                pass

    return game_dict


def get_game_data(soup, game_dict):
    """Given a soup object this function returns the general game data,
    ranging from date of the game, the result, the referee as well as the
    name and url of both teams."""

    # Get date and time data.
    date_soup = soup.find("div", {"class": "spielbericht_tipp_status"})
    try:
        league = date_soup.div.span.text
        date_string = date_soup.div.text
        date = re.search(r'\d{2}.\d{2}.\d{2}', date_string).group(0)
        time = re.search(r'\d{2}:\d{2}', date_string).group(0)
        matchday = re.search(r'[|]\d+', date_string).group(0)[1:]

        game_dict["league"] = league
        game_dict["date"] = date
        game_dict["time"] = time
        game_dict["matchday"] = matchday
    except:
        pass

    # Get game result and write to game dataframe.
    try:
        result = soup.find("div", {"class": "stand"}).text
        game_dict["result"] = result
    except:
        pass

    # Try to get the referee name.
    try:
        referee = soup.find("span", {"class": "schiri_link"}).text
        game_dict["referee"] = referee
    except:
        pass

    try:
        smmry_soup = soup.find(
            "div", {"class": "spielbericht_ergebnis_wrapper"})
        club_title = smmry_soup.find_all("img")
        team_title = smmry_soup.findAll("div", {"class": "teaminfo"})

        # Loop through home- and awayside team to retrieve team name and url
        # as well as club name (teams are subdivisions within a club).
        for j, team in enumerate(["home_", "away_"]):
            game_dict[team + "team"] = team_title[j].a["title"]
            game_dict[team + "team_url"] = team_title[j].a["href"]
            game_dict[team + "club"] = club_title[j]["title"]
    except:
        pass

    return game_dict


def get_dict_keys():
    """Computes a dictionary with all possible occuring keys in the
    scraping process."""
    dict_keys = ["time", "date", "league",
                 "game_url", "referee", "result", "matchday"]
    for team in ["home", "away"]:
        primary_keys = ["{0}_{1}".format(team, x) for x in [
            "club", "team_url", "team", "card_red", "card_yllw"]]
        dict_keys += primary_keys
        for j in range(11):
            identifier = ["_plyr_url_", "_plyr_",
                          "_card_plyr_", "_card_min_", "_card_clr_"]
            further_keys = ["{0}{1}{2}".format(team, x, j) for x in identifier]
            dict_keys += further_keys

    return dict_keys


def run_scraping(game_url_list, dict_keys, game_df):
    """This function loops through all game urls in a dataframe
    and stores all relevant game data in the prespecified game 
    dictionary and afterwards appends to the overall dataframe."""
    try:
        for game_url in game_url_list:
            game_request = http.request("GET", game_url)
            soup = BeautifulSoup(game_request.data, 'lxml')

            game_dict = {key: None for key in dict_keys}
            game_dict["game_url"] = game_url
            game_dict = get_game_data(soup, game_dict)
            game_dict = get_player_data(soup, game_dict)
            #game_dict = get_coach_data(soup, game_dict)
            #game_dict = get_goal_data(soup, game_dict)
            game_dict = get_card_data(soup, game_dict)

            game_df = game_df.append(game_dict, ignore_index=True)
    except:
        pass

    return game_df

if __name__ == '__main__':
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    # At this stage we have to make sure to use the same dictionary
    # throughout the scraping to not run into issues in the appending
    # of the dataframe.
    dict_keys = get_dict_keys()

    # Get all matchday files stores in folder.
    matchday_files = glob.glob(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "*.csv"))

    # Loop through all matchday files.
    for i, file in enumerate(matchday_files):
        # Load matchday csv files.
        matchday_df = pd.read_csv(
            ppj("OUT_DATA_FOOTBALL_MTCHDAY", "{}".format(file)), encoding='cp1252')
        # Get all game urls within each matchday file to a list
        game_url_list = matchday_df["game_url"].tolist()[0:10]

        # Initialize dataframe and run scraping.
        game_df = pd.DataFrame()
        game_df = run_scraping(game_url_list, dict_keys, game_df)
        game_id = matchday_df.loc[i, "ID"]
        game_df["game_id"] = game_id

        # Split date into day, month and year and store in seperate columns.
        date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
        game_df = pd.concat(
            [game_df, game_df["date"].str.extract(date_data).astype(int)], axis=1)
        # To four digit integer.
        game_df["fb_year"] = game_df["fb_year"] + 2000

        # Save as csv file.
        game_df.to_csv(ppj("OUT_DATA_FOOTBALL_FINAL",
                           "{}.csv".format(game_id)), index=False)

    open(ppj("OUT_DATA_FOOTBALL_FINAL", "game_scraping_finished.txt"), 'a').close()
