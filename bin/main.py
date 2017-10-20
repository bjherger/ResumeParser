#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import logging

import os

import pandas
import textract

import lib


def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.getLogger().setLevel(logging.DEBUG)

    # Extract data from upstream. 
    extract()

    # Transform data to have appropriate fields
    transform()

    # Load data for downstream consumption
    load()

    pass

def extract():
    # TODO Docstring
    logging.info('Begin extract')

    # Reference variables
    candidate_file_agg = list()

    # Create list of candidate files
    for root, subdirs, files in os.walk(lib.get_conf('resume_directory')):

        folder_files = map(lambda x: os.path.join(root, x), files)
        candidate_file_agg.extend(folder_files)

    # Convert list to a pandas DataFrame
    observations = pandas.DataFrame(data=candidate_file_agg, columns=['file_path'])
    logging.info('Found {} candidate files'.format(len(observations.index)))

    # Subset candidate files to supported extensions
    observations['extension'] = observations['file_path'].apply(lambda x: os.path.splitext(x)[1])
    observations = observations[observations['extension'].isin(lib.AVAILABLE_EXTENSIONS)]
    logging.info('Subset candidate files to extensions w/ available parsers. {} files remain'.
                 format(len(observations.index)))

    # Attempt to extract text from files
    observations['text'] = observations['file_path'].apply(textract.process)

    # Archive schema and return
    lib.archive_dataset_schemas('extract', locals(), globals())
    logging.info('End extract')
    return observations

def transform():
    # TODO Docstring

    # TODO Extract candidate name

    # TODO Extract skills

    # TODO Extract contact fields

    # TODO Archive schema and return
    pass

def load():
    pass


# Main section
if __name__ == '__main__':
    main()
