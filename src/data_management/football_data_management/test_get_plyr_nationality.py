import pytest
import numpy as np
from src.data_management.football_data_management.get_plyr_data import get_age_nat


def test_first_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/lars-derksen-294421.html")

	assert plyr_dict["age"] == 25
	assert game_dict["nat"] == "Deutschland"


def test_second_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/takahito-ohno-1483823.html")

	assert plyr_dict["age"] == np.nan
	assert game_dict["nat"] == "Japan"


def test_third_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/ergin-abdul-576029.html")

	assert plyr_dict["age"] == 26
	assert game_dict["nat"] == "Mazedonien"
