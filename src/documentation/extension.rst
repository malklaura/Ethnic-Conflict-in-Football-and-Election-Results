.. _extension:

*****************
Project Extension
*****************

Extension
==========

If you wish to extend the scope of this project beyond the state of NRW, two parts of the code need to be adjusted, both in the election and football management part. 

Election data management
-------------------------

Navigate to lines 79-82 in *src/data_management/election_data_management/get_elec_mun.py* and comment out the second line to scrape all election data across Germany or change the name of the state accordingly.

.. literalinclude:: ../../src/data_management/election_data_management/get_elec_mun.py
    :language: python
    :lines: 83-86


Football data management
-------------------------

The football data scraping can be extended by navigating to lines 150-155 in *src/data_management/football_data_management/get_matchday_data.py* and adding further regions to the regions list. An overview of the regions constituting all of German amateur football is given on `<https://fupa.net/>`_.

.. literalinclude:: ../../src/data_management/football_data_management/get_matchday_data.py
    :language: python
    :lines: 159-161

**Note that if you want to merge the two resulting datasets, the regions in the football scraping have to correspond to the states specified in the election scraping.**