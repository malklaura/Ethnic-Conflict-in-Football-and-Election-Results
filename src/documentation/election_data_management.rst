.. _election_data_management:

************************
Election data management
************************

Documentation of the code in *src.data_management.election_data_management*.

.. _get_scrapable_municipalties:
Get scrapable municipalties
===========================

Documentation of the code in *src.data_management.election_data_management.get_scrapable_mun*, which returns scrapable municpalities from the `Votemanager Site <https://wahlen.votemanager.de/>`_.

.. automodule:: src.data_management.election_data_management.get_scrapable_mun
    :members: 


.. _scrape_download_urls:
Scrape download urls
====================
Documentation of the code in *src.data_management.election_data_management.scrape_dwnld_urls*, which returns a dataframe containing all election information for each municipality present in `Votemanager Site <https://wahlen.votemanager.de/>`_. In particular, this includes the download url for the csv file containing electionr results on the lowest voting level, i.e. election office. 

.. automodule:: src.data_management.election_data_management.scrape_dwnld_urls
    :members:

.. automodule:: src.data_management.election_data_management.get_dwnld_urls
    :members:


.. _merge_election_files:
Merge election files
====================
Documentation of the code in *src.data_management.election_data_management.scrape_dwnld_urls*, which merges election information to municipality name.
.. automodule:: src.data_management.election_data_management.merge_election_files
    :members:


.. _download_election_csv_files:
Download election CSV files
===========================
Documentation of the code in *src.data_management.election_data_management.dwnld_election_files*, which downloads all csv stored in *bld.out.data.election_files.election_mun_urls.csv* to *bld.out.data.election_files.download_csv*. The code also combines all .csv files and appends relevant election information on the fly. The resulting dataframe is stored in *bld.out.data.election_files.election_combined.csv*.

.. automodule:: src.data_management.election_data_management.dwnld_election_files
    :members:


.. _get_geodata_by_election_office:
Get geodata by election office
==============================
Documentation of the code in *src.data_management.election_data_management.get_longlat_coords*, which returns longitude, latitude data for each election office in the *bld.out.data.election_files.election_combined.csv* by doing a google maps search for each election office. The resulting dataframe is stored in *bld.out.data.election_files.election_final.csv*.

.. automodule:: src.data_management.election_data_management.get_longlat_coords
    :members:

