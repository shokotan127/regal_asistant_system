import time  # timeモジュールをインポートする。
from typing import Iterator
import requests
import lxml.html


def main():
    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        time.sleep(1)  # 1秒のウェイトを入れる
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)
        # break


def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数。
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する。
    """
    html = lxml.html.fromstring(response.text)
    ebook = {
        'url': response.url,  # URL
        'title': html.cssselect('#bookTitle')[0].text_content(),  # タイトル
        'price': html.cssselect('.buy')[0].text.strip(),  # 価格（strip()で前後の空白を削除）
        'content': [h3.text_content() for h3 in html.cssselect('#content > h3')],  # 目次
    }
    return ebook  # dictを返す。

if __name__ == '__main__':
    main()
