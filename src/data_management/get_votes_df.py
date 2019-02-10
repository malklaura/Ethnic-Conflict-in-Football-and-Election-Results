import certifi
import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

os.chdir("C:/Users/maxim/Documents/master_eco/effective_programming")

def get_elections_soup(municipality_url):
    municipality_page = http.request("GET", municipality_url)
    page_soup = BeautifulSoup(municipality_page.data, 'lxml')
    elections_soup = page_soup.find_all("tr")[1:]
    return elections_soup


def get_export_url(level_soup, election_url):
    export_soup = level_soup.find_all("ul", {"class": "dropdown-menu"})[-1]
    export_href = export_soup.find_all("a")[-1]["href"]
    votes_dict["export_url"] = election_url.rsplit('/', 1)[0] + '/' + export_href


def get_voting_level(poss_election, election_url):
    zweitstimmen = poss_election.a["href"]
    zweitstimmen_url = election_url.rsplit('/', 1)[0] + '/' + zweitstimmen
    zweitstimmen_page = http.request("GET", zweitstimmen_url)
    zweitstimmen_soup = BeautifulSoup(zweitstimmen_page.data, 'lxml')

    voting_level = zweitstimmen_soup.find_all(
        "div", {"class": "container-fluid"})[0]
    voting_level = voting_level.find("ul", {"class": "nav navbar-nav"})
    voting_level = voting_level.find_all("a")
    return zweitstimmen_url, voting_level


def get_poss_elections(municipality_url, election):
    election_url = municipality_url.rsplit('/', 2)[0] + election.a["href"][2:]
    election_page = http.request("GET", election_url)
    election_soup = BeautifulSoup(election_page.data, 'lxml')
    poss_elections = election_soup.find_all("div", {"class": "well well-sm"})
    return election_url, poss_elections


def get_election_type_str(election):
    election_date = election.a.text
    election_type_str = election.text.strip().replace(election_date, "")
    return election_date, election_type_str


def bundestag_check(election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url):
    if "Bundestag" in election_type_str:
        for poss_election in poss_elections:
            if all(word in poss_election.script.get_text() for word in ["Bundestag", "Zweitstimmen"]):
                zweitstimmen_url, voting_level = get_voting_level(
                    poss_election, election_url)

                for level in voting_level:
                    if "Wahlbezirk" in level.text:
                        votes_dict = dict()
                        votes_dict = fill_votes_dict(
                            votes_dict, zweitstimmen_url, level, "BW", municipality_url, election_date, election_url)
                        votes_df = votes_df.append(
                            votes_dict, ignore_index=True)
    return votes_df


def landtag_check(election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url):
    if "Landtag" in election_type_str:
        for poss_election in poss_elections:
            if all(word in poss_election.script.get_text() for word in ["Landtag", "Zweitstimmen"]):
                zweitstimmen_url, voting_level = get_voting_level(
                    poss_election, election_url)

                for level in voting_level:
                    if "Stimmbezirk" in level.text:
                        votes_dict = dict()
                        votes_dict = fill_votes_dict(
                            votes_dict, zweitstimmen_url, level, "LW", municipality_url, election_date, election_url)
                        votes_df = votes_df.append(
                            votes_dict, ignore_index=True)
    return votes_df


def europawahl_check(election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url):
    if "Europa" in election_type_str:
        for poss_election in poss_elections:
            if "Europa" in poss_election.script.get_text():
                zweitstimmen_url, voting_level = get_voting_level(
                    poss_election, election_url)

                for level in voting_level:
                    if "Wahlbezirk" in level.text:
                        votes_dict = dict()
                        votes_dict = fill_votes_dict(
                            votes_dict, zweitstimmen_url, level, "EW", municipality_url, election_date, election_url)
                        votes_df = votes_df.append(
                            votes_dict, ignore_index=True)
    return votes_df


def fill_votes_dict(votes_dict, zweitstimmen_url, level, election_abbrev, municipality_url, election_date, election_url):
    votes_dict["municipality_url"] = municipality_url
    votes_dict["election_date"] = election_date
    votes_dict["election_type"] = election_abbrev
    votes_dict["election_url"] = election_url
    votes_dict["zweitstimmen_url"] = zweitstimmen_url
    votes_dict["voting_level"] = level.text

    level_href = level["href"]
    if "Erststimmen" in level_href:
        level_href = level_href.replace(
            "Erststimmen", "Zweitstimmen")

    level_url = election_url.rsplit(
        '/', 1)[0] + '/' + level_href
    level_page = http.request("GET", level_url)
    level_soup = BeautifulSoup(
        level_page.data, 'lxml')

    votes_dict["level_url"] = level_url
    votes_dict["export_url"] = get_export_url(
        level_soup, election_url)

    return votes_dict

def run_scrapping(municipality_url, votes_df):
    elections_soup = get_elections_soup(municipality_url)

    for election in elections_soup:
        election_date, election_type_str = get_election_type_str(election)

        if any(word in election_type_str for word in ["Bundestag", "Landtag", "Europa"]):
            election_url, poss_elections = get_poss_elections(municipality_url, election)
            
            votes_df = bundestag_check(
	            election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url)
            votes_df = landtag_check(
	            election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url)
            votes_df = europawahl_check(
	            election_type_str, poss_elections, votes_df, election_url, election_date, municipality_url)
        else:
            pass
    return votes_df

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

# Read in municipality_df.
municipality_df = pd.read_csv(
    "municipality_df.csv", encoding='cp1252')

# Run web scraping device only on scrappable municipalities as defined in get_mun.py
scrappable_municipalities = municipality_df[
    municipality_df["scrappable"] == 1]["href"].tolist()
# Just for faster computation in this phase 
scrappable_municipalities = scrappable_municipalities[0:10]

# Start scraping process.
votes_df = pd.DataFrame()
votes_dict = dict()

for municipality_url in tqdm(scrappable_municipalities):
    try:
    	votes_df = run_scrapping(municipality_url, votes_df)
    except:
    	pass

votes_df.to_csv("votes_df.csv")
