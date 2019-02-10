import re
import csv
import glob
import pandas as pd
from urllib.request import urlretrieve
from bld.project_paths import project_paths_join as ppj

municipality_longlat_df = pd.read_csv(
    ppj("OUT_DATA", "municipality_lt_df.csv"), encoding='cp1252')

votes_df = pd.read_csv(
    ppj("OUT_DATA", "votes_df.csv"), encoding='cp1252')

votes_df = pd.merge(votes_df, municipality_longlat_df,  how='left', left_on=[
                    'municipality_url'], right_on=['href'])

umlaute_dict = {"ä": "ae", "Ä": "Ae", "ö": "oe",
                "Ö": "Oe", "ü": "ue", "Ü": "Ue", "ß": "ss"}
votes_df.replace(umlaute_dict, regex=True, inplace=True)
votes_df["mun_clearname"] = votes_df["municipality"].apply(
    lambda x: re.sub('Stadt |Gemeinde ', '', x))
votes_df["ID"] = votes_df["mun_clearname"] + "_" + \
    votes_df["election_type"] + "_" + votes_df["election_date"]

export_urls = votes_df["export_url"].tolist()

columns_list = [""]
for i, export_url in enumerate(export_urls):
    urlretrieve(export_url, ppj(
        "OUT_CSV", '{}.csv'.format(votes_df.loc[i, "ID"])))
    temp_df = pd.read_csv(ppj("OUT_CSV", "{}.csv".format(
        votes_df.loc[i, "ID"])), encoding='cp1252', sep=";")
    temp_df["postal"] = votes_df.loc[i, "postal"]
    temp_df["ID"] = votes_df.loc[i, "ID"]
    temp_df["mun_clearname"] = votes_df.loc[i, "mun_clearname"]
    temp_df["mun_name"] = votes_df.loc[i, "municipality"]
    temp_df["voting_level"] = votes_df.loc[i, "voting_level"]
    temp_df["state"] = votes_df.loc[i, "state"]
    temp_df.to_csv(ppj("OUT_CSV", '{}.csv'.format(votes_df.loc[i, "ID"])))

    # Get columns of temp_df and append to overall columns list.
    temp_columns = list(temp_df)

    for columns in temp_columns:
        if columns not in columns_list:
            columns_list.append(columns)

# Load all csv files from csv voting folder.
input_files = [i for i in glob.glob(ppj("OUT_CSV", '*.{}'.format('csv')))]

# Combine files using columns lsit.
with open(ppj("OUT_DATA", "combined_votes.csv"), "w", newline="") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=columns_list)
    writer.writeheader()
    for filename in input_files:
        with open(ppj("OUT_CSV", filename), "r", newline="") as file_in:
            reader = csv.DictReader(file_in)
            for line in reader:
                writer.writerow(line)

comb_votes_df = pd.read_csv(ppj("OUT_DATA", "combined_votes.csv"))
comb_votes_df["Name"].replace(umlaute_dict, regex=True, inplace=True)
comb_votes_df["Name"] = comb_votes_df["Name"].apply(
    lambda x: re.sub(r'[^a-zA-Z\s]', u'', x, flags=re.UNICODE).lstrip())
comb_votes_df.to_csv(ppj("OUT_DATA", "combined_votes.csv"))


target_list = []
for file_name in votes_df["ID"].tolist():
    new_target = "ctx.path_to(ctx, 'OUT_DATA', {}.csv)".format(file_name)
    target_list.append(new_target)

target_list =",".join(target_list)