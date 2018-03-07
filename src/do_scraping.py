# -*- coding: utf-8 -*-

# built-in
import json
import logging
import os
import re
import sys
import time

# mymodule
from scraping import amazon

def fetch_from_amazon(isbn_or_filename):
    if isbn_or_filename.isdigit():
        isbn = isbn_or_filename
        formatted = amazon.scraping(isbn)
        print(formatted)
    else:
        filename = isbn_or_filename
        with open(filename, 'r') as f:
            results = list()
            isbns = f.readlines()
            for i, isbn in enumerate(isbns):
                isbn = isbn[:-1]
                print('{}/{}, isbn={}'.format(str(i + 1), str(len(isbns)), isbn))
                try:
                    results.append(amazon.scraping(isbn))
                except Exception as e:
                    print(e)
                time.sleep(10)
            print(results)

def main():
    logger = logging.getLogger(__name__)

    web_site = sys.argv[1]
    isbn_or_filename = sys.argv[2]
    
    if web_site == 'amazon':
        fetch_from_amazon(isbn_or_filename)

if __name__ == '__main__':
    main()
