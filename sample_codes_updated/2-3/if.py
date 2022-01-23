a = 1

# if文で処理を分岐できる。
if a == 1:
    print('a is 1')  # if文の式が真のときに実行される。
elif a == 2:
    print('a is 2')  # elif節の式が真のときに実行される（elif節はなくても良い）。
else:
    print('a is not 1 nor 2')  # どの条件にも当てはまらなかったときに実行される（else節はなくても良い）。

print('a is 1' if a == 1 else 'a is not 1')  # 条件式で1行で書ける。可読性が下がるので多用しない。
