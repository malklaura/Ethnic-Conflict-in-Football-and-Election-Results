import numpy as np
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
from bld.project_paths import project_paths_join as ppj


def get_geo_distance(final_df, index):
    """This functions returns the kilometer distance between all matched football games and 
    election offices, based on longitude and latitude data."""

    # Compute geographic distance in kilometers using geopy package if possible
    # otherwise return np.nan.
    try:
        fb_coords = final_df.loc[index, ["home_long", "home_lat"]]
        elec_coords = final_df.loc[index, ["elec_long", "elec_lat"]]
        return geodesic(fb_coords, elec_coords).km
    except:
        return np.nan


def get_time_distance(final_df):
    """This functions returns the time disrance in days between all matched football games and 
    election offices, based on the respective date columns"""

    # Get respective date columns into python date-format.
    final_df["elec_date"] = [datetime.strptime(
        x, "%d.%m.%Y") for x in final_df["elec_date"]]
    final_df["fb_date"] = [datetime.strptime(
        x, "%d.%m.%y") for x in final_df["fb_date"]]

    # Compute time difference in days.
    final_df["time_dist"] = [(final_df.loc[
                              x, "elec_date"] - final_df.loc[x, "fb_date"]).days for x in range(len(final_df))]

    return final_df["time_dist"]

if __name__ == '__main__':
    # Read in both final datasets, containing all election and football game
    # data.
    election_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_final.csv"))
    football_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"))

    # Merge dataframes according to postal code and year column.
    final_df = pd.merge(election_df, football_df, left_on=[
                        "elec_postal", "elec_year"], right_on=["home_postal", "fb_year"])

    # Compute kilometer between election office and homeside football court as well as time disrance
    # between election and game date for all merged rows.
    final_df["geo_dist"] = [get_geo_distance(
        final_df, x) for x in range(len(final_df))]
    final_df["time_dist"] = get_time_distance(final_df)

    # Drop those matches that are within 20km and no longer apart than two
    # weeks.
    #final_df = final_df[final_df["geo_dist"] < 20]
    #final_df = final_df[final_df["time_dist"].between(0, 14, inclusive=True)]

    # Group by election id and date, which results in the final dataframe.
    final_df = final_df.groupby(['elec_off_name', 'elec_id']).mean().reset_index()

    # Save to csv.
    final_df.to_csv(ppj("OUT_DATA", "master_file.csv"), index=False)
