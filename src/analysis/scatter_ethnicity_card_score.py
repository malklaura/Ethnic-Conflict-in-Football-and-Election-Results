import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from bld.project_paths import project_paths_join as ppj


def bin_scatter_nat_card_score(df, team, nationality, bins):
    # Get nationality and card score values.
    perc_national = df["{0}_{1}_perc".format(team, nationality)]
    card_score = df["{}_card_yllw".format(
        team)] + df["{}_card_red".format(team)]

    # Plot binned scatter of nationality in a game vs. card score.
    bin_means, bin_edges, binnumber = stats.binned_statistic(
        perc_national, card_score, statistic='mean', bins=bins)

    plt.figure()
    plt.plot(perc_national, card_score, 'b.', label='raw data')
    plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:],
               colors='g', lw=5, label='binned statistic of data')
    plt.xlabel("Card score")
    plt.ylabel("Percentage of {} in {} team".format(nationality, team))
    plt.legend()

    # Save figure.
    mp.savefig(ppj("OUT_FIGURES",
                   "scatter_{}_perc_{}_card_score.png".format(team, nationality)))


if __name__ == '__main__':

    # Read game data.
    election_df = pd.read_csv(ppj("OUT_DATA_FOOTBALL", "games_final.csv"))

    # Loop through teams and nationality.
    for team in ["home", "away"]:
        for national in ["ger", "tur", "nonger"]:
            bin_scatter_nat_card_score(election_df, team, nationality, bins=20)
