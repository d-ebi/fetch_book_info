# -*- coding: utf-8 -*-

# built-in
import json
import re
import sys
import time

# mymodule
from scraping import amazon

def main():
    web_site = sys.argv[1]
    isbn = sys.argv[2]
    
    if web_site == 'amazon':
        formatted = amazon.scraping(isbn)
        print(formatted)

if __name__ == '__main__':
    main()
