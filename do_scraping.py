# -*- coding: utf-8 -*-

# built-in
import json
import re
import urllib.error, urllib.parse,  urllib.request
import sys
import time

# pip
import lxml.html

# mymodule
from fetcher import amazon
from utils import scraperlib

def get_item_detail_url(isbn):
    search_url = amazon.base_url.format(isbn=isbn)
    search_results = scraperlib.fetch_page(search_url)
    dom = scraperlib.parse_page(search_results)
    item_detail_url = amazon.extract_search_results(dom)

    return item_detail_url

def get_paper_book_url(dom):
    paper_book_url = amazon.extract_paper_book_url(dom)

    if paper_book_url:
        return paper_book_url

def main():
    isbn = sys.argv[1]

    item_detail_url = get_item_detail_url(isbn)

    item_detail_page = scraperlib.fetch_page(item_detail_url)
    dom = scraperlib.parse_page(item_detail_page)

    paper_book_url = amazon.extract_paper_book_url(dom)
    if paper_book_url:
        response = scraperlib.fetch_page(paper_book_url)
        dom = scraperlib.parse_page(response)
        item_detail_url = paper_book_url
    
    results = dict()
    results['isbn'] = isbn
    results['url']  = item_detail_url
    results['product_img_url'] = amazon.extract_product_image(dom)
    results['product_name'] = amazon.extract_product_name(dom)
    results['classification'] = amazon.extract_classification(dom)
    results['issued_date'] = amazon.extract_issued_date(dom)
    results['authors'] = amazon.extract_authors(dom)
    results['price'] = amazon.extract_price(dom)
    results['recommended_degree'] = amazon.extract_recommended_degree(dom)
    results['publisher'] = amazon.extract_publisher(dom)
    results['categories'] = amazon.extract_categories(dom)
    results['number_of_pages'] = amazon.extract_number_of_pages(dom)

    formatted = json.dumps(results, indent=4, ensure_ascii=False) 
    print(formatted)

if __name__ == '__main__':
    main()
