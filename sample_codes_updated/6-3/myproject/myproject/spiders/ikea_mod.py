from scrapy.spiders import SitemapSpider


class IkeaSpider(SitemapSpider):
    name = 'ikea_mod'
    allowed_domains = ['www.ikea.com']

    # この設定がないと 504 Gateway Time-out となることがある。
    # settings.pyでUSER_AGENTを設定している場合、この設定は削除してよい。
    custom_settings = {
        'USER_AGENT': 'ikeabot',
    }

    # XMLサイトマップのURLのリスト。
    # robots.txtのURLを指定すると、SitemapディレクティブからXMLサイトマップのURLを取得する。
    sitemap_urls = [
        'https://www.ikea.com/robots.txt',
    ]
    # サイトマップインデックスからたどるサイトマップURLの正規表現のリスト。
    # このリストの正規表現にマッチするURLのサイトマップのみをたどる。
    # sitemap_followを指定しない場合は、すべてのサイトマップをたどる。
    sitemap_follow = [
        r'prod-ja-JP',  # 日本語の製品のサイトマップのみたどる。
    ]
    # サイトマップに含まれるURLを処理するコールバック関数を指定するルールのリスト。
    # ルールは (正規表現, 正規表現にマッチするURLを処理するコールバック関数) という2要素のタプルで指定する。
    # sitemap_rulesを指定しない場合はすべてのURLのコールバック関数はparseメソッドとなる。
    sitemap_rules = [
        (r'/jp/ja/p/', 'parse_product'),  # 製品ページをparse_productで処理する。
    ]

    def parse_product(self, response):
        # 製品ページから製品の情報を抜き出す。
        yield {
            'url': response.url,  # URL
            'name': response.css('.range-revamp-header-section__title--big::text').get().strip(),  # 名前
            'type': response.css('.range-revamp-header-section__description-text::text').get().strip(),  # 種類
            'price': response.css('.range-revamp-price__integer::text').get().strip(), # 価格（通貨は無し）
        }
