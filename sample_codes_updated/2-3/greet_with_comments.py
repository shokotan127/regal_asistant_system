import sys  # import文でsysモジュールを読み込む。

# def文でgreet()関数を定義する。インデントされている行が関数の中身を表す。
def greet(name):
    # 組み込み関数print()は文字列を出力する。
    # f'...' の文字列内部では {変数名} で変数を展開できる。
    print(f'Hello, {name}!')

# if文でもインデントが範囲を表す。sys.argvはコマンドライン引数のリストを表す変数。
if len(sys.argv) > 1:
    # if文の条件が真のとき
    name = sys.argv[1]  # 変数は定義せずに代入できる。
    greet(name)  # nameを引数としてgreet()関数を呼び出す。
else:
    # if文の条件が偽のとき
    greet('world')  # 文字列 'world' を引数としてgreet()関数を呼び出す。

