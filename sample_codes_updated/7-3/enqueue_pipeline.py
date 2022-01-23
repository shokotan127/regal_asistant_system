from scraper_tasks import scrape


class EnqueuePipeline:
    """
    キューにタスクを投入するPipeline。
    """

    def process_item(self, item, spider):
        """
        キーを引数として、キューにタスクを投入する。
        """
        scrape.delay(item['key'])
        return item
