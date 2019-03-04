import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from bld.project_paths import project_paths_join as ppj


def bin_scatter_nat_card_score(df, team, nationality, bins):
    """
    Computes binned scatter plots of nationality vs. card score. The
    number of bins can be changed by the *bins* argument. *Team* has to 
    be one of 'home' or 'away'. *Nationality* arguments include *ger*, 
    *nonger* and *tur* for German, Non-German, and Turkish nationals,
    respectively.
    """

    # Card scroe as sum of yellow and red cards.
    df['card_score'] = df['{}_card_yllw'.format(
        team)] + df['{}_card_red'.format(team)]

    # Get bubble plot, indicating number of occurrences of nationality card
    # scroe combination.
    df['count'] = 1
    grouped_df = df.groupby(['{0}_{1}_perc'.format(
        team, nationality), 'card_score']).sum().reset_index()
    bubble_national = grouped_df["{0}_{1}_perc".format(team, nationality)]
    bubble_card_score = grouped_df['card_score']
    bubble_count = grouped_df['count']

    # Get binned nationality and card score values.
    perc_national = df["{0}_{1}_perc".format(team, nationality)].tolist()
    card_score = df['card_score'].fillna(0).tolist()

    bin_y, bin_edges, binnumber = stats.binned_statistic(
        perc_national, card_score, statistic='mean', bins=bins)
    bin_x = [np.mean([bin_edges[x + 1], bin_edges[x]])
             for x in range(len(bin_edges) - 1)]

    # Plot both information in one graph.
    fig = plt.figure()
    plt.scatter(bubble_national, bubble_card_score, bubble_count, alpha=0.4)
    plt.plot(bin_x, bin_y,  'r.', markersize=12, label='raw data')
    plt.ylabel("Card score {} team".format(team))
    plt.xlabel("Percentage of {} in {} team".format(nationality, team))

    # Save figure.
    fig.savefig(ppj("OUT_FIGURES",
                    "scatter_{}_perc_{}_card_score.png".format(team, nationality)))


def main():
    # Read game data.
    games_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "games_final.csv"))

    # Loop through teams and nationality.
    for team in ["home", "away"]:
        for national in ["ger", "tur", "nonger"]:
            bin_scatter_nat_card_score(games_df, team, national, bins=20)

if __name__ == '__main__':
    main()
