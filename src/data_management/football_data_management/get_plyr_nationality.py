import certifi
import csv
import datetime
import glob
import re
import urllib3
import numpy as np
import pandas as pd
import multiprocessing as mp
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_unique_plyrs(game_df):
    """ Get columns containining individual player urls from homeside and
    awayside teams."""

    filter_col = [col for col in game_df if '_plyr_url' in col]

    # Only keep unique player urls.
    unique_plyrs = []
    for col in filter_col:
        unique_plyrs += game_df[col].tolist()

    unique_plyrs = list(set(unique_plyrs))[1:]

    return unique_plyrs


def get_age_nat(plyr_url):
    """This function return age and  nationality of a player from 
    the provided player url."""

    plyr_dict = {"url": plyr_url}

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    page_request = http.request("GET", plyr_url)
    plyr_soup = BeautifulSoup(page_request.data, 'lxml')
    info_soup = plyr_soup.find("td", {"class": "stammdaten"})

    # Scrape age and nationality information from each page. Due to the
    # possible specification of a nickname the location of age and
    # nationality is not unqiuely defined by a single "tr" object, which
    # is why one need to check two possibilities.
    try:
        if "Geburtsdatum" in info_soup.table.find_all("tr")[1].text:
            birthday = info_soup.table.find_all("tr")[1].text
            plyr_dict["age"] = re.search(
                r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyr_dict["nat"] = info_soup.table.find_all("tr")[2].img["title"]
        elif "Geburtsdatum" in info_soup.table.find_all("tr")[2].text:
            birthday = info_soup.table.find_all("tr")[2].text
            plyr_dict["age"] = re.search(
                r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyr_dict["nat"] = info_soup.table.find_all("tr")[3].img["title"]
        else:
            plyr_dict["age"] = np.nan
            plyr_dict["nat"] = np.nan
    # To ensure that dictionary is appended to dataframe.
    except:
        plyr_dict["age"] = np.nan
        plyr_dict["nat"] = np.nan

    return plyr_dict

# def get_stations(plyr_soup, plyr_dict):
#     try:
#         stations_soup = plyr_soup.find("table", {"class": "stationen content_table_std"})
#         stations = stations_soup.find_all("b")
#         saisons = stations_soup.find_all("td", {"class": "saison"})
#         leagues = stations_soup.find_all("div", {"class": "liga_zusatz"})

#         for j, station in enumerate(stations[0:10]):
#             plyr_dict["station_verein_" + str(j)] = station.text
#             plyr_dict["saison_verein_" + str(j)] = saisons[j].span.text
#             plyr_dict["league_verein_" + str(j)] = leagues[j].a.text

#     except:
#         pass

#     return plyr_dict

if __name__ == '__main__':
    # Read in final dataset, containing all games and player data.
    game_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_combined.csv"))
    unique_plyrs = get_unique_plyrs(game_df)

    # Scraping via multiprocessing.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(get_age_nat, unique_plyrs)
        dict_list.extend(out)

    plyr_df = pd.DataFrame(dict_list) # Dicts to df.

    # Save player url, age and nationality in seperate csv file.
    plyr_df.to_csv(ppj("OUT_DATA_FOOTBALL", "player_data.csv"), index=False)
