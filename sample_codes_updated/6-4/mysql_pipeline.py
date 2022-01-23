import MySQLdb


class MySQLPipeline:
    """
    ItemをMySQLに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMySQLサーバーに接続する。
        itemsテーブルが存在しない場合は作成する。
        """
        settings = spider.settings  # settings.pyから設定を読み込む。
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'scraping'),  # データベース名
            'user': settings.get('MYSQL_USER', ''),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', ''),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続。
        self.c = self.conn.cursor()  # カーソルを取得。
        # itemsテーブルが存在しない場合は作成。
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `items` (
                `id` INTEGER NOT NULL AUTO_INCREMENT,
                `title` VARCHAR(200) NOT NULL,
                PRIMARY KEY (`id`)
            )
        """)
        self.conn.commit()  # 変更をコミット。

    def close_spider(self, spider):
        """
        Spiderの終了時にMySQLサーバーへの接続を切断する。
        """
        self.conn.close()

    def process_item(self, item, spider):
        """
        Itemをitemsテーブルに挿入する。
        """
        self.c.execute('INSERT INTO `items` (`title`) VALUES (%(title)s)', dict(item))
        self.conn.commit()  # 変更をコミット。
        return item
