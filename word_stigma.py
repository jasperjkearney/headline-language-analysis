import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

word_scores = {}  # Keys are words, values are lists of all scores of headlines that the word has appeared in.

for headline in headline_data.unique_headlines():
    words = headline.words()
    headline_score = headline.vader_sentiment_scores['compound']
    for word in words:
        if word not in word_scores:
            word_scores[word] = [headline_score]
        else:
            word_scores[word].append(headline_score)

for w, s in word_scores.items():
    if len(s) > 10:  # If the word has appeared in more than 10 different headlines
        word_scores[w] = sum(s)/len(s)  # Calculate the average score of the headlines that it has appeared in.
    else:
        word_scores[w] = 0

word_scores = sorted(word_scores.items(), key=lambda i: i[1])

most_negative = word_scores[:10]
most_positive = word_scores[-10:][::-1]

for pos, neg in zip(most_negative, most_positive):
    print('{} & {:.3f} & {} & {:.3f} \\\\'.format(*pos, *neg))

