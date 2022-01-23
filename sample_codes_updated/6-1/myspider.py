import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'  # Spiderの名前。
    start_urls = ['https://blog.scrapinghub.com']  # クロールを開始するURLのリスト。

    def parse(self, response):
        """
        ページから投稿のタイトルをすべて抜き出し、次のページへのリンクがあればたどる。
        """
        # ページから投稿のタイトルをすべて抜き出す。
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        # 次のページ（OLDER POST）へのリンクがあればたどる。
        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)
