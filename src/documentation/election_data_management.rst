.. _election_data_management:

************************
Election data management
************************

Documentation of the code in *src.data_management.election_data_management*. This part of the project compiles a dataset consisting of all election results on the election office level in NRW across the last ten years. The follow the hierarchial structure of the wscript file.

.. _get_scrapable_municipalties:

Get scrapable municipalties
===========================

Documentation of the code in *src.data_management.election_data_management.get_elec_mun*, which returns scrapable municpalities from the `<https://wahlen.votemanager.de/>`_. The resulting dataframe is stored in *bld.out.data.election_files.scrapable_mun.csv*.

.. automodule:: src.data_management.election_data_management.get_elec_mun
    :members: 


.. _get_elec_data:

Get election data
===========================

Documentation of the code in *src.data_management.election_data_management.get_elec_data*, which scrapes relevant election information from a given municipal url and returns a game dictionary with the respective data. In particular, the download url for the lowest voting level is returned. 

.. automodule:: src.data_management.election_data_management.get_elec_data
    :members:

Test "get election data"
===========================

Documentation of the code in *src.data_management.election_data_management.test_get_elec_data*, which tests if scraping of election data is working as intended by using pytest.

.. automodule:: src.data_management.election_data_management.test_get_elec_data
    :members:


.. _scrape_elec_data:

Scrape election data
====================

Documentation of the code in *src.data_management.election_data_management.scrape_elec_data*, which uses *multiprocessing* and *src.data_management.election_data_management.get_elec_data* to scrape all election information from the scrapable municipal urls stored in *bld.out.data.election_files.scrapable_mun.csv*. The information are combined in a dataframe, which is stored in *bld.out.data.election_files.election_data.csv*.

.. automodule:: src.data_management.election_data_management.scrape_elec_data
    :members:


.. _build_election_id:

Build election ID
====================

Documentation of the code in *src.data_management.election_data_management.build_elec_id*, which create an unique ID for each election, which functions as file name. Also, the municipality name is merged to the election information. The resulting dataframe is stored in *bld.out.data.election_files.election_id_data.csv*.

.. automodule:: src.data_management.election_data_management.build_elec_id
    :members:


.. _download_election_csv:

Download election CSV files
===========================

Documentation of the code in *src.data_management.election_data_management.dwnld_elec_csv*, which downloads all *.csv* files from the urls provided in *bld.out.data.election_files.election_id_data.csv*. The script also combines all *.csv* files and appends relevant election information on the fly. The resulting dataframe is stored in *bld.out.data.election_files.elections_combined.csv*.

.. automodule:: src.data_management.election_data_management.dwnld_elec_csv
    :members:


.. _get_election_office_geodata:

Get election office geodata
==============================

Documentation of the code in *src.data_management.election_data_management.get_elec_off_longlat*, which returns longitude, latitude and postal code data for each election office in *bld.out.data.election_files.election_combined.csv* by doing a google maps search by election office and municipal name. The resulting data are stored in *bld.out.data.election_files.elec_off_longlat.csv*, while a merged version with the combined election results is stored in *bld.out.data.election_files.elections_final.csv*.

.. automodule:: src.data_management.election_data_management.get_elec_off_longlat
    :members:

