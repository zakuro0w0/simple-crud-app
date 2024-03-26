# 開発メモ

## TerraformでFirestoreインスタンスを作る
- GCPリソースの操作にはサービスアカウントのキーが必要
- キーの情報をTerraformに渡せる状態にしておく必要がある
- サービスアカウントのキー作成時にダウンロードできるjsonファイルをローカルに保存
- `terraform.tfvars`で以下のように記述しておくとTerraform環境変数に読み込まれる

```
GOOGLE_APPLICATION_CREDENTIALS = "path/to/gcp-service-account-key.json"
project_id                     = "****************"
region                         = "****************"
```

- 環境変数は`main.tf`などにて`var.{環境変数名}`でアクセスできる

```tf
provider "google" {
  credentials = file("${var.GOOGLE_APPLICATION_CREDENTIALS}")
  project     = var.project_id
  region      = var.region
}
```

- サービスアカウントはTerraformやその他プログラムがリソース操作に使うためのアカウント
- このサービスアカウントはリソース操作に必要な権限を持っている必要がある
  - 権限はロールで表現され、`Cloud Datastoreオーナー`等がある
  - 権限が不足していると`terraform apply`時にエラーが発生する
- サービスアカウントやロールの設定はGCPコンソールのIAMから行う

## Firebase SDKでFirestoreデータベースにデータを挿入する
- Firestoreデータベース名を **`(default)`** にする必要がある点に注意 :warning:
  - Firebase SDKはGCPプロジェクトに紐付くデフォルトのFirestoreデータベースを対象とする
  - つまり、デフォルト名である`(default)`と名付けられたFirestoreデータベースを参照する
  - TerraformのHCLでFirestoreリソースを定義する際、`name`属性を必須で要求されるが、ここを`(default)`にしておかないといけない
  - Firebase SDKでFirestoreデータベース名を明示的に指定することはできない
  - Firebase SDKはサービスアカウントのキーからGCPプロジェクトIDを特定し、アカウントに付与された権限を使って`(default)`データベースにアクセスする
- [insert_firestore.py](./src/insert_firestore.py)のコードで認証し、Firestoreデータベースにデータを挿入できた

![alt text](./images/firebase-sdk-insert.png)
