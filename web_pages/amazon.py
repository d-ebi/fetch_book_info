# -*- coding: utf-8 -*-

import urllib.parse
import re

base_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords={ISBN}'

def extract_search_results(dom, number=0):
    xpath = '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]'.format(number = str(number))
    extract = dom.xpath(xpath)[0]
    return extract.get('href') 

def extract_product_image(dom):
    xpath = '//img[@id="imgBlkFront"]'
    extract = dom.xpath(xpath)[0]
    return extract.get('src')

def extract_product_name(dom):
    xpath = '//span[@id="productTitle"]'
    extract = dom.xpath(xpath)[0]
    return extract.text

def extract_classification(dom):
    xpath ='//h1[@id="title"]/span[2]' 
    extract = dom.xpath(xpath)[0]
    return extract.text

def extract_issued_date(dom):
    xpath = '//h1[@id="title"]/span[3]'
    extract = dom.xpath(xpath)[0]
    return re.search(r'(\d{4}/\d{1,2}/\d{1,2})', extract.text).group(1)

def extract_authors(dom):
    xpath = '//span[contains(@class, "author")]//a[contains(@class, "a-link-normal")]'
    extract = dom.xpath(xpath)
    authors = list()
    for author in extract:
        author_name_pattern  = r'field-author=(.+?)&'
        author_name_searched = re.search(author_name_pattern, author.get('href'))
        if author_name_searched:
            author_name = author_name_searched.group(1)
            authors.append(urllib.parse.unquote(author_name, 'utf-8').replace('+', ' '))
    return authors
        
def extract_price(dom):
    xpath = '//div[@id="buyNewSection"]//span[contains(@class, "a-color-price")]'
    extract = dom.xpath(xpath)[0]
    return extract.text[2:].replace(',', '')

def extract_recommended_degree(dom):
    xpath = '//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]'
    extract = dom.xpath(xpath)[0]
    return extract.text.replace('5つ星のうち ', '')

def extract_publisher(dom):
    xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "出版社")]'
    extract = dom.xpath(xpath)[0]
    return re.search(r' (.+?) \(.+?\)', extract.tail).group(1)

def extract_categories(dom):
    xpath = '//li[@id="SalesRank"]//span[@class="zg_hrsr_ladder"]'
    extract = dom.xpath(xpath)
    categories = list()
    for category in extract:
        exclude_invalid_str = category.text_content()[2:]
        categories.append(exclude_invalid_str.split(' > '))
    return categories

def extract_number_of_pages(dom):
    xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "ページ")]'
    extract = dom.xpath(xpath)[0]
    return re.search(r'(\d+)ページ', extract.text_content()).group(1)

xpaths = {
    # numberは検索結果の何個目かを示す. 0オリジン.
    'search_results_extract': '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]',
    # 書籍名
    'book_name': '//span[@id="productTitle"]',
    # 種別
    'classification': '//h1[@id="title"]/span[2]',
    # 発行年月日
    'issued_date': '//h1[@id="title"]/span[3]',
    # 著者名 HACK:このxpath,臭う
    'authors': '//span[contains(@class, "author")]//a[contains(@href, "dp_byline_sr_book") or contains(@href, "dp_byline_cont_book")]',
    # 金額
    'price': '//div[@id="buyNewSection"]//span[contains(@class, "a-color-price")]', 
    # おすすめ度
    'recommended_degree': '//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]',
    # 出版社
    'publisher': '//div[@id="detail_bullets_id"]//*[contains(text(), "出版社")]',
    # カテゴリ階層
    'categories': '//li[@id="SalesRank"]//span[@class="zg_hrsr_ladder"]',
    # ページ数 TODO: 要検証
    'number_of_pages': '//div[@id="detail_bullets_id"]//*[contains(text(), "ページ")]',
}
