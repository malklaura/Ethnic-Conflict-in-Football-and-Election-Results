import glob
import urllib3
import certifi
import pandas as pd
import multiprocessing as mp
from bld.project_paths import project_paths_join as ppj
from src.data_management.football_data_management.scrape_games import scrape_game_data


def main():
    # Get all previously scraped matchday files.
    matchday_files = glob.glob(ppj("OUT_DATA_FOOTBALL_MTCHDAY", "*.csv"))

    # Loop through all matchday files.
    for i, file in enumerate(matchday_files):
        # Load matchday csv files.
        mtchdy_df = pd.read_csv(
            ppj("OUT_DATA_FOOTBALL_MTCHDAY", "{}".format(file)), encoding='cp1252')
        # Crawl information from website and store information in dict
        # that is appended to a list containing all game dicts.

        # Scraping.
        dict_list = []

        with mp.Pool() as pool:
            out = pool.map(scrape_game_data, mtchdy_df.game_url.values)
            dict_list.extend(out)

        # To dicts to daraframe.
        df = pd.DataFrame(dict_list)

        game_id = mtchdy_df.loc[i, "ID"]
        df["game_id"] = game_id

        # # Split date into day, month and year and store in seperate columns.
        # date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
        # df = pd.concat(
        #     [df, df["date"].str.extract(date_data).astype(int)], axis=1)
        # # To four digit integer.
        # df["fb_year"] = df["fb_year"] + 2000

        # Save as csv file.
        df.to_csv(ppj("OUT_DATA_FOOTBALL_FINAL",
                      "{}.csv".format(game_id)), index=False)

    open(ppj("OUT_DATA_FOOTBALL_FINAL", "game_scraping_finished.txt"), 'a').close()

if __name__ == '__main__':
    main()
