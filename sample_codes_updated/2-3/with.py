# open()関数の戻り値を変数fに代入し、with節のブロック内で使う。
# このブロックを抜ける際（例外発生時を含む）に、f.close()が自動的に呼び出される。
with open('index.html') as f:
    print(f.read())

# このwith文の処理は次のコードと同等。
f = open('index.html')
try:
    print(f.read())
finally:
    f.close()
