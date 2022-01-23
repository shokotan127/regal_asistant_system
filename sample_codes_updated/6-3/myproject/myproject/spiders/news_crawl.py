from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline


class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']

    # リンクをたどるためのルールのリスト。
    rules = (
        # トピックスのページへのリンクをたどり、レスポンスをparse_topics()メソッドで処理する。
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す。
        """
        item = Headline()
        item['title'] = response.css('.tpcNews_title::text').get()
        item['body'] = response.css('.tpcNews_summary').xpath('string()').get()
        yield item
