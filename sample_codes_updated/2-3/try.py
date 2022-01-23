d = {'a': 1, 'b': 2}

try:
    print(d['x'])  # 例外が発生する可能性がある処理。
except KeyError:
    # try節内でexcept節に書いた例外（ここではKeyError）が発生した場合、except節が実行される。
    print('x is not found')  # キーが存在しない場合の処理。
finally:
    # finally節は例外発生の有無によらず、ブロックを抜ける際に実行される。
    # except節とfinally節はどちらかがあれば良い。
    print('post-processing')
