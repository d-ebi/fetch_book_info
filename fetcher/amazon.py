# -*- coding: utf-8 -*-

import urllib.parse
import re

base_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&field-keywords={isbn}'

def extract_search_results(dom, number=0):
    xpath = '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]'.format(number = str(number))
    extract = dom.xpath(xpath)[0]
    return extract.get('href') 

def extract_paper_book_url(dom):
    xpath   = '//div[@id="tmmSwatches"]//a[@class="a-button-text"]'
    extract = dom.xpath(xpath)
    if len(extract) <= 1: return None
    for book_type_toggle in extract:
        if not 'Kindle版' in book_type_toggle.text_content():
            href = book_type_toggle.get('href')
            if 'javascript' in href:
                return None
            else:
                return 'https://www.amazon.co.jp' + urllib.parse.quote(book_type_toggle.get('href'))
    
    return None

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
    return re.search(r'(\d{4}/\d{1,2}/\d{1,2}|\d{4}/\d{1,2})', extract.text).group(1)

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
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return extract[0].text[2:].replace(',', '')
    else:
        return ''

def extract_recommended_degree(dom):
    xpath = '//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]'
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return extract[0].text.replace('5つ星のうち ', '')
    else:
        return ''

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
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return re.search(r'(\d+)ページ', extract[0].text_content()).group(1)
    else:
        return ''

