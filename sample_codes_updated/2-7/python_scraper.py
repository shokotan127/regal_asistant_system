import csv
from typing import List  # 型ヒントのためにインポート

import requests
import lxml.html


def main():
    """
    メインの処理。fetch(), scrape(), save()の3つの関数を呼び出す。
    """

    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('books.csv', books)


def fetch(url: str) -> str:
    """
    引数urlで与えられたURLのWebページを取得する。
    WebページのエンコーディングはContent-Typeヘッダーから取得する。
    戻り値：str型のHTML
    """

    r = requests.get(url)
    return r.text  # HTTPヘッダーから取得したエンコーディングでデコードした文字列を返す。


def scrape(html: str, base_url: str) -> List[dict]:
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す。
    引数base_urlは絶対URLに変換する際の基準となるURLを指定する。
    戻り値：書籍 (dict) のリスト
    """

    books = []
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)  # すべてのa要素のhref属性を絶対URLに変換する。

    # cssselect()メソッドで、セレクターに該当するa要素のリストを取得して、個々のa要素に対して処理を行う。
    # セレクターの意味：id="listBook"である要素 の直接の子である li要素 の直接の子である itemprop="url"という属性を持つa要素 
    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        # a要素のhref属性から書籍のURLを取得する。
        url = a.get('href')

        # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()  # wbr要素などが含まれるのでtextではなくtext_content()を使う。

        books.append({'url': url, 'title': title})

    return books


def save(file_path: str, books: List[dict]):
    """
    引数booksで与えられた書籍のリストをCSV形式のファイルに保存する。
    ファイルのパスは引数file_pathで与えられる。
    戻り値：なし
    """

    with open(file_path, 'w', newline='') as f:
        # 第1引数にファイルオブジェクトを、第2引数にフィールド名のリストを指定する。
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()  # 1行目のヘッダーを出力する。
        # writerows()で複数の行を一度に出力する。引数は辞書のリスト。
        writer.writerows(books)


# pythonコマンドで実行された場合にmain()関数を呼び出す。これはモジュールとして他のファイルから
# インポートされたときに、main()関数が実行されないようにするための、Pythonにおける一般的なイディオム。
if __name__ == '__main__':
    main()
