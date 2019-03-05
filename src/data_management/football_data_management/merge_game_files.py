"""Combine games on matchday level to combined file."""

import csv
import glob
import pandas as pd

from bld.project_paths import project_paths_join as ppj


def get_unique_colnames(inputs):
    """
    Returns a list containing all unique column names across all CSV files
    specified in *inputs*.
    """

    # Get list of all column names.
    colnames = []
    for file in inputs:
        with open(ppj('OUT_DATA_FOOTBALL_CSV', file), 'r', newline='') as f_in:
            reader = csv.reader(f_in)
            headers = next(reader)  # Get header.
            for h in headers:
                if h not in colnames:
                    colnames.append(h)  # Append to list.

    return colnames


def merge_csv_files(colnames, inputs):
    """
    Merges CSV files specified in *inputs* according to unique column
    names given in *colnames*.
    """

    # Merge CSV files on columns-names list.
    with open(ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'), 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=colnames)
        writer.writeheader()  # Headers.
        for file in inputs:
            with open(ppj('OUT_DATA_FOOTBALL_CSV', file), 'r', newline='', encoding='utf-8') as f_in:
                reader = csv.DictReader(f_in)  # Use column names from list.
                for line in reader:
                    try:
                        writer.writerow(line)  # Write line by line.
                    except UnicodeEncodeError:
                        pass
                        # Encode in case of unicode error.
                        # line = {key: val.encode('utf-8') for key, val in line.items()}
                        # writer.writerow(line)


def main():
    # All matchday-game CSV files.
    inputs = [i for i in glob.glob(ppj('OUT_DATA_FOOTBALL_CSV', '*.csv'))]

    # Get list of all column names and merge CSV files.
    colnames = get_unique_colnames(inputs)
    merge_csv_files(colnames, inputs)

    # Read combined file.
    game_df = pd.read_csv(
        ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'), dtype=str, encoding='latin-1')

    # Define data types.
    float_keys = ['_card_clr', 'card_red', 'card_yllw']
    float_clmns = [col for col in game_df if any(x in col for x in float_keys)]
    for col in float_clmns:
        game_df[col] = game_df[col].astype(float)

    # Drop duplicates.
    game_df.drop_duplicates(
        game_df.columns.difference(['mtchday_id']), inplace=True)

    # Save as csv.
    game_df.to_csv(ppj('OUT_DATA_FOOTBALL', 'games_combined.csv'), index=False)

if __name__ == '__main__':
    main()
