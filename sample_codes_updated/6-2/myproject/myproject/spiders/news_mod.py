import scrapy

from myproject.items import Headline  # ItemのHeadlineクラスをインポート。


class NewsSpider(scrapy.Spider):
    name = 'news_mod'  # Spiderの名前。
    allowed_domains = ['news.yahoo.co.jp']  # クロール対象とするドメインのリスト。
    start_urls = ['https://news.yahoo.co.jp/']  # クロールを開始するURLのリスト。

    def parse(self, response):
        """
        トップページのトピックス一覧から個々のトピックスへのリンクを抜き出してたどる。
        """
        for url in response.css('section.topics a::attr("href")').re(r'/pickup/\d+$'):
            yield response.follow(url, self.parse_topics)

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す。
        """
        item = Headline()  # Headlineオブジェクトを作成。
        item['title'] = response.css('[data-ual-view-type="digest"] > a > p::text').get()  # タイトル
        item['body'] = response.css('[data-ual-view-type="digest"] > p').xpath('string()').get()  # 本文
        yield item  # Itemをyieldして、データを抽出する。
