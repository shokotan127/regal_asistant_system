# これはScrapyのWebサイト（https://scrapy.org/）に掲載されているサンプルコードに
# コメントを追加したものです。
# ブログの構造の変化に合わせて myspider.py の時点のサンプルコードから変わっています。
# Scrapy 1.4.0以降で動作します。

import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'  # Spiderの名前。
    # クロールを開始するURLのリスト。
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        """
        ページから投稿のタイトルをすべて抜き出し、ベージャーをたどる。
        """

        # ページから投稿のタイトルをすべて抜き出す。
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').extract_first()}

        # ページャーの次のページへのリンクを取得し、次のページがあればたどる。
        # 次のページもparse()メソッドで処理する。
        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)
