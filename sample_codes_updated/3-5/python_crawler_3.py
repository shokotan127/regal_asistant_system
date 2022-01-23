from typing import Iterator
import requests
import lxml.html


def main():
    """
    クローラーのメインの処理。
    """
    session = requests.Session()  # 複数のページをクロールするのでSessionを使う。
    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)  # Sessionを使って詳細ページを取得する。
        ebook = scrape_detail_page(response)  # 詳細ページからスクレイピングして電子書籍の情報を得る。
        print(ebook)  # 電子書籍の情報を表示する。
        break  # まず1ページだけで試すため、break文でループを抜ける。


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
        'price': html.cssselect('.buy')[0].text,  # 価格（.textで直接の子である文字列のみを取得）
        'content': [h3.text_content() for h3 in html.cssselect('#content > h3')],  # 目次
    }
    return ebook  # dictを返す。

if __name__ == '__main__':
    main()
