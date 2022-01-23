from pyquery import PyQuery as pq

# HTMLファイルを読み込んでPyQueryオブジェクトを得る。
d = pq(filename='dp.html')
d.make_links_absolute('https://gihyo.jp/dp')  # すべてのリンクを絶対URLに変換する。

# d()でセレクターに該当するa要素のリストを取得して、個々のa要素に対して処理を行う。
for a in d('#listBook > li > a[itemprop="url"]'):
    # a要素のhref属性から書籍のURLを取得する。
    # 変数aで取得できるのはlxmlのElementなので、d(a)としてPyQueryオブジェクトを取得している。
    url = d(a).attr('href')

    # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
    p = d(a).find('p[itemprop="name"]').eq(0)
    title = p.text()

    # 書籍のURLとタイトルを出力する。
    print(url, title)
