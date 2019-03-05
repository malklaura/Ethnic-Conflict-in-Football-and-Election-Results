"""Get geodata for each home club in dataset."""

import geocoder
import numpy as np
import pandas as pd
import multiprocessing as mp

from bld.project_paths import project_paths_join as ppj


def get_geodata(home_club):
    """
    Returns longitude and latitude coordinates
    based on the provided club name. If possible also postal
    code and location name are returned.
    """

    # Dict and dataframe o store geo information.
    club_dict = {'home_club': home_club}

    # Get coordinates for search term.
    key = 'AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE'
    geo = geocoder.google(home_club, key=key)

    # Store longitude, latitude, postal code and locality.
    try:
        club_dict['home_lat'] = geo.latlng[0]
        club_dict['home_long'] = geo.latlng[1]
    except:
        club_dict['home_lat'] = np.nan
        club_dict['home_long'] = np.nan

    try:
        club_dict['home_postal'] = geo.postal
        club_dict['home_locality'] = geo.locality
    except:
        club_dict['home_postal'] = np.nan
        club_dict['home_locality'] = np.nan

    return club_dict


def main():
    # Open final football file csv.
    final_df = pd.read_csv(
        ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'), low_memory=False)

    # Get unique set of clubs for both home and away teams.
    unique_home = final_df['home_club'].unique().tolist()
    unique_away = final_df['away_club'].unique().tolist()
    unique_clubs = unique_home + unique_away  # Combined list.
    unique_clubs = list(set(unique_clubs))[1:]  # Unique intersection.

    unique_clubs = unique_clubs[0:150]  # !!Subset!!

    # Scraping via multiprocessing.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(get_geodata, unique_clubs)
        dict_list.extend(out)

    # Dicts to dataframe.
    club_longlat_df = pd.DataFrame(dict_list)

    # Merge to game data and store as csv.
    club_longlat_df.to_csv(
        ppj('OUT_DATA_FOOTBALL', 'club_longlat.csv'), index=False)


if __name__ == '__main__':
    main()
