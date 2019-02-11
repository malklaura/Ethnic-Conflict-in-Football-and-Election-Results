import pandas as pd
from bld.project_paths import project_paths_join as ppj

if __name__ == '__main__':
    elec_mun_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_mun.csv"), encoding='cp1252')

    elec_df = pd.read_csv(
        ppj("OUT_DATA_ELEC", "election_urls.csv"), encoding='cp1252')

    elec_master_df = pd.merge(elec_df, elec_mun_df,  how='left',
                        left_on=['mun_url'], right_on=['href'])

    umlaute_dict = {"ä": "ae", "Ä": "Ae", "ö": "oe",
                    "Ö": "Oe", "ü": "ue", "Ü": "Ue", "ß": "ss"}

    elec_master_df = elec_master_df.replace(umlaute_dict, regex=True, inplace=True)

    elec_master_df["mun_clearname"]=elec_master_df["mun"].apply(
        lambda x: re.sub('Stadt |Gemeinde ', '', x))

    elec_master_df["ID"]=elec_master_df["mun_clearname"] + "_" +
        votes_df["elec_type"] + "_" + votes_df["elec_date"]

    elec_master_df.to_csv(ppj("OUT_DATA_ELEC", "election_master.csv"))
