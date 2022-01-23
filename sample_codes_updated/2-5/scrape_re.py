import re
from html import unescape
from urllib.parse import urljoin

# 前節でダウンロードしたファイルを開き、中身を変数htmlに格納する。
with open('dp.html') as f:
    html = f.read()

# re.findall()を使って、書籍1冊に相当する部分のHTMLを取得する。
# *?は*と同様だが、なるべく短い文字列にマッチする（non-greedyである）ことを表すメタ文字。
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
    # 書籍のURLは itemprop="url" という属性を持つa要素のhref属性から取得する。
    url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
    url = urljoin('https://gihyo.jp/', url)  # 相対URLを絶対URLに変換する。

    # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
    title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)  # まずはp要素全体を取得する。
    title = title.replace('<br/>', ' ')  # brタグをスペースに置き換える。str.replace()は文字列を置換する。
    title = re.sub(r'<.*?>', '', title)  # タグを取り除く。
    title = unescape(title)  # 文字参照（後のコラムを参照）が含まれている場合は元に戻す。

    print(url, title)
