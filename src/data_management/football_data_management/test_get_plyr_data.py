import pytest
from src.data_management.football_data_management.get_game_data import get_player_data

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

def test_player_names(get_game_soup):
	game_dict = {}
	game_dict = get_player_data(get_game_soup, game_dict)
	assert game_dict["home_plyr_0"] == "Jüttemeier, Christopher"
	assert game_dict["home_plyr_1"] == "Derksen, Lars"
	assert game_dict["home_plyr_2"] == "Ohno, Takahito"

	assert game_dict["away_plyr_0"] == "Salmen, Christian"
	assert game_dict["away_plyr_1"] == "Wirsing, Philipp"
	assert game_dict["away_plyr_2"] == "Krämer, Jan Luca"
