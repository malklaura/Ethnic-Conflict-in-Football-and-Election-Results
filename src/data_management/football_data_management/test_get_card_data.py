import pytest
from src.data_management.football_data_management.get_game_data import get_card_data

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

def test_number_of_yellow_cards(get_game_soup):
	game_dict = {}
	game_dict = get_card_data(get_game_soup, game_dict)
	assert game_dict["home_card_min_0"] == 83
	assert game_dict["home_card_min_0"] == None
	assert game_dict["home_card_min_0"] == None
	assert game_dict["away_card_min_0"] == 63
	assert game_dict["away_card_min_1"] == 63
	assert game_dict["away_card_min_2"] == 67
	
	assert game_dict["home_card_clr_0"] == 2
	assert game_dict["home_card_clr_1"] == None
	assert game_dict["home_card_yllw"] == None
	assert game_dict["home_card_red"] == 1

	assert game_dict["away_card_clr_0"] == 1
	assert game_dict["away_card_clr_1"] == 1
	assert game_dict["away_card_yllw"] == 6
	assert game_dict["away_card_red"] == 0