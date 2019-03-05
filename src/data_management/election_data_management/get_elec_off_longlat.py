"""Get geodata for each unique election office."""

import geocoder
import numpy as np
import pandas as pd
import multiprocessing as mp

from bld.project_paths import project_paths_join as ppj


def get_srch_term_list(elec_df):
    """
    Returns a list containing all search terms needed for the subsequent 
    Google search. To this end, the election office name is stripped from 
    substrings and characters that could invalidate the search.
    """

    # Get search term by combining municipal name and election office name.
    elec_df['srch_term'] = elec_df['mun_clearname'] + \
        ' ' + elec_df['elec_off_name']

    # We want to exclude certain words from possible search terms, that could
    # invalidate the google query.
    elec_df['srch_term'] = elec_df['srch_term'].str.replace(r'\(.*\)', '')
    elec_df['srch_term'] = elec_df['srch_term'].str.replace('\d+', '')
    elec_df['srch_term'] = [clean_srch_term(x) for x in elec_df['srch_term']]
    elec_df['srch_term'] = elec_df['srch_term'].str.replace(r'\s\w\s', '')

    # Mark postal ballots.
    elec_df['postal_vote'] = [postal_indicator(
        x) for x in elec_df['elec_off_name']]

    # Only use unique search terms and those which are not None.
    srch_term_list = elec_df['srch_term'].unique().tolist()
    srch_term_list = [x for x in srch_term_list if x is not None]

    return srch_term_list[0:1500]  # !!Subset!!


def clean_srch_term(srch_term):
    """
    Cleans the search term form substrings not helping to identify
    the location of the election office and thereby invalidate the 
    google search.
    """

    exclusion_dict = {'Briefwahlbezirk': '',
                      'Wahlbezirk': '',
                      'Stimmbezirk': '',
                      'Briefwahl': '',
                      'Obere': '',
                      'Mittlere': '',
                      'Untere': ''}

    for word, replacement in exclusion_dict.items():
        try:
            if word in srch_term:
                return srch_term.replace(word, replacement)
        except:
            pass
    return srch_term


def postal_indicator(elec_off_name):
    """
    Returns one if the election office name contains a keyword indicating
    a postal ballot, otherwise zero.
    """

    postal_keywords = ['Briefwahl', 'Briefwahlbezirk']
    try:
        if any(key in elec_off_name for key in postal_keywords):
            return 1
        else:
            return 0
    except:
        pass


def gmaps_elec_offices(srch_term):
    """
    Gets longitude, latitude and postal code data from a
    google maps search for a provided search term. For each search 
    term a dictionary is returned.
    """

    # Dict and dataframe o store geo information.
    elec_off_dict = {'srch_term': srch_term}

    # Get coordinates for search term.
    key = 'AIzaSyCfFTBllwpO1fIkKbUvduBDyo_WXXxAFZE'
    geo = geocoder.google(srch_term, key=key)

    # Store longitude, latitude, postal code and locality in
    # prespecified dictionary.
    try:
        elec_off_dict['elec_lat'] = geo.latlng[0]
        elec_off_dict['elec_long'] = geo.latlng[1]
    except:
        elec_off_dict['elec_lat'] = np.nan
        elec_off_dict['elec_long'] = np.nan

    # Also try to get postal code and locality name.
    try:
        elec_off_dict['elec_postal'] = geo.postal
        elec_off_dict['elec_locality'] = geo.locality
    except:
        elec_off_dict['elec_postal'] = np.nan
        elec_off_dict['elec_locality'] = np.nan

    return elec_off_dict


def main():
    # Read in combined election csv.
    elec_df = pd.read_csv(
        ppj('OUT_DATA_ELEC', 'elections_combined.csv'),
        low_memory=False)

    # Election office name plus municipality name as search name.
    srch_term_list = get_srch_term_list(elec_df)

    # Google maps search via multiprocessing.
    dict_list = []
    with mp.Pool() as pool:
        out = pool.map(gmaps_elec_offices, srch_term_list)
        dict_list.extend(out)

    # Dicts to dataframe.
    long_lat_df = pd.DataFrame(dict_list)
    long_lat_df.to_csv(
        ppj('OUT_DATA_ELEC', 'elec_off_longlat.csv'), index=False)

    # Merge latitude and longitude data to combined election csv.
    elec_final_df = pd.merge(elec_df, long_lat_df,
                             how='left', on='srch_term')
    elec_final_df.to_csv(
        ppj('OUT_DATA_ELEC', 'elections_final.csv'), index=False)

    # Final data without postal ballots.
    elec_final_df = elec_final_df[elec_final_df['postal_vote'] == 0]
    elec_final_df.to_csv(
        ppj('OUT_DATA_ELEC', 'elections_final_wo_postal.csv'), index=False)


if __name__ == '__main__':
    main()
