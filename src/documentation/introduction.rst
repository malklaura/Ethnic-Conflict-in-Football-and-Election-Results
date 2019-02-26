.. _introduction:


************
Introduction
************

This project deals with the web scraping of amateur football and election data from Germany. The project is meant to provide the data basis for a subsequent analysis of the effect of ethnic conflict in amateur football on preceding election results.

In a first step both data are scraped from [ELECTION] and [FOOTBALL]. In a next step both data are combined using time and geodata distance measures. The final file in as panel containing election results and a measure of ehtnicity and violence constructed of all football games within a certain geographical and time distance for each election office in NRW across the last ten years.

.. _getting_started:

Getting started
===============

**This assumes you have completed the steps in the** `README.md file <https://github.com/hmgaudecker/econ-project-templates/>`_ **and everything worked.**

The logic of this project works by step of the analysis: 

1. Data management
1a. Election data management
1aa. Scraping of election download url
1ab. Get geodata for each election office
1b. Football data management
1ba. Scrape football game data
1bb. Scrape player ethnicity
1bc. Get geodata for each football club
2. Merge election and football files
3. Visualisation and results formatting
4. Research paper and presentations. 

Once you have done that, move your source data to **src/original_data/** and start filling up the actual steps of the project workflow (data management, analysis, final steps, paper). All you should need to worry about is to call the correct task generators in the wscript files. Always specify the actions in the wscript that lives in the same directory as your main source file. Make sure you understand how the paths work in Waf and how to use the auto-generated files in the language you are using particular language (see the section :ref:`project_paths` below).


.. _project_paths:

Project paths
=============

A variety of project paths are defined in the top-level wscript file. These are exported to header files in other languages. So in case you require different paths (e.g. if you have many different datasets, you may want to have one path to each of them), adjust them in the top-level wscript file.

The following is taken from the top-level wscript file. Modify any project-wide path settings there.

.. literalinclude:: ../../wscript
    :start-after: out = "bld"
    :end-before:     # Convert the directories into Waf nodes


As should be evident from the similarity of the names, the paths follow the steps of the analysis in the :file:`src` directory:

    1. **data_management** → **OUT_DATA**
    1a. **election_data_management** → **OUT_DATA_ELEC** 
    1b. **football_data_management** → **OUT_DATA_FOOTBALL**
    2. **analysis** → **OUT_ANALYSIS**
    3. **final** → **OUT_FINAL**, **OUT_FIGURES**, **OUT_TABLES**

These will re-appear in automatically generated header files by calling the ``write_project_paths`` task generator (just use an output file with the correct extension for the language you need -- ``.py``, ``.r``, ``.m``, ``.do``)

By default, these header files are generated in the top-level build directory, i.e. ``bld``. The Python version defines a dictionary ``project_paths`` and a couple of convencience functions documented below. You can access these by adding a line::

    from bld.project_paths import XXX

at the top of you Python-scripts. Here is the documentation of the module:

    **bld.project_paths**

    .. automodule:: bld.project_paths
        :members:
