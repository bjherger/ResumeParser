# pdf_reader.py
# A component of: resumes
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Created on 10/8/14, at 2:51 PM
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
#
# imports
# *********************************
import os
import re
import sys
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

# global variables
# *********************************
from pdfminer.pdfinterp import PDFResourceManager

__author__ = 'bjherger'
__license__ = 'http://opensource.org/licenses/MIT'
__version__ = '1.0'
__email__ = '13herger@gmail.com'
__status__ = 'Development'
__maintainer__ = 'bjherger'

# functions
# *********************************



from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def pdfs_to_strings(path = os.listdir('.') ):
    file_list = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        os.path.join(dirpath)
        filenames = [os.path.join(dirpath, filename) for filename in filenames]
        file_list.extend(filenames)
    strings = [convert_pdf_to_txt(filename) for filename in file_list]
    return strings

def convert_pdf_to_txt(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos= set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str
    except:
        print "error occured: ", path
        return ""


def main():
    # print convert_pdf_to_txt("test.pdf")
    # print pdfs_to_strings("/Users/bjherger")
    html_list =  pdfs_to_strings("/Users/bjherger/Google Drive/Developer/resumes/data")
    text_list = [BeautifulSoup(raw_html) for raw_html in html_list]
    print text_list


# main
# *********************************

if __name__ == '__main__':
    print 'Begin Main'
    main()
    print 'End Main'

