base_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords={ISBN}'
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