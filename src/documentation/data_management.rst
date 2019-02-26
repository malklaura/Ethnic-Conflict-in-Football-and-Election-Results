.. _data_management:

***************
Data management
***************

Documentation of the code in *src.data_management.football_data_management*.

Documentation of the code in *src.data_management.final_merge*, which merges *bld.out.data.election_files.election_final.csv* and *bld.out.data.football_files.football_final.csv*. In a first step to each election-office / election observation all football games are merged with the same year and postal code. In a second step geographical and time distances between merged election offices and games are computed. Observations above a prespecified threshold are dropped, those below are grouped by election office name and election type to *bld.out.data.election_game.csv*

.. automodule:: src.data_management.final_merge
    :members: get_geo_distance

.. automodule:: src.data_management.final_merge
    :members: get_time_distance