Web Scraping of Election and Football Files from NRW
===================================================

Introduction
------------

This project deals with the web scraping of amateur football and election data
from Germany. The project is meant to provide the data for a subsequent analysis
of the effect of ethnic conflict in amateur football on election results. 

In a first step both data are scraped from [ELECTION]_ and [FOOTBALL]_. In a next 
step both data are combined using time and geodata distance measures.


Background
----------


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
