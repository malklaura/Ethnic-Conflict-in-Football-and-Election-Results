import pytest
import warnings
import numpy as np
from src.data_management.football_data_management.get_plyr_nationality import get_age_nat


def test_first_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/lars-derksen-294421.html")

	assert plyr_dict["age"] == "21.09.1993"
	assert plyr_dict["nat"] == "Deutschland"


def test_second_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/eduard-kelm-620335.html")
	assert plyr_dict["age"] == "06.08.1991"
	assert plyr_dict["nat"] == "Russische Föderation"


def test_third_player():
	plyr_dict = get_age_nat("https://www.fupa.net/spieler/ergin-abdul-576029.html")

	assert plyr_dict["age"] == "03.02.1993"
	assert plyr_dict["nat"] == "Mazedonien"
