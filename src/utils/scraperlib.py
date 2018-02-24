# -*- coding: utf-8 -*-

'''
Webスクレイピングにおける,基本的な関数群を提供する.
'''

# built-in
import http.client
import json
import random
import re
import urllib.error, urllib.parse,  urllib.request
import sys
import time

# pip
import lxml.html

# mymodule
from utils import get_module_logger

logger = get_module_logger(__name__)

def fetch_page(url, retry=3, wait_time=10):
    '''
    指定されたURLのWebページにアクセスし,http.client.HTTPResponseを返す.
    503等でアクセスできなかった場合は,再取得を行なう.

    Args:
        :url (str): 対象のURL
        :retry (int): 対象ページがエラーとなった場合の再試行回数
        :wait_time (int): 再試行時の待ち時間(秒)

    Returns:
        :http.client.HTTPResponse: httpレスポンスのオブジェクト

    >>> fetch_page('https://www.google.co.jp').url
    'https://www.google.co.jp'
    '''
    
    logger.debug('start')
    
    #: list, 問い合わせに行くときのUser agent
    user_agents = [
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0 ',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (X11; FreeBSD amd64; rv:41.0) Gecko/20100101 Firefox/41.0',
    ]

    ua_index = random.randint(0, len(user_agents) -1)
    request = urllib.request.Request(url)
    opener  = urllib.request.build_opener()
    user_agent = user_agents[ua_index]
    opener.addheaders = [('User-agent', user_agent)]
    
    logger.debug('user agent -> {}'.format(user_agent))

    http_error_count = 0
    response = None
    
    while True:
        try:
            logger.info('open url -> {}'.format(url))
            response = opener.open(request)
            break
        except urllib.error.HTTPError as e:
            if http_error_count >= retry:
                logger.error(e)
                raise urllib.error.HTTPError(e.code, e.reason, e.headers, e.hdrs, e.fp)
            else:
                http_error_count += 1
                logger.warning('retry request. {0}...'.format(http_error_count))
                time.sleep(wait_time)
    logger.debug('end')
    
    return response 

def parse_page(response, retry=10, wait_time=10, charset='utf-8'):
    '''
    http.client.HTTPResponseを解釈し,lxml.html.HtmlElementとして返す.
    responseのread()に時間がかかった場合エラーとなるため,その場合再試行する.

    Args:
        :param response (http.client.HTTPResponse): httpレスポンスのオブジェクト
        :param retry (int): レスポンスの読み込みエラーとなった場合の再試行回数
        :param wait_time (int): 再試行時の待ち時間(秒)
        :param charset (str): デコードする際の文字コード
    Returns:
        :lxml.html.HtmlElement: HTMLの解釈済みDOM
    
    >>> response = fetch_page('https://www.google.co.jp/')
    >>> parse_page(response).xpath('//title')[0].text
    'Google'
    '''

    logger.debug('start')

    read_count = 0
    response_html_str = ''

    while True:
        try:
            logger.debug('read response')
            response_html_str = response.read()
            break
        except http.client.IncompleteRead as e:
            if read_count >= retry:
                logger.error(e)
                raise http.client.IncompleteRead(e.partial)
            else:
                read_count += 1
                logger.warning('retry response read. {0}...'.format(read_count))
                time.sleep(wait_time)
    decoded = response_html_str.decode(charset, errors='ignore')
    logger.debug('end')
    
    return lxml.html.fromstring(decoded)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
