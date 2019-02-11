import certifi
import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from bld.project_paths import project_paths_join as ppj


def get_soup_object(url):
    """This function returns a soup object from a given url."""
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    page_request = http.request("GET", url)
    page_soup = BeautifulSoup(page_request.data, 'lxml')
    return page_soup


def get_elections_soup(mun_url):
    """This function returns a soup object containing all elections
    contained in the municipality url."""
    page_soup = get_soup_object(mun_url)
    elections_soup = page_soup.find_all("tr")[1:]
    return elections_soup


def get_elec_type_str(elec):
    """This function returns the name of the considered election."""
    elec_date = elec.a.text
    elec_type_str = elec.text.strip().replace(elec_date, "")

    elec_dict["elec_date"] = elec_date
    return elec_type_str


def get_pssbl_elections(elec):
    """This function returns all elections that took place on a certain date.
    The need for this function arises from the fact, that more than one election
    can take place on the same day and that some elections have the possibility
    of Erst- and Zweistimmen."""
    elec_url = mun_url.rsplit('/', 2)[0] + elec.a["href"][2:]
    elec_soup = get_soup_object(elec_url)

    elec_dict["elec_url"] = elec_url

    poss_elections = elec_soup.find_all("div", {"class": "well well-sm"})
    return poss_elections


def get_voting_lvl(poss_election):
    """For each election data are available for different aggregation levels.
    I am only interested in the lowest level."""
    sublvl_href = poss_election.a["href"]
    sublvl_url = elec_dict["elec_url"].rsplit(
        '/', 1)[0] + '/' + sublvl_href
    sublvl_soup = get_soup_object(sublvl_url)

    voting_lvl = sublvl_soup.find_all(
        "div", {"class": "container-fluid"})[0]
    voting_lvl = voting_lvl.find("ul", {"class": "nav navbar-nav"})
    voting_lvl = voting_lvl.find_all("a")
    return voting_lvl


def get_dwnld_url(level, elec_abbrev):
    """This function returns the download url for a given voting level."""
    level_href = level["href"]
    if "Erststimmen" in level_href:
        level_href = level_href.replace(
            "Erststimmen", "Zweitstimmen")

    level_url = elec_dict["elec_url"].rsplit(
        '/', 1)[0] + '/' + level_href
    level_soup = get_soup_object(level_url)

    dwnld_soup = level_soup.find_all("ul", {"class": "dropdown-menu"})[-1]
    dwnld_href = dwnld_soup.find_all("a")[-1]["href"]
    dwnld_url = elec_dict["elec_url"].rsplit(
        '/', 1)[0] + '/' + dwnld_href

    elec_dict["dwnld_url"] = dwnld_url
    elec_dict["abbrev"] = elec_abbrev

    return elec_dict


def elec_type_check(elec_type_str, pssbl_elections, elec_type, elec_df):
    """This function checks, wheter a possible elections fulfills the requirements
    of the elections we want to download. The specific requirements are stored in 
    the elec_type dictionary."""
    if elec_type["srch_trm"] in elec_type_str:
        for poss_elec in pssbl_elections:
            if all(word in poss_elec.script.get_text() for word in [elec_type["srch_trm"], elec_type["class"]]):
                voting_lvl = get_voting_lvl(poss_elec)

                for level in voting_lvl:
                    if elec_type["level"] in level.text:
                        elec_dict = get_dwnld_url(level, elec_type["abbrev"])
                        elec_df = elec_df.append(elec_dict, ignore_index=True)
    return elec_df


def run_scrapping(mun_url, elec_df, elec_type_dict):
    """Run web scraping process over all scrapable municipalities. In the end 
    a dataframe containing all download urls is returned for those elections
    of interest."""
    elec_soup = get_elections_soup(mun_url)

    for elec in elec_soup:
        elec_type_str = get_elec_type_str(elec)
        elections_of_interest = ["Bundestag", "Landtag", "Europa"]
        if any(word in elec_type_str for word in elections_of_interest):
            pssbl_elections = get_pssbl_elections(elec)

            for elec_type in elec_type_dict.values():
                elec_df = elec_type_check(
                    elec_type_str, pssbl_elections, elec_type, elec_df)

    return elec_df

if __name__ == '__main__':
    # Read in municipality_df.
    elec_mun_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_mun.csv"), encoding='cp1252')

    scrapable_mun = elec_mun_df[elec_mun_df["scrapable"] == 1]["href"].tolist()[
        0:10]

    bw_dict = {"srch_trm": "Bundestag", "class": "Zweitstimmen",
               "level": "Wahlbezirk", "abbrev": "BW"}
    lw_dict = {"srch_trm": "Landtag", "class": "Zweitstimmen",
               "level": "Stimmbezirk", "abbrev": "LW"}
    ew_dict = {"srch_trm": "Europa", "class": "Europa",
               "level": "Wahlbezirk", "abbrev": "EW"}

    elec_type_dict = {"Bundestagswahl": bw_dict,
                      "Landtagswahl": lw_dict,
                      "Europawahl": ew_dict}

    # Start scraping process.
    elec_df = pd.DataFrame()
    elec_dict = {}

    for mun_url in tqdm(scrapable_mun):
        try:
            elec_df = run_scrapping(mun_url, elec_df, elec_type_dict)
        except:
            pass

    # Save election dataframe to .csv.
    elec_df.to_csv(ppj("OUT_DATA_ELEC", "election_urls.csv"))
