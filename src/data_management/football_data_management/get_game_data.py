import urllib3
import certifi
import re
import glob
import pandas as pd
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_card_data(soup, game_df, i):
    try:
        cards_soup = soup.find_all("td", {"valign": "top"})
        hmsd_cards = cards_soup[0].findAll("div", {"class": "tn_item"})
        awsd_cards = cards_soup[1].findAll("div", {"class": "tn_item"})
        
        for team in [hmsd_cards, awsd_cards]:
            ident = str(j)[0:3]

            for j, card in enumerate(team):
                game_df.at[i, ident + "_card_plyr_" + str(j)] = card.a.text
                game_df.at[
                    i, ident + "_card_min_" + str(j)] = card.find("span", {"class": "klammerzahl"}).text[:-1]

                if card.div["style"] == "color:#FBDB04;":
                    game_df.at[i, ident + "_card_clr_" + str(j)] = 1 # yellow = 1
                    game_df.at[i, ident + "_card_yllw"] += 1
                elif card.div["style"] == "color:#D7110C;":
                    game_df.at[i, ident + "_card_clr_" + str(j)] = 2  # red = 2
                    game_df.at[i, ident + "_card_red"] += 1
                elif card.div["class"][0] == "icon_gelbrot":
                    game_df.at[i, ident + "_card_clr_" + str(j)] = 3  # yellow / red = 3
                    game_df.at[i, ident + "_card_yllw"] += 1
                else:
                    game_df.at[i, ident + "_card_clr_" + str(j)] = "unknown card_clr"
    except:
        pass

    return game_df


def get_goal_data(soup, game_df, i):
    try:
        goals_soup = soup.find(
            "table", {"class": "content_table_std torschuetzen"})
        goals = goals_soup.findAll(
            "div", {"class": "tn_item torschuetzen_ausgabe"})

        for j, goal in enumerate(goals):
            game_df.at[
                i, "goal_" + str(j)] = goal.find("span", {"class": "spielstand"}).text
            game_df.at[i, "goal_plyr_" + str(j)] = goal.img["title"]
            game_df.at[
                i, "goal_min" + str(j)] = goal.find("span", {"class": "klammerzahl"}).text[:-1]
    except:
        pass

    return game_df


def get_coach_data(soup, game_df, i):
    try:
        coach_hmsd = soup.findAll(
            "div", {"class": "aufstellung_ausgabe_block homeside"})[2]
        game_df.at[i, "coach_hmsd"] = coach_hmsd.a.text
        coach_awsd = soup.findAll(
            "div", {"class": "aufstellung_ausgabe_block awayside"})[2]
        game_df.at[i, "coach_awsd"] = coach_awsd.a.text
    except:
        pass

    return game_df


def get_player_data(soup, game_df, i):
    try:
        hmsd = soup.findAll(
            "div", {"class": "aufstellung_ausgabe_block homeside"})[0]
        hmsd_plyr = hmsd.findAll("a", {"class": "spieler_linkurl"})

        awsd = soup.findAll(
            "div", {"class": "aufstellung_ausgabe_block awayside"})[0]
        awsd_plyr = awsd.findAll("a", {"class": "spieler_linkurl"})
    except:
        pass

    try:
        for team in [hmsd_plyr, awsd_plyr]:
            ident = str(team)

            for j, plyr in enumerate(team):
                try:
                    game_df.at[i, ident + "_" + str(j + 1)] = plyr[j].text
                    game_df.at[i, ident + "_url_" + str(j + 1)] = plyr[j]["href"]
                except:
                    pass
    except:
        pass

    return game_df


def get_game_data(soup, game_df, i):
        # Summary Statistics
    try:
        date_soup = soup.find("div", {"class": "spielbericht_tipp_status"})
        game_df.at[i, "league"] = date_soup.div.span.text
        date_str = date_soup.div.text
        game_df.at[i, "date"] = re.search(
            r'\d{2}.\d{2}.\d{2}', date_str).group(0)
        game_df.at[i, "time"] = re.search(r'\d{2}:\d{2}', date_str).group(0)
        game_df.at[i, "matchday"] = re.search(
            r'[|]\d+', date_str).group(0)[1:]
    except:
        pass

    try:
        game_df.at[i, "result"] = soup.find("div", {"class": "stand"}).text
    except:
        pass

    try:
        game_df.at[i, "referee"] = soup.find(
            "span", {"class": "schiri_link"}).text
    except:
        pass

    smmry_container = soup.find(
        "div", {"class": "spielbericht_ergebnis_wrapper"})
    club_title = smmry_container.find_all("img")
    team_title = smmry_container.findAll("div", {"class": "teaminfo"})

    teams = ["hmsd_", "awsd_"]

    for j, team in enumerate(teams):
        game_df.at[i, team + "team"] = team_title[j].a["title"]
        game_df.at[i, team + "team_url"] = team_title[j].a["href"]
        game_df.at[i, team + "club"] = club_title[j]["title"]

# =============================================================================
#     try:
#         game_df.at[i, "avg_hmsd"] = hmsd.div.a.text[-5:]
#         game_df.at[i, "avg_awsd"] = awsd.div.a.text[-5:]
#     except AttributeError as e:
#         pass
# =============================================================================

    return game_df

if __name__ == '__main__':
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    matchday_files = glob.glob(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "*.csv"))

    for file in matchday_files[0:1]:
        game_df = pd.read_csv("{}".format(file), encoding='cp1252')
        game_url_list = game_df["game_url"].tolist()

        for i, game_url in enumerate(game_url_list):
            game_request = http.request("GET", game_url)
            soup = BeautifulSoup(game_request.data, 'lxml')

            game_df = get_game_data(soup, game_df, i)
            game_df = get_player_data(soup, game_df, i)
            game_df = get_coach_data(soup, game_df, i)
            game_df = get_goal_data(soup, game_df, i)
            game_df = get_card_data(soup, game_df, i)

        if game_df["doable"].mean() == 1:
            game_df.to_csv(ppj("OUT_DATA_FOOTBALL_FINAL", "{}".format(file)))
        else:
            game_df.to_csv(ppj("OUT_DATA_FOOTBALL_PRELIM",
                                 "./prelim_csv/{}".format(file)))
