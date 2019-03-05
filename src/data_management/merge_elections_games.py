"""Merges election and game data."""

import numpy as np
import pandas as pd

from datetime import datetime
from geopy.distance import geodesic
from bld.project_paths import project_paths_join as ppj


def get_geo_distance(final_df, index):
    """
    Returns the kilometer distance between the longitude latitude data
    of a football club and and those of a election office. The returned distance is provided 
    in kilometres.
    """

    # Compute geographic distance in kilometers using geopy package if
    # possible.
    try:
        fb_coords = final_df.loc[index, ['home_long', 'home_lat']]
        elec_coords = final_df.loc[index, ['elec_long', 'elec_lat']]

        return geodesic(fb_coords, elec_coords).km

    except:

        return np.nan


def get_time_distance(final_df):
    """
    Returns the time distance in days between matched matched football games and 
    elections, based on the respective date columns.
    """

    # Get respective date columns into python date-format.
    final_df['elec_date'] = [datetime.strptime(
        x, '%d.%m.%Y') for x in final_df['elec_date']]
    final_df['fb_date'] = [datetime.strptime(
        x, '%d.%m.%y') for x in final_df['fb_date']]

    # Compute time difference in days.
    final_df['time_dist'] = [(final_df.loc[
                              x, 'elec_date'] - final_df.loc[x, 'fb_date']).days for x in range(len(final_df))]

    return final_df['time_dist']


def main():
    # Read in both final datasets, containing all election and football data.
    election_df = pd.read_csv(
        ppj('OUT_DATA_ELEC', 'elections_final.csv'), low_memory=False)
    game_df = pd.read_csv(
        ppj('OUT_DATA_FOOTBALL', 'games_final.csv'), low_memory=False)

    # Drop NaN values.
    election_df.dropna(subset=['elec_postal'], inplace=True)
    game_df.dropna(subset=['home_postal'], inplace=True)

    # Merge dataframes according to postal code and year column.
    final_df = pd.merge(election_df, game_df, left_on=[
                        'elec_postal', 'elec_year'], right_on=['home_postal', 'fb_year'])

    # Compute geodistance and keep matches within 20km.
    final_df['geo_dist'] = [get_geo_distance(
        final_df, x) for x in range(len(final_df))]
    final_df = final_df[final_df['geo_dist'] < 20]

    # Compute time distance amd keep mtaches within 14 days.
    final_df['time_dist'] = get_time_distance(final_df)
    final_df = final_df[final_df['time_dist'].between(0, 14, inclusive=True)]

    # Group by election id and date, which results in the final dataframe.
    final_df = final_df.groupby(
        ['elec_off_name', 'elec_id']).mean().reset_index()

    # Save to csv.
    final_df.to_csv(ppj('OUT_DATA', 'elections_games_final.csv'), index=False)

if __name__ == '__main__':
    main()
