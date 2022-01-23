import os

from requests_oauthlib import OAuth1Session

# 環境変数から認証情報を取得する。
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET_KEY = os.environ['TWITTER_API_SECRET_KEY']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# 認証情報を使ってOAuth1Sessionオブジェクトを得る。
twitter = OAuth1Session(TWITTER_API_KEY,
                        client_secret=TWITTER_API_SECRET_KEY,
                        resource_owner_key=TWITTER_ACCESS_TOKEN,
                        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET)

# ユーザーのタイムラインを取得する。
response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

# APIのレスポンスはJSON形式の文字列なので、response.json()でパースしてlistを取得できる。
# statusはツイート（Twitter APIではStatusと呼ばれる）を表すdict。
for status in response.json():
    print('@' + status['user']['screen_name'], status['text'])  # ユーザー名とツイートを表示する。
