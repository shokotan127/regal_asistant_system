import os
import logging
from typing import List  # 型ヒントのためにインポート

import requests
from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.common.exceptions import NoSuchElementException

# WebhookのURLを環境変数から取得する。
SLACK_INCOMING_WEBHOOK_URL = os.environ['SLACK_INCOMING_WEBHOOK_URL']


def main():
    """
    メインの処理。
    """
    options = ChromeOptions()
    # ヘッドレスモードを無効にするには、次の行をコメントアウトする。
    options.headless = True
    driver = Chrome(options=options)  # ChromeのWebDriverオブジェクトを作成する。
    # Windows上の仮想マシンの場合は、前の行をコメントアウトして、次の行のコメントアウトを解除する。
    # driver = Remote('http://10.0.2.2:4444', options=options)

    navigate(driver)  # noteのトップページに遷移する。
    contents = scrape_contents(driver)  # コンテンツのリストを取得する。
    logging.info(f'Found {len(contents)} contents.')  # 取得したコンテンツの数を表示する。

    # スキの数が最も多いコンテンツを取得する。
    content = sorted(contents, key=lambda c: c['like'], reverse=True)[0]
    logging.info(f'Notifying to Slack: {content["url"]}')
    # 取得したコンテンツのスキの数とURLをSlackに通知する。
    requests.post(SLACK_INCOMING_WEBHOOK_URL, json={
        'text': f':heart: {content["like"]} {content["url"]}',
        'unfurl_links': True,  # リンクのタイトルや画像を表示する。
    })

    driver.quit()  # ブラウザーを終了する。


def navigate(driver: Remote):
    """
    目的のページに遷移する。
    """
    logging.info('Navigating...')
    driver.get('https://note.mu/')  # noteのトップページを開く。
    assert 'note' in driver.title  # タイトルに'note'が含まれていることを確認する。


def scrape_contents(driver: Remote) -> List[dict]:
    """
    文章コンテンツのURL、タイトル、概要、スキの数を含むdictのリストを取得する。
    """
    contents = []  # 取得したコンテンツを格納するリスト。

    # コンテンツを表すdiv要素について反復する。
    for div in driver.find_elements_by_css_selector('.o-timeline__item'):
        a = div.find_element_by_css_selector('a')
        try:
            description = div.find_element_by_css_selector('p').text
        except NoSuchElementException:
            description = ''  # 画像コンテンツなどp要素がない場合は空文字にする。

        # URL、タイトル、概要、スキの数を取得して、dictとしてリストに追加する。
        contents.append({
            'url': a.get_attribute('href'),
            'title': div.find_element_by_css_selector('h3').text,
            'description': description,
            'like': int(div.find_element_by_css_selector('.o-noteStatus__item--like .o-noteStatus__label').text),
        })

    return contents

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # INFOレベル以上のログを出力する。
    main()
