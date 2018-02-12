# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import sys
import time

import lxml.html

from web_pages import amazon

def fetch_parsed_web_page(url, retry=3, charset='utf-8'):
    request  = urllib.request.Request(url)
    http_error_count = 0
    sleep_time = 5
    
    while True:
        try:
            response = urllib.request.urlopen(request)
            break
        except urllib.error.HTTPError as e:
            if http_error_count >= retry:
                raise urllib.error.HTTPError(e.code, e.reason, e.headers)
            else:
                time.sleep(sleep_time)
                http_error_count += 1
    
    return lxml.html.fromstring(response.read().decode(charset))

def main():
    # TODO: あとで標準入力から受けるように変える
    # print(sys.argv[1])
    ISBN     = '9784776209676'

    dom = fetch_parsed_web_page(amazon.base_url.format(ISBN = ISBN))
    search_results_first_item = dom.xpath(amazon.xpaths['search_results_extract'].format(number = '0'))[0]
    item_detail_url = search_results_first_item.get('href')
    print(item_detail_url)
    
    # TODO:検索結果にて,Kindle版がある場合,Kindle版ではない方を拾うようにしないといけない
    # TODO: dom2は無いので変える,上と下で明らかに処理が違うので関数を分離
    dom2 = fetch_parsed_web_page(item_detail_url)
    print('書籍名      :' + dom2.xpath(amazon.xpaths['book_name'])[0].text)
    print('本の種別    :' + dom2.xpath(amazon.xpaths['classification'])[0].text)
    print('発行年月日  :' + dom2.xpath(amazon.xpaths['issued_date'])[0].text)
    for author in dom2.xpath(amazon.xpaths['authors']):
        print('著者名      :' + author.text)
    print('金額        :' + dom2.xpath(amazon.xpaths['price'])[0].text)
    print('おすすめ度  :' + dom2.xpath(amazon.xpaths['recommended_degree'])[0].text)
    print('出版社      :' + dom2.xpath(amazon.xpaths['publisher'])[0].tail)
    for category in dom2.xpath(amazon.xpaths['categories']):
        print('カテゴリ階層:' + category.text_content())
    print('ページ数    :' + dom2.xpath(amazon.xpaths['number_of_pages'])[0].text_content())
    
if __name__ == '__main__':
    main()