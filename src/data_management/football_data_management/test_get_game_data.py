import pytest

from src.data_management.football_data_management.get_game_data import *


@pytest.fixture
def get_game_soup():
    import urllib3
    import certifi
    from bs4 import BeautifulSoup

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    game_url = 'https://www.fupa.net/spielberichte/sc-borussia-lindenthal-hohenlind-ssv-homburg-nuembrecht-6517307.html'
    game_request = http.request('GET', game_url)
    game_soup = BeautifulSoup(game_request.data, 'lxml')

    return game_soup


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_card_color_and_min(get_game_soup):
    """
    Tests card scraping for both home and away team.
    """

    game_dict = {}
    game_dict = get_card_data(get_game_soup, game_dict)

    # Home team cards.
    assert game_dict['home_card_min_0'] == 83

    assert game_dict['home_card_clr_0'] == 2

    assert game_dict['home_card_yllw'] == 0
    assert game_dict['home_card_red'] == 1

    # Not present in specified game.
    with pytest.raises(KeyError):
        assert game_dict['home_card_min_1'] == None
        assert game_dict['home_card_min_2'] == None
        assert game_dict['home_card_min_3'] == None

        assert game_dict['home_card_clr_1'] == None
        assert game_dict['home_card_clr_2'] == None
        assert game_dict['home_card_clr_3'] == None

    # Away team cards.
    assert game_dict['away_card_min_0'] == 63
    assert game_dict['away_card_min_1'] == 66
    assert game_dict['away_card_min_2'] == 67
    assert game_dict['away_card_min_3'] == 70

    assert game_dict['away_card_clr_0'] == 1
    assert game_dict['away_card_clr_1'] == 1
    assert game_dict['away_card_clr_2'] == 3
    assert game_dict['away_card_clr_3'] == 3

    assert game_dict['away_card_yllw'] == 6
    assert game_dict['away_card_red'] == 0


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_player_name(get_game_soup):
    """
    Tests for player names for both home and away team.
    We cannot directly test game_dict['home_plyr_1'] == 'xxx', since player
    enumeration changes on the website. However, since we check for all 
    players and split the game dictionary in home and away team, this 
    approach should yield equivalent results.
    """

    game_dict = {}
    game_dict = get_player_data(get_game_soup, game_dict)

    # Dictionary of home team.
    home_dict = {k: v for k, v in game_dict.items()
                 if k.startswith('home_plyr')}

    # Assert player names.
    assert 'Jüttemeier, Christopher' in home_dict.values()
    assert 'Derksen, Lars' in home_dict.values()
    assert 'Sarbo, Julian' in home_dict.values()
    assert 'Klein, Tom-Luca' in home_dict.values()
    assert 'Spiegel, Daniel' in home_dict.values()
    assert 'Sanganaza, Mauriphile-Ekaba' in home_dict.values()
    assert 'Pletto, Gero' in home_dict.values()
    assert 'Reichling, Jeff' in home_dict.values()
    assert 'Caspari, Stefan' in home_dict.values()
    assert 'Ohno, Takahito' in home_dict.values()
    assert 'Dürscheid, Thomas' in home_dict.values()

    # Assert dictionary enumeration.
    assert 'home_plyr_0' in home_dict.keys()
    assert 'home_plyr_1' in home_dict.keys()
    assert 'home_plyr_2' in home_dict.keys()
    assert 'home_plyr_3' in home_dict.keys()
    assert 'home_plyr_4' in home_dict.keys()
    assert 'home_plyr_5' in home_dict.keys()
    assert 'home_plyr_6' in home_dict.keys()
    assert 'home_plyr_7' in home_dict.keys()
    assert 'home_plyr_8' in home_dict.keys()
    assert 'home_plyr_9' in home_dict.keys()
    assert 'home_plyr_10' in home_dict.keys()

    # Dictionary of away team.
    away_dict = {k: v for k, v in game_dict.items()
                 if k.startswith('away_plyr')}

    # Assert player names.
    assert 'Salmen, Christian' in away_dict.values()
    assert 'Wirsing, Philipp' in away_dict.values()
    assert 'Krämer, Jan Luca' in away_dict.values()
    assert 'Schwarz, Julian' in away_dict.values()
    assert 'Ziegler, Thomas' in away_dict.values()
    assert 'Bauerfeind, Ricardo' in away_dict.values()
    assert 'Seinsche, Kilian' in away_dict.values()
    assert 'Kelm, Daniel' in away_dict.values()
    assert 'Henscheid, Jonas' in away_dict.values()
    assert 'Barth, Tom' in away_dict.values()
    assert 'Rüttgers, Christian' in away_dict.values()

    # Assert dictionary enumeration.
    assert 'away_plyr_0' in away_dict.keys()
    assert 'away_plyr_1' in away_dict.keys()
    assert 'away_plyr_2' in away_dict.keys()
    assert 'away_plyr_3' in away_dict.keys()
    assert 'away_plyr_4' in away_dict.keys()
    assert 'away_plyr_5' in away_dict.keys()
    assert 'away_plyr_6' in away_dict.keys()
    assert 'away_plyr_7' in away_dict.keys()
    assert 'away_plyr_8' in away_dict.keys()
    assert 'away_plyr_9' in away_dict.keys()
    assert 'away_plyr_10' in away_dict.keys()


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_player_url(get_game_soup):
    """
    Tests for player urls. Structure follows argument of 
    *test_player_name* test.
    """

    game_dict = {}
    game_dict = get_player_data(get_game_soup, game_dict)

    # Home team.
    home_dict = {k: v for k, v in game_dict.items()
                 if k.startswith('home_plyr_url')}

    # Home player URLs.
    assert 'https://www.fupa.net/spieler/christopher-juettemeier-745314.html' in home_dict.values()
    assert 'https://www.fupa.net/spieler/thomas-duerscheid-729687.html' in home_dict.values()

    # Assert dictionary enumeration.
    assert 'home_plyr_url_0' in home_dict.keys()
    assert 'home_plyr_url_1' in home_dict.keys()
    assert 'home_plyr_url_2' in home_dict.keys()
    assert 'home_plyr_url_3' in home_dict.keys()
    assert 'home_plyr_url_4' in home_dict.keys()
    assert 'home_plyr_url_5' in home_dict.keys()
    assert 'home_plyr_url_6' in home_dict.keys()
    assert 'home_plyr_url_7' in home_dict.keys()
    assert 'home_plyr_url_8' in home_dict.keys()
    assert 'home_plyr_url_9' in home_dict.keys()
    assert 'home_plyr_url_10' in home_dict.keys()

    # Away team.
    away_dict = {k: v for k, v in game_dict.items()
                 if k.startswith('away_plyr_url')}

    # Away player URLs.
    assert 'https://www.fupa.net/spieler/jan-luca-kraemer-337727.html' in away_dict.values()
    assert 'https://www.fupa.net/spieler/jonas-henscheid-298305.html' in away_dict.values()

    # Assert dictionary enumeration.
    assert 'away_plyr_url_0' in away_dict.keys()
    assert 'away_plyr_url_1' in away_dict.keys()
    assert 'away_plyr_url_2' in away_dict.keys()
    assert 'away_plyr_url_3' in away_dict.keys()
    assert 'away_plyr_url_4' in away_dict.keys()
    assert 'away_plyr_url_5' in away_dict.keys()
    assert 'away_plyr_url_6' in away_dict.keys()
    assert 'away_plyr_url_7' in away_dict.keys()
    assert 'away_plyr_url_8' in away_dict.keys()
    assert 'away_plyr_url_9' in away_dict.keys()
    assert 'away_plyr_url_10' in away_dict.keys()


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_game_smmry_stats(get_game_soup):
    """
    Tests for game summary statistics.
    """

    game_dict = {}
    game_dict = get_smmry_data(get_game_soup, game_dict)

    assert game_dict['league'] == 'Landesliga, St. 1'
    assert game_dict['fb_date'] == '02.09.18'
    assert game_dict['fb_time'] == '15:30'
    assert game_dict['matchday'] == '2'
    assert game_dict['result'] == '3:1'
    assert game_dict['referee'] == 'Scheffel, Thomas'

    assert game_dict['home_team'] == 'SC Borussia Lindenthal-Hohenlind'
    assert game_dict[
        'home_team_url'] == 'https://www.fupa.net/club/sc-borussia-lindenthal-hohenlind/team/m1'
    assert game_dict['home_club'] == 'SC Borussia Lindenthal-Hohenlind'

    assert game_dict['away_team'] == 'SSV Homburg-Nümbrecht'
    assert game_dict[
        'away_team_url'] == 'https://www.fupa.net/club/ssv-homburg-nuembrecht/team/m1'
    assert game_dict[
        'away_club'] == 'SG Homburg-Nümbrecht/Elsenroth/Drabenderhöhe'
