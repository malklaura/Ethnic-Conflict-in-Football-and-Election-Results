import re
import urllib3
import certifi
import pandas as pd
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_soup_obj(url):
    page_request = http.request("GET", url)
    soup = BeautifulSoup(page_request.data, 'lxml')
    return soup


def get_kreise_list(region, main_url, matchday_dict):
    region_url = main_url + "/" + region
    region_soup = get_soup_obj(region_url)

    matchday_dict["region"] = region
    matchday_dict["region_url"] = region_url

    kreise_soup = region_soup.find("td", {"class": "kreise_select"}).div
    kreise_url_list = [main_url + a['href']
                       for a in kreise_soup.find_all('a', href=True) if a.text]
    kreise_url_list = [x for x in kreise_url_list if not "profi" in x]
    kreise_url_list.remove(region_url)
    return kreise_url_list


def get_league_list(kreis_url, matchday_dict):
    kreis_soup = get_soup_obj(kreis_url)
    kreis = kreis_soup.find(
        "td", {"class": "kreise_select"}).div.a.span.text

    matchday_dict["kreis"] = re.sub('\s|-', '_', kreis).lower()
    matchday_dict["kreis_url"] = kreis_url

    leagues_soup = kreis_soup.find(
        "td", {"class": "liga-select first-selected"}).div
    leagues_url_list = [main_url + a['href']
                        for a in leagues_soup.find_all('a', href=True) if a.text]
    # At this stage I exclude pokal championships, since the structure is
    # quite different from normal leagues.
    exclsn_strngs = ["pokal", "hallen", "cup"]
    leagues_url_list = [x for x in leagues_url_list if not any(
        strng in x for strng in exclsn_strngs)]
    return leagues_url_list


def get_seaons_list(league_url, matchday_dict):
    league_soup = get_soup_obj(league_url)

    # League identifier to create unique ID in the end.
    league_identifier = league_soup.find(
        "div", {"class": "content_team_header"}).h1.text
    league_identifier = re.sub('\s|-', '_', re.sub(
        ",", "", league_identifier)).lower()

    # Write league and corresponding url in dictionary.
    matchday_dict["league"] = league_identifier
    matchday_dict["league_url"] = league_url

    # To also extract all past seasons, I locate the archive and the items
    # therein.
    seasons_list = league_soup.find(
        "table", {"class": "liga_tabelle_archiv"})
    seasons_list = seasons_list.findAll("a")
    return seasons_list


def get_matchday_url(season, matchday_dict, matchday_df):
    season_identifier = re.sub('/', '_', season.text)

    # For the current season the way to access the matchday page is
    # slightly different from the one to access past seasons.
    if "html" in season["href"]:
        mtchdy_season_url = season["href"].replace(
            ".html", "/spielplan.html")
    else:
        mtchdy_season_url = season["href"] + "/spielplan"

    matchday_dict["season"] = season_identifier
    matchday_dict["matchday_url"] = mtchdy_season_url
    matchday_dict["ID"] = "_".join([matchday_dict["region"], matchday_dict[
                                   "kreis"], matchday_dict["league"], matchday_dict["season"]])

    matchday_df = matchday_df.append(
        matchday_dict, ignore_index=True)
    return matchday_df
    

if __name__ == '__main__':
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    main_url = "https://www.fupa.net"
    # Although data for all parts of Germany exist, in a first step I want to
    # focus on those constituting NRW.
    regions = ["mittelrhein"]
    #regions = ["mittelrhein", "niederrhein", "ruhrgebiet", "westrhein"]

    matchday_dict = dict()
    matchday_df = pd.DataFrame()

    for region in regions:
        kreise_url_list = get_kreise_list(region, main_url, matchday_dict)

        for kreis_url in kreise_url_list:
            leagues_url_list = get_league_list(kreis_url, matchday_dict)

            for league_url in leagues_url_list:
                seasons_list = get_seaons_list(league_url, matchday_dict)

                for season in seasons_list:
                    matchday_df = get_matchday_url(season, matchday_dict, matchday_df)

    matchday_df.to_csv(ppj("OUT_DATA", "matchday_df.csv"))
