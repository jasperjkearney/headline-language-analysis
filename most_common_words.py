import pickle
from collections import Counter

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))
headline_data = headline_data.unique_headlines()

# Use Counter object to sum word occurrences:
word_counter = Counter(headline_data.all_words(min_word_length=5))

# Normalise data to get proportion of headlines that words occur in:
num_of_headlines = len(list(headline_data))
for word in word_counter.keys():
    word_counter[word] /= num_of_headlines

for i, (word, count) in enumerate(word_counter.most_common(10)):
    print('{}. & {} & {:.3f}\\% \\\\'.format(i+1, word, count*100))
