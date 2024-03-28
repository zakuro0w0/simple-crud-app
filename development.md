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

## オニオンアーキテクチャにする
- ディレクトリ構成を以下のように変更

```py
app/ # FastAPIプロジェクトのルートディレクトリ
├── application/ # application層: ユースケースやビジネスロジックを定義する
│   ├── __init__.py
│   └── task_service.py
├── domain/ # domain層: ドメインオブジェクトやエンティティを定義する
│   ├── __init__.py
│   └── task.py
├── infrastructure/ # infrastructure層: データベースやキャッシュへのアクセスを定義する
│   ├── __init__.py
│   └── task_repository.py
├── interface/ # interface層(presentation層): ユーザーインターフェイスやAPIを定義する
│   ├── __init__.py
│   ├── controller.py # ユースケースやリポジトリの生成知識を隠蔽する
│   ├── models.py # webAPIのリクエスト/レスポンスモデルを定義する
│   └── routes.py # FastAPIのルーティングを定義する
└── main.py # FastAPIプログラムのエントリポイント
```

### オニオンアーキテクチャのシーケンス図
```plantuml
participant interface
participant application
participant domain
participant infrastructure

-> interface: webAPIリクエスト
interface -> application: ユースケースの呼び出し
application -> domain: 必要に応じてドメインオブジェクトを操作
application -> infrastructure: データベースへのアクセス
infrastructure -> application: データベースからの結果
application -> interface: ユースケースの結果を返す
<- interface : レスポンスの生成&送信
```

## ドメインモデルとwebAPIの入出力モデルについて
- 例えばToDo管理アプリではDBにToDoとなるタスクを登録するユースケースがある
- このタスクをドメインモデルとして定義すると以下のようになる

```py
class Task(BaseModel):
  """
  タスクモデル。

  属性:
  title: str - タスクのタイトル。
  description: str - タスクの説明。
  completed: bool - タスクの完了状態。デフォルトはFalse。
  created_at: datetime - タスクの作成時刻。デフォルトは現在時刻。
  updated_at: datetime - タスクの最終更新時刻。デフォルトは現在時刻。
  """

  title: str
  description: str
  completed: bool = False
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)
```

- 一方でタスクを登録するPOSTリクエストのbodyに必要なモデルは以下のようになる

```py
class TaskCreateIn(BaseModel):
  """
  タスクの入力モデルを表します。

  属性:
      title (str): タスクのタイトルです。
      description (str): タスクの説明です。
  """

  title: str
  description: str
```

- `Task`にあったいくつかの属性は`TaskCreateIn`では不要となる
- このように、ドメインモデルとwebAPIの入出力モデルは必ずしも一致しない
- webAPIの設計によっては`requied`なデータと`optional`なデータに分かれるため、そこでもドメインモデルと一致しない場合が出てくる
- 無理に共通化するべきではなく、ドメインモデルとwebAPIの入出力モデルは別々に定義するべき
  - このトレードオフとして、ドメインモデル変更時にwebAPIの入出力モデルも変更する必要がある
