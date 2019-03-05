Web Scraping of Election and Football Files from NRW
=====================================================

Introduction
============

This project deals with the web scraping of amateur football and election data from Germany. The project is meant to provide the data for a future analysis of the effect of ethnic conflict in amateur football on subsequent election results. 

In a first step, both data are scraped from `<https://fupa.net>`_ and `<https://wahlen.votemanager.de>`_ respectively. The election dataset consists of election results by election office (~1,000 eligible voters), while the football dataset consists of individual games, including percentage data on the ethnic composition of each team and a measure of violence (sum of red and yellow cards per team). In a next step, game data are merged on election offices by postal and year data. For those matches, time and geodata distance measures are computed. Observations are dropped when they lie outside a prespecified threshold. The remaining data are grouped by election office id and election. The final dataset is a panel indexed by election office and election with a meaned measure of ethnic composition and violence of time and geographic close football games.


Waf template
-----------------

This project works with the waf environment provided by `Gaudecker <https://github.com/hmgaudecker/econ-project-templates/>`_. To get accustomed with the workflow in the template I refer you to the documentation of the `waf template <https://github.com/hmgaudecker/econ-project-templates/>`_. All you should need to worry about is to call the correct task generators in the wscript files. Always specify the actions in the wscript that lives in the same directory as your main source file. Make sure you understand how the paths work in Waf and how to use the auto-generated files in the particular language you are using.


!Effective Programming Version!
================================

As mentioned below this project requires a Google API-Key to extract geodata from GoogleMaps, which in turn requires the deposit of credit card information. To properly evaluate this term paper **my own API-Key** is stored in the relevant scripts. However, because the key only allows for up to 300 USD of free use and each subsequent query is subject to a charge, the project in this version only extracts geodata for a really limited subset of election offices and football clubs, as can be seen in

1. **src/data_management/election_data_management/get_elec_off_longlat.py, line 35** and 
2. **src/data_management/football_data_management/get_club_longlat.py, line 52**

Therefore, the resulting merged dataframe of both data sources is much smaller than theoretical possible.

Also, note that a **current version of the GeckoDriver corresponding to your operating system is needed**. For further details see the prerequisites section below.

Finally, to save computing time football game data are only crawled for the last five seasons. To lift this restriction simply remove the list constraint in **src/data_management/football_data_management/get_matchday_data.py, line 109**.

Installation
============

Clone repository
-----------------

To play with the project, clone the repository to your disk with

.. code-block:: bash

    $ git clone https://github.com/mmaeh/Ethnic-Conflict-in-Football-and-Election-Results.git


Get prerequisites
------------------

Although the script is meant to run in one go, two external requirements are required before initializing the building process.

GeckoDriver
++++++++++++

In a first step a recent version of the *GeckoDriver*, a WebDriver engine, is required. The scraping of the election data requires a browser automation framework, which is provided by *Selenium Python*, which requires such a WebDriver. The major advantage of using *GeckoDriver* as opposed to the default Firefox driver is the compatibility of *GeckoDriver* with the W3C WebDriver protocol to communicate with Selenium, which is a universally defined standard for WebDrivers. Recent versions of the driver are available on `<https://github.com/mozilla/geckodriver/releases>`_. After downloading the appropriate version for your operating system, provide the path to the driver in **src/data_management/election_data_management/get_elec_mun.py line 103**. 

There are drivers for all major browsers, for their use see the documentation on `<https://selenium-python.readthedocs.io/installation.html>`_. However, the project is not tested for other WebDrivers.

Google API key
+++++++++++++++

Further, the collection of longitude and latitude data for the football club and election office locations requires a *google API KEY*, to use google services on an automated scale. The key generation requires a google account and a sign up to googles cloud platform https://cloud.google.com/maps-platform/. The provided key allows for free monthly search queries of up to 300.00 USD, which should be more than sufficient for this project. Once your personal key is generated you need to provide it in **src/data_management/election_data_management/get_elec_off_longlat.py line 89** and in **src/data_management/football_data_management/get_club_longlat.py line 20**.

Python modules
++++++++++++++++

Lastly, make sure to install the following python modules if they are not already present on your machine::

    pip install beautifulsoup4
    pip install certifi
    pip install geocoder
    pip install multiprocessing
    pip install selenium
    pip install unidecode
    pip install urllib3

Build project
---------------

After completing the above steps, you can run the following two commands to start the building process

.. code-block:: bash

    $ python waf.py configure
    $ python waf.py build

Note that the first command only needs to be run once after cloning the repository. For subsequent buildings, only the second command is required.

Be aware, that especially the google queries to get the geodata will take much time, although running on multiprocessing. When the process is finished, you find the merged dataset in **bld/out/final_data/elections_games_final.csv**.

To generate the project documentation and the .pdf presentation file additionally run

.. code-block:: bash

    $ python waf.py install


Project Structure
==================

The logic of this project works according to the following hierarchic structure:

1. Election data management
    a. Determination of scrapable municipalties
    b. Scrape election information and download url of election results
    c. Download election .csv files and combine to one .csv file
    d. Get geodata for each election office in combined .csv file
2. Football data management
    a. Get data of all leagues present in `<https://fupa.net/>`_
    b. Get dataframe of all game urls within those leagues
    c. Scrape football game data for each game and store in separate matchday CSV files
    d. Merge CSV files from c. to one combined file.
    e. Scrape player ethnicity from player urls
    f. Get geodata for each football club
    g. Merge e. and f. to d.
3. Merge election and football files
4. Visualisation of results
5. Compile sample presentation and documentation 

Note that this structure just gives a rough intuition behind the steps executed in the building process. In the actual building several scripts will be run simultaneously. The dependencies of each file is determined thorugh the the top-level wscript files, stored in the separate folders of the *src* part.