import pandas as pd
import multiprocessing as mp
from bld.project_paths import project_paths_join as ppj
from src.data_management.football_data_management.get_game_data import scrape_game_data


def main():
    game_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "game_data.csv"))

    # Scraping.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(scrape_game_data, game_df.game_url[0:20].values)
        dict_list.extend(out)

    df = pd.DataFrame(dict_list)  # Dicts to dataframe.
    # Save as csv file.
    df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_combined.csv"), index=False)

if __name__ == '__main__':
    main()
