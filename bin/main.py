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
    pass

def transform():
    pass

def load():
    pass


# Main section
if __name__ == '__main__':
    main()
