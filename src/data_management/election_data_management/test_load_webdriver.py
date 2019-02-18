import pytest
from src.data_management.election_data_management.get_scrapable_mun import load_webdriver

def test_delay_as_string():
	with pytest.raises(TypeError):
		load_webdriver(r"C:/Users/maxim/Documents/master_eco/eco/geckodriver.exe", "http://wahlen.votemanager.de", "2")

def test_wrong_webdriver_path():
	from selenium import webdriver
	with pytest.raises(selenium.common.exceptions.WebDriverException):
		load_webdriver(r"C:/Users/maxim/Documents/master_eco/eco/nodriver.exe", "http://wahlen.votemanager.de", 2)

def test_invalid_url():
	load_webdriver(r"C:/Users/maxim/Documents/master_eco/eco/geckodriver.exe", "http://wahlenvotemanager.de", 2)
