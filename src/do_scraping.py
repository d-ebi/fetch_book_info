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

def main():
    logger = logging.getLogger(__name__)

    web_site = sys.argv[1]
    isbn = sys.argv[2]
    
    if web_site == 'amazon':
        formatted = amazon.scraping(isbn)
        print(formatted)

if __name__ == '__main__':
    main()
