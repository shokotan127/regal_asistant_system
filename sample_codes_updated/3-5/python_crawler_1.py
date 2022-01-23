import requests
import lxml.html

response = requests.get('https://gihyo.jp/dp')
html = lxml.html.fromstring(response.text)
html.make_links_absolute(response.url)  # 絶対URLに変換する。

for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
    url = a.get('href')
    print(url)
