import geocoder
import pandas as pd
from bld.project_paths import project_paths_join as ppj


def get_srch_term_list(elec_comb_df):
    """This functions returns a list containing all search terms needed for the
    subsequent google search."""
    exclusion_dict = {"Briefwahl": None, "Wahlbezirk": None,
                      "Stimmbezirk": None, "Briefwahlbezirk": None, "Wahlbez": None}

    elec_comb_df["srch_term"] = elec_comb_df[
        "mun_name"] + " " + elec_comb_df["Name"]
    elec_comb_df["srch_term"].replace(
        exclusion_dict, regex=True, inplace=True)
    srch_term_list = elec_comb_df["srch_term"].unique().tolist()[0:10]
    srch_term_list = [x for x in srch_term_list if x is not None]
    return srch_term_list[0:10]


if __name__ == '__main__':
    # Read in combined election csv.
    elec_comb_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_combined.csv"), encoding='cp1252')

    # Initialize pandas dataframe and dictionary to store coordinates.
    elec_off_df = pd.DataFrame()
    elec_off_dict = {}

    # Combine election office name plus municipality name to get list of
    # search terms to be used in google search.
    srch_term_list = get_srch_term_list(elec_comb_df)

    # API-Key for google analysis.
    key = "AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE"
    # Get coordinates for search term.
    for srch_term in srch_term_list:
        geo = geocoder.google(srch_term, key=key)

        # Store longitude, latitude, zip code and locality in
        # prespecified dictionary.
        elec_off_dict["srch_term"] = srch_term
        elec_off_dict["elec_lat"] = geo.latlng[0]
        elec_off_dict["elec_long"] = geo.latlng[1]
        try:
            elec_off_dict["elec_postal"] = geo.postal
            elec_off_dict["elec_locality"] = geo.locality
        except:
            pass

        # Append dictionary to dataframe.
        elec_off_df = elec_off_df.append(elec_off_dict, ignore_index=True)

    # Merge latitude and longitude data to combined election dataframe.
    elec_final_df = pd.merge(elec_comb_df, elec_off_df,
                             how='left', on='srch_term')
    elec_final_df.to_csv(
        ppj("OUT_DATA_ELEC", "election_final.csv"), index=False)
