import pandas as 
import matplotlib.pyplot as plt

from scipy import stats
from bld.project_paths import project_paths_join as ppj

# Plot binned scatter of percentage of non germans in a game and the corresponding number of cards.
election_df = pd.read_csv(ppj("OUT_DATA_ELEC", "elections_final.csv"))

perc_nonger = election_df["home_other_perc"]
card_score = election_df["home_card_yllw"] + election_df["home_card_red"]**2
bin_means, bin_edges, binnumber = stats.binned_statistic(perc_nonger, card_score, statistic='mean', bins=20)

plt.figure()
plt.plot(perc_nonger, card_score, 'b.', label='raw data')
plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='g', lw=5, label='binned statistic of data')
plt.legend()

#election_df = pd.read_csv(ppj("OUT_FINAL", "scatter_ethn_cards.png"))
