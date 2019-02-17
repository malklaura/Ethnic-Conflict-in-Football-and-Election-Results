import certifi
import csv
import glob
import re
import urllib3
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime
from bld.project_paths import project_paths_join as ppj

def get_geo_distance():
	elec_longlat = final_df[["elec_long", "elec_lat"]]
	hmsd_longlat = final_df[["hmsd_long", "hmsd_lat"]]
	final_df["geo_dist"] = geodesic(elec_longlat, hmsd_longlat).km

	return final_df["geo_dist"]


def get_time_distance(final_df):
	final_df["elec_date"] = datetime.strptime(final_df["elec_date"], )
	final_df["game_date"] = datetime.strptime(final_df["game_date"], )
	final_df["time_dist"] = datetime.timedelta(final_df[["elec_date", "game_date"]])

	return final_df["time_dist"]

if __name__ == '__main__':
    # Read in final dataset, containing all games and player data.
	election_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_final.csv"), encoding='cp1252')
	football_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	final_df = pd.merge(election_df, football_df, on="postal")

	final_df["geo_dist"] = get_geo_distance(final_df)
	final_df["time_dist"] = get_time_distance(final_df)

	final_df[final_df["geo_dist"] > 20]["drop"] = 1
	final_df[final_df["time_dist"] > 14]["drop"] = 1

	final_df = final_df[final_df["drop"] != 1]
	final_df = final_df.groupby(['elec_id', 'elec_date']).mean()

    final_df.to_csv(ppj("OUT_DATA", "master_file.csv"))
