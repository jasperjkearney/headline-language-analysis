import datetime
import csv
import functools
import nltk.tokenize.regexp
from nltk.sentiment.vader import SentimentIntensityAnalyzer


@functools.lru_cache()
def vader_sentiment_scores(s):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(s)


class Headline:

    def __init__(self, headline, organisation, datetime):
        self.headline_string = headline
        self.organisation = organisation
        self.datetime = datetime

        self.vader_sentiment_scores = vader_sentiment_scores(self.headline_string)

    def __str__(self):
        return '\n'.join([self.headline_string,
                          ' -'+self.organisation,
                          str(self.datetime.date())])

    def __repr__(self):
        return 'Headline(\'{}\', \'{}\', {})'.format(self.headline_string,
                                                     self.organisation,
                                                     repr(self.datetime))

    def words(self, min_word_length=0):
        """Returns a list of words in the headline string longer than the min word length, converts to lowercase"""

        word_tokenizer = nltk.RegexpTokenizer(r'\b[^\s]+\b')
        headline_string = self.headline_string.lower().replace("’", "'")
        return [word for word in word_tokenizer.tokenize(headline_string) if len(word) >= min_word_length]


class HeadlineData:

    def __init__(self, headlines):
        self.headlines = headlines  # The headlines attribute is a list of Headline objects.
        self.organisations = list(set(headline.organisation for headline in self))
        self.datetimes = list(set(headline.datetime for headline in self))

    def __iter__(self):
        return iter(self.headlines)

    def all_words(self, min_word_length=0):
        """Returns a list of all words from all headlines longer than the
        min_word_length, converted to lowercase"""
        return [word for headline in self.headlines for word in
                headline.words(min_word_length=min_word_length)]

    def unique_headlines(self):
        """Returns a HeadlineData object containing all headlines with unique headline strings, earlier
           headlines are prioritised"""

        all_headlines = sorted(self.headlines, key=lambda x: x.datetime, reverse=True)
        unique_headlines = list(dict((headline.headline_string, headline)
                                     for headline in all_headlines).values())

        return HeadlineData(unique_headlines)

    def org_headlines(self, org):
        """Returns a HeadlineData object containing headlines that match the given news organisation name string."""

        if org in self.organisations:
            return HeadlineData([headline for headline in self.headlines if
                                 headline.organisation == org])

        raise ValueError("Organisation '{}' not found.".format(org))

    def datetime_range(self, start_datetime, end_datetime):
        """Returns a HeadlineData object containing headlines between the 2 given datetime objects inclusive. """

        if isinstance(start_datetime, datetime.datetime) and isinstance(end_datetime, datetime.datetime):
            return HeadlineData([headline for headline in self.headlines if
                                 start_datetime <= headline.datetime <= end_datetime])

        raise ValueError("Expected 2 datetime objects.")

    @classmethod
    def from_file(cls, path):

        with open(path) as headline_data_file:
            reader = csv.reader(headline_data_file)

            # Store the unprocessed data from the csv file in a list.
            raw_data = [row for row in reader]

        # Remove and store the names of the news organisations from the raw_data.
        organisations = raw_data.pop(0)[1:]
        organisations = [o for o in organisations if o]

        # A list of Headline objects is used to store the headline data.
        headlines = []

        # Iterate over the remaining rows, adding Headline objects to the list.
        for row in raw_data:
            # Store the datetime as a datetime object.
            # The time is not stored to a smaller fidelity than the closest hour.
            datetime_string = row.pop(0)[:13]  # Slice string to get 'Year-Month-Day Hour'
            datetime_format = '%Y-%m-%d %H'
            row_datetime = datetime.datetime.strptime(datetime_string, datetime_format)

            # Store all valid headlines in a list of Headline objects:
            error_prefix = '!ERROR! -'

            for org, headline in zip(organisations, row):
                if headline and error_prefix not in headline:
                    headlines.append(Headline(headline, org, row_datetime))

        return cls(headlines)
