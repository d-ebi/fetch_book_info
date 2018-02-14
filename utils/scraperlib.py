# -*- coding: utf-8 -*-

'''
Webスクレイピングにおける,基本的な関数群を提供する.
'''

# built-in
import http.client
import json
import re
import urllib.error, urllib.parse,  urllib.request
import sys
import time

# pip
import lxml.html

def fetch_page(url, retry=3, wait_time=10):
    '''
    指定されたURLのWebページにアクセスし,http.client.HTTPResponseを返す.
    503等でアクセスできなかった場合は,再取得を行なう.
    
    @param url str: 対象のURL
    @param retry int: 対象ページがエラーとなった場合の再試行回数
    @param wait_time int: 再試行時の待ち時間(秒)
    @return http.client.HTTPResponse: httpレスポンスのオブジェクト
    '''

    request = urllib.request.Request(url)
    opener  = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]

    http_error_count = 0
    response = None
    
    while True:
        try:
            response = opener.open(request)
            break
        except urllib.error.HTTPError as e:
            if http_error_count >= retry:
                raise urllib.error.HTTPError(e.code, e.reason, e.headers, e.hdrs, e.fp)
            else:
                http_error_count += 1
                print('retry request. {0}...'.format(http_error_count))
                time.sleep(wait_time)
    return response 

def parse_page(response, retry=10, wait_time=10, charset='utf-8'):
    '''
    http.client.HTTPResponseを解釈し,lxml.html.HtmlElementとして返す.
    responseのread()に時間がかかった場合エラーとなるため,その場合再試行する.
    
    @param response http.client.HTTPResponse: httpレスポンスのオブジェクト
    @param retry int: レスポンスの読み込みエラーとなった場合の再試行回数
    @param wait_time int: 再試行時の待ち時間(秒)
    @param charset str: デコードする際の文字コード
    @return lxml.html.HtmlElement: HTMLの解釈済みDOM
    '''

    read_count = 0
    response_html_str = ''

    while True:
        try:
            response_html_str = response.read()
            break
        except http.client.IncompleteRead as e:
            if read_count >= retry:
                raise http.client.IncompleteRead(e.partial)
            else:
                read_count += 1
                print('retry response read. {0}...'.format(read_count))
                time.sleep(wait_time)
    return lxml.html.fromstring(response_html_str.decode(charset))

