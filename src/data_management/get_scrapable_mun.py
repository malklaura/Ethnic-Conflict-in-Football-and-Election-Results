from bs4 import BeautifulSoup
import urllib3
import certifi
import time
import pandas as pd
from selenium import webdriver
from bld.project_paths import project_paths_join as ppj

def load_webdriver(url):
    """Given a league url this function returns a list, containing the
    url of all past seasons of this league. League name and url are
    stored in the matchday dictionary.""" 
    driver = webdriver.Firefox(executable_path=r"C:/Users/maxim/Documents/master_eco/eco/geckodriver.exe")
    driver.get(url)
    # Use some delay, since webdriver needs some time to load. Otherwise script will run on unloaded webdriver and fail.
    time.sleep(5)

def get_mun_soup(driver):
    """Given a league url this function returns a list, containing the
    url of all past seasons of this league. League name and url are
    stored in the matchday dictionary."""
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    mun_soup = soup.find_all("tr", {"role":"row"})[1:]
    return mun_soup


def fill_mun_dict(mun, mun_df):
    """Given a league url this function returns a list, containing the
    url of all past seasons of this league. League name and url are
    stored in the matchday dictionary."""
    mun_dict = dict()
    mun_dict["href"] = mun.a["href"]
    mun_dict["municipality"] = mun.a.text
    mun_dict["state"] = mun.find_all("td")[2].text
                
    mun_df = mun_df.append(votes_dict, ignore_index=True)
    return mun_df

if __name__ == '__main__':
    # Needed to work with htpps sites.
    http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

    # Open Firefox driver and open votemanager site.
    votemanger_url = "http://wahlen.votemanager.de"
    load_webdriver(votemanger_url)

    mun_df = pd.DataFrame()

    while True:    
        mun_soup = get_mun_soup(driver)

        for mun in mun_soup:
            if mun.find_all("td")[2].text == "Nordrhein-Westfalen":
                mun_df fill_mun_dict(mun, mun_df)

        driver.find_element_by_xpath('//a[text()="weiter"]').click()
        
        if soup.find("li", {"class": "paginate_button next disabled"}) != None:
            driver.close()
            break

    key_indicators = ["://votemanager.", "://wahlen."]    
    mun_df["scrapable"] = mun_df["href"].apply(lambda x: 1 if any(key in x for key in key_indicators) else 0)

    mun_df.to_csv(ppj("OUT_DATA", "mun_df.csv"))
