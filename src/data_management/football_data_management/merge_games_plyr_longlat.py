"""Merge geodata and player nationalities to game data."""

import pandas as pd
import numpy as np

from bld.project_paths import project_paths_join as ppj


def merge_nationality(final_df, plyr_df):
    """
    Merges player information from given player dataframe to combined
    games dataframe, by looping through all player URL columns.
    """

    # All player url columns for both teams.
    plyr_url_col = [col for col in final_df if '_plyr_url' in col]

    # Loop through all player URL columns and match player nationality by url.
    for col in plyr_url_col:
        final_df = pd.merge(final_df, plyr_df[['url', 'nat']],  how='left',
                            left_on=str(col), right_on='url')
        final_df.drop('url', axis=1, inplace=True)

        # Match nationality to player.
        nat_colname = str(col).replace('url', 'nat')
        final_df.rename(columns={'nat': nat_colname}, inplace=True)

    return final_df


def relative_nationality(df):
    """
    Expands dataframe by columns containing absolute and relative information
    on player nationality by team.
    """

    # Loop through teams.
    for team in ['home', 'away']:
        # Columns containing nationality information by team.
        nat_col = [col for col in df if '{}_plyr_nat'.format(team) in col]

        # Number of germans and non-germans.
        n_ger = (df[nat_col] == "Deutschland").sum(axis=1)
        n_tur = (df[nat_col] == "Türkei").sum(axis=1)
        n_nan = (df[nat_col] == np.nan).sum(axis=1)
        n_nonger = len(nat_col) - n_ger - n_nan
        n_obs_total = n_ger + n_nonger
        # Percentages.
        perc_ger = n_ger / n_obs_total
        perc_tur = n_tur / n_obs_total
        perc_nonger = n_nonger / n_obs_total

        # To dataframe.
        df['{}_ger'.format(team)] = n_ger
        df['{}_tur'.format(team)] = n_tur
        df['{}_nan'.format(team)] = n_nan
        df['{}_nonger'.format(team)] = n_nonger
        df['{}_obs_total'.format(team)] = n_obs_total
        df['{}_ger_perc'.format(team)] = perc_ger
        df['{}_tur_perc'.format(team)] = perc_tur
        df['{}_nonger_perc'.format(team)] = perc_nonger

    return df


def main():
    # Load game-, player- and geo-data
    plyr_df = pd.read_csv(ppj('OUT_DATA_FOOTBALL', 'plyr_nationality.csv'))
    longlat_df = pd.read_csv(ppj('OUT_DATA_FOOTBALL', 'club_longlat.csv'))
    games_df = pd.read_csv(
        ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'), low_memory=False)

    # Merge all files to final csv.
    # Merge geo- and game data.
    final_df = pd.merge(games_df, longlat_df, how='left', on='home_club')

    # Merge geo-, gamedata on player nationality data.
    final_df = merge_nationality(final_df, plyr_df)

    # Get relative ethnicity for each team.
    final_df = relative_nationality(final_df)

    # Split date into day, month and year and store in seperate columns.
    date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
    final_df = pd.concat(
        [final_df, final_df['fb_date'].str.extract(date_data).astype(int)], axis=1)
    final_df['fb_year'] = final_df['fb_year'] + 2000  # To four digit integer.

    # Save as CSV file.
    final_df.to_csv(
        ppj('OUT_DATA_FOOTBALL', 'games_final.csv'), index=False)

if __name__ == '__main__':
    main()
