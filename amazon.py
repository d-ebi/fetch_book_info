# -*- coding: utf-8 -*-

import re
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
                raise urllib.error.HTTPError(e.code, e.reason, e.headers, e.hdrs, e.fp)
            else:
                time.sleep(sleep_time)
                http_error_count += 1
    
    return lxml.html.fromstring(response.read().decode(charset))

def main():
    # TODO: あとで標準入力から受けるように変える
    # print(sys.argv[1])
    ISBN     = sys.argv[1] #'9784776209676'

    dom = fetch_parsed_web_page(amazon.base_url.format(ISBN = ISBN))
    item_detail_url = amazon.extract_search_results(dom)
    
    # TODO:検索結果にて,Kindle版がある場合,Kindle版ではない方を拾うようにしないといけない
    # TODO: dom2は無いので変える,上と下で明らかに処理が違うので関数を分離
    dom2 = fetch_parsed_web_page(item_detail_url)
    print('URL         :' + item_detail_url)
    print('書籍名      :' + amazon.extract_product_name(dom2))
    print('本の種別    :' + amazon.extract_classification(dom2))
    print('発行年月日  :' + amazon.extract_issued_date(dom2))
    print(dom2.xpath('//span[contains(@class, "author")]'))
    for author in amazon.extract_authors(dom2):
        print('著者名      :' + author)
    print('金額        :' + amazon.extract_price(dom2))
    print('おすすめ度  :' + amazon.extract_recommended_degree(dom2))
    print('出版社      :' + amazon.extract_publisher(dom2))
    for category in amazon.extract_categories(dom2):
        print('カテゴリ階層:' + str(category))
    print('ページ数    :' + amazon.extract_number_of_pages(dom2))
    
if __name__ == '__main__':
    main()
