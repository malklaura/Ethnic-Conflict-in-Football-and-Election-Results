'''Scrape download urls on election office level using multiprocessing.'''
import itertools
import pandas as pd
import multiprocessing as mp
from bld.project_paths import project_paths_join as ppj
from src.data_management.election_data_management.get_dwnld_urls import scrape_elec_data


def main():
    # Load previously scraped matchday files, containing municipal urls.
    elec_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_mun.csv"))

    # List to store resulting election dictionaries.
    dict_list = []

    # Multiprocessed scraping.
    with mp.Pool() as pool:
        out = pool.map(run_scraping, elec_df.mun_url.values)
        out = list(itertools.chain.from_iterable(out))  # Flatten list.
        dict_list.extend(out)  # Extent dictionaries to list.

    # Create dataframe from dictionaries and save as csv.
    df = pd.DataFrame(dict_list)
    df.to_csv(ppj("OUT_DATA_ELEC", "election_urls.csv"), index=False)

if __name__ == '__main__':
    main()

