import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj

def get_geodata(club_longlat_df, unique_clubs):
	# Do the google API search by name.
	api_key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"

	for club in unique_clubs[0:10]:
		club_dict = {}
		club_dict["hmsd_club"] = club
		geo = geocoder.google(club, key = api_key)
		try:
		    club_dict["hmsd_lat"] = geo.latlng[0]
		    club_dict["hmsd_long"] = geo.latlng[1]
		except:
			pass
		try:
		    club_dict["hmsd_postal"] = geo.postal
		    club_dict["hmsd_locality"] = geo.locality
		except:
			pass
		club_longlat_df = club_longlat_df.append(
		    club_dict, ignore_index=True)

	return club_longlat_df


if __name__ == '__main__':
	# Open final football file csv.
	final_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	# Get unique set of clubs for both home and away teams. 
	unique_hmsd = final_df["hmsd_club"].unique().tolist()
	unique_awsd = final_df["awsd_club"].unique().tolist()
	# Unique intersection.
	unique_clubs = unique_hmsd + unique_awsd
	unique_clubs = list(set(unique_clubs))[1:]

	# Create dataframe to store unqiue club - longlat data.
	club_longlat_df = pd.DataFrame()

	club_longlat_df = get_geodata(club_longlat_df, unique_clubs)

	merged_df = pd.merge(final_df, club_longlat_df,  how='left', on='hmsd_club')

	club_longlat_df.to_csv(ppj("OUT_DATA_FOOTBALL", "club_longlat.csv"), index=False)
	merged_df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final_longlat.csv"), index=False)
