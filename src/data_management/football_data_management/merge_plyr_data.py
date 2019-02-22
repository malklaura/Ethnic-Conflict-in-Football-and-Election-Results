import pandas as pd
import numpy as np
from bld.project_paths import project_paths_join as ppj


def merge_nationality(final_df, plyr_df):
    # All player url columns for both teams.
    plyr_url_col = [col for col in final_df if '_plyr_url' in col]

    # Loop through all player url columns and match player nat by url.
    # df.
    for col in plyr_url_col:
        final_df = pd.merge(final_df, plyr_df[["url", "nat"]],  how='left',
                            left_on=str(col), right_on='url')
        final_df.drop('url', axis=1, inplace=True)

        # Match nationality to player by number of team.
        nat_colname = str(col).replace("url", "nat")
        final_df.rename(columns={"nat": nat_colname}, inplace=True)

    return final_df


def get_ethn_perc(final_df):
    # Get percentage of German and non-German players in each team. Of course,
    # the binary differentiation in German and non-Germans is too much of a
    # simplification, however, this project is merely meant to manage the data
    # properly. Further analysis will conduct a much more differentiated analysis
    # of ethnicity.
    for team in ["hmsd", "awsd"]:
        nat_col = [
            col for col in final_df if '{}_plyr_nat'.format(team) in col]

        # Count number of German players within each team.
        final_df["{}_ger".format(team)] = (
            final_df[nat_col] == "Deutschland").sum(axis=1)
        # Number of NaNs.
        final_df["{}_nan".format(team)] = (
            final_df[nat_col] == np.nan).sum(axis=1)
        # Non-Germans as difference beween Germans and NaNs.
        final_df["{}_other".format(team)] = len(
            nat_col) - final_df[["{}_ger".format(team), "{}_nan".format(team)]].sum(axis=1)

        # Sum of german and non-germans.
        observed_total = final_df[
            ["{}_ger".format(team), "{}_other".format(team)]].sum(axis=1)
        final_df["{}_nat_sum".format(team)] = observed_total
        # Percentage of Germans.
        final_df["{}_ger_perc".format(team)] = final_df["{}_ger".format(
            team)] / final_df["{}_nat_sum".format(team)]
        # Percentage of Non-Germans.
        final_df["{}_other_perc".format(
            team)] = 1 - final_df["{}_ger_perc".format(team)]

    return final_df

if __name__ == '__main__':
    final_df = pd.read_csv(
        ppj("OUT_DATA_FOOTBALL", "football_final_longlat.csv"), encoding='cp1252')
    plyr_df = pd.read_csv(
        ppj("OUT_DATA_FOOTBALL", "player_data.csv"), encoding='cp1252')

    # Merge nationality by url and get nationality per team in percentage
    # points.
    final_df = merge_nationality(final_df, plyr_df)
    final_df = get_ethn_perc(final_df)
    final_df.to_csv(
        ppj("OUT_DATA_FOOTBALL", "football_final_longlat_nat.csv"), index=False)
