import pandas as pd
import numpy as np
from bld.project_paths import project_paths_join as ppj


def merge_nationality(final_df, plyr_df):
    # All player url columns for both teams.
    plyr_url_col = [col for col in final_df if '_plyr_url' in col]

    # Loop through all player url columns and match player nationality by url.
    for col in plyr_url_col:
        final_df = pd.merge(final_df, plyr_df[["url", "nat"]],  how='left',
                            left_on=str(col), right_on='url')
        final_df.drop('url', axis=1, inplace=True)

        # Match nationality to player.
        nat_colname = str(col).replace("url", "nat")
        final_df.rename(columns={"nat": nat_colname}, inplace=True)

    return final_df


def relative_nationality(df):
    # Get percentage of German and non-German players in each team. Of course,
    # the binary differentiation in German and non-Germans is too much of a
    # simplification, however, this project is merely meant to manage the data
    # properly. Further analysis will conduct a much more differentiated analysis
    # of ethnicity.

    for team in ["home", "away"]:
        # Columns containing nationality information by team.
        nat_col = [col for col in df if '{}_plyr_nat'.format(team) in col]

        # Number of germans and non-germans.
        n_ger = (df[nat_col] == "Deutschland").sum(axis=1)
        n_nan = (df[nat_col] == np.nan).sum(axis=1)
        n_non_ger = len(nat_col) - n_ger - n_nan
        n_obs_total = n_ger + n_non_ger
        # Percentages.
        perc_ger = n_ger / n_obs_total
        perc_non_ger = n_non_ger / n_obs_total

        # To dataframe.
        df["{}_ger".format(team)] = n_ger
        df["{}_nan".format(team)] = n_nan
        df["{}_other".format(team)] = n_non_ger
        df["{}_obs_total".format(team)] = n_obs_total
        df["{}_ger_perc".format(team)] = perc_ger
        df["{}_other_perc".format(team)] = perc_non_ger

    return df

if __name__ == '__main__':
    # Load game-, player- and geo-data
    games_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "games_combined.csv"))
    plyr_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "plyr_nationality.csv"))
    longlat_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "club_longlat.csv"))

    # Merge all files to final csv.
    # Merge geo- and game data.
    final_df = pd.merge(games_df, longlat_df, how='left', on='home_club')

    # Merge geo-, gamedata on player nationality data.
    final_df = merge_nationality(final_df, plyr_df)

    # Get relative ethnicity for each team.
    final_df = relative_nationality(final_df)

    # Split date into day, month and year and store in seperate columns.
    date_data = '(?P<fb_day>[^.]+).(?P<fb_month>[^.]+).(?P<fb_year>[^.]+)'
    final_df = pd.concat([final_df, final_df["fb_date"].str.extract(date_data).astype(int)], axis=1)
    final_df["fb_year"] = final_df["fb_year"] + 2000 # To four digit integer.

    # Save as .csv file.
    final_df.to_csv(
        ppj("OUT_DATA_FOOTBALL", "games_final.csv"), index=False)
