import pytest

# Import headline data object located in processing-headlines directory.
import sys
import os.path
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/../'.format(script_directory))
from HeadlineData import Headline, HeadlineData

from datetime import datetime, timedelta

h1 = Headline("This is Headline 1", "Organisation 1", datetime.now())
h2 = Headline("Headline 2, abcde., 12345 @bcde", "Organisation 2",
              datetime.min)
h3 = Headline("This is Headline 3", "Organisation 3", datetime.max)
hd = HeadlineData([h1]*2 + [h2]*3 + [h3])

def test_Headline_words():
    assert h1.words(min_word_length=4) == ["this", "headline"]
    assert sorted(h2.words()) == sorted(["headline", "2", "abcde", "12345", "bcde"])

def test_HeadlineData_all_words():
    assert sorted(hd.all_words()) == sorted(h1.words()*2+h2.words()*3+h3.words())

def test_HeadlineData_organisations():
    assert sorted(hd.organisations) == sorted(["Organisation {}".format(str(i))
                                               for i in range(1, 4)])

def test_HeadlineData_unique_headlines():
    assert set(hd.unique_headlines()) == \
           set(HeadlineData([h1, h2, h3]))

def test_HeadlineData_org_headlines():
    assert hd.org_headlines("Organisation 1").headlines == [h1]*2
    with pytest.raises(Exception):
        x = hd.org_headlines("Fictional Organisation")

def test_HeadlineData_datetime_range():
    one_day = timedelta(days=1)
    start_date = datetime.now() - one_day
    end_date = datetime.now() + one_day

    assert hd.datetime_range(start_date, end_date).headlines == [h1]*2


