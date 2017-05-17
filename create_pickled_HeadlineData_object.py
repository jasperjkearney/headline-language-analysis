import pickle

from HeadlineData import HeadlineData

# Create headline data object using the headline data file.
headline_data_file = 'storing-headlines/headline_data.csv'
headline_data = HeadlineData.from_file(headline_data_file)

# Pickle the HeadlineData object, save in new file.
pickle.dump(headline_data, open('headline_data.p', 'wb'))
