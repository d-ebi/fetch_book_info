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
    debug_level_os_env = 'FETCH_BOOK_INFO_DEBUG_LEVEL'
    debug_level = os.environ[debug_level_os_env] if debug_level_os_env in os.environ else ''
    if debug_level:
        try:
            debug_level = getattr(logging, debug_level)
        except AttributeError as e:
            sys.stderr.write('Error: {e}\n'.format(e=e))
            sys.stderr.write('''The supported debug levels are as follows. ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']''')
            sys.exit(1)
    debug_level = debug_level if debug_level else logging.WARNING
    logger.setLevel(debug_level)

    web_site = sys.argv[1]
    isbn = sys.argv[2]
    
    if web_site == 'amazon':
        formatted = amazon.scraping(isbn)
        print(formatted)

if __name__ == '__main__':
    main()
