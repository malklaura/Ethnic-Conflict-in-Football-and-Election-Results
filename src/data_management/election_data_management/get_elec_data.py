import certifi
import urllib3
from bs4 import BeautifulSoup


def get_soup_object(url):
    """
    Returns a soup object from a given url.
    """

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    page_request = http.request('GET', url)
    page_soup = BeautifulSoup(page_request.data, 'lxml')

    return page_soup


def get_elections_soup(mun_url):
    """
    Returns a soup object containing all elections
    objects included in the municipality url.
    """

    page_soup = get_soup_object(mun_url)
    elections_soup = page_soup.find_all('tr')[1:]

    return elections_soup


def get_elec_type_str(elec, elec_dict):
    """
    Returns the name of the considered election.
    """

    elec_date = elec.a.text
    elec_type_str = elec.text.strip().replace(elec_date, '')

    # Write to dict.
    elec_dict['elec_date'] = elec_date

    return elec_type_str


def get_pssbl_elections(elec, mun_url, elec_dict):
    """
    Returns all elections that took place on a certain date.
    The need for this function arises from the fact, that more than one election
    can take place on the same day and that some elections have the possibility
    of Erst- and Zweistimmen.
    """

    # Construct election url.
    elec_url = mun_url.rsplit('/', 2)[0] + elec.a['href'][2:]
    elec_soup = get_soup_object(elec_url)
    elec_dict['elec_url'] = elec_url

    # Find possible elections.
    poss_elections = elec_soup.find_all('div', {'class': 'well well-sm'})

    return poss_elections


def get_voting_lvl(poss_election, elec_dict):
    """
    Returns the class of all possible voting levels for a given
    election, e.g., municipal or election office level.
    """

    sublvl_href = poss_election.a['href']
    sublvl_url = elec_dict['elec_url'].rsplit(
        '/', 1)[0] + '/' + sublvl_href
    sublvl_soup = get_soup_object(sublvl_url)

    voting_lvl = sublvl_soup.find_all(
        'div', {'class': 'container-fluid'})[0]
    voting_lvl = voting_lvl.find('ul', {'class': 'nav navbar-nav'})
    voting_lvl = voting_lvl.find_all('a')

    return voting_lvl


def get_dwnld_url(level, elec_abbrev, elec_dict):
    """
    Returns the download url for a given voting level.
    """

    # Make sure to get 'Zweitstimmen'.
    level_href = level['href']
    if 'Erststimmen' in level_href:
        level_href = level_href.replace(
            'Erststimmen', 'Zweitstimmen')

    level_url = elec_dict['elec_url'].rsplit(
        '/', 1)[0] + '/' + level_href
    level_soup = get_soup_object(level_url)

    # Construct download url.
    dwnld_soup = level_soup.find_all('ul', {'class': 'dropdown-menu'})[-1]
    dwnld_href = dwnld_soup.find_all('a')[-1]['href']
    dwnld_url = elec_dict['elec_url'].rsplit(
        '/', 1)[0] + '/' + dwnld_href

    # Write to dict.
    elec_dict['dwnld_url'] = dwnld_url
    elec_dict['abbrev'] = elec_abbrev

    return elec_dict


def get_elec_type_dict():
    """
    Creates an election specific dictionary for each election. Those
    are stored in an encompassing dictionary.
    """

    # Dictionary with relevant information for all considered elections.
    bw_dict = {'srch_trm': 'Bundestag',
               'level': 'Wahlbezirk', 'abbrev': 'BW'}
    lw_dict = {'srch_trm': 'Landtag',
               'level': 'Stimmbezirk', 'abbrev': 'LW'}
    ew_dict = {'srch_trm': 'Europa',
               'level': 'Wahlbezirk', 'abbrev': 'EW'}

    # Store all dictionaries in an election type dictionary.
    elec_type_dict = {'Bundestagswahl': bw_dict,
                      'Landtagswahl': lw_dict,
                      'Europawahl': ew_dict}

    return elec_type_dict


def elec_type_check(elec, mun_url, elec_dict, elec_dict_list):
    """
    Checks, whether a possible election object fulfills the requirements 
    specified in the election type dictionaries. If this is the case, 
    election information and corresponding download URL are stored in a 
    dictionary.
    """

    # Needed since there are occurrences of multiple elections on same day.
    pssbl_elections = get_pssbl_elections(elec, mun_url, elec_dict)

    # Relod election type dict.
    elec_type_dict = get_elec_type_dict()

    # Loop through all listed elections.
    for poss_elec in pssbl_elections:
        # Loop through election type dicts.
        for key, elec_type in elec_type_dict.copy().items():
            # for key, elec_type in elec_type_dict.items():
            # Check if possible election matches election type criteria.
            if elec_type['srch_trm'] in poss_elec.script.get_text():
                voting_lvl = get_voting_lvl(poss_elec, elec_dict)
                for level in voting_lvl:
                    # Get csv download url on election office (Wahlbuero)
                    # level.
                    if elec_type['level'] in level.text:
                        elec_dict = get_dwnld_url(
                            level, elec_type['abbrev'], elec_dict)
                        elec_dict_list.append(elec_dict)
                        # Exclude used election type dict from further
                        # consideration.
                        del elec_type_dict[key]
            else:
                pass

    return elec_dict_list


def scrape_elec_data(mun_url):
    """
    Run web scraping process over all scrapable municipalities. In the end 
    a dataframe containing all download URLs is returned for all elections
    of interest.
    """

    # Append all election dictionaries to this list.
    elec_dict_list = []

    try:
        # Get elections.
        elec_soup = get_elections_soup(mun_url)

        # Loop through all declared elections.
        for elec in elec_soup:
            elec_dict = {'mun_url': mun_url}
            # Name of Election
            elec_type_str = get_elec_type_str(elec, elec_dict)

            # Check if we want to scrap this type of election.
            elections_of_interest = ['Bundestag', 'Landtag', 'Europa']
            if any(word in elec_type_str for word in elections_of_interest):
                # If relevant, try to get download url.
                elec_dict_list = elec_type_check(
                    elec, mun_url, elec_dict, elec_dict_list)
    except:
        pass

    return elec_dict_list
