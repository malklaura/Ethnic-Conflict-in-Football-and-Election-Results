.. _football_data_management:

************************
Football data management
************************

Documentation of the code in *src.data_management.football_data_management*.

.. _get_matchday_data:

Get matchday data
===========================

Documentation of the code in *src.data_management.football_data_management.get_matchday_data*, which scrapes `fupa <https://fupa.net/>`_ to return a dataframe containg all matchday-information and -urls for all amateur football games within NRW over the last ten years. The resulting dataframe is stored in *bld.out.data.football_files.matchday_data.csv*.

.. automodule:: src.data_management.football_data_management.get_matchday_data
    :members:


.. _get_game_urls:

Get game URLs
==================

Documentation of the code in *src.data_management.football_data_management.get_game_urls*, which scrapes all game urls for each matchday scraped in *src.data_management.football_data_management.get_matchday_data* using *multiprocessing*. The resulting dataframe is stored in *bld.out.data.football_files.game_urls.csv*.

.. automodule:: src.data_management.football_data_management.get_game_urls
    :members:


.. _get_game_data:

Get game data
===========================
Documentation of the code in *src.data_management.football_data_management.get_game_data*, which scrapes relevant game information from a given game url and returns a game dictionary with the respective data. 

.. automodule:: src.data_management.football_data_management.get_game_data
    :members:


.. _scrape_game_data:

Scrape game data
===========================

Documentation of the code in *src.data_management.football_data_management.scrape_game_data*, which uses *multiprocessing* and *src.data_management.football_data_management.get_game_data* to scrape all game data from the game urls specified in *bld.out.data.football_files.game_urls.csv*. Resulting game dictionaries are combined to a dataframe by matchday ID and saved in *bld.out.data.football_files.matchday_csv*.

.. automodule:: src.data_management.football_data_management.scrape_game_data
    :members:

.. _merge_game_files:

Merge game files
=================

Documentation of the code in *src.data_management.football_data_management.merge_game_files*, which merges all matchday CSV files to single combined file. In the first step, a list containing all column names in all matchday CSV files is constructed. In the next step, those files are written line by line to the combined file. In the end, duplicates are dropped resulting from transregional leagues that are presented in multiple matchday files.

.. automodule:: src.data_management.football_data_management.merge_game_files
    :members:


.. _get_player_nationality:

Get player nationality
===========================

Documentation of the code in *src.data_management.football_data_management.get_plyr_nationality*, which scrapes player nationality and age via mutliprocessing from individual player urls returned by *src.data_management.football_data_management.get_game_data*. The resulting dataframe is stored in *bld.out.data.football_files.plyr_nationality.csv*.

.. automodule:: src.data_management.football_data_management.get_plyr_nationality
    :members:


.. _get_geodata:

Get club geodata
===========================

Documentation of the code in *src.data_management.football_data_management.get_club_longlat*, which utilizes geocoding to get longitude, latitude and postal code for each football club present in player nationality and age via mutliprocessing from individual player urls returned by *src.data_management.football_data_management.get_game_data*. Resulting dataframe is stored in *games_combined.csv*. The resulting data are stored in *bld.out.data.football_files.club_longlat.csv*.

.. automodule:: src.data_management.football_data_management.get_club_longlat
    :members:


.. _merge_game_player_geo_data:

Merge nationality- and geo-data to games
========================================

Documentation of the code in *src.data_management.football_data_management.merge_games_plyr_longlat*, which merges player nationality data and geoinformation data to *games_combined.csv*. The resulting dataframe is stored as *games_final.csv*.

.. automodule:: src.data_management.football_data_management.merge_games_plyr_longlat
    :members: