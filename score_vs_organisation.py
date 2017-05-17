import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

plot_data = {}  # Dictionary to store each organisation's average compound VADER score 

for org in headline_data.organisations:
    unique_org_headlines = headline_data.org_headlines(org).unique_headlines()
    org_scores = [getattr(headline, 'vader_sentiment_scores')['compound'] for headline in unique_org_headlines]
    plot_data[org] = org_scores

# Sort the score data by mean compound VADER score:
plot_data = sorted(plot_data.items(), key=lambda i: sum(i[1]) / len(i[1]))

y_labels, x_values = zip(*plot_data)

fig, ax = plt.subplots()

medianprops = dict(linestyle='-', linewidth=1.5, label='Median')
meanprops = dict(linestyle='-', linewidth=1.5, label='Mean')

ax.boxplot(x_values,
           vert=False,
           whis='range',
           medianprops=medianprops,
           meanprops=meanprops,
           showmeans=True, meanline=True)

medianline = mlines.Line2D([], [], **medianprops)
meanline = mlines.Line2D([], [], **meanprops)

legend = ax.legend(handles=[medianline, meanline],
                   bbox_to_anchor=(0.6, 1), loc=2,
                   framealpha=1)

ax.set_yticks(range(1, len(x_values)+1))
ax.set_yticklabels(y_labels)
ax.set_xlim([-1, 1])
ax.set_xlabel('Average compound VADER sentiment score')
ax.grid(axis='x')

fig.savefig('./output/score_vs_organisation.pgf')
plt.show()
