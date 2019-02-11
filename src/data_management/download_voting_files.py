import csv
import glob
import re
import pandas as pd
from urllib.request import urlretrieve
from bld.project_paths import project_paths_join as ppj


def combine_voting_files(colnames_list):
    """This function combines all voting csv files into a single
    csv file by using a predefined list of all occuring columns."""
    inputs = [i for i in glob.glob(ppj("OUT_DATA", "*.{}".format('csv')))]

    # Write all csv files line by line to the new combined csv file.
    with open(ppj("OUT_DATA", "election_combined.csv"), "w", newline="") as file_out:
        writer = csv.DictWriter(file_out, fieldnames=colnames_list)
        writer.writeheader()
        for filename in inputs:
            with open(filename, "r", newline="") as file_in:
                reader = csv.DictReader(file_in)
                for line in reader:
                    writer.writerow(line)

    out_csv = pd.read_csv(ppj("OUT_DATA_ELEC", "election_combined.csv"))
    out_csv["Name"].replace(umlaute_dict, regex=True, inplace=True)
    out_csv["Name"] = out_csv["Name"].apply(lambda x: re.sub(
        r'[^a-zA-Z\s]', u'', x, flags=re.UNICODE).lstrip())
    return out_csv


def expand_voting_files(votes_df):
    """This function downloads all csv files from the corresponding
    export url in the votes_df. Each file is expanded by columns
    containing the ID, municipality name, voting level and state.
    Further a list containing all occuring column names is created."""
    export_urls = votes_df["export_url"].tolist()

    colnames_list = [""]
    for i, export_url in enumerate(export_urls):
        urlretrieve(export_url, ppj(
            "OUT_DATA_ELEC_CSV", '{}.csv'.format(votes_df.loc[i, "ID"])))
        temp_df = pd.read_csv(ppj("OUT_DATA", "{}.csv".format(
            votes_df.loc[i, "ID"])), encoding='cp1252', sep=";")
        # poastal im missing here
        temp_df["ID"] = votes_df.loc[i, "ID"]
        temp_df["mun_name"] = votes_df.loc[i, "mun_clearname"]
        temp_df["voting_level"] = votes_df.loc[i, "voting_level"]
        temp_df["state"] = votes_df.loc[i, "state"]
        temp_df.to_csv(ppj("OUT_DATA_ELEC_CSV", '{}.csv'.format(votes_df.loc[i, "ID"])))

        # Get columns of temp_df and append to overall columns list.
        temp_columns = list(temp_df)

        for columns in colnames_list:
            if columns not in colnames_list:
                columns_list.append(columns)
    return colnames_list


if __name__ == '__main__':
    elec_master_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_master.csv"), encoding='cp1252')

    colnames_list = expand_voting_files(elec_master_df)

    # Load all csv files from csv voting folder.
    out_csv = combine_voting_files(colnames_list)

    out_csv.to_csv(ppj("OUT_DATA_ELEC", "election_combined.csv"))
