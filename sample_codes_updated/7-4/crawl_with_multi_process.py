import concurrent.futures
import logging

import feedparser
import requests
from bs4 import BeautifulSoup


def main():
    # 人気エントリーのRSSからURLのリストを取得する。
    d = feedparser.parse('http://b.hatena.ne.jp/hotentry.rss')
    urls = [entry.link for entry in d.entries]
    logging.info(f'Extracted {len(urls)} URLs')

    # 最大3プロセスで並行処理するためのExecutorオブジェクトを作成。
    executer = concurrent.futures.ProcessPoolExecutor(max_workers=3)
    futures = []  # Futureオブジェクトを格納しておくためのリスト。
    for url in urls:
        # 関数の実行をスケジューリングし、Futureオブジェクトを得る。
        # submit()の第2引数以降はfetch_and_scrape()関数の引数として渡される。
        future = executer.submit(fetch_and_scrape, url)
        futures.append(future)

    # Futureオブジェクトを完了したものから取得する。
    for future in concurrent.futures.as_completed(futures):
        print(future.result())  # Futureオブジェクトから結果（関数の戻り値）を取得して表示する。


def fetch_and_scrape(url: str) -> dict:
    """
    引数で指定したURLのページを取得して、URLとタイトルを含むdictを返す。
    """
    logging.info(f'Start downloading {url}')

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return {
        'url': url,
        'title': soup.title.text.strip(),
    }

if __name__ == '__main__':
    # INFOレベル以上のログを出力し、ログにプロセスIDを含める。
    logging.basicConfig(level=logging.INFO, format='[%(process)d] %(message)s')
    main()
