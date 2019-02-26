import re
import pandas as pd
from unidecode import unidecode
from bld.project_paths import project_paths_join as ppj


def main():
    # Read in relevant files.
    elec_mun_df = pd.read_csv(ppj("OUT_DATA_ELEC", "scrapable_mun.csv"))
    elec_url_df = pd.read_csv(ppj("OUT_DATA_ELEC", "election_data.csv"))

    # Merge files containing election and municipal information.
    elec_df = pd.merge(elec_url_df, elec_mun_df,  how='left', on='mun_url')

    # Create clearname for each municiplaity.
    elec_df["mun_clearname"] = elec_df["mun_name"].apply(
        lambda x: re.sub('Stadt |Gemeinde ', '', x))

    # Create election ID from clearname, election abbreviation and date.
    elec_df["elec_id"] = elec_df["mun_clearname"] + "_" + \
        elec_df["abbrev"] + "_" + elec_df["elec_date"]
    elec_df["elec_id"] = [unidecode(x) for x in elec_df["elec_id"]]
    elec_df["elec_id"] = elec_df["elec_id"].replace("[^a-zA-Z0-9_]+", "", regex=True)

    # Split date into day, month and year and store in separate columns.
    date_clmns = '(?P<elec_day>[^.]+).(?P<elec_month>[^.]+).(?P<elec_year>[^.]+)'
    elec_df = pd.concat(
        [elec_df, elec_df["elec_date"].str.extract(date_clmns).astype(int)], axis=1)

    # Save as csv.
    elec_df.to_csv(ppj("OUT_DATA_ELEC", "election_id_data.csv"), index=False)

if __name__ == '__main__':
    main()
