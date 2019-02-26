import csv
import glob
import re
import pandas as pd
from unidecode import unidecode
from urllib.request import urlretrieve
from bld.project_paths import project_paths_join as ppj


def combine_voting_files(colnames_list):
    """This function combines all voting csv files into a single
    csv file by using a predefined list of all occuring columns."""

    inputs = [i for i in glob.glob(
        ppj("OUT_DATA_ELEC_CSV", "*.{}".format('csv')))]

    # Write all csv files line by line to new combined csv file.
    with open(ppj("OUT_DATA_ELEC", "election_combined.csv"), "w", newline="") as file_out:
        writer = csv.DictWriter(file_out, fieldnames=colnames_list)
        writer.writeheader()
        for filename in inputs:
            with open(ppj("OUT_DATA_ELEC_CSV", filename), "r", newline="") as file_in:
                reader = csv.DictReader(file_in)
                for line in reader:
                    writer.writerow(line)


def expand_voting_files(elec_master_df):
    """This function downloads all csv files from the corresponding
    export url. Each file is expanded by columns containing the ID, 
    municipality name, voting level and state. Further a list containing 
    all occuring column names is created."""

    dwnld_url_list = elec_master_df["dwnld_url"].tolist()

    colnames_list = [""]
    for i, export_url in enumerate(dwnld_url_list):
        # Download respective csv file and store it in seperate folder
        # according to previously defined id name.
        file_name = elec_master_df.loc[i, "elec_id"]
        urlretrieve(export_url, ppj(
            "OUT_DATA_ELEC_CSV", '{}.csv'.format(file_name)))

        # Merge identifying variables to newly downloaded csv files.
        temp_df = pd.read_csv(
            ppj("OUT_DATA_ELEC_CSV", "{}.csv".format(file_name)), sep=";")

        # Get column names to ASCI.
        temp_df.columns = [unidecode(x).lower() for x in temp_df.columns]
        temp_df.rename(columns={"name": "elec_off_name"}, inplace=True)

        # Expand election data.
        temp_df["elec_id"] = elec_master_df.loc[i, "elec_id"]
        temp_df["mun_clearname"] = elec_master_df.loc[i, "mun_clearname"]
        temp_df["state"] = elec_master_df.loc[i, "state"]
        temp_df["elec_year"] = elec_master_df.loc[i, "elec_year"]
        temp_df["elec_date"] = elec_master_df.loc[i, "elec_date"]

        # Overwrite original csv file with with expanded columns.
        temp_df.to_csv(
            ppj("OUT_DATA_ELEC_CSV", '{}.csv'.format(file_name)), index=False)

        # Get columns of temp_df and append those to overall columns list.
        temp_columns = list(temp_df)
        for columns in temp_columns:
            if columns not in colnames_list:
                colnames_list.append(columns)

    # Create .txt file to indicate finshing of download process.
    open(ppj("OUT_DATA_ELEC_CSV", "election_dwnld_finished.txt"), 'a').close()

    return colnames_list

if __name__ == '__main__':
    # Read in dataframe.
    elec_master_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_id_data.csv"))

    # Download .csv files and get unique column names.
    colnames_list = expand_voting_files(elec_master_df)

    # Combine all csv files and save as csv.
    combine_voting_files(colnames_list)
