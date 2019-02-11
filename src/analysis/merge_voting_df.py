import pandas as pd


if __name__ == '__main__':
    municipality_df = pd.read_csv(
        ppj("OUT_DATA", "mun_df.csv"), encoding='cp1252')

    votes_df = pd.read_csv(
        ppj("OUT_DATA", "votes_df.csv"), encoding='cp1252')


    votes_df = pd.merge(votes_df, municipality_df,  how='left',
                        left_on=['municipality_url'], right_on=['href'])

    umlaute_dict = {"ä": "ae", "Ä": "Ae", "ö": "oe",
                    "Ö": "Oe", "ü": "ue", "Ü": "Ue", "ß": "ss"}

    votes_df.replace(umlaute_dict, regex=True, inplace=True)

    votes_df["mun_clearname"] = votes_df["municipality"].apply(
        lambda x: re.sub('Stadt |Gemeinde ', '', x))

    votes_df["ID"] = votes_df["mun_clearname"] + "_" + \
        votes_df["election_type"] + "_" + votes_df["election_date"]

    votes_df.to_csv(ppj("OUT_DATA", "combined_votes_df.csv"))