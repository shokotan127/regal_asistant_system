import os
import logging
import json
import html
from datetime import timezone
from io import BytesIO

import tweepy
from google.cloud import bigquery

# 環境変数から認証情報を取得する。
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


def main():
    """
    メインとなる処理。
    """
    # BigQueryのクライアントを作成し、テーブルを取得する。
    client = bigquery.Client()
    table = get_or_create_table(client, 'twitter', 'tweets')
    # OAuthHandlerオブジェクトを作成し、認証情報を設定する。
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    logging.info('Collecting tweets...')
    # OAuthHandlerとStreamListenerを指定してStreamオブジェクトを取得する。
    # MyStreamListenerのコンストラクターにはBigQueryのクライアントとテーブルの参照を渡す。
    stream = tweepy.Stream(auth, MyStreamListener(client, table.reference))
    # 公開されているツイートをサンプリングしたストリームを受信する。
    # 言語を指定していないので、あらゆる言語のツイートを取得できる。
    stream.sample()


def get_or_create_table(client: bigquery.Client, dataset_id: str, table_id: str) -> bigquery.Table:
    """
    BigQueryのデータセットとテーブルを作成する。既に存在する場合は取得する。
    """
    logging.info(f'Creating dataset {dataset_id} if not exists...')
    dataset = client.create_dataset(dataset_id, exists_ok=True)  # データセットを作成または取得する。

    logging.info(f'Creating table {dataset_id}.{table_id} if not exists...')
    table_ref = dataset.table(table_id)
    return client.create_table(  # テーブルを作成または取得する。
        bigquery.Table(table_ref, schema=[
            bigquery.SchemaField('id', 'string', description='ツイートのID'),
            bigquery.SchemaField('lang', 'string', description='ツイートの言語'),
            bigquery.SchemaField('screen_name', 'string', description='ユーザー名'),
            bigquery.SchemaField('text', 'string', description='ツイートの本文'),
            bigquery.SchemaField('created_at', 'timestamp', description='ツイートの日時'),
        ]),
        exists_ok=True
    )


class MyStreamListener(tweepy.StreamListener):
    """
    Streaming APIで取得したツイートを処理するためのクラス。
    """
    def __init__(self, client: bigquery.Client, table_ref: bigquery.TableReference):
        self.client = client
        self.table_ref = table_ref
        self.status_list = []  # BigQueryにまとめてロードするStatusオブジェクトを溜めておくリスト。
        self.num_loaded = 0  # BigQueryにロードした行数。
        super().__init__()  # 親クラスの__init__()を呼び出す。

    def on_status(self, status: tweepy.Status):
        """
        ツイートを受信したときに呼び出されるメソッド。引数はツイートを表すStatusオブジェクト。
        """
        self.status_list.append(status)  # Statusオブジェクトをstatus_listに追加する。

        if len(self.status_list) >= 500:
            # status_listに500件溜まったらBigQueryにロードする。
            self.load_tweets_into_bigquery()

            # num_loadedを増やして、status_listを空にする。
            self.num_loaded += len(self.status_list)
            self.status_list = []
            logging.info(f'{self.num_loaded} rows loaded.')

            # 料金が高額にならないように、5000件をロードしたらFalseを返して終了する。
            # 継続的にロードしたいときは次の2行をコメントアウトしてください。
            if self.num_loaded >= 5000:
                return False

    def load_tweets_into_bigquery(self):
        """
        ツイートデータをBigQueryにロードする。
        """
        # TweepyのStatusオブジェクトのリストを改行区切りのJSON（JSON Lines形式）文字列に変換する。
        # 改行区切りのJSON文字列はBytesIO（メモリ上のファイルオブジェクト）に書き込む。
        bio = BytesIO()
        for status in self.status_list:
            json_text = json.dumps({
                'id': status.id_str,
                'lang': status.lang,
                'screen_name': status.author.screen_name,
                'text': html.unescape(status.text),  # textには文字参照が含まれることがあるので元に戻す。
                # datetimeオブジェクトをUTCのPOSIXタイムスタンプに変換する。
                'created_at': status.created_at.replace(tzinfo=timezone.utc).timestamp(),
            }, ensure_ascii=False)  # ensure_ascii=False は絵文字などの文字化けを回避するハック。
            bio.write(json_text.encode('utf-8'))
            bio.write(b'\n')

        bio.seek(0)  # 先頭から読み込めるようBytesIOを先頭にシークする。

        # BigQueryにデータをロードするジョブを実行する。
        logging.info('Loading tweets into table...')
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)  # JSON Lines形式を指定。
        job = self.client.load_table_from_file(bio, self.table_ref, job_config=job_config)
        job.result()  # ジョブの完了を待つ。エラーを無視する場合は待たなくても良い。

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFOレベル以上のログを出力する。
    main()
