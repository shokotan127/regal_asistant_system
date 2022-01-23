import re

from pyqs import task
import lxml.html
from pymongo import MongoClient


@task(queue='ebook')
def scrape(key: str):
    """
    ワーカーで実行するタスク。
    """
    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続する。
    html_collection = client.scraping.ebook_htmls  # scrapingデータベースのebook_htmlsコレクションを得る。

    ebook_html = html_collection.find_one({'key': key})  # MongoDBからkeyに該当するデータを探す。
    ebook = scrape_detail_page(key, ebook_html['url'], ebook_html['html'])

    ebook_collection = client.scraping.ebooks  # ebooksコレクションを得る。
    # keyで高速に検索できるように、ユニークなインデックスを作成する。
    ebook_collection.create_index('key', unique=True)
    # ebookを保存する。複数回実行してもエラーにならないようupsertを使用する。
    ebook_collection.update_one({'key': key}, {'$set': ebook}, upsert=True)


def scrape_detail_page(key: str, url: str, html: str) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで得る。
    """
    root = lxml.html.fromstring(html)
    ebook = {
        'url': url,  # URL
        'key': key,  # URLから抜き出したキー
        'title': root.cssselect('#bookTitle')[0].text_content(),  # タイトル
        'price': root.cssselect('.buy')[0].text.strip(),  # 価格
        'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],  # 目次
    }
    return ebook


def normalize_spaces(s: str) -> str:
    """
    連続する空白を1つのスペースに置き換え、前後の空白を削除した新しい文字列を取得する。
    """
    return re.sub(r'\s+', ' ', s).strip()
