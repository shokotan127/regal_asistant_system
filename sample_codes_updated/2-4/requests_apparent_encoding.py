import sys
import requests

url = sys.argv[1]  # 第1引数からURLを取得する。
r = requests.get(url)  # URLで指定したWebページを取得する。
r.encoding = r.apparent_encoding  # バイト列の特徴から推定したエンコーディングを使用する。
print(f'encoding: {r.encoding}', file=sys.stderr)  # エンコーディングを標準エラー出力に出力する。
print(r.text)  # デコードしたレスポンスボディを標準出力に出力する。
