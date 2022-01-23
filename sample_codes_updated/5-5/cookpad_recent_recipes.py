import os
import logging

import mechanicalsoup

# 認証の情報は環境変数から取得する。
COOKPAD_LOGIN = os.environ['COOKPAD_LOGIN']
COOKPAD_PASSWORD = os.environ['COOKPAD_PASSWORD']


def main():
    browser = mechanicalsoup.StatefulBrowser()

    # 最近見たレシピのページを開く。
    logging.info('Navigating...')
    browser.open('https://cookpad.com/recipe/history')

    # ログインページにリダイレクトされていることを確認する。
    assert '/login' in browser.get_url()

    # ログインフォーム（class="login_form" の要素内にあるform）を埋める。
    browser.select_form('.login_form form')
    browser['login'] = COOKPAD_LOGIN  # name="login" という入力ボックスを埋める。
    browser['password'] = COOKPAD_PASSWORD  # name="password" という入力ボックスを埋める。

    # フォームを送信する。
    logging.info('Signing in...')
    browser.submit_selected()

    # ログインに失敗する場合は、次のいずれかの行のコメントを外して確認すると良い。
    # browser.launch_browser()  # 現在のページのHTMLをブラウザーで表示する（macOSなどGUIの環境のみ）。
    # print(browser.get_current_page().prettify())  # 現在のページのHTMLソースを表示する。

    # 最近見たレシピのページが表示されていることを確認する。
    assert '最近見たレシピ' in browser.get_current_page().title.string

    # 最近見たレシピの名前とURLを表示する。
    for a in browser.get_current_page().select('#main a.recipe-title'):
        print(a.text)
        print(browser.absolute_url(a.get('href')))  # href属性の値は相対URLなので、絶対URLに変換する。

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFOレベル以上のログを出力する。
    main()
