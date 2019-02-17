import certifi
import csv
import glob
import re
import urllib3
import numpy as np
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
from datetime import datetime
from bld.project_paths import project_paths_join as ppj

def get_geo_distance():
	elec_longlat = final_df[["elec_long", "elec_lat"]]
	hmsd_longlat = final_df[["hmsd_long", "hmsd_lat"]]
	final_df["geo_dist"] = [geodesic(final_df.loc[x, ["hmsd_long", "hmsd_lat"]], final_df.loc[x, ["elec_long", "elec_lat"]]).km for x in range(len(final_df))]

	return final_df["geo_dist"]


def get_time_distance(final_df):
	final_df["elec_date"] = [datetime.strptime(x, "%d.%m.%y") for x in final_df["elec_date"]]
	final_df["fb_date"] = [datetime.strptime(x, "%d.%m.%y") for x in final_df["fb_date"]]
	final_df["time_dist"] = [(final_df.loc[x, "elec_date"]-final_df.loc[x, "fb_date"]).days for x in range(len(final_df))]

	return final_df["time_dist"]

if __name__ == '__main__':
    # Read in final dataset, containing all games and player data.
	election_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_final.csv"), encoding='cp1252')
	football_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	final_df = pd.merge(election_df, football_df, left_on=["", ""], right_on=["hmsd_postal", "fb_year"])

	final_df["geo_dist"] = get_geo_distance(final_df)
	final_df["time_dist"] = get_time_distance(final_df)

	final_df[final_df["geo_dist"] > 20]["drop"] = 1
	final_df[final_df["time_dist"] > 14 | final_df["time_dist"] < 0]["drop"] = 1

	final_df = final_df[final_df["drop"] != 1]
	final_df = final_df.groupby(['elec_id', 'elec_date']).mean()

    final_df.to_csv(ppj("OUT_DATA", "master_file.csv"))
