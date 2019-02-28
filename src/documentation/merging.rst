.. _merging_process:
****************
Merging Process
****************

Merging
========

After the scraping of both election and football data is finished, the latter are merged on the former according to geographical and time measures. The process is roughly as follows:

1. Merge games on election offices and election by postal code and year
2. Compute for merged observations two measures
	a. geographic distance between election office and home arena in kilomtres from longitude and latitude data
	b. time distance in days from election and game date
3. Only keep observations for which 
	a. geogrpahic distance between election office and home arena is below 20km
	b. games dates no longer back than 14 days from election date
4. Group remaining observation by election office name and election

The corresponding code can be found in *src.data_management.final_merge.py*. Especially 

.. automodule:: src.data_management.merge_elections_games
    :members: 
