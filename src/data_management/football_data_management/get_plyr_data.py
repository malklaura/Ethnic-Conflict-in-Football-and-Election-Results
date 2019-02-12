from bs4 import BeautifulSoup
import certifi
import csv
import datetime
import glob
import numpy as np
import pandas as pd
import re 
import urllib3
from bld.project_paths import project_paths_join as ppj


df_list = glob.glob('df_**.csv')

# First determine the field names from the top line of each input file
# Comment 1 below
fieldnames = []
for filename in df_list:
  with open(filename, "r", newline="") as f_in:
    reader = csv.reader(f_in, delimiter = ";")
    headers = next(reader)
    for h in headers:
      if h not in fieldnames:
        fieldnames.append(h)

# Then copy the data
with open("merged_games_df.csv", "w", newline="") as f_out:   # Comment 2 below
  writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter = ";")
  writer.writeheader()
  for filename in df_list:
    with open(filename, "r", newline="") as f_in:
      reader = csv.DictReader(f_in, delimiter = ";")  # Uses the field names in this file
      for line in reader:
        # Comment 3 below
        writer.writerow(line)
   
# Read in newly merged dataset     
merged_df = pd.read_csv("merged_games_df.csv", sep = ";", encoding='cp1252')

filter_col = [col for col in merged_df if f'{col[0]}{col[-1]}'.lower() == 'hl'][1:]
filter_col = filter_col + [col for col in merged_df if f'{col[0]}{col[-1]}'.lower() == 'al'][1:]

unique_plyrs = []
for col in filter_col:
    unique_plyrs = merged_df[col].unique_plyrs().tolist() + unique_plyrs
    
unique_plyrs = list(set(unique_plyrs))[1:]

# create players dataset
http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

plyrs_df = pd.DataFrame(columns = ["href", "age", "nat"])
plyrs_df = pd.DataFrame()

for i, url in enumerate(unique_plyrs):
    plyrs_df.at[i, "href"] = url
    
    my_url = url
    r = http.request("GET", my_url)
    soup = BeautifulSoup(r.data, 'lxml')
    
    info_soup = soup.find("td", {"class":"stammdaten"})
    
    try:
        if "Geburtsdatum" in info_soup.table.find_all("tr")[1].text:
            birthday = info_soup.table.find_all("tr")[1].text
            plyrs_df.at[i, "age"] = re.search(r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyrs_df.at[i, "nat"] = info_soup.table.find_all("tr")[2].img["title"]
        elif "Geburtsdatum" in info_soup.table.find_all("tr")[2].text:
            birthday = info_soup.table.find_all("tr")[2].text
            plyrs_df.at[i, "age"] = re.search(r'\d{2}.\d{2}.\d{4}', birthday).group(0)
            plyrs_df.at[i, "nat"] = info_soup.table.find_all("tr")[3].img["title"]
        else:
            plyrs_df.at[i, "age"] = np.nan
            plyrs_df.at[i, "nat"] = np.nan
                  
    except:
        plyrs_df.at[i, "age"] = np.nan
        plyrs_df.at[i, "nat"] = np.nan
     
    try:    
        stations_soup = soup.find("table", {"class": "stationen content_table_std"})
        stations = stations_soup.find_all("b")
        saisons = stations_soup.find_all("td", {"class": "saison"})
        leagues = stations_soup.find_all("div", {"class": "liga_zusatz"})
        
        for j, station in enumerate(stations):
            plyrs_df.at[i, "station_verein_" + str(j)] = station.text
            plyrs_df.at[i, "saison_verein_" + str(j)] = saisons[j].span.text
            plyrs_df.at[i, "league_verein_" + str(j)] = leagues[j].a.text
    
    except:
        pass
