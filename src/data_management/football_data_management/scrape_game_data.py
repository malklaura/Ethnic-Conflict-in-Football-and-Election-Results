import tqdm
import os.path
import pandas as pd
import multiprocessing as mp

from bld.project_paths import project_paths_join as ppj
from src.data_management.football_data_management.get_game_data import scrape_game_data


def mp_scraping(mtchday, game_df):
    """
    Checks wheter CSV file for specified *mtchday* ID already exists, if not
    games corresponding to this ID are scraped via multiprocessing. The game
    URLs are stored in *game_df* connecting matchday ID and game URLs. The 
    resulting dataframe is saved as a CSV file.
    """

    # Check wheter matchday games are already scraped.
    if not os.path.isfile(ppj('OUT_DATA_FOOTBALL_CSV', '{}.csv'.format(mtchday))):
        temp_urls = game_df[(game_df['mtchday_id'] == mtchday) & (game_df['doable'] == 1)][
            'game_url'].unique().tolist()

        # Scraping via multiprocessing.
        dict_list = []
        with mp.Pool() as pool:
            out = pool.map(scrape_game_data, temp_urls)
            dict_list.extend(out)

        # Dicts to dataframe and save as CSV.
        df = pd.DataFrame(dict_list)
        df['mtchday_id'] = mtchday
        df.to_csv(ppj('OUT_DATA_FOOTBALL_CSV',
                      '{}.csv'.format(mtchday)), index=False)
    else:
        pass


def main():
    # Load game URL data and get unique ID list.
    game_df = pd.read_csv(ppj('OUT_DATA_FOOTBALL', 'game_urls.csv'))
    mtchday_list = game_df['mtchday_id'].unique().tolist()

    # Run multiprocessed scraping by matchday ID.
    for mtchday in mtchday_list:
        mp_scraping(mtchday, game_df)

    # Create .txt file to indicate end of scraping process.
    open(ppj('OUT_DATA_FOOTBALL_CSV', 'scraping_finished.txt'), 'a').close()

if __name__ == '__main__':
    main()
