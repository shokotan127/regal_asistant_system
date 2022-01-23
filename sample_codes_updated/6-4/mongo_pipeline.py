from pymongo import MongoClient


class MongoPipeline:
    """
    ItemをMongoDBに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMongoDBに接続する。
        """
        self.client = MongoClient('localhost', 27017)  # ホストとポートを指定してクライアントを作成。
        self.db = self.client['scraping-book']  # scraping-book データベースを取得。
        self.collection = self.db['items']  # items コレクションを取得。

    def close_spider(self, spider):
        """
        Spiderの終了時にMongoDBへの接続を切断する。
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Itemをコレクションに追加する。
        """
        # insert_one()の引数は書き換えられるので、コピーしたdictを渡す。
        self.collection.insert_one(dict(item))
        return item
