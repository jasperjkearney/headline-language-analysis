import pickle
import datetime
import matplotlib.pyplot as plt

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

WORDS = ['trump', 'clinton', 'obama', 'russia', 'china']

# Create plot data:
first = min(headline_data.datetimes)
last = max(headline_data.datetimes)
x_step = datetime.timedelta(1)
x = [first + x_step*x for x in range(((last-first)//x_step)+1)]

y_data = dict((word, []) for word in WORDS)
MIN_WORD_LENGTH = len(min(WORDS, key=lambda x: len(x)))
for day in x:
    hd = headline_data.datetime_range(day-x_step, day)
    day_words = hd.all_words(min_word_length=MIN_WORD_LENGTH)
    n = len(hd.headlines)
    for word in y_data.keys():
        y_data[word].append(100 * day_words.count(word) / n)

# Begin plotting:
fig, axes = plt.subplots(len(WORDS), figsize=[5, 4.5])
axes = dict((word, ax) for word, ax in zip(WORDS, axes))


def plot_vert_line(date):
    x_pos = (date - x[0].date()) // x_step
    ax.axvline(x=x_pos, color='gray', alpha=0.5)

inaug_date = datetime.date(2017, 1, 20)
election_date = datetime.date(2016, 11, 8)

for word in WORDS:
    ax = axes[word]

    ax.plot(range(len(x)), y_data[word], linewidth=1.5)

    plot_vert_line(inaug_date)
    plot_vert_line(election_date)

    ax.set_xlim(0, len(x))
    ax.set_ylim([0, 100])

    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([0, 50, 100])
    ax.set_yticklabels([])

    ax.set_title(word)

ax = axes[WORDS[0]]
ax.set_yticklabels(map(str, ax.get_yticks()))

wiretap_accusation_date = datetime.date(2017, 3, 5)
x_pos = (wiretap_accusation_date - x[0].date()) // x_step
axes['obama'].annotate('1.',
                       xy=(x_pos, y_data['obama'][x_pos]),
                       xytext=(x_pos+10, y_data['obama'][x_pos]+15),
                       arrowprops=dict(arrowstyle='-'))

fig.tight_layout()

fig.savefig('./output/word_frequency_vs_time.pgf')
plt.show()
