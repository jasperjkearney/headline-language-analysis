#!/usr/bin/env python3

import csv
import os.path
import urllib.request
import urllib.error
from datetime import datetime

from bs4 import BeautifulSoup

from initialise_results_file import initialise_results_file


def fetch_headline(url, headline_element_type, identifying_attribute, attribute_value):

    error_prefix = '!ERROR! -'

    # Try to get the html of the news site (setting user agent as browser so as not to be identified as bot)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
        web_page = urllib.request.urlopen(req).read()

    except urllib.error.HTTPError as error:

        if error.code == 404:
            return '{} 404 Page not found!'.format(error_prefix)
        elif error.code == 403:
            return '{} 403 Access denied!'.format(error_prefix)
        else:
            return '{} Unknown HTTPError, code {}'.format(error_prefix, error.code)

    except urllib.error.URLError as error:
        return '{} URL error, {}'.format(error_prefix, error.reason)

    # If the html was successfully retrieved:

    # Create beautiful soup object using the html.
    soup = BeautifulSoup(web_page, 'html.parser')

    # Get the first element in the html with attributes of a headline.
    try:
        headline_element = soup.find_all(headline_element_type, attrs={identifying_attribute: attribute_value})[0]

    except IndexError:
        return '{} Could not find headline on page!'.format(error_prefix)

    # Get text from the headline element and remove whitespace.
    return headline_element.get_text().strip().replace('&apos;', '\'')


def fetch_headlines(source_configs):
    # Remove the organisation name from each source config (not needed to fetch headline).
    organisations = [source_config.pop(0) for source_config in source_configs]

    # Use the source config data to fetch headlines from each source.
    return [fetch_headline(*source_config) for source_config in source_configs]


def append_row_to_file(row_data, filename):
    with open(filename, 'a', newline='') as results_file:
        results_file_writer = csv.writer(results_file, quoting=csv.QUOTE_ALL)
        results_file_writer.writerow(row_data)


def get_config_data(path):

    with open(path) as config:
        reader = csv.reader(config)
        return [source_config for source_config in reader]


if __name__ == '__main__':
    # Get the directory that the script has been run from.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Expect the config and results files to be in the current directory.
    config_filepath = '{}/news_sources_config.csv'.format(script_directory)
    results_filepath = '{}/headline_data.csv'.format(script_directory)

    # If needed, create a results file to store the retrieved headlines.
    if not os.path.isfile(results_filepath):
        initialise_results_file(config_filepath, results_filepath)

    # Get news source config data from file
    news_source_configs = get_config_data(config_filepath)

    # Get the current time
    current_time = str(datetime.now())

    # Fetch the current headlines
    current_headlines = fetch_headlines(news_source_configs)

    # Write the headlines and the current time to the results file
    append_row_to_file([current_time] + current_headlines, results_filepath)

