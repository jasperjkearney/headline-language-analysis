from wordcloud import WordCloud
import pickle

# Create HeadlineData object from pickled scored headline data file:
headline_data = pickle.load(open('headline_data.p', 'rb'))

# Create list of words from all unique headlines.
words = headline_data.unique_headlines().all_words(min_word_length=5)

# Word cloud parameters:
params = {'width'            : 800,
          'height'           : 600,
          'colormap'         : 'Vega10',
          'collocations'     : False,
          'normalize_plurals': False,
          'regexp'           : r'\b[^\s]+\b',
          'background_color' : 'white'}

# Generate and save a word cloud image.
wordcloud = WordCloud(**params).generate(' '.join(words))
wordcloud.to_file('output/word_cloud.png')

# A word cloud can also be created for a specific news organisation:
'''
import random; org = random.choice(headline_data.organisations)
org_headline_data = headline_data.org_headlines(org)
words = org_headline_data.unique_headlines().all_words(min_word_length=5)

org_wordcloud = WordCloud(**params).generate(' '.join(words))
wordcloud.to_file('output/{}_word_cloud.png'.format(org))
'''
