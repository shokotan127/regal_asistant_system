import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news3'  # Spiderの名前。サンプルコードでは、nameの衝突を回避するため変更している。
    allowed_domains = ['news.yahoo.co.jp']  # クロール対象とするドメインのリスト。
    start_urls = ['https://news.yahoo.co.jp/']  # クロールを開始するURLのリスト。

    def parse(self, response):
        """
        トップページのトピックス一覧から個々のトピックスへのリンクを抜き出してたどる。
        """
        for url in response.css('ul.topicsList_main a::attr("href")').re(r'/pickup/\d+$'):
            yield response.follow(url, self.parse_topics)

    def parse_topics(self, response):
        pass
