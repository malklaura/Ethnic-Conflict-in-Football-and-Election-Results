import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj

# Open merged games file
merged_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"), encoding='cp1252')

unique_clubs = merged_df["home_club"].unique().tolist() + merged_df["away_club"].unique().tolist()
unique_clubs = list(set(unique_clubs))[1:]

clubs_longlat_df = pd.DataFrame()

clubs_longlat_df["club"] = unique_clubs

# Do the google analysis
for i, club in enumerate(unique_clubs):
    geo = geocoder.google(club, key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE")
    try:
        clubs_longlat_df.at[i, "lat"] = geo.latlng[0]
        clubs_longlat_df.at[i, "long"] = geo.latlng[1]
    except:
        print(club)

merged_df = pd.merge(merged_df, clubs_longlat_df,  how='left',
                              left_on=['home_club'], right_on=['club'])

merged_df.to_csv(ppj("OUT_DATA_FOOTBALL", "football_final.csv"))
