import certifi
import re
import urllib3
import numpy as np
import pandas as pd
import multiprocessing as mp

from bs4 import BeautifulSoup
from bld.project_paths import project_paths_join as ppj


def get_unique_plyrs(game_df):
    """
    Get columns containining individual player urls from homeside and
    awayside team.
    """

    filter_col = [col for col in game_df if '_plyr_url' in col]

    # Only keep unique player urls.
    unique_plyrs = []
    for col in filter_col:
        unique_plyrs += game_df[col].unique().tolist()

    # Keep unique and string entries.
    unique_plyrs = list(set(unique_plyrs))[1:]
    unique_plyrs = [x for x in unique_plyrs if type(x) is str]

    return unique_plyrs[0:100]


def get_age_nat(plyr_url):
    """
    Returns age and nationality of a player from 
    a provided player url in a dictionary.
    """

    plyr_dict = {'url': plyr_url}
    
    try:
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        page_request = http.request('GET', plyr_url)
        plyr_soup = BeautifulSoup(page_request.data, 'lxml')
        info_soup = plyr_soup.find('td', {'class': 'stammdaten'})

        # Scrape age and nationality information from each page. Due to the
        # possible specification of a nickname the location of age and
        # nationality is not unqiuely defined by a single 'tr' object, which
        # is why one need to check two possibilities.
        if 'Geburtsdatum' in info_soup.table.find_all('tr')[1].text:
            birthday = info_soup.table.find_all('tr')[1].text
            plyr_dict['age'] = re.search(
                r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyr_dict['nat'] = info_soup.table.find_all('tr')[2].img['title']
        elif 'Geburtsdatum' in info_soup.table.find_all('tr')[2].text:
            birthday = info_soup.table.find_all('tr')[2].text
            plyr_dict['age'] = re.search(
                r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyr_dict['nat'] = info_soup.table.find_all('tr')[3].img['title']
        else:
            plyr_dict['age'] = np.nan
            plyr_dict['nat'] = np.nan
    # To ensure that dictionary is appended to dataframe.
    except:
        pass

    return plyr_dict


def main():
    # Read in final dataset, containing all games and player data.
    game_df = pd.read_csv(ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'))
    unique_plyrs = get_unique_plyrs(game_df)

    # Scraping via multiprocessing.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(get_age_nat, unique_plyrs)
        dict_list.extend(out)

    plyr_df = pd.DataFrame(dict_list)  # Dicts to df.

    # Save player url, age and nationality in seperate csv file.
    plyr_df.to_csv(
        ppj('OUT_DATA_FOOTBALL', 'plyr_nationality.csv'), index=False)

if __name__ == '__main__':
    main()
