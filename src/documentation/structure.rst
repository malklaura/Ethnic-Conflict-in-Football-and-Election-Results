.. _project_structure:

*****************
Project Structure
*****************

General Structure
==================

The logic of this project works according to the following hierarchic structure:

1. Election data management
    a. Determination of scrapable municipalties
    b. Scrape election information and download url of election results
    c. Download election CSV files and combine to one CSV file
    d. Get geodata for each election office in combined CSV file
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

Project paths
=============

Waf makes it easy to proceed in a step-wise manner by letting the user distribute wscript files across a directory hierarchy. When those functions are called, they will descend into a subfolder *src*, look for a file called wscript and invoke the build function defined therein. Within this project a variety of project paths are defined in the top-level wscript files. In case you want to modify the project and require different paths adjust them in the top-level wscript file.

The following is taken from the top-level wscript file. Modify any project-wide path settings there.

.. literalinclude:: ../../wscript
    :start-after: out = "bld"
    :end-before:     # Convert the directories into Waf nodes

As should be evident from the similarity of the names, the paths follow the steps of the analysis in the :file:`src` directory:

1. **data_management** → **OUT_DATA**
    a. **election_data_management** → **OUT_DATA_ELEC**, **OUT_DATA_ELEC_CSV**
    b. **football_data_management** → **OUT_DATA_FOOTBALL**, **OUT_DATA_FOOTBALL_CSV**
2. **analysis** → **OUT_FIGURES**

These will re-appear in automatically generated header files by calling the ``write_project_paths`` task generator.

By default, these header files are generated in the top-level build directory, i.e. ``bld``. The Python version defines a dictionary ``project_paths`` and a couple of convencience functions documented below. You can access these by adding a line::

    from bld.project_paths import XXX

at the top of you Python-scripts. Here is the documentation of the module:

    **bld.project_paths**

    .. automodule:: bld.project_paths
        :members: