#!/usr/bin/env python
"""
coding=utf-8

A utility to make handling many resumes easier by automatically pulling contact information, required skills and
custom text fields. These results are then surfaced as a convenient summary CSV.

"""
import argparse
import csv
import functools
import glob
import logging
import os
import re

import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

logging.basicConfig(level=logging.DEBUG)

__author__ = 'bjherger'
__license__ = 'http://opensource.org/licenses/MIT'
__version__ = '2.0'
__email__ = '13herger@gmail.com'
__status__ = 'Development'
__maintainer__ = 'bjherger'


def main():
    """
    Main method for ResumeParser. This utility will:
     - Read in `data_path` and `output_path` from command line arguments
     - Create a list of documents to scan
     - Read the text from those documents
     - Pull out desired information (e.g. contact info, skills, custom text fields)
     - Output summary CSV

    :return: None
    :rtype: None
    """
    logging.info('Begin Main')

    # Parse command line arguments
    logging.info('Parsing input arguments')
    parser = argparse.ArgumentParser(
        description='Script to parse PDF resumes, and create a csv file containing contact info '
                    'and required fields')
    parser.add_argument('--data_path', help='Path to folder containing documents ending in .pdf',
                        required=True)
    parser.add_argument('--output_path', help='Path to place output .csv file',
                        default='../data/output/resumes_output.csv')

    args = parser.parse_args()

    logging.info('Command line arguments: {}'.format(vars(args)))

    # Create resume resume_df
    resume_df = create_resume_df(args.data_path)

    # Output to CSV
    resume_df.to_csv(args.output_path, quoting=csv.QUOTE_ALL, encoding='utf-8')
    logging.info('End Main')


def convert_pdf_to_txt(path):
    try:
        logging.debug('Converting pdf to txt: ' + str(path))
        # Setup pdf reader
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        # Iterate through pages
        path_open = file(path, 'rb')
        for page in PDFPage.get_pages(path_open, pagenos, maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            interpreter.process_page(page)
        path_open.close()
        device.close()

        # Get full string from PDF
        full_string = retstr.getvalue()
        retstr.close()

        # Normalize a bit, removing line breaks
        full_string = full_string.replace("\r", "\n")
        full_string = full_string.replace("\n", " ")

        # Remove awkward LaTeX bullet characters
        full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
        return full_string.decode('ascii', errors='ignore')

    except Exception, e:
        logging.error('Error in file: ' + path + str(e))
        return ''


def check_phonenumber(string_to_search):
    try:
        regular_expression = re.compile(r"\(?"  # open parenthesis
                                        r"(\d{3})?"  # area code
                                        r"\)?"  # close parenthesis
                                        r"[\s\.-]{0,2}?"  # area code, phone separator
                                        r"(\d{3})"  # 3 digit local
                                        r"[\s\.-]{0,2}"  # 3 digit local, 4 digit local separator
                                        r"(\d{4})",  # 4 digit local
                                        re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.groups()
            result = "-".join(result)
        return result
    except Exception, e:
        logging.error('Issue parsing phone number: ' + string_to_search + str(e))
        return None


def check_email(string_to_search):
    try:
        regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()
        return result
    except Exception, e:
        logging.error('Issue parsing email number: ' + string_to_search + str(e))
        return None


def check_address(string_to_search):
    try:
        regular_expression = re.compile(r"[0-9]+ [a-z0-9,\.# ]+\bCA\b", re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()

        return result
    except Exception, e:
        logging.error('Issue parsing email number: ' + string_to_search + str(e))

        return None


def term_count(string_to_search, term="me"):
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return len(result)
    except Exception, e:
        logging.error('Issue parsing term: ' + str(term) + ' from string: ' + str(
            string_to_search) + ': ' + str(e))
        return 0


def term_match(string_to_search, term="me"):
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return result[0]
    except Exception, e:
        logging.error('Issue parsing term: ' + str(term) + ' from string: ' +
                      str(string_to_search) + ': ' + str(e))
        return None


def create_resume_df(data_path):
    """

    This function creates a Pandas DF with one row for every input resume, and columns including the resumes's
    file path and raw text.

    This is achieved through the following steps:
     - Create a list of documents to scan
     - Read the text from those documents
     - Pull out desired information (e.g. contact info, skills, custom text fields)
    :param data_path: Path to a folder containing resumes. Any files ending in .pdf in this folder will be treated as a
    resume.
    :type data_path: str
    :return: A Pandas DF with one row for every input resume, and columns including the resumes's
    file path and raw text
    :rtype: pd.DataFrame
    """

    # Create a list of documents to scan
    logging.info('Searching path: ' + str(data_path))

    # Find all files in the data_path which end in `.pdf`. These will all be treated as resumes
    path_glob = os.path.join(data_path, '*.pdf')

    # Create list of files
    file_list = glob.glob(path_glob)

    logging.info('Iterating through file_list: ' + str(file_list))
    df = pd.DataFrame()

    # Store metadata, raw text, and word count
    df["file_path"] = file_list
    df["raw_text"] = df["file_path"].apply(convert_pdf_to_txt)
    df["num_words"] = df["raw_text"].apply(lambda x: len(x.split()))

    # Scrape contact information
    df["phone_number"] = df["raw_text"].apply(check_phonenumber)
    df["area_code"] = df["phone_number"].apply(functools.partial(term_match, term=r"\d{3}"))
    df["email"] = df["raw_text"].apply(check_email)
    df["email_domain"] = df["email"].apply(functools.partial(term_match, term=r"@(.+)"))
    df["address"] = df["raw_text"].apply(check_address)
    df["linkedin"] = df["raw_text"].apply(functools.partial(term_count, term=r"linkedin"))
    df["github"] = df["raw_text"].apply(functools.partial(term_count, term=r"github"))

    # Scrape education information
    df["phd"] = df["raw_text"].apply(functools.partial(term_count, term=r"ph.?d.?"))

    # Scrape skill information
    df["java_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"java"))
    df["python_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"python"))
    df["R_count"] = df["raw_text"].apply(functools.partial(term_count, term=r" R[ ,]"))
    df["latex_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"latex"))
    df["stata_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"stata"))
    df["CS_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"computer science"))
    df["mysql_count"] = df["raw_text"].apply(functools.partial(term_count, term=r"mysql"))
    df["ms_office"] = df["raw_text"].apply(functools.partial(term_count, term=r"microsoft office"))
    df["analytics"] = df["raw_text"].apply(functools.partial(term_count, term=r"analytics"))

    # Return enriched DF
    return df


if __name__ == '__main__':
    main()
