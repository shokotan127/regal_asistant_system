import re
import time
from typing import Iterator
import requests
from pymongo import MongoClient
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def main():
    """
    クローラーのメインの処理。
    """
    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続する。
    collection = client.scraping.ebooks  # scrapingデータベースのebooksコレクションを得る。
    # データを一意に識別するキーを格納するkeyフィールドにユニークなインデックスを作成する。
    collection.create_index('key', unique=True)

    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')  # 一覧ページを取得する。
    urls = scrape_list_page(response)  # 詳細ページのURL一覧を得る。
    for url in urls:
        key = extract_key(url)  # URLからキーを取得する。

        ebook = collection.find_one({'key': key})  # MongoDBからkeyに該当するデータを探す。
        if not ebook:  # MongoDBに存在しない場合だけ、詳細ページをクロールする。
            time.sleep(1)
            response = session.get(url)  # 詳細ページを取得する。
            ebook = scrape_detail_page(response)
            collection.insert_one(ebook)  # 電子書籍の情報をMongoDBに保存する。

        print(ebook)  # 電子書籍の情報を表示する。


def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数。
    """
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.select('#listBook > li > a[itemprop="url"]'):
        url = urljoin(response.url, a.get('href'))  # 絶対URLに変換する。
        yield url


def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する。
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    ebook = {
        'url': response.url,  # URL
        'key': extract_key(response.url),  # URLから抜き出したキー
        'title': soup.select_one('#bookTitle').text,  # タイトル。select_one()はselect()の結果の最初の要素を取得するメソッド。
        'price': soup.select_one('.buy').contents[0].strip(),  # 価格（strip()で前後の空白を削除）
        'content': [normalize_spaces(h3.text) for h3 in soup.select('#content > h3')],  # 目次
    }
    return ebook  # dictを返す。


def extract_key(url: str) -> str:
    """
    URLからキー（URLの末尾のISBN）を抜き出す。
    """
    m = re.search(r'/([^/]+)$', url)  # 最後の/から文字列末尾までを正規表現で取得。
    return m.group(1)


def normalize_spaces(s: str) -> str:
    """
    連続する空白を1つのスペースに置き換え、前後の空白を削除した新しい文字列を取得する。
    """
    return re.sub(r'\s+', ' ', s).strip()

if __name__ == '__main__':
    main()
