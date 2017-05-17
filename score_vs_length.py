import matplotlib.pyplot as plt
import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))
headline_data = headline_data.unique_headlines()

# Create x and y data
x = [len(headline.words()) for headline in headline_data]
y = [headline.vader_sentiment_scores['compound'] for headline in headline_data]

fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [5, 2]})

# Scatter plot of sentiment score vs headline length:
ax1.scatter(x, y, marker='.', s=2)
ax1.set_xticks(range(0, max(x)+1, 5))
ax1.set_xticks(range(max(x)+1), minor=True)
ax1.set_yticks([i/10 for i in range(-10, 11, 2)])
ax1.axis([0, 50, -1, 1])
ax1.grid()
ax1.set_ylabel('VADER Sentiment Score (compound)')

# Histogram of headline length distribution
ax2.hist(x, max(x), range=(0.5, max(x)+0.5), color='orange', edgecolor='black')
ax2.grid()
ax2.set_yticks(range(0, 2000, 500))
ax2.set_xlabel('Headline length (words)')
ax2.set_ylabel('Frequency')

fig.savefig('./output/score_vs_length.pgf')
plt.show()

