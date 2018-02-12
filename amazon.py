# -*- coding: utf-8 -*-

import urllib.request, urllib.parse
import sys

import lxml.html

# TODO: あとで標準入力から受けるように変える
# print(sys.argv[1])
ISBN     = '9784776209676'
url_base = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords={ISBN}'
url = url_base.format(ISBN = ISBN)


# TODO: numberは検索の順番
result_id = 'result_{number}'
request  = urllib.request.Request(url)
response = urllib.request.urlopen(request)
dom = lxml.html.fromstring(response.read())
search_results_extract_xpath = '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]'
target_element = dom.xpath(search_results_extract_xpath.format(number = '0'))[0]
target_url = target_element.get('href')
print(target_url)
#aiueo = list([dom.xpath(search_results_extract_xpath.format(number = '0'))[0].text_content()])
#print(aiueo)
