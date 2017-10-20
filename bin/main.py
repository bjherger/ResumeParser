#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import logging




def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.getLogger().setLevel(logging.DEBUG)

    # Extract data from upstream
    extract()

    # Transform data to have appropriate fields
    transform()

    # Load data for downstream consumption
    load()

    pass

def extract():
    # TODO Docstring
    logging.info('Begin extract')

    # TODO Create list of candidate files

    # TODO Subset candidate files to supported extensions

    # TODO Attempt to extract text from files

    # TODO Archive schema and return

    logging.info('End extract')
    pass

def transform():
    pass

def load():
    pass


# Main section
if __name__ == '__main__':
    main()
