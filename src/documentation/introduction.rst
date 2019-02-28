.. _introduction:
************
Introduction
************

Summary
========
This project deals with the web scraping of amateur football and election data from Germany. The project is meant to provide the data basis for a subsequent analysis of the effect of ethnic conflict in amateur football on subsequent election results. 

In a first step both election and game data are scraped from `<https://wahlen.votemanager.de/>`_ and `<https://fupa.net/>`_ respectively. In a next step the datasets are augmented with longitude and latitude data from a google search query. Lastly, both datasets are merged by using time and geodata distance measures. The final dataset in as panel containing each election office (and the corresponding election results) as well as a measure of ehtnicity and violence constructed of all football games within a certain geographical and time distance of an election office. Right now the panel covers the state of NRW across the last ten years, although the script can easily be extended to include all german states as described in the *Project Extension* section.

Waf template
------------

This project works with the waf enviroment provided by :cite:`GaudeckerEconProjectTemplates`. To get accustomed with the workflow in the template I refer you to the documentation of the `waf template <https://github.com/hmgaudecker/econ-project-templates/>`_.  All you should need to worry about is to call the correct task generators in the wscript files. Always specify the actions in the wscript that lives in the same directory as your main source file. Make sure you understand how the paths work in Waf and how to use the auto-generated files in the language you are using particular language (see the section :ref:`project_paths` below).


.. _installation:
Installation
============

Clone repository
-----------------

To play with the project, clone the repository to your disk with

.. code-block:: bash

    $ git clone https://github.com/mmaeh/...

After that create an environment with ``conda`` and activate it by running

.. code-block:: bash

    $ conda env create -n sp -f environment.yml
    $ activate sp

Get prerequisites
------------------

Although the script is meant to run in one go, two external requirements are required before initializing the building process.

GeckoDriver
++++++++++++

In a first step a recent version of the *GeckoDriver*, a WebDriver engine, is required. The scraping of the election data requires a browser automation framework, which is provided by *Selenium Python*, whichm requires such a WebDriver. The major advantage of using *GeckoDriver* as opposed to the default Firefox driver is the compatibility of *GeckoDriver* with the W3C WebDriver protocol to communicate with Selenium, which is a universally defined standard for WebDrivers. Recent versions of the driver are available on `<https://github.com/mozilla/geckodriver/releases>`_. **After downloading the appropriate version for your operating system, provide the path to the driver in *src.data_management.election_data_management.get_elec_mun.py* line *90***. 

.. literalinclude:: ../../src/data_management/election_data_management/get_elec_mun.py
    :lines: 88-92

There are drivers for all major browsers, for their use see the documentation on `<https://selenium-python.readthedocs.io/installation.html>`_, however, the project is not tested for other WebDrivers.

Google API key
+++++++++++++++

Further, the collection of longitude and latitude data for football club and election office locations requires a *google API KEY*, to use google services on an automated scale. The key generation requires a google account and a sign up to googles cloud platform https://cloud.google.com/maps-platform/. The provided key allows for free monthly search queries of up to 300.00 USD, which should be more than sufficient for this project. Once your personal key is generated **you need to provide it in *src.data_management.election_data_management.get_elec_off_longlat.py* line *74* and in *src.data_management.football_data_management.get_club_longlat.py* line *17***.

Python modules
++++++++++++++++

In a last step, make sure to install the following python modules if they are not already present on your machine::

    pip install beautifulsoup4
    pip install certifi
    pip install geocoder
    pip install multiprocessing
    pip install selenium
    pip install unidecode
    pip install urllib3

Build project
---------------

After completing the above steps you can run the following two commands to start the building process

.. code-block:: bash

    $ python waf.py configure distclean
    $ python waf.py build

Be aware, that especially the google queries to get the geodata will take a lot of time. When the process is finished you find the merged dataset in *bld.out.final_data.elections_games_final.csv*.

To generate this documentation and the .pdf presentation file run

.. code-block:: bash

    $ python waf.py install
