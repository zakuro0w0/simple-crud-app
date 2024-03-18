## コンテナで使いたいaliasを設定する
cp .devcontainer/.bash_aliases ~/.bash_aliases

## ホスト側で使っていて、コンテナでも使いたいsshの設定をコピーする
## .devcontainer/.ssh/配下に予めconfigや秘密鍵を配置しておくこと
cp .devcontainer/.ssh/* ~/.ssh/

## python関連パッケージのインストール
pip install -r requirements.txt

## GCPサービスアカウントキーを環境変数に設定する
export GOOGLE_APPLICATION_CREDENTIALS=".devcontainer/gcp-service-account-key.json"

