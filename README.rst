Web Scraping of Election and Football Files from NRW
===================================================

Introduction
------------

This project deals with the web scraping of amateur football and election data from Germany. The project is meant to provide the data for a subsequent analysis of the effect of ethnic conflict in amateur football on subsequent election results. 

In a first step both data are scraped from [fupa.net]_ and [wahlen.votemanager.de]_ respectively. The election dataset consists of election results by election office (~1,000 eligible voters), while the football dataset consists of individual games, including percentage data on the ethnic composition of each team and a measure of violence (sum of red and yellow cards per team). In a next step  game data are merged on election offices by postal and year data. For those matches time and geodata distance measures are computed. Observations are dropped when they lie outside a prespecified threshold, the remaining data are grouped by election office id and election. The final dataset is a panel indexed by election office and election with a meaned measure of ethnic composition and violence of time and geographic close football games.


Background
----------
There exists a large literature on both ethnic conflict and 
While there are a lot of papers analyzing the realtionship between migration and right-wing voting behaviour my framework relies on interaction between minorities and natives on the football court. The project builds on the idea of context dependenc in ethnic conflicts as described by Bordalo et al. 2016, i.e., that the stereotype of a target group depends on the characteristics of the reference group it is compared to. In this context decision makers overweight a group’s most distinctive characteristics compared to othes, when making predictions (stereotypes) about a group. 

This argument is in line with Glaeser 2005, who argues that the transition from from individual to group hatred requires two leaps. Other members of the victim’s group must both identify with the victim and must decide that all members of the aggressor’s group are guilty of the crime or are at least dangerous. My framework allows me to explicitly tests this hypothesis.


Installation
------------

To play with the project, clone the repository to your disk with

.. code-block:: bash

    $ git clone https://github.com/mmaeh/Term-Paper-Eff.-Programming-Maehr/

After that create an environment with ``conda`` and activate it by running

.. code-block:: bash

    $ conda env create -n sp -f environment.yml
    $ activate sp


Then, run the following two commands to replicate the results.

.. code-block:: bash

    $ python waf.py configure distclean
    $ python waf.py build


References
----------

.. [ELECTION] https://wahlen.votemanager.de/
.. [FOOTBALL] https://www.fupa.net/
