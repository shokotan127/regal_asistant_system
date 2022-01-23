class MySpider(scrapy.Spider):
    # ...

    def parse(self, response):
        yield MyItem(
            url=response.url,
            key=extract_key(response.url),
            html=response.text)
