import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj

elec_comb_df = pd.read_csv(
    ppj("OUT_DATA", "election_combined.csv"), encoding='cp1252')

exclusion_dict = {"Briefwahl": None, "Wahlbezirk": None,
                  "Stimmbezirk": None, "Briefwahlbezirk": None, "Wahlbez": None}

combined_votes["elec_off_srch_term"] = combined_votes[
    "mun_name"] + " " + combined_votes["Name"]
combined_votes["elec_off_srch_term"].replace(
    exclusion_dict, regex=True, inplace=True)
elec_offices = combined_votes["elec_off_srch_term"].unique().tolist()[0:10]
elec_offices = [x for x in elec_offices if x is not None]

elec_off_df = pd.DataFrame()
elec_off_dict = {}

# Do the google analysis
key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"

for office in elec_offices:
    geo = geocoder.google(office, key=key)
    elec_off_dict["elec_off"] = elec_office
    elec_off_dict["lat"] = geo.latlng[0]
    elec_off_dict["long"] = geo.latlng[1]
    elec_off_df = elec_off_df.append(
        elec_off_dict, ignore_index=True)

elec_final_df = pd.merge(elec_comb_df, elec_off_df,  how='left', left_on=[
                          'elec_off_srch_term'], right_on=['elec_off'])
elec_final_df.to_csv(ppj("OUT_DATA", "election_final.csv"))
