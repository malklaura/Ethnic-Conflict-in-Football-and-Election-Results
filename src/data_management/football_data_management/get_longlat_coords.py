import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj

def get_geodata(club_longlat_df, unique_clubs):
    """This function returns longitude and latitude coordinates
    based on the provided club names. If possible also postal
    code and location name are returned."""

	# API key needed for google search.
	api_key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"

	# Loop through club list.
	for club in unique_clubs[0:10]:
		club_dict = {}
		club_dict["home_club"] = club

		# Do google search.
		geo = geocoder.google(club, key = api_key)
		try:
		    club_dict["home_lat"] = geo.latlng[0]
		    club_dict["home_long"] = geo.latlng[1]
		except:
			pass
		try:
		    club_dict["home_postal"] = geo.postal
		    club_dict["home_locality"] = geo.locality
		except:
			pass

		# Append dictionary to dataframe
		club_longlat_df = club_longlat_df.append(
		    club_dict, ignore_index=True)

	return club_longlat_df


if __name__ == '__main__':
	# Open final football file csv.
	final_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	# Get unique set of clubs for both home and away teams. 
	unique_home = final_df["home_club"].unique().tolist()
	unique_away = final_df["away_club"].unique().tolist()
	# Unique intersection.
	unique_clubs = unique_home + unique_away
	unique_clubs = list(set(unique_clubs))[1:]

	# Create dataframe to store unqiue club - longlat data.
	club_longlat_df = pd.DataFrame()

	club_longlat_df = get_geodata(club_longlat_df, unique_clubs)

	merged_df = pd.merge(final_df, club_longlat_df,  how='left', on='home_club')

	club_longlat_df.to_csv(ppj("OUT_DATA_FOOTBALL", "club_longlat.csv"), index=False)
	merged_df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final_longlat.csv"), index=False)
