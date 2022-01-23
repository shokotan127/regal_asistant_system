from scrapy.exceptions import DropItem


class ValidationPipeline:
    """
    Itemを検証するPipeline。
    """

    def process_item(self, item, spider):
        if not item['title']:
            # titleフィールドが取得できていない場合は破棄する。
            # DropItem()の引数は破棄する理由を表すメッセージ。
            raise DropItem('Missing title')

        return item  # titleフィールドが正しく取得できている場合。
