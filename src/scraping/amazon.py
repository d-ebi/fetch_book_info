# -*- coding: utf-8 -*-

# built-in
import json
import urllib.parse
import re
import sys

# my modules
from scraping.error import ExtractError
sys.path.append('../utils/')
from utils import get_module_logger
from utils import scraperlib

logger = get_module_logger(__name__)

class BookDetailScraper():
    def __init__(self, isbn, url):
        self.isbn = isbn
        self.url = url
        self.dom = self.fetch_book_page()
        paper_book_url = self.extract_paper_book_url()
        if paper_book_url:
            self.url = paper_book_url
            self.dom = self.fetch_book_page()
        self.image_url = self.extract_book_image()
        self.name = self.extract_book_name()
        self.classification = self.extract_classification()
        self.issued_date = self.extract_issued_date()
        self.authors = self.extract_authors()
        self.price = self.extract_price()
        self.recommended_degree = self.extract_recommended_degree()
        self.publisher = self.extract_publisher()
        self.categories = self.extract_categories()
        self.number_of_pages = self.extract_number_of_pages()

    def __str__(self):
        '''
        
        Returns:
            :str: 書籍情報のJSON
        '''
       
        book_infos = dict()
        book_infos['url'] = self.url
        book_infos['isbn'] = self.isbn
        book_infos['image_url'] = self.image_url
        book_infos['name'] = self.name
        book_infos['classification'] = self.classification
        book_infos['issued_date'] = self.issued_date
        book_infos['authors'] = self.authors
        book_infos['price'] = self.price
        book_infos['recommended_degree'] = self.recommended_degree
        book_infos['publisher'] = self.publisher
        book_infos['categories'] = self.categories
        book_infos['number_of_pages'] = self.number_of_pages
       
        formatted = json.dumps(book_infos, indent=4, ensure_ascii=False)
        return formatted
   
    def fetch_book_page(self):
        book_detail_page = scraperlib.fetch_page(self.url)
        return scraperlib.parse_page(book_detail_page)

    def is_failure_extract(self, extract):
        return len(is_failure_extract) == 0

    def get_isbn_log_str(self):
        return 'ISBN={}'.format(self.isbn)

    def extract_paper_book_url(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 紙版の商品URL
        '''
        
        xpath  = '//div[@id="tmmSwatches"]//a[@class="a-button-text"]'
        extract = self.dom.xpath(xpath)
        if len(extract) <= 1: return None
    
        for book_type_toggle in extract:
            if not 'Kindle版' in book_type_toggle.text_content():
                href = book_type_toggle.get('href')
                if 'javascript' in href:
                    return None
                else:
                    return 'https://www.amazon.co.jp' + urllib.parse.quote(book_type_toggle.get('href'))
        return None
    
    def extract_book_image(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 対象商品の画像URL
        '''
    
        xpath = '//img[@id="imgBlkFront"]'
        extract = self.dom.xpath(xpath)
        if self.is_failure_extract(extract):
            logger.warning('The book image failed to fetch. {}'.format(self.get_isbn_log_str()))
            return str()
    
        image_url_json = extract[0].get('data-a-dynamic-image')
        image_urls = list(json.loads(image_url_json).keys())
        return image_urls[0]
    
    def extract_book_name(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 対象商品の名称
        '''
    
        xpath = '//span[@id="productTitle"]'
        extract = self.dom.xpath(xpath)

        if self.is_failure_extract(extract):
            logger.error('The book name failed to fetch. {}'.format(self.get_isbn_log_str())
            return str()

        return extract[0].text
    
    def extract_classification(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 対象商品の分類（単行本,コミック等）
        '''
    
        xpath ='//h1[@id="title"]/span[2]' 
        extract = self.dom.xpath(xpath)

        if self.is_failure_extract(extract):
            logger.warning('The book classification ')

        return extract[0].text
    
    def extract_issued_date(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 発売日
        '''
    
        xpath = '//h1[@id="title"]/span[3]'
        extract = self.dom.xpath(xpath)[0]
        return re.search(r'(\d{4}/\d{1,2}/\d{1,2}|\d{4}/\d{1,2})', extract.text).group(1)
    
    def extract_authors(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 著者
        '''
    
        xpath = '//span[contains(@class, "author")]//a[contains(@class, "a-link-normal")]'
        extract = self.dom.xpath(xpath)
        authors = list()
        for author in extract:
            author_name_pattern  = r'field-author=(.+?)&'
            author_name_searched = re.search(author_name_pattern, author.get('href'))
            if author_name_searched:
                author_name = author_name_searched.group(1)
                authors.append(urllib.parse.unquote(author_name, 'utf-8').replace('+', ' '))
        return authors
            
    def extract_price(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 価格
        '''
    
        xpath = '//div[@id="buyNewSection"]//span[contains(@class, "a-color-price")]'
        extract = self.dom.xpath(xpath)
        if len(extract) > 0:
            return extract[0].text[2:].replace(',', '')
        else:
            return ''
    
    def extract_recommended_degree(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 評価
        '''
    
        xpath = '//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]'
        extract = self.dom.xpath(xpath)
        if len(extract) > 0:
            return extract[0].text.replace('5つ星のうち ', '')
        else:
            return ''
    
    def extract_publisher(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: 出版社
        '''
    
        xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "出版社")]'
        extract = self.dom.xpath(xpath)[0]
        return re.search(r' (.+?) \(.+?\)', extract.tail).group(1)
    
    def extract_categories(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: カテゴリ
        '''
    
        xpath = '//li[@id="SalesRank"]//span[@class="zg_hrsr_ladder"]'
        extract = self.dom.xpath(xpath)
        categories = list()
        for category in extract:
            exclude_invalid_str = category.text_content()[2:]
            categories.append(exclude_invalid_str.split(' > '))
        return categories
    
    def extract_number_of_pages(self):
        '''
        
        Args:
            :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        Returns:
            :str: ページ数
        '''
    
        xpath = '//div[@id="detail_bullets_id"]//*[contains(text(), "ページ")]'
        extract = self.dom.xpath(xpath)
        if len(extract) > 0:
            return re.search(r'(\d+)ページ', extract[0].text_content()).group(1)
        else:
            return ''

search_base_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&field-keywords={isbn}'
   
def get_book_detail_url(isbn):
    '''
    
    Args:
        :isbn (str): ISBNコード
    Returns:
        :str: 対象のISBNコードを持つ書籍の商品URL
    '''
 
    search_url = search_base_url.format(isbn=isbn)
    search_results = scraperlib.fetch_page(search_url)
    dom = scraperlib.parse_page(search_results)
    return extract_search_results(dom)

def extract_search_results(dom, number=0):
    '''
    Args:
        :dom (lxml.html.HtmlElement): HTMLの解釈済みDOM
        :number (int): 検索結果の中から取得するアイテムのindex
    Returns:
        :str: 対象アイテムのリンクurl
    '''
     
    xpath = '//li[@id="result_{number}"]//a[contains(@class, "s-access-detail-page")]'.format(number = str(number))
    extract = dom.xpath(xpath)

    if len(extract) > 0: return extract[0].get('href')
    
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

    # isbnは13桁
    if len(isbn) != 13:
        logger.error('Iliegal isbn. ISBN={}'.format(isbn))
        return None

    book_detail_url = get_book_detail_url(isbn)
    if not book_detail_url:
        logger.error('Not found. ISBN={}'.format(isbn))
        return None

    book_detail_scraper = BookDetailScraper(isbn, book_detail_url)
    return book_detail_scraper
