# Data Analytics アウトライン
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/28c9314a-7bb9-4e8e-b275-9771974a3cac/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/37069647-5d4a-429c-a852-d8ad92711760/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1a7cd662-1274-4c1e-8ddf-ac2e959e5490/Untitled.png)

# Data Warehouse（BigQuery, Dataproc）
# Data Warehouse

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e8d322fa-55e4-4923-8742-88bf579afa8c/Untitled.png)

- 大規模なデータを集約、保存、管理するためのデータベースシステム

## BigQuery

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/624e5931-32fa-4c76-9490-313eb3d775cf/Untitled.png)

### データサンプル

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/34d49f43-5aae-481e-bc6c-0b0e5eb7e08d/Untitled.png)

- 数ペタバイト規模のデータにもクエリを実行できる

### 処理の特徴

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4867d723-f1bd-4fce-bbb9-50156c5ef7f6/Untitled.png)

### BigQueryの活用事例

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/898bca21-01b2-4bd7-bdb1-70ca50e26436/Untitled.png)

### 料金体系と料金項目

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/977eeffe-afc7-4c09-b58d-ced40d406919/Untitled.png)

- 料金項目
    - オンデマンド・・・使用量に応じて
    - 定額料金・・・指定した期間に応じて
- 料金体系
    - 分析料金・・・クエリ処理にかかる費用
    - ストレージ料金・・・BigQueryに読み込むデータを保存する費用

## Dataproc

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/88ea069b-8c3f-42ce-8e9f-26c76e04bdfb/Untitled.png)

- Google Cloudが提供するマネージドなHadoop/Sparkサービス

### Hadoop

- 大規模なデータを並列分散処理するアーキテクチャ。Apacheが管理するオープンソース
- 認定試験では、詳細な構成を問われることはない
    - Cloud DataprocでHadoopを使用できるという事実のみ知っていればOK
- 構成
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1f07fdfc-b513-4149-8486-ea92ed773643/Untitled.png)
    
    - HDFS
        - 大規模なデータを分散して保存する
        - GoogleCloudでは、HDFSの代わりにCloudStorageを使用することができる
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/efa312c6-78b9-48e8-89da-5b6a4adda953/Untitled.png)
    
    - HBase
        - マスターノード
            - クラスタ全体の管理や制御を行う
        - ZooKeeper
            - クラスタの状態を監視し、マスターノードの故障の検出やリーダーの選出を行う
        - クライアントノード
            - HDFSへのクエリを行うインターフェース
        - スレーブノード
            - 実際のデータの保存や操作を担当するノード。マスターノードの指示のもと動作する
    - HDFS
        - 特定のノードが中心的な役割を果たしている
        - マスタノード
            - クラスタ全体のメタデータや、ファイルシステムの管理
        - クライアントノード
            - ファイルの読み書きをHDFS上で行うためのインターフェース
        - スレーブノード
            - 実際のデータの保存や操作を担当するノード。マスターノードの指示のもと動作する
    
    ### MapReduceのアーキテクチャ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/cb161c07-590d-4851-9a89-5731da3c8ac3/Untitled.png)
    

### 用途に応じたスケール

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/77deab14-c3d2-452f-b5d4-3be16378b644/Untitled.png)

ストレージとcomputeを分離してそれぞれでスケールすることが可能

Storage

- CloudStorageやCloudSQL

ユースケースに応じてcomputeをスケール

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/da905ba8-f823-41cc-96fd-d3ec1433aadd/Untitled.png)

## Dataprocを中心としたアーキテクチャ構成図

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8fee5e6e-9834-4112-bbe1-2e4ec5f5043e/Untitled.png)

### Dataproc Hub

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/299b13d4-7a30-4098-8611-315dc2498976/Untitled.png)

# Messaging (Pub)
## データ取り込みの方法

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8e481ced-ba3c-4648-853f-0a7159dbcbe8/Untitled.png)

- データの取り込みには、リアルタイムの取り込みとバッチの取り込みの2種類がある
- メッセージキューイングサービスはリアルタイムなデータ取り込みを効率的に行うためのツールの一つとなる

## Cloud Pub/Sub

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/57f44f55-3006-4b7b-85bd-60bb3e41af73/Untitled.png)

- メッセージキューイングサービス
    - メッセージをキュー(待ち行列)に入れて、非同期に処理をすること
- トピックとサブスクリプションは1対1に対応する

### メッセージ送信の確実性を担保する仕組み

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/09fab5f3-a19f-406a-909f-512c29db40da/Untitled.png)

### 設定

## (ハンズオン) Cloud Pub/Subの操作
## トピックの作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/686907de-0237-48cb-9210-673b48fcc45a/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/86aae964-eff1-4910-96e6-7bec6bc31164/Untitled.png)

- 「デフォルトのサブスクリプションを追加する」を選択し作成

Pub/Sub トピックが生成される

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7c398ec7-3a28-4a4b-8b17-fde1c4d7e57c/Untitled.png)