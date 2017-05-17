import matplotlib.pyplot as plt
import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

# Generate plot data:
plot_data = {}  # Dictionary to store each organisation's average headline update time.

for org in headline_data.organisations:
    org_headline_data = headline_data.org_headlines(org)
    plot_data[org] = len(list(org_headline_data)) / len(list(org_headline_data.unique_headlines()))

plot_data = sorted(plot_data.items(), key=lambda i: i[1])

# Begin plotting:
y_labels, x_values = zip(*plot_data)
fig, ax = plt.subplots()

ax.barh(range(len(x_values)), x_values, edgecolor='black')

ax.set_yticks(range(len(x_values)))
ax.set_yticklabels(y_labels)
ax.set_xlim([0, int(max(x_values)+1)])
ax.set_xticks(range(int(max(x_values)+2)))
ax.set_xlabel('Average time between headline updates [hours]')
ax.grid(True, axis='x')

fig.savefig('./output/update_time_vs_organisation.pgf')
plt.show()
