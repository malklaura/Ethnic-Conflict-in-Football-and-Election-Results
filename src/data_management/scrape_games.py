import datetime
import os.path
import urllib3
import certifi
import pandas as pd
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def get_soup_obj(url):
    page_request = http.request("GET", url)
    soup = BeautifulSoup(page_request.data, 'lxml')
    return soup

matchday_checker = pd.read_csv(
    ppj("OUT_DATA", "matchday_df.csv"), encoding='cp1252')
matchday_urls = matchday_df["matchday_url"]

for i, matchday_url in enumerate(matchday_urls):
    matchday_soup = get_soup_obj(matchday_url)
    games = matchday_soup.findAll("td", {"class": "liga_spielplan_container"})

    file_name = matchday_df.loc[i, "ID"]

    if not os.path.isfile(ppj("OUT_DATA", "{}.csv".format(file_name))):

        matchday_df = pd.DataFrame()

        for j, game in enumerate(games):

            game_dict = dict()

            game_dict["href"] = game.a["href"]
            if game.find("div", {"liga_spieltag_vorschau_datum_content_ergebnis"}) != None:
                game_dict["doable"] = 1
                #matchdays_df.at[i, "date"] = datetime.datetime.now()
            elif game.find("div", {"class": "liga_spieltag_vorschau_datum_content"}) != None:
                if game.find("div", {"class": "liga_spieltag_vorschau_datum_content"}).text == 'abg.':
                    game_dict["doable"] = 1
                    game_dict["abgesagt"] = 1
                elif game.find("div", {"class": "liga_spieltag_vorschau_datum_content"}).text == 'abbr.':
                    game_dict["doable"] = 1
                    game_dict["abbruch"] = 1
                else:
                    game_dict["doable"] = 0
                    try:
                        game_dict["date"] = datetime.datetime.strptime(game.find(
                            "div", {"class": "liga_spieltag_vorschau_datum_content"}).text + str(2019), '%d.%m.%Y')
                    except ValueError:
                        game_dict["note"] = "check date manually"
            elif game.find("div", {"class", "liga_spieltag_vorschau_datum "}).text == '\nabbr.\n':
                game_dict["doable"] = 1
                game_dict["abbruch"] = 1
            else:
                print(i)

            matchday_df = matchday_df.append(game_dict, ignore_index=True)

        matchday_df.to_csv(ppj("OUT_DATA", "{}.csv".format(file_name)))

        matchday_checker.loc[j, "done"] = 1

    else:
        pass

matchday_checker.to_csv(ppj("OUT_DATA", "matchday_checker.csv"))