import pytest
from src.data_management.football_data_management.get_game_data import *

@pytest.fixture
def get_game_soup():
	import urllib3
	import certifi
	from bs4 import BeautifulSoup

	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

	game_url = "https://www.fupa.net/spielberichte/sc-borussia-lindenthal-hohenlind-ssv-homburg-nuembrecht-6517307.html"
	game_request = http.request("GET", game_url)
	game_soup = BeautifulSoup(game_request.data, 'lxml')

	return game_soup

def test_card_color_and_min(get_game_soup):
	game_dict = {}
	game_dict = get_card_data(get_game_soup, game_dict)

	assert game_dict["home_card_min_0"] == 83

	assert game_dict["away_card_min_0"] == 63
	assert game_dict["away_card_min_1"] == 66
	assert game_dict["away_card_min_2"] == 67
	assert game_dict["away_card_min_3"] == 70
	
	assert game_dict["home_card_clr_0"] == 2

	assert game_dict["home_card_yllw"] == 0
	assert game_dict["home_card_red"] == 1

	assert game_dict["away_card_clr_0"] == 1
	assert game_dict["away_card_clr_1"] == 1
	assert game_dict["away_card_clr_2"] == 3
	assert game_dict["away_card_clr_3"] == 3

	assert game_dict["away_card_yllw"] == 6
	assert game_dict["away_card_red"] == 0

	with pytest.raises(KeyError):
		assert game_dict["home_card_min_1"] == None
		assert game_dict["home_card_min_2"] == None
		assert game_dict["home_card_min_3"] == None
		assert game_dict["home_card_clr_1"] == None


def test_player_name_and_url(get_game_soup):
	game_dict = {}
	game_dict = get_player_data(get_game_soup, game_dict)

	assert game_dict["home_plyr_0"] == "Jüttemeier, Christopher"
	assert game_dict["home_plyr_1"] == "Derksen, Lars"
	assert game_dict["home_plyr_4"] == "Sarbo, Julian"
	assert game_dict["home_plyr_5"] == "Klein, Tom-Luca"
	assert game_dict["home_plyr_6"] == "Spiegel, Daniel"
	assert game_dict["home_plyr_7"] == "Sanganaza, Mauriphile-Ekaba"
	assert game_dict["home_plyr_8"] == "Pletto, Gero"
	assert game_dict["home_plyr_9"] == "Reichling, Jeff"
	assert game_dict["home_plyr_10"] == "Caspari, Stefan"
	assert "Ohno, Takahito" in game_dict.values()
	assert "Dürscheid, Thomas" in game_dict.values()
	assert "home_plyr_2" in game_dict.keys()
	assert "home_plyr_3" in game_dict.keys()

	assert "Salmen, Christian" in game_dict.values()
	assert "Wirsing, Philipp" in game_dict.values()
	assert "Krämer, Jan Luca" in game_dict.values()
	assert "Schwarz, Julian" in game_dict.values()
	assert "Ziegler, Thomas" in game_dict.values()
	assert "Bauerfeind, Ricardo" in game_dict.values()
	assert "Seinsche, Kilian" in game_dict.values()
	assert "Kelm, Daniel" in game_dict.values()
	assert "Henscheid, Jonas" in game_dict.values()
	assert "Barth, Tom" in game_dict.values()
	assert "Rüttgers, Christian" in game_dict.values()

	# assert game_dict["home_plyr_url_1"] == 
	# assert game_dict["home_plyr_url_2"] == 
	# assert game_dict["home_plyr_url_3"] == 
	# assert game_dict["home_plyr_url_4"] == 
	# assert game_dict["home_plyr_url_5"] == 
	# assert game_dict["home_plyr_url_6"] == 
	# assert game_dict["home_plyr_url_7"] == 
	# assert game_dict["home_plyr_url_8"] == 
	# assert game_dict["home_plyr_url_9"] == 
	# assert game_dict["home_plyr_url_10"] == 

	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==
	# assert game_dict["away_plyr_url_0"] ==

def test_game_smmry_stats(get_game_soup):
	game_dict = {}
	game_dict = get_smmry_data(get_game_soup, game_dict)

	assert game_dict["league"] == "Landesliga, St. 1"
	assert game_dict["fb_date"] == "02.09.18"
	assert game_dict["fb_time"] == "15:30"
	assert game_dict["matchday"] == "2"
	assert game_dict["result"] == "3:1"
	assert game_dict["referee"] == "Scheffel, Thomas"

	assert game_dict["home_team"] == "SC Borussia Lindenthal-Hohenlind"
	assert game_dict["home_team_url"] == "https://www.fupa.net/club/sc-borussia-lindenthal-hohenlind/team/m1"
	assert game_dict["home_club"] == "SC Borussia Lindenthal-Hohenlind"

	assert game_dict["away_team"] == "SSV Homburg-Nümbrecht"
	assert game_dict["away_team_url"] == "https://www.fupa.net/club/ssv-homburg-nuembrecht/team/m1"
	assert game_dict["away_club"] == "SG Homburg-Nümbrecht/Elsenroth/Drabenderhöhe"
