import pickle
import datetime
import matplotlib.pyplot as plt

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

WORD = 'trump'

# Create plot data:
first = min(headline_data.datetimes)
last = max(headline_data.datetimes)
step = datetime.timedelta(1)
x = [first + step*x for x in range(((last-first)//step)+1)]

y_data = []

for day in x:
    hd = headline_data.datetime_range(day-step, day)
    day_words = hd.all_words(min_word_length=len(WORD))
    n = len(hd.headlines)
    y_data.append(100 * day_words.count(WORD) / n)

# Begin plotting:
fig, ax = plt.subplots(figsize=[6.5, 3.5])

ax.plot(range(len(x)), y_data, linewidth=0.5, marker='.', ms=2)
ax.set_xlim(0, len(x))

# Plot and label vertical lines representing election and inauguration dates:
def plot_vert_line(date, label):
    x_pos = (date - first.date()) / step
    ax.axvline(x=x_pos, color='grey', linewidth=1)
    ax.text(x_pos+2, 1, label, rotation='vertical', va='bottom', style='italic')

inaug_date = datetime.date(2017, 1, 20)
election_date = datetime.date(2016, 11, 8)
plot_vert_line(inaug_date, 'Inauguration')
plot_vert_line(election_date, 'Election')

# Add labels for earliest date, latest date, and 1st date of each month:
x_labels, ticks = zip(*[(dt.strftime("%d/%m/%y"), i) for i, dt in enumerate(x)
                        if i == 0 or i == len(x)-1 or dt.day == 1])
ax.set_xticks(ticks)
ax.set_xticklabels(x_labels)
fig.autofmt_xdate()
ax.set_ylim([0, 70])
ax.set_ylabel('Proportion of unique headlines containing. [\%]')
ax.grid(True, axis='y')

fig.savefig('./output/trump_frequency_vs_time.pgf')
plt.show()

