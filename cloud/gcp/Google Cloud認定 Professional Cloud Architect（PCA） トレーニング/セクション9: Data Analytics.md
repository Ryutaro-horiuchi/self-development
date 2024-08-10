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

- トピック・・・送信するためのリソースである

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/686907de-0237-48cb-9210-673b48fcc45a/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/86aae964-eff1-4910-96e6-7bec6bc31164/Untitled.png)

- 「デフォルトのサブスクリプションを追加する」を選択し作成

Pub/Sub トピックが生成される

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7c398ec7-3a28-4a4b-8b17-fde1c4d7e57c/Untitled.png)

## サブスクリプションの作成

- サブスクリプション・・・受信するためのリソース

![Monosnap test-topic – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 11-21-08.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c7c2a02c-3a91-4657-a230-cf896b58bbea/Monosnap_test-topic__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_11-21-08.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/60237b2f-819a-4a94-b6a5-11286378cbdc/image.png)

- サブスクリプションID
    - 任意のID
- 配信タイプ
    - pull サブスクライバーが必要な時にメッセージをpull(リクエスト)する
    - push サブスクライバーにすぐにメッセージをpushする
    - 今回はpull
- メッセージ保持期間
    - 未確認のメッセージの保持期間の指定
        - 「確認済みメッセージを保持」を有効にすると、上記の保持期間が確認ずみのメッセージにも適用される
    - 今回はデフォルトのまま

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ae34df2a-cd8c-49c0-9be9-5fe6510058f3/image.png)

- 確認応答期限
    - Pub/Sub がメッセージを再送信する前にサブスクライバーからの受信確認を待つ時間です
    - 今回はデフォルトのまま
- サブスクリプション フィルタ
    - フィルタ構文が指定されている場合、サブスクライバーはフィルタに一致するメッセージのみを受信する
    - 今回はデフォルトのまま

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bcf80c01-9337-4220-bea4-c5c2b071cd98/image.png)

- 重複対応
    - 下記の項目はパフォーマンスとトレードオフの関係にある
    - 1回限りの配信
        - サブスクリプションに送信されたメッセージが、メッセージの確認応答の期限が切れる前に再送信されないことが保証されます。
        - 今回はデフォルトのまま
    - メッセージの順序指定
        - 同じ順序指定キーがタグ付けされているメッセージは、公開順に受信されます
        - 今回はデフォルトのまま
- デッドレタリング
    - ネットワークエラーなどで配信に失敗した際に、再びオンラインになったタイミングでデッドレターキューから再施行される
    - 今回はデフォルトのまま
- 再試行ポリシー
    - 再試行する場合、すぐに行うか、指数バックオフ期間の経過後に送信するかを選択できる
    - 今回はデフォルトのまま

→ 「作成」

## メッセージを送信する

### トピックからメッセージを送信する

![Monosnap test-topic – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 11-46-57.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/04b76648-9f3d-4790-ad45-ce288696b47c/Monosnap_test-topic__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_11-46-57.png)

- 「メッセージをパブリッシュ」を選択

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ea2d4745-0f97-4770-b469-085622262ffc/image.png)

任意のメッセージを書いて公開(publish)

## メッセージを受信する

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a109cfed-9546-4894-9b9e-07586111cfa7/image.png)

- サブスクリプションを選択する

![Monosnap test-topic-sub – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 11-52-07.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9c90315c-0940-49a3-85fd-1f93a7b50752/Monosnap_test-topic-sub__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_11-52-07.png)

- 任意のサブスクリプション → メッセージタブから「PULL」を選択
    
    

![Monosnap test-topic-sub – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 11-54-00.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1a570dde-4af2-4beb-aacb-3940056936f2/Monosnap_test-topic-sub__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_11-54-00.png)

- メッセージが受信できた

別のサブスクリプションでも、上記の手順でメッセージを受信できる

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/07dcb768-6a40-4046-b300-75e96fad7170/image.png)

### 確認応答する

![Monosnap test-topic-sub-2 – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 12-02-28.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e5a88c85-ef3f-4022-841e-4c30fee93b0f/Monosnap_test-topic-sub-2__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_12-02-28.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c729f86e-d61d-4830-9cf6-d3ffa8427dce/image.png)

- 確認したメッセージが削除された(設定で確認後も保持することも可能)

## スナップショット

![Monosnap スナップショット – Pub:Sub – PCA-Udemy – Google Cloud コンソール 2024-08-10 12-07-06.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/10d3e859-9291-460b-ade7-2ccd991d3887/Monosnap_%E3%82%B9%E3%83%8A%E3%83%83%E3%83%95%E3%82%9A%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88__PubSub__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-08-10_12-07-06.png)

- サブスクリプションのメッセージ確認応答状態をキャプチャしてくれる

## スキーマの作成

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d5ed410d-337b-49f7-a4b7-2f8d871c4bed/image.png)

- 「スキーマを作成」をクリック

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/929b96ea-ea16-4e33-9a73-2da35e19ac1c/image.png)

メッセージのスキーマを設定することができる

- Avroとプロトコルバッファの2種類

- テスト
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4a2dc0d1-1369-40dd-bd64-c207cc314623/image.png)
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f4562b50-f05d-4dc0-b7f0-6eeabda8df9d/image.png)
    
    - スキーマに対して有効か確認できる

# Data Processing （Dataflow, Data Fusion, Dataprep）データ処理・データ加工サービス
## Cloud Dataflow

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c36f6c4a-00cf-46e9-8f97-2719f251966d/image.png)

- バッジとストリーミングの両方に対応
- 一連の処理のことをパイプラインと呼ぶ
- Apache Beamsのサンプル
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9c2cc377-5336-4765-bd31-03307df65bee/image.png)
    

### ウインドウ

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/62770df2-5cd4-4397-8e19-25c44f00a332/image.png)

### Dataflowのサービスイメージ

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1db92fb6-bd90-4e75-9af1-83d2389c895f/image.png)

- ジョブグラフ
    - データの流れと変換を含むパイプラインをビジュアルで表示する
- ジョブ指標
    - ジョブの実行に関する詳細な情報や統計を提供する
    - パフォーマンス、リソースの使用状況、エラーの発生状況をリアルタイムで確認できる

## Cloud Data Fusion

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/01e67182-d06a-47e4-b994-032a2a42d7d3/image.png)

- CDAP
    - データ分析アプリケーションの開発や運用をグラフィカルに可視化して、データフローを抽象化するためのツール
- コードが不要であるため、非エンジニアでも直感的な操作が可能

### 構成要素のイメージ図

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ae93a2ec-d265-48f5-9829-b7374ba81a2d/image.png)

## Cloud Dataprep

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/98110c38-2ce4-45e2-b20d-9023b0ef1a97/image.png)

### 操作イメージ

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/01b5a7c8-35f8-4d9f-8dd5-7c64954e2ff9/image.png)