import lxml.html
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.scraping  # scrapingデータベースを取得する。
collection = db.books  # booksコレクションを取得する。
# このスクリプトを何回実行しても同じ結果になるようにするため、コレクションのドキュメントをすべて削除する。
collection.delete_many({})

# HTMLファイルを読み込み、getroot()メソッドでHtmlElementオブジェクトを得る。
tree = lxml.html.parse('dp.html')
html = tree.getroot()
# 引数のURLを基準として、すべてのa要素のhref属性を絶対URLに変換する。
html.make_links_absolute('https://gihyo.jp/')

# cssselect()メソッドで、セレクターに該当するa要素のリストを取得して、個々のa要素に対して処理を行う。
# セレクターの意味：id="listBook"である要素 の子である li要素 の子である itemprop="url"という属性を持つa要素
for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
    # a要素のhref属性から書籍のURLを取得する。
    url = a.get('href')

    # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
    p = a.cssselect('p[itemprop="name"]')[0]
    title = p.text_content()  # wbr要素などが含まれるのでtextではなくtext_content()を使う。

    # 書籍のURLとタイトルをMongoDBに保存する。
    collection.insert_one({'url': url, 'title': title})

# コレクションのすべてのドキュメントを_idの順にソートして取得する。
for link in collection.find().sort('_id'):
    print(link['_id'], link['url'], link['title'])
