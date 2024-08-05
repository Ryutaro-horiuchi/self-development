# アウトライン
## 全体像

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/502a8b94-d51b-4c54-bd6a-cbaf2706a356/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0d24a284-7be0-4047-9e17-3ff89a455b8c/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/054bc56d-e692-4a82-aade-e54e451449e9/Untitled.png)

## GoogleCloud データベースの一般的な利点

### 高カスタマイズ性とスケーラビリティ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8303c79f-234e-40ba-b393-f7d58ca06b65/Untitled.png)

### パフォーマンス

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c3ee6c90-cc26-48f9-877c-4a9e482879ff/Untitled.png)

- 読み書き可能なインスタンス → Primary Instance
- 読み取り専用のレプリカ → Read-Replica

### 高可用性

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/94feca0a-c942-46fa-84d3-77c4339f355a/Untitled.png)

- 図はマルチゾーンのフェイルオーバー構成

### バックアップとリストア

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/49c13dec-ceb9-4a37-9fee-622a0fe38f6b/Untitled.png)

[バックアップ設計](https://www.notion.so/d2b56b2d96a64ce19b89568c36ec58b0?pvs=21) 

### セキュリティ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/473fcfea-db22-47a0-b457-22b73bac3abe/Untitled.png)

### メンテナンスとモニタリング / ロギング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fcbd9cb0-e26a-4edb-990d-679ad6fd4938/Untitled.png)

### 料金従量制

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f1511e74-b922-47f2-833d-a90b6992a593/Untitled.png)

# Relational Database (Cloud SQL, Cloud Spanner)
## Cloud SQL

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/28805991-ba1b-4601-9b6a-75c97fc54fbc/Untitled.png)

- 管理タスクがGoogleによって自動的に行われる
- 自動フェイルオーバーを提供している
- スケーリングが数分で行われるため、DBのサイズ、CPU、メモリを簡単に拡張できる

### RDBMSの種類

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/443cd67a-86c8-4339-8bb7-3dcb131970f7/Untitled.png)

### Cloud SQL Auth Proxy

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/901d7b1e-e16a-434e-99c2-206db9bfb196/Untitled.png)

### MySQLの設定画面

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0fc607ba-8d30-42ca-becc-eb5fbe5c8a93/Untitled.png)

### マシンタイプのカスタマイズ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/81f409bf-ec69-49a9-95bd-694c0256ab73/Untitled.png)

- データベースエンジンによって、使用可能なスペックが異なる点は抑えておく

## Cloud Spanner

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/73edf404-2107-4b9e-9ff6-ce41aaa5edb4/Untitled.png)

- **グローバルスケール**のRDB
    
    <aside>
    💡 認定試験で「グローバルスケール」と出たら、Cloud Spanner
    
    </aside>
    
- 高可用性 99.999%
- 動的なスケーリング(リソースを動的に作成したり削除したり)
    - 動的なスケーリングを提供する際、一般的にトランザクションは難しいが、Cloud Spannerでは強力なトランザクション整合性を持っている
- 標準のSQLを使用することが可能

### トランザクションとは

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b6c5892b-0404-4b72-bf35-31b976cd7cdb/Untitled.png)

- ACIDのサンプル
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0065bb63-1b74-4a3f-b4d0-4ec04d4e0e7c/Untitled.png)
    

### シャーディングとは

- DBのデータを複数の部分(シャード)に分割して保存すること
- ベストプラクティス
    - ランダムな値を主キーとすることで、データのホットスポットを防いている、均等なデータの

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2e9ab8b4-e212-46cb-92a6-109629f433de/Untitled.png)

## ハンズオン
### Cloud SQLの基礎とテーブル作成
## インスタンス作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9120e856-3bd9-4682-a8e7-5b882d94ee17/Untitled.png)

- 使用したいDBエンジンを選択する
- 今回はMySQL

### エディションの選択

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2726af2c-4302-4b48-bcd7-4b8c97a22558/Untitled.png)

- 今回はEnterprise

### プリセット

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1655f59e-369e-408a-a985-06ad359c210f/Untitled.png)

- 今回はサンドボックス

### インスタンスの情報

- バージョンの選択
    - メジャー
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/081a5a7d-7abe-4c0b-b2db-a648bf5c4f3f/Untitled.png)
        
    - マイナー
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/87f35dfa-d48f-4443-89a1-a4770b4c4df7/Untitled.png)
        
    
    今回はMySQL8系。マイナーはデフォルト
    
- インスタンスIDとパスワード
    - IDは適当な名前
    - パスワードは今回なしを設定
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ee31e646-76fc-45ac-9c44-74356f086965/Untitled.png)
    

### **リージョンとゾーンの可用性の選択**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/447b48b6-c582-4a62-9ae9-111bc236a559/Untitled.png)

- リージョンは東京
- **高可用性で複数のゾーンを指定することができる**
    - 今回はシングルゾーン

## データベースの作成

- メニューバー > データベースから新規にデータベースを作成できる

## テーブルの作成

- メニューバー > 概要 「Cloud SHELLを開く」からコンソールでテーブルを作成
- 以降、mysql上の操作に入る。割愛

