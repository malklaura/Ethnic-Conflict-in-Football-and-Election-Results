import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj

if __name__ == '__main__':
	# Open final football file csv.
	final_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

	# Get unique set of clubs, consisting of both home and away teams. 
	unique_clubs = final_df["hmsd_club"].unique().tolist() + final_df["awsd_club"].unique().tolist()
	unique_clubs = list(set(unique_clubs))[1:]

	# Create dataframe to store unqiue club - longlat data.
	club_longlat_df = pd.DataFrame()

	# Do the google API search by name.
	api_key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"

	for club in unique_clubs[0:10]:
		club_dict["club"] = club
	    geo = geocoder.google(club, key = api_key)
	    try:
	        club_dict["lat"] = geo.latlng[0]
	        club_dict["long"] = geo.latlng[1]
	    except:
	        print(club)

	    club_longlat_df = club_longlat_df.append(
	        club_dict, ignore_index=True)

	club_longlat_df.to_csv(ppi("OUT_DATA_FOOTBALL", "club_longlat.csv"))

	# merged_df = pd.merge(final_df, clubs_longlat_df,  how='left',
	#                               left_on=['home_club'], right_on=['club'])

	# merged_df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final_longlat.csv"))
