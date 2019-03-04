import csv
import glob
import pandas as pd
from unidecode import unidecode
from urllib.request import urlretrieve
from bld.project_paths import project_paths_join as ppj


def combine_voting_files(colnames_list):
    '''
    Combines all voting CSV files into a single CSV file by 
    using a predefined list of all occurring columns.
    '''

    # All downloaded files.
    inputs = [i for i in glob.glob(
        ppj('OUT_DATA_ELEC_CSV', '*.csv'))]

    # Write all csv files line by line to new combined csv file.
    with open(ppj('OUT_DATA_ELEC', 'elections_combined.csv'), 'w', newline='') as file_out:
        writer = csv.DictWriter(file_out, fieldnames=colnames_list)
        writer.writeheader()  # Headers.
        for filename in inputs:  # Loop through single files.
            with open(ppj('OUT_DATA_ELEC_CSV', filename), 'r', newline='') as file_in:
                reader = csv.DictReader(file_in)
                for line in reader:
                    writer.writerow(line)  # Write line by line.


def expand_voting_files(elec_master_df):
    '''
    Downloads all CSV files from the corresponding download url. 
    Each file is expanded by columns containing ID, municipality 
    name, voting level, and state information. Further, a list 
    containing all occurring column names is created.
    '''

    # List to store all column names.
    colnames_list = ['']

    # Loop through download urls.
    dwnld_url_list = elec_master_df['dwnld_url'].tolist()
    for i, export_url in enumerate(dwnld_url_list):

        # Create file name form election ID.
        file_name = elec_master_df.loc[i, 'elec_id']
        # Download file to separate folder.
        urlretrieve(export_url, ppj(
            'OUT_DATA_ELEC_CSV', '{}.csv'.format(file_name)))

        # Read in downloaded file.
        temp_df = pd.read_csv(
            ppj('OUT_DATA_ELEC_CSV', '{}.csv'.format(file_name)), sep=';')

        # Get column names to ASCI.
        temp_df.columns = [unidecode(x).lower() for x in temp_df.columns]
        temp_df.rename(columns={'name': 'elec_off_name'}, inplace=True)

        # Expand election results with election information.
        temp_df['elec_id'] = elec_master_df.loc[i, 'elec_id']
        temp_df['mun_clearname'] = elec_master_df.loc[i, 'mun_clearname']
        temp_df['state'] = elec_master_df.loc[i, 'state']
        temp_df['elec_year'] = elec_master_df.loc[i, 'elec_year']
        temp_df['elec_date'] = elec_master_df.loc[i, 'elec_date']

        # Get columns of temp_df and append those to overall columns list.
        temp_columns = list(temp_df)
        for columns in temp_columns:
            if columns not in colnames_list:
                colnames_list.append(columns)

        # Overwrite original csv file.
        temp_df.to_csv(
            ppj('OUT_DATA_ELEC_CSV', '{}.csv'.format(file_name)), index=False)

    # Create .txt file to indicate finshing of download process.
    open(ppj('OUT_DATA_ELEC_CSV', 'election_dwnld_finished.txt'), 'a').close()

    return colnames_list


def main():
    # Read in dataframe.
    elec_master_df = pd.read_csv(ppj('OUT_DATA_ELEC', 'election_id_data.csv'))

    # Download .csv files and get unique column names.
    colnames_list = expand_voting_files(elec_master_df)

    # Combine all csv files and save as csv.
    combine_voting_files(colnames_list)


if __name__ == '__main__':
    main()
