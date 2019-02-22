import geocoder
import numpy as np
import pandas as pd
from bld.project_paths import project_paths_join as ppj


def get_geodata(unique_clubs, key):
	"""This function returns longitude and latitude coordinates
	based on the provided club names. If possible also postal
	code and location name are returned."""

	# Dict and dataframe o store geo information.
    club_dict = {}
    club_df = pd.DataFrame()
    
    # Get coordinates for search term.
    for home_club in unique_clubs:
        geo = geocoder.google(home_club, key=key)

        # Store longitude, latitude, postal code and locality.
        club_dict["home_club"] = home_club
        club_dict["home_lat"] = geo.latlng[0]
        club_dict["home_long"] = geo.latlng[1]

        try:
            club_dict["home_postal"] = geo.postal
            club_dict["home_locality"] = geo.locality
        except:
        	club_dict["home_postal"] = np.nan
            club_dict["home_locality"] = np.nan

        # Append dictionary to dataframe.
        club_df = club_df.append(club_dict, ignore_index=True)
    
    return club_df


if __name__ == '__main__':
	# Open final football file csv.
	final_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	# Get unique set of clubs for both home and away teams. 
	unique_home = final_df["home_club"].unique().tolist()
	unique_away = final_df["away_club"].unique().tolist()
	unique_clubs = unique_home + unique_away # Combined list.
	unique_clubs = list(set(unique_clubs))[1:] # Unique intersection.

	# Do google maps search.
	api_key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"
	club_longlat_df = get_geodata(unique_clubs, api_key)

	# Merge to game data and store as csv.
	merged_df = pd.merge(final_df, club_longlat_df,  how='left', on='home_club')
	club_longlat_df.to_csv(ppj("OUT_DATA_FOOTBALL", "club_longlat.csv"), index=False)
	merged_df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final_longlat.csv"), index=False)
