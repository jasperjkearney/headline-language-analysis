#!/usr/bin/env python3

import csv
import os.path


def initialise_results_file(config_file, results_file, overwrite=False):

    try:
        with open(config_file) as config:
            reader = csv.reader(config)
            organisations = [source_data[0] for source_data in reader]

    except FileNotFoundError as err:
        raise err

    if not os.path.isfile(results_file) or overwrite:
        with open(results_file, 'w', newline='') as results:
            results_file_writer = csv.writer(results)
            results_file_writer.writerow(["Datetime"] + organisations)
        return 0

    raise FileExistsError('Results file already exists, specify overwrite = True to replace.')

if __name__ == '__main__':
    # Look for config file in current directory.
    # Create results file in the current directory, overwriting any existing file.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    config_filepath = '{}/news_sources_config.csv'.format(script_directory)
    results_filepath = '{}/headline_data.csv'.format(script_directory)

    initialise_results_file(config_filepath, results_filepath, True)

