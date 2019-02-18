import datetime
import urllib3
import certifi
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_soup_obj(url):
    page_request = http.request("GET", url)
    soup = BeautifulSoup(page_request.data, 'lxml')
    return soup


def get_mtchdy_data(games, matchday_df, file_name):
    for j, game in enumerate(games):

        game_dict = {}
        game_dict["ID"] = file_name

        game_dict["game_url"] = game.a["href"]
        if game.find("div", {"liga_spieltag_vorschau_datum_content_ergebnis"}) != None:
            game_dict["doable"] = 1
            game_dict["reason"] = 0
        elif game.find("div", {"class": "liga_spieltag_vorschau_datum_content"}) != None:
            game_dict["doable"] = 0
            game_dict["reason"] = game.find(
                "div", {"class": "liga_spieltag_vorschau_datum_content"}).text
        else:
            game_dict["doable"] = 0
            game_dict["reason"] = np.nan

        matchday_df = matchday_df.append(game_dict, ignore_index=True)
    return matchday_df

if __name__ == '__main__':
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    league_df = pd.read_csv(
        ppj("OUT_DATA_FOOTBALL", "matchday_data.csv"), encoding='cp1252')
    league_url_list = league_df["mtchdy_url"].tolist()[0:2]

    for i, url in enumerate(league_url_list):

        matchday_df = pd.DataFrame()
        file_name = league_df.loc[i, "ID"]

        matchday_soup = get_soup_obj(url)
        games = matchday_soup.findAll(
            "td", {"class": "liga_spielplan_container"})

        matchday_df = get_mtchdy_data(games, matchday_df, file_name)

        matchday_df.to_csv(ppj("OUT_DATA_FOOTBALL_MTCHDAY",
                               "{}.csv".format(file_name)), index=False)

    open(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "mtchday_scraping_finished.txt"), 'a').close()

