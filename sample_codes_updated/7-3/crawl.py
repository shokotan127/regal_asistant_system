import time
import re
from typing import Iterator
import logging

import requests
import lxml.html
from pymongo import MongoClient

from scraper_tasks import scrape


def main():
    """
    クローラーのメインの処理。
    """
    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続する。
    collection = client.scraping.ebook_htmls  # scrapingデータベースのebook_htmlsコレクションを得る。
    # keyで高速に検索できるように、ユニークなインデックスを作成する。
    collection.create_index('key', unique=True)

    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')  # 一覧ページを取得する。
    urls = scrape_list_page(response)  # 詳細ページのURL一覧を得る。
    for url in urls:
        key = extract_key(url)  # URLからキーを取得する。

        ebook_html = collection.find_one({'key': key})  # MongoDBからkeyに該当するデータを探す。
        if not ebook_html:  # MongoDBに存在しない場合だけ、詳細ページをクロールする。
            time.sleep(1)
            logging.info(f'Fetching {url}')
            response = session.get(url)  # 詳細ページを取得する。

            # HTMLをMongoDBに保存する。
            collection.insert_one({
                'url': url,
                'key': key,
                'html': response.content,
            })
            scrape.delay(key)  # キューにタスクを追加する。


def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数。
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url


def extract_key(url: str) -> str:
    """
    URLからキー（URLの末尾のISBN）を抜き出す。
    """
    m = re.search(r'/([^/]+)$', url)  # 最後の/から文字列末尾までを正規表現で取得。
    return m.group(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFOレベル以上のログを出力する。
    main()
