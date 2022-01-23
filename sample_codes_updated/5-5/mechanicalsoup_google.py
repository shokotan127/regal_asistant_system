import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()  # StatefulBrowserオブジェクトを作成する。
browser.open('https://www.google.co.jp/')  # open()メソッドでGoogleのトップページを開く。

# 検索語を入力して送信する。
browser.select_form('form[action="/search"]')  # 検索フォームを選択する。
browser['q'] = 'Python'  # 選択したフォームにある name="q" の入力ボックスに検索語を入力する。
browser.submit_selected()  # 選択したフォームを送信する。

# 検索結果のタイトルとURLを抽出して表示する。
page = browser.get_current_page()  # 現在のページのBeautifulSoupオブジェクトを取得する。
for a in page.select('h3 > a'):  # select()でCSSセレクターにマッチする要素（Tagオブジェクト）のリストを取得する。
    print(a.text)
    print(browser.absolute_url(a.get('href')))  # リンクのURLを絶対URLに変換して表示する。
