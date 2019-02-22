import geocoder
import numpy as np
import pandas as pd
from bld.project_paths import project_paths_join as ppj


def get_srch_term_list(elec_comb_df):
    """This functions returns a list containing all search terms needed for the
    subsequent google search."""

    # We want to exclude certain words from possible search terms, that could
    # invalidate the google query.
    exclusion_dict = {"Briefwahl": None, "Wahlbezirk": None,
                      "Stimmbezirk": None, "Briefwahlbezirk": None, "Wahlbez": None}

    # Get search term by combining municipal name and election office name.
    elec_comb_df["srch_term"] = elec_comb_df[
        "mun_name"] + " " + elec_comb_df["Name"]
    # Apply exclusion dictionary to this search term column.
    elec_comb_df["srch_term"].replace(
        exclusion_dict, regex=True, inplace=True)
    # Only use unique search terms and those which are not None.
    srch_term_list = elec_comb_df["srch_term"].unique().tolist()
    srch_term_list = [x for x in srch_term_list if x is not None]

    return srch_term_list[0:10]


def gmaps_elec_offices(srch_term_list, key):
    """This functions get longitude, latitude and postal code data from a
    google maps search. For each search term a dictionary is initalized
    and appended to a dataframe."""

    # Dict and dataframe o store geo information.
    elec_off_dict = {}
    elec_off_df = pd.DataFrame()

    # Get coordinates for search term.
    for srch_term in srch_term_list:
        geo = geocoder.google(srch_term, key=key)

        # Store longitude, latitude, postal code and locality in
        # prespecified dictionary.
        elec_off_dict["srch_term"] = srch_term
        elec_off_dict["elec_lat"] = geo.latlng[0]
        elec_off_dict["elec_long"] = geo.latlng[1]

        # Also try to get postal code and locality name.
        try:
            elec_off_dict["elec_postal"] = geo.postal
            elec_off_dict["elec_locality"] = geo.locality
        except:
            elec_off_dict["elec_postal"] = np.nan
            elec_off_dict["elec_locality"] = np.nan

        # Append dictionary to dataframe.
        elec_off_df = elec_off_df.append(elec_off_dict, ignore_index=True)

    return elec_off_df


if __name__ == '__main__':
    # Read in combined election csv.
    elec_comb_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_combined.csv"), encoding='cp1252')

    # Election office name plus municipality name as search name.
    srch_term_list = get_srch_term_list(elec_comb_df)
    key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"

    long_lat_df = gmaps_elec_offices(srch_term_list, key):

        # Merge latitude and longitude data to combined election csv.
    elec_final_df = pd.merge(elec_comb_df, long_lat_df,
                             how='left', on='srch_term')

    # Save as csv file.
    elec_final_df.to_csv(
        ppj("OUT_DATA_ELEC", "election_final.csv"), index=False)
