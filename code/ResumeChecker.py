# ResumeChecker.py
# A component of: resumes
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Created on 10/10/14, at 10:29 AM
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
#
# imports
# *********************************
import csv
import functools
import glob
import logging
import os
import re
import argparse

import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


# global variables
# *********************************


__author__ = 'bjherger'
__license__ = 'http://opensource.org/licenses/MIT'
__version__ = '1.0'
__email__ = '13herger@gmail.com'
__status__ = 'Development'
__maintainer__ = 'bjherger'

# functions
# *********************************


def list_files(path=os.getcwd()):
    file_list = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        os.path.join(dirpath)
        filenames = [os.path.join(dirpath, filename) for filename in filenames]
        file_list.extend(filenames)
    return file_list


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
                                        r"(\d{4})"  # 4 digit local
                                        , re.IGNORECASE)
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
        # regular_expression = re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
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
        # regular_expression = re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
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
        logging.error('Issue parsing term: ' + str(term)+' from string: ' + str(
            string_to_search) + ': ' + str(e))
        return 0


def term_match(string_to_search, term="me"):
    try:
        regular_expression = re.compile(term, re.IGNORECASE)
        result = re.findall(regular_expression, string_to_search)
        return result[0]
    except Exception, e:
        logging.error('Issue parsing term: ' + str(term) + ' from string: ' +
                      str(string_to_search) +': ' + str(e))
        return None


def build_dataframe(path):
    logging.info('Searching path: ' + str(path))
    path_glob = os.path.join(path, '*.pdf')
    file_list =[pdf_file for pdf_file in glob.glob(path_glob)]

    logging.info('Iterating through file_list: ' + str(file_list))
    df = pd.DataFrame()

    # Get file information
    df["file_name"] = file_list
    df["html"] = df["file_name"].apply(convert_pdf_to_txt)

    # Scrape contact information
    df["phone_number"] = df["html"].apply(check_phonenumber)
    df["area_code"] = df["phone_number"].apply(functools.partial(term_match, term=r"\d{3}"))
    df["email"] = df["html"].apply(check_email)
    df["email_domain"] = df["email"].apply(functools.partial(term_match, term=r"@(.+)"))
    df["address"] = df["html"].apply(check_address)
    df["linkedin"] = df["html"].apply(functools.partial(term_count, term=r"linkedin"))
    df["github"] = df["html"].apply(functools.partial(term_count, term=r"github"))

    # Pull a few other interesting features
    df["num_words"] = df["html"].apply(lambda x: len(x.split()))
    df["phd"] = df["html"].apply(functools.partial(term_count, term=r"ph.?d.?"))

    # And skills
    df["java_count"] = df["html"].apply(functools.partial(term_count, term=r"java"))
    df["python_count"] = df["html"].apply(functools.partial(term_count, term=r"python"))
    df["R_count"] = df["html"].apply(functools.partial(term_count, term=r" R[ ,]"))
    df["latex_count"] = df["html"].apply(functools.partial(term_count, term=r"latex"))
    df["stata_count"] = df["html"].apply(functools.partial(term_count, term=r"stata"))
    df["CS_count"] = df["html"].apply(functools.partial(term_count, term=r"computer science"))
    df["mysql_count"] = df["html"].apply(functools.partial(term_count, term=r"mysql"))
    df["ms_office"] = df["html"].apply(functools.partial(term_count, term=r"microsoft office"))
    df["analytics"] = df["html"].apply(functools.partial(term_count, term=r"analytics"))



    return df


def main():
    parser = argparse.ArgumentParser(
        description='Script to parse PDF resumes, and create a csv file containing contact info '
                    'and required fields')
    parser.add_argument('--data_path', help='Path to folder containing PDF resumes.',
                        required=True)
    parser.add_argument('--output_path', help='Path to place output .csv file',
                        default='resumes_output.csv')

    args = parser.parse_args()

    # Setup logger
    logging.basicConfig(level=logging.INFO)
    logging.info('Begin Main')

    # Create dataframe
    df = build_dataframe(args.data_path)

    # Output to CSV
    df.to_csv(args.output_path)
    logging.info('End Main')


# main
# *********************************

if __name__ == '__main__':

    main()


