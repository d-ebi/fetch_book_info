# -*- coding: utf-8 -*-

import json
import urllib.parse
import re
import sys

sys.path.append('../utils/')
from utils import get_module_logger
from utils import scraperlib

base_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&field-keywords={isbn}'
logger = get_module_logger(__name__)

def extract_search_results(dom, number=0):
    '''
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        :number (int): 検索結果の中から取得するアイテムのindex
    Returns:
        :str: 対象アイテムのリンクurl
    '''
    
    xpath = '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]'.format(number = str(number))
    extract = dom.xpath(xpath)[0]
    return extract.get('href') 

def extract_paper_book_url(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 紙版の商品URL
    '''
    
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
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 対象商品の画像URL
    '''

    xpath = '//img[@id="imgBlkFront"]'
    extract = dom.xpath(xpath)[0]
    image_url_json = extract.get('data-a-dynamic-image')
    image_urls = list(json.loads(image_url_json).keys())
    return image_urls[0]

def extract_product_name(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 対象商品の名称
    '''

    xpath = '//span[@id="productTitle"]'
    extract = dom.xpath(xpath)[0]
    return extract.text

def extract_classification(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 対象商品の分類（単行本,コミック等）
    '''

    xpath ='//h1[@id="title"]/span[2]' 
    extract = dom.xpath(xpath)[0]
    return extract.text

def extract_issued_date(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 発売日
    '''

    xpath = '//h1[@id="title"]/span[3]'
    extract = dom.xpath(xpath)[0]
    return re.search(r'(\d{4}/\d{1,2}/\d{1,2}|\d{4}/\d{1,2})', extract.text).group(1)

def extract_authors(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 著者
    '''

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
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 価格
    '''

    xpath = '//div[@id="buyNewSection"]//span[contains(@class, "a-color-price")]'
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return extract[0].text[2:].replace(',', '')
    else:
        return ''

def extract_recommended_degree(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 評価
    '''

    xpath = '//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]'
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return extract[0].text.replace('5つ星のうち ', '')
    else:
        return ''

def extract_publisher(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 出版社
    '''

    xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "出版社")]'
    extract = dom.xpath(xpath)[0]
    return re.search(r' (.+?) \(.+?\)', extract.tail).group(1)

def extract_categories(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: カテゴリ
    '''

    xpath = '//li[@id="SalesRank"]//span[@class="zg_hrsr_ladder"]'
    extract = dom.xpath(xpath)
    categories = list()
    for category in extract:
        exclude_invalid_str = category.text_content()[2:]
        categories.append(exclude_invalid_str.split(' > '))
    return categories

def extract_number_of_pages(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: ページ数
    '''

    xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "ページ")]'
    extract = dom.xpath(xpath)
    if len(extract) > 0:
        return re.search(r'(\d+)ページ', extract[0].text_content()).group(1)
    else:
        return ''

def get_item_detail_url(isbn):
    '''
    
    Args:
        :isbn (str): ISBNコード
    Returns:
        :str: 対象のISBNコードを持つ書籍の商品URL
    '''

    search_url = base_url.format(isbn=isbn)
    search_results = scraperlib.fetch_page(search_url)
    dom = scraperlib.parse_page(search_results)
    item_detail_url = extract_search_results(dom)

    return item_detail_url

def get_paper_book_url(dom):
    '''
    
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
    Returns:
        :str: 紙版のURL
    '''

    paper_book_url = extract_paper_book_url(dom)

    if paper_book_url:
        return paper_book_url

def get_book_infos(dom):
    '''
    
    Args:
        :dom (http.client.HTTPResponse): httpレスポンスのオブジェクト
    Returns:
        :dict: 書籍情報の一覧
    '''
    
    results = dict()
    results['product_img_url'] = extract_product_image(dom)
    results['product_name'] = extract_product_name(dom)
    results['classification'] = extract_classification(dom)
    results['issued_date'] = extract_issued_date(dom)
    results['authors'] = extract_authors(dom)
    results['price'] = extract_price(dom)
    results['recommended_degree'] = extract_recommended_degree(dom)
    results['publisher'] = extract_publisher(dom)
    results['categories'] = extract_categories(dom)
    results['number_of_pages'] = extract_number_of_pages(dom)
    
    return results

def scraping(isbn):
    '''
    ISBNコードを元に,書籍情報を取得する.
    処理フローは下記である.
    
    1. ISBNを元にAmazonで検索
    2. 検索結果の商品詳細ページ情報を取得
    3. Kindle版ページの場合,紙書籍の情報ページへ移動
    4. 欲しい情報を取得
    
    戻り値はJSON文字列.
    
    Args:
        :isbn (str): isbnコード
    Returns
        :str: json文字列
    '''
    
    item_detail_url = get_item_detail_url(isbn)

    item_detail_page = scraperlib.fetch_page(item_detail_url)
    dom = scraperlib.parse_page(item_detail_page)

    paper_book_url = extract_paper_book_url(dom)
    if paper_book_url:
        response = scraperlib.fetch_page(paper_book_url)
        dom = scraperlib.parse_page(response)
        item_detail_url = paper_book_url
    
    book_infos = get_book_infos(dom)
    book_infos['isbn'] = isbn
    book_infos['url']  = item_detail_url

    formatted = json.dumps(book_infos, indent=4, ensure_ascii=False) 
    return formatted
