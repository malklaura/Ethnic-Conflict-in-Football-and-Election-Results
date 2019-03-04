import pytest
from src.data_management.election_data_management.get_elec_data import scrape_elec_data


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_scrape_elec_data():
    elec_dict_list = scrape_elec_data(
        'https://wahlen.regioit.de/AC/05334002/index.html')

    bw_2017_dict = elec_dict_list[0]
    assert bw_2017_dict['abbrev'] == 'BW'
    assert bw_2017_dict['elec_date'] == '24.09.2017'
    assert bw_2017_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/BW17/05334002/html5/index.html'
    assert bw_2017_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/BW17/05334002/html5/Bundestagswahl706.csv'

    lw_2017_dict = elec_dict_list[1]
    assert lw_2017_dict['abbrev'] == 'LW'
    assert lw_2017_dict['elec_date'] == '14.05.2017'
    assert lw_2017_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/LW17/05334002/html5/index.html'
    assert lw_2017_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/LW17/05334002/html5/Landtagswahl_NRW696.csv'

    ew_2014_dict = elec_dict_list[2]
    assert ew_2014_dict['abbrev'] == 'EW'
    assert ew_2014_dict['elec_date'] == '25.05.2014'
    assert ew_2014_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/KWEW14/05334002/html5/index.html'
    assert ew_2014_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/KWEW14/05334002/html5/Europawahl6.csv'

    bw_2013_dict = elec_dict_list[3]
    assert bw_2013_dict['abbrev'] == 'BW'
    assert bw_2013_dict['elec_date'] == '22.09.2013'
    assert bw_2013_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/BW13/05334002/html5/index.html'
    assert bw_2013_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/BW13/05334002/html5/Bundestagswahl6.csv'

    lw_2012_dict = elec_dict_list[4]
    assert lw_2012_dict['abbrev'] == 'LW'
    assert lw_2012_dict['elec_date'] == '13.05.2012'
    assert lw_2012_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/LW12/05334002/html5/index.html'
    assert lw_2012_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/LW12/05334002/html5/Landtagswahl_NRW6.csv'

    lw_2010_dict = elec_dict_list[5]
    assert lw_2010_dict['abbrev'] == 'LW'
    assert lw_2010_dict['elec_date'] == '09.05.2010'
    assert lw_2010_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/LW10/05334002/html5/index.html'
    assert lw_2010_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/LW10/05334002/html5/Landtagswahl6.csv'

    bw_2009_dict = elec_dict_list[6]
    assert bw_2009_dict['abbrev'] == 'BW'
    assert bw_2009_dict['elec_date'] == '27.09.2009'
    assert bw_2009_dict[
        'elec_url'] == 'https://wahlen.regioit.de/AC/BW09/05334002/html5/index.html'
    assert bw_2009_dict[
        'dwnld_url'] == 'https://wahlen.regioit.de/AC/BW09/05334002/html5/Bundestagswahl6.csv'
