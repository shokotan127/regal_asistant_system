from jsonschema import validate  # pip install jsonschema

# 次の4つのルールを持つスキーマ（期待するデータ構造）を定義する。
schema = {
    "type": "object",  # ルール1: 値はJSONにおけるオブジェクト（Pythonにおけるdict）である。
    "properties": {
        # ルール2：nameの値は文字列である。
        "name": {
            "type": "string"
        },
        # ルール3：priceの値は文字列で、patternに指定した正規表現にマッチする。
        "price": {
            "type": "string",
            "pattern": "^[0-9,]+$"
        }
    },
    "required": ["name", "price"]  # ルール4：dictのキーとしてnameとpriceは必須である。
}

# validate()関数は、第1引数のオブジェクトを第2引数のスキーマでバリデーションする。
validate({
    'name': 'ぶどう',
    'price': '3,000',
}, schema)  # スキーマに適合するので例外は発生しない。

validate({
    'name': 'みかん',
    'price': '無料',
}, schema)  # スキーマに適合しないので、例外jsonschema.exceptions.ValidationErrorが発生する。
