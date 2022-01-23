import requests
from cachecontrol import CacheControl  # pip install CacheControl[filecache]
from cachecontrol.caches import FileCache

session = requests.Session()
# sessionをラップしたcached_sessionを作る。
# キャッシュはファイルとして .webcache ディレクトリ内に保存する。
cached_session = CacheControl(session, cache=FileCache('.webcache'))

response = cached_session.get('https://docs.python.org/3/')  # 通常のSessionと同様に使用する。

# response.from_cache属性でキャッシュから取得されたレスポンスかどうかを取得できる。
print(f'from_cache: {response.from_cache}')  # 初回はFalse。2回目以降はTrue。
print(f'status_code: {response.status_code}')  # ステータスコードを表示。
print(response.text)  # レスポンスボディを表示。
