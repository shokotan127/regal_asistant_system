#!/bin/bash

# このシェルスクリプトがあるディレクトリに移動する。
cd $(dirname $0)

# 仮想環境を有効にする。
. scraping/bin/activate

# PyQSのワーカーを実行する。
# .envファイルの環境変数が必要な場合は、forego runをつける。
pyqs ebook --loglevel INFO
