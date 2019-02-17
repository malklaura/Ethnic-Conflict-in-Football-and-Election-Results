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
    try:
        cards_soup = soup.find("table", {"class": "content_table_std spielerstrafen"})
        cards_soup = cards_soup.find_all("td", {"valign": "top"})
        hmsd_cards = cards_soup[0].findAll("div", {"class": "tn_item"})
        awsd_cards = cards_soup[1].findAll("div", {"class": "tn_item"})

        minmax = min(max(len(hmsd_cards), len(awsd_cards)), 11)
        for j in range(minmax):    
            try:
                player = hmsd_cards[j].a.text
                minute = hmsd_cards[j].find("span", {"class": "klammerzahl"}).text[:-1]
                
                game_dict["hmsd_card_plyr_" + str(j)] = player
                game_dict["hmsd_card_min_" + str(j)] = minute
                
                # Scraping of card colors.
                if hmsd_cards[j].div["style"] == "color:#FBDB04;":
                    game_dict["hmsd_card_clr_" + str(j)] = 1  # yellow = 1
                    game_dict["hmsd_card_yllw"] += 1
                elif hmsd_cards[j].div["style"] == "color:#D7110C;":
                    game_dict["hmsd_card_clr_" + str(j)] = 2  # red = 2
                    game_dict["hmsd_card_red"] += 1
                elif hmsd_cards[j].div["class"][0] == "icon_gelbrot":
                    game_dict["hmsd_card_clr_" + str(j)] = 3  # yellow / red = 3
                    game_dict["hmsd_card_yllw"] += 1  # counted as two yellow cards
                else:
                    game_dict["hmsd_card_clr_" + str(j)] = np.nan
            except:
                pass
            
            try:
                player = awsd_cards[j].a.text
                minute = awsd_cards[j].find("span", {"class": "klammerzahl"}).text[:-1]
                
                game_dict["awsd_card_plyr_" + str(j)] = player
                game_dict["awsd_card_min_" + str(j)] = minute
                
                # Scraping of card colors.
                if hmsd_cards[j].div["style"] == "color:#FBDB04;":
                    game_dict["awsd_card_clr_" + str(j)] = 1  # yellow = 1
                    game_dict["awsd_card_yllw"] += 1
                elif hmsd_cards[j].div["style"] == "color:#D7110C;":
                    game_dict["awsd_card_clr_" + str(j)] = 2  # red = 2
                    game_dict["awsd_card_red"] += 1
                elif hmsd_cards[j].div["class"][0] == "icon_gelbrot":
                    game_dict["awsd_card_clr_" + str(j)] = 3  # yellow / red = 3
                    game_dict["awsd_card_yllw"] += 1  # counted as two yellow cards
                else:
                    game_dict["awsd_card_clr_" + str(j)] = np.nan
                    
            except:
                pass
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
#         coach_hmsd = soup.findAll(
#             "div", {"class": "aufstellung_ausgabe_block homeside"})[2]
#         game_dict["coach_hmsd"] = coach_hmsd.a.text
#         coach_awsd = soup.findAll(
#             "div", {"class": "aufstellung_ausgabe_block awayside"})[2]
#         game_dict["coach_awsd"] = coach_awsd.a.text
#     except:
#         pass

#     return game_dict


def get_player_data(soup, game_dict):
    """This function returns player data for both the home- and awayteam
    from a  soup object and writes those information in the according 
    matchday dataframe. Besides player names, also corresponding player
    urls are retrieved."""

    try:
        hmsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block homeside"})[0]
        plyrs_hmsd = hmsd.findAll("a", {"class": "spieler_linkurl"})
    except:
        pass
    
    try:
        awsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block awayside"})[0]
        plyrs_awsd = awsd.findAll("a", {"class": "spieler_linkurl"})
    except:
        pass
    
    for j in range(11):
        try:
            game_dict["hmsd_plyr_" + str(j)] = plyrs_hmsd[j].text
            game_dict["hmsd_plyr_url_" + str(j)] = plyrs_hmsd[j]["href"]
        except:
            pass
        try:
            game_dict["awsd_plyr_" + str(j)] = plyrs_awsd[j].text
            game_dict["awsd_plyr_url_" + str(j)] = plyrs_awsd[j]["href"]
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
        for j, team in enumerate(["hmsd_", "awsd_"]):
            game_dict[team + "team"] = team_title[j].a["title"]
            game_dict[team + "team_url"] = team_title[j].a["href"]
            game_dict[team + "club"] = club_title[j]["title"]
    except:
        pass

    return game_dict


def get_dict_keys():
    dict_keys = ["time", "date", "league", "game_url", "referee", "result", "matchday"]
    for team in ["hmsd", "awsd"]:
        primary_keys = ["{0}_{1}".format(team, x) for x in ["club", "team_url", "team", "card_red", "card_yllw"]]
        dict_keys += primary_keys
        for j in range(11):
            identifier = ["_plyr_url_", "_plyr_", "_card_plyr_", "_card_min_", "_card_clr_"]
            further_keys = ["{0}{1}{2}".format(team, x, j) for x in identifier]
            dict_keys += further_keys

    return dict_keys


def run_scraping(game_url_list, dict_keys, game_df):
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

    dict_keys = get_dict_keys()

    matchday_files = glob.glob(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "*.csv"))
    for i, file in enumerate(matchday_files):
        matchday_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "{}".format(file)), encoding='cp1252')
        game_url_list = matchday_df["game_url"].tolist()[0:10]
        game_df = pd.DataFrame()

        game_df = run_scraping(game_url_list, dict_keys, game_df)
        
        date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
        game_df = pd.concat([game_df, game_df["date"].str.extract(date_data).astype(int)], axis=1)
        game_df["fb_year"] = game_df["fb_year"] + 2000      

        game_df.to_csv(ppj("OUT_DATA_FOOTBALL_FINAL", "{}.csv".format(i)), index=False)
