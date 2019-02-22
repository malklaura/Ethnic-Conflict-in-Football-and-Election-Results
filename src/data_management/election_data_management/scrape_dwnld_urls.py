'''Scrape download urls on election office level using multiprocessing.'''
import itertools
import pandas as pd
import multiprocessing as mp
from bld.project_paths import project_paths_join as ppj
from src.data_management.election_data_management.get_dwnld_urls import run_scraping


def main():
    # Load previously scraped matchday files, containing municipal urls.
    elec_mun_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_mun.csv"), encoding='cp1252')
    scrapable_mun = elec_mun_df[elec_mun_df[
        "scrapable"] == 1]["elec_page"].values

    # List to store resulting election dictionaries.
    dict_list = []

    # Multiprocessed scraping.
    with mp.Pool() as pool:
        out = pool.map(run_scraping, scrapable_mun)
        out = list(itertools.chain.from_iterable(out))  # Flatten list.
        dict_list.extend(out)  # Extent dictionaries to list.

    # Create dataframe from dictionaries and save as csv.
    df = pd.DataFrame(dict_list)
    df.to_csv(ppj("OUT_DATA_ELEC", ".csv"))

if __name__ == '__main__':
    main()
