import sys
import re
import requests

url = sys.argv[1]  # 第1引数からURLを取得する。
r = requests.get(url)  # URLで指定したWebページを取得する。

# charsetはHTMLの最初のほうに書かれていると期待できるので、
# レスポンスボディの先頭1024バイトをASCII文字列としてデコードする。
# ASCII範囲外の文字はU+FFFD（REPLACEMENT CHARACTER）に置き換え、例外を発生させない。
scanned_text = r.content[:1024].decode('ascii', errors='replace')

# デコードした文字列から正規表現でcharsetの値を抜き出す。
match = re.search(r'charset=["\']?([\w-]+)', scanned_text)
if match:
    r.encoding = match.group(1)  # charsetが見つかった場合は、その値を使用する。
else:
    r.encoding = 'utf-8'  # charsetが明示されていない場合はUTF-8とする。

print(f'encoding: {r.encoding}', file=sys.stderr)  # エンコーディングを標準エラー出力に出力する。
print(r.text)  # デコードしたレスポンスボディを標準出力に出力する。
