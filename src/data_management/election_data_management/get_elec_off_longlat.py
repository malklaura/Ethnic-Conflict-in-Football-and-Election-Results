import geocoder
import numpy as np
import pandas as pd
import multiprocessing as mp
from bld.project_paths import project_paths_join as ppj


def get_srch_term_list(elec_df):
    """This functions returns a list containing all search terms needed for the
    subsequent google search."""

    # Get search term by combining municipal name and election office name.
    elec_df["srch_term"] = elec_df["mun_clearname"] + \
        " " + elec_df["elec_off_name"]

    # We want to exclude certain words from possible search terms, that could
    # invalidate the google query.
    elec_df["srch_term"] = elec_df["srch_term"].str.replace(r"\(.*\)","")
    elec_df["srch_term"] = elec_df["srch_term"].str.replace("\d+", "")
    elec_df["srch_term"] = [clean_srch_term(x) for x in elec_df["srch_term"]]
    elec_df["srch_term"] = elec_df["srch_term"].str.replace(r"\s\w\s","")

    # Only use unique search terms and those which are not None.
    srch_term_list = elec_df["srch_term"].unique().tolist()
    srch_term_list = [x for x in srch_term_list if x is not None]

    return srch_term_list[0:10]


def clean_srch_term(srch_term):
    """This functions cleans the search term form unnecessary substrings
    that could invalidate the google maps search."""

    exclusion_dict = {"Briefwahl": "",
                      "Wahlbezirk": "",
                      "Stimmbezirk": "",
                      "Briefwahlbezirk": "",
                      "bezirk": "",
                      "Obere": "",
                      "Mittlere": "",
                      "Untere": ""}

    for word, replacement in exclusion_dict.items():
        if word in srch_term:
            return srch_term.replace(word, replacement)
    return srch_term


def gmaps_elec_offices(srch_term):
    """This functions get longitude, latitude and postal code data from a
    google maps search. For each search term a dictionary is initalized
    and appended to a dataframe."""

    # Dict and dataframe o store geo information.
    elec_off_dict = {"srch_term": srch_term}

    # Get coordinates for search term.
    key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"
    geo = geocoder.google(srch_term, key=key)

    # Store longitude, latitude, postal code and locality in
    # prespecified dictionary.
    try:
        elec_off_dict["elec_lat"] = geo.latlng[0]
        elec_off_dict["elec_long"] = geo.latlng[1]
    except:
        elec_off_dict["elec_lat"] = np.nan
        elec_off_dict["elec_long"] = np.nan

    # Also try to get postal code and locality name.
    try:
        elec_off_dict["elec_postal"] = geo.postal
        elec_off_dict["elec_locality"] = geo.locality
    except:
        elec_off_dict["elec_postal"] = np.nan
        elec_off_dict["elec_locality"] = np.nan

    return elec_off_dict


if __name__ == '__main__':
    # Read in combined election csv.
    elec_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_combined.csv"))

    # Election office name plus municipality name as search name.
    srch_term_list = get_srch_term_list(elec_df)
    print(srch_term_list)

    # Google maps search via multiprocessing.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(gmaps_elec_offices, srch_term_list)
        dict_list.extend(out)

    long_lat_df = pd.DataFrame(dict_list)  # Dicts to dataframe.
    print(long_lat_df)
    long_lat_df.to_csv(
        ppj("OUT_DATA_ELEC", "elec_off_longlat.csv"), index=False)

    # Merge latitude and longitude data to combined election csv.
    elec_final_df = pd.merge(elec_df, long_lat_df,
                             how='left', on='srch_term')
    elec_final_df.to_csv(
        ppj("OUT_DATA_ELEC", "election_final.csv"), index=False)
