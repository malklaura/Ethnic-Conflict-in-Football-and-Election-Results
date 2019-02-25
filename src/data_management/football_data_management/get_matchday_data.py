import datetime
import urllib3
import certifi
import numpy as np
import pandas as pd
import multiprocessing as mp
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_soup_obj(url):
    """This function return the soup object from a given url."""

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    page_request = http.request("GET", url)
    soup = BeautifulSoup(page_request.data, 'lxml')

    return soup


def get_mtchdy_data(league_url):
    """This function return the games for a given league url. Moreover, it is 
    indicated wheter the respective game already took place and if not, when 
    it will be played."""

    # Get games soup.
    matchday_soup = get_soup_obj(league_url)
    games = matchday_soup.findAll(
        "td", {"class": "liga_spielplan_container"})

    # Get game information.
    matchday_df = pd.DataFrame()
    for j, game in enumerate(games):
        game_dict = {}
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

    if len(matchday_df) != 0:
        matchday_df["mtchdy_url"] = league_url
        return matchday_df
    else:
        pass


if __name__ == '__main__':
    # Load league data.
    league_df = pd.read_csv(
        ppj("OUT_DATA_FOOTBALL", "matchday_data.csv"), encoding='cp1252')

    # Scrape matchday data via multiprocessing.
    df_list = []
    with mp.Pool() as pool:
        out = pool.map(get_mtchdy_data, league_df.mtchdy_url.values)
        df_list.extend(out)

    game_df = pd.concat(df_list) # Create df from df list.
    game_df = game_df.merge(league_df, on="mtchdy_url") # Merge to league data.
    game_df.to_csv(ppj("OUT_DATA_FOOTBALL", "game_data.csv"), index=False) # Save as csv.