## コンソールの画面

### 概要

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/076243c6-bec7-46b4-b6cd-4e25825ca743/Untitled.png)

### 接続

- 概要
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c999beb9-3a7f-41d2-9dc6-5b28009b7475/Untitled.png)
    
- ネットワーキング
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/61c0196b-eeed-437a-8036-13a469094b70/Untitled.png)
    

### オペレーション

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/42aae431-f907-4ea1-aa75-0c2e6c3878a9/Untitled.png)

### レプリカ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/70f10cce-7271-4a99-ad03-88fa65627e63/Untitled.png)

リードレプリカの作成ができる

- リードレプリカ
    - プライマリの読み取りの負荷軽減
    - バージョン、エディションはプライマリと同様。
    - リージョンやゾーンは選択できる
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f2204697-8e22-4139-b4a6-5ab2fa8963d7/Untitled.png)
    

### バックアップ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2ffe15b9-45f7-4599-bc4e-d498db957ef3/Untitled.png)

- バックアップの時間帯等設定を編集できる
- 手動でバックアップの作成もできる

### Query Insights

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/385d221c-efe8-46a1-8140-60f9de3911f1/Untitled.png)

- 過去のクエリを解析し、どのクエリが時間がかかっているかなどを確認できる

### システム分析情報

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2a8b8436-a595-4ea9-a208-359333cbf575/Untitled.png)

- CPU, ディスクの使用率が確認できる

### Cloud Spannerの基礎
## インスタンスの作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4d73d247-078c-4b92-8b00-5bd8a58746eb/Untitled.png)

→ 「プロビジョニングされたインスタンスを作成」

### インスタンス名を指定する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/066ad988-0b61-48ba-967c-47c7e75c5471/Untitled.png)

### インスタンスを構成する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/49dc1965-5239-439a-b060-8c5ec624747e/Untitled.png)

- リージョン、デュアルリージョン、マルチリージョンが選べる
    - デュアル、マルチはそれぞれデフォルトで用意されている組み合わせから選ぶ
- 今回はリージョンを選択

「作成」

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/640525b8-ccd1-4b65-a2d5-1b9e867700c9/Untitled.png)

## データベースの作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/09545a0e-e7a7-4e29-97b6-950aa3795562/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/988014da-808a-4aa3-87b4-cd833320c3f2/Untitled.png)

- データベースの言語
    - Cloud Spannerでは、Google 標準SQLか、PostgreSQLから選択する
- スキーマの定義
    - テーブルの作成ができる
- 「作成」へ

## テーブルの確認

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a3a40065-0b0d-4ab8-beae-c24e69619536/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ac5b9741-84b6-4216-8d2b-4d44b75d3dd0/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c56a57a7-aa17-41fa-9519-4e13821a0a7f/Untitled.png)

- 左側に作成したテーブルなど構造がわかる
- エディタでクエリがかける
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2e1c596e-b757-459a-b816-4d3aaff2e629/Untitled.png)
    

## コンソール画面

### システム分析情報

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/142a3ddc-de60-417d-96b0-e8f5ef24e03a/Untitled.png)

- Cloud Monitoringをこちらで確認できる

### インポート / エクスポート

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/757603ae-7c45-4c0f-ac84-8fd286fde691/Untitled.png)

- Dataflowからのデータをインポートできる
- 作成したデータをGCSにエクスポートできる

# Non-Relational
# Cloud Bigtable

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4bb3d340-d08e-4b47-b0b0-3a14d16000fc/Untitled.png)

- 大規模な分散をサポートする高性能なNoSQLデータベースサービス
- 時系列データ、分析などのユースケースに用いられる

## 構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e1a35001-d57a-4954-a057-5c73d579e665/Untitled.png)

- Key-Value型のDBを拡張したカラムファミリー型のDB
- まとまりをKeyspaceと呼んでいる
- 1レコードをPartitionという括りに分割して、その中のカラムがKey Valueでひとつずつ管理される

### Partition Keyによって、異なるカラム(Key Value)を持たせることができる

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f00bdd45-5e10-4001-91a8-cc8a78f1ba0d/Untitled.png)

## 特徴

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/dc205466-05be-43ce-9112-aa88e28209bb/Untitled.png)

- 人間が変化に気づくのは13ミリ秒

## ビッグデータ技術のフレームワーク

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0f8793d3-3ce1-41d1-8248-e2383ee632cc/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6ca7b5ec-d2f0-429b-a3dc-3c4b01de0a5c/Untitled.png)

## ユースケース例

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/dc85b6d7-c1d7-40bd-8a3d-e42dd59a23e9/Untitled.png)

# Cloud Firestore

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fb2afe81-c1a0-408c-9155-51574b68e55e/Untitled.png)

- FirebaseはGoogleが買収したリアルタイムなデータ提供を行うプラットフォーム
- データはドキュメントとして保存される
- Firebaseと組み合わせることで、バックエンドサーバーを必要としない

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/881cb05a-c4e5-445d-9e7a-3853f3acc979/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/316aa6f1-7531-441e-b071-be3c8b4a470f/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c69cbcee-fcdb-4f9a-a9d0-66c8403703da/Untitled.png)