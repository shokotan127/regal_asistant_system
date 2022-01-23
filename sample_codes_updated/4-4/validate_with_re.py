import re


def validate_price(value: str):
    """
    valueが価格として正しい文字列（数字とカンマのみを含む文字列）であるかどうかを判別し、
    正しくない値の場合は例外ValueErrorを発生させる。
    """
    if not re.search(r'^[0-9,]+$', value):  # 数字とカンマのみを含む正規表現にマッチするかチェックする。
        raise ValueError(f'Invalid price: {value}')  # マッチしない場合は例外を発生させる。

validate_price('3,000')  # 価格として正しい文字列なので例外は発生しない。
validate_price('無料')  # 価格として正しくない文字列なので例外が発生する。
