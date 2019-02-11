import urllib3
import certifi
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def load_webdriver(url, sec):
    """This functions loads the firefox webdriver for a prespecified 
    url. The sec argument generates some delay to ensure that the 
    driver is properly loaded before further code is run."""
    driver = webdriver.Firefox(
        executable_path=r"C:/Users/maxim/Documents/master_eco/eco/geckodriver.exe")
    driver.get(url)
    # Use some delay, since webdriver needs some time to load.
    time.sleep(sec)
    return driver


def get_mun_soup(driver):
    """Given a webdriver object this function returns the
    corresponding soup object containing all municipalites
    listed on current site."""
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    mun_soup = soup.find_all("tr", {"role": "row"})[1:]
    return soup, mun_soup


def fill_mun_dict(mun, elec_mun_df):
    """This functions stores the name, state and url of a single
    municipality in a dictionary that afterwards is appended to 
    a prespecified dataframe."""
    mun_dict = dict()
    mun_dict["elec_page"] = mun.a["href"]
    mun_dict["mun_name"] = mun.a.text
    mun_dict["state"] = mun.find_all("td")[2].text

    elec_mun_df = elec_mun_df.append(mun_dict, ignore_index=True)
    return elec_mun_df


def run_scraping(driver):
    """This function scrapes all relevant information of municipalities
    in the state of NRW. As soon as the end of a page is read, the scraping
    automatically continues on the next site, until the last page of 
    the votemanager site is reached."""
    elec_mun_df = pd.DataFrame()

    while True:
        soup, mun_soup = get_mun_soup(driver)

        # Loop through all municipalities on a site.
        for mun in mun_soup:
            if mun.find_all("td")[2].text == "Nordrhein-Westfalen":
                elec_mun_df = fill_mun_dict(mun, elec_mun_df)

        # Go to next page when all municipalties are scraped.
        driver.find_element_by_xpath('//a[text()="weiter"]').click()

        # After each iteration check if last page is reached.
        if soup.find("li", {"class": "paginate_button next disabled"}) != None:
            driver.close()
            break

    # Idnetiefy scrapable municipalties by substing in url.
    key_indicators = ["://votemanager.", "://wahlen."]
    elec_mun_df["scrapable"] = elec_mun_df["url"].apply(
        lambda x: 1 if any(key in x for key in key_indicators) else 0)
    return elec_mun_df

if __name__ == '__main__':
    # Needed to work with htpps sites.
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    # Open Firefox driver and open votemanager site.
    votemanger_url = "http://wahlen.votemanager.de"
    driver = load_webdriver(votemanger_url, 5)

    # Run scraping process, afterwards store resulting dataframe.
    elec_mun_df = run_scraping(driver)
    elec_mun_df.to_csv(ppj("OUT_DATA_ELEC", "election_mun.csv"))
