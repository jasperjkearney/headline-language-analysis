import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))
headline_data = headline_data.unique_headlines()

# Create list of scores for unique headlines:
x = [getattr(headline, 'vader_sentiment_scores')['compound'] for headline in headline_data]

# Plot histogram:
fig, ax = plt.subplots(figsize=(6, 3))
ax.hist(x, 41, range=(-1, 1), edgecolor='black')
ax.set_xlim([-1, 1])
ax.set_ylim([0, 5000])

# Add labels:
ax.set_xticks([i/10 for i in range(-10, 11, 5)])
ax.set_xlabel('VADER sentiment score (compound)')
ax.set_ylabel('Occurrences')
ax.grid(True, axis='y')

# Add shading to show positive and negative ranges, annotate with totals:
ax.add_patch(patches.Rectangle((-1, 0), 0.5, 5000, alpha=0.2, color='red'))
ax.add_patch(patches.Rectangle((0.5, 0), 0.5, 5000, alpha=0.2, color='green'))
total_neg = len([s for s in x if s <-0.5])
total_pos = len([s for s in x if s > 0.5])
total_neu = len(x) - total_neg - total_pos
ax.text(-0.95, 4300, 'Negative: {:.0f}\%'.format(100*total_neg/len(x)))
ax.text(0.55, 4300, 'Positive: {:.0f}\%'.format(100*total_pos/len(x)))
ax.text(-0.45, 4300, 'Neutral:  {:.0f}\%'.format(100*total_neu/len(x)))

# Add label to show amount of 0.0 scores:
total_zero_scores = len([s for s in x if s == 0])
ax.annotate('{:.0f}\% of scores\n({}) were 0.0'.format(100 * total_zero_scores / len(x), total_zero_scores),
            xy=(0, total_zero_scores),
            xytext=(0.05, 3200),
            arrowprops=dict(arrowstyle='-'))

fig.savefig('./output/score_distribution_plot.pgf')
plt.show()
