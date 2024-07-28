- オブジェクトストレージ
    - Cloud Storage
- ブロックストレージ
    - 物理マシーンに紐付けるボリュームをさらに分割して保存する
- ファイルストレージ
    - ディレクトリという階層構造上にファイルを保存する

# Cloud Storage

---

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8c343c25-70e5-4eae-825b-1efc4a13caa2/Untitled.png)

- 高可用性
    - マルチリージョンによる冗長性

### ストレージクラス

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a3bf0a68-2164-465b-a52e-cf94c7c29643/Untitled.png)

- ニアライン、コールドライン、アーカイブは最低保存期間がある
    - 最低保存期間よりも早い削除は、早期削除料金がかかる
- 保存料金と取り出し料金はトレードオフ

### ライフサイクル管理

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c044d92e-6557-4474-a75c-3875de0f5208/Untitled.png)

### 高可用性

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0541c06a-3697-4a82-961b-12898b31ea99/Untitled.png)

- デュアルリージョンストレージクラス(Dual-Region)
    - リージョンの位置を、詳細に制御したい場合に有効
- 料金
    - マルチリージョンストレージ > デュアルリージョンストレージ > リージョナルストレージ

## セキュリティ

---

### 暗号化

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3b175a09-dd32-4330-93f4-95142d32dc31/Untitled.png)

### バージョニング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4ab6b96f-d1fa-4bbf-a8b7-478e568edbc0/Untitled.png)

- 以前のバージョンのオブジェクトを取り出すことができる。つまり、上書き
保存をしても、以前のバージョンのオブジェクトを参照することができる
- 同じKeyでも、IDが違うためバージョニングが可能

### バケットロック

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7b87d092-4092-4d3d-bb7a-4630a0b4a99c/Untitled.png)

一定期間、削除や変更不可の状態にすること

### 署名付きURL

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/68d22c61-eba4-4b0a-bab5-7160f3f194ef/Untitled.png)

- 認証情報を持たないユーザーでも、リソースに対する操作を実行できるようにするために使用される
- 2種類ある
    - リソースベースの署名付きURL
        
        特定のリソースに対して、アクセスを許可するURL
        
    - スコープベースの署名付きURL・・・
        
        特定の操作に対して、アクセスを許可するURL
        
- 署名付きURLの例
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/707211f2-4caa-41ec-8d0a-e7fb8588a930/Untitled.png)
    

### アクセス管理

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e0ffd5f1-2509-4eff-9eb0-b403e60bcf37/Untitled.png)

- 均一な管理
    - バケットレベルのアクセス制御
- きめ細かい管理
    - バケットレベルとオブジェクトレベルの両方でアクセスを制御
- Tips
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/99c20078-8d1e-4067-ad94-5125c444667a/Untitled.png)
    

## 作成画面

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b17e39b1-2953-4241-b2b6-dff93e35b820/Untitled.png)

### ルール

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/82cdbba9-2834-480c-950d-9f1d1dc062de/Untitled.png)

## gsutilコマンド

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7d8b7c35-f590-4bc5-a0f4-e598b271b7ad/Untitled.png)

## アップロードとダウンロードのオプション

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/99de20b4-296f-4f5c-bc43-95656ed144ec/Untitled.png)

- インターネット経由でアップロード、ダウンロードするため、通信状況によって失敗する場合がある
    - → 大きなアップロード、ダウンロードは並列にした方が良い
    - 全て覚える必要はないが、ストリーミング用のオプションがあることも押さえておく。
- 参考
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/aa1d2d85-ac4f-47c5-b621-c37c2ce031d8/Untitled.png)
    
    - 左のグラフ
        - 縦軸がファイルの容量
    - 右のグラフ
        - 縦軸がファイルのアップロードにかかった時間

# Cloud Filestore

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ec4f6f99-5082-4ab4-9c37-a7994f043d5d/Untitled.png)

- IOPS
    - 1秒あたりのデータの書き込み・読み込み
    - IO
        
        データの「書き込み・読み込み」
        
    - PS
        - Per Second(1秒あたりの)
- 最大ランダム読み取りスループット
    - 例
        
        4K画質の映像をストリーミングするには秒あたり400MB必要
        

## Transfer Appliance

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/913bce67-29e7-4711-9d46-2fa86f872807/Untitled.png)

- 物理的にGoogle Cloudへ移行するためのアプライアンス(物理ハードウェア)
- 数十TB以上の大量のデータがある場合に使用する

### アップロード方法の判断

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6d62b66d-1733-4ebb-9fbd-ecd65fbf7e51/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5f57f874-9c42-4d4d-afdb-75cf898ce88c/Untitled.png)

- GCS環境、他のクラウド環境
    
    → Google Transfer Service
    
- コーロケーション施設や接続状態が良い
    - gsutilのコマンド
- 接続状況が悪いオンプレミス環境
    - Google Transfer Appliance


# ハンズオン バケットの設定
## バケットの作成

---

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e49d1470-9c23-463a-8dae-bba7553e4fe2/Untitled.png)

### バケットに名前をつける

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/990c67c1-9674-44ad-9d0f-e34480c50d4e/Untitled.png)

- 今回はラベルは省略

### **データの保存場所の選択**

- Multi-region
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0adb1992-2fb1-412b-a28d-d792725fd1f5/Untitled.png)
    
- Dual-region
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/079b879a-53a8-40f0-8beb-0177c9f3e1a5/Untitled.png)
    
    - 一つを選択すると、組み合わせが不可能なものは非活性になる
- Region
    - 今回はasia-northeast1を選択

### **データのストレージ クラスを選択する**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5f8ba8c0-4702-41ad-93bd-30eb4e8a7222/Untitled.png)

- Autoclass
    
    オブジェクトレベルのアクティビティに基づいて、各オブジェクトを Standard または Nearlineクラスへ自動的に移行し、費用とレイテンシを最適化します
    
    - 最初の 30 日間はすべてのデータが Standard クラスに保存されます
    - 30 日間アクセスされなかったデータは、アクセス頻度の低い（コールドな）ストレージ クラスに移行されます

### **オブジェクトへのアクセスを制御する方法を選択する**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/199eb910-bea1-44f3-aed1-bfe1033c4cd5/Untitled.png)

- アクセス制御
    
    一般的には均一が使われることが多い
    
- 今回は均一

### **オブジェクト データを保護する方法を選択する**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/551e2898-f323-4df1-87eb-b6bc51a7b98e/Untitled.png)

- 今回は選択なし

→ 「作成」

## コンソール画面

### 構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/04afbb17-fdaa-42ca-8211-d04ac5e01bf1/Untitled.png)

- ✏️のマークがあるものは作成後から編集できる
    - ストレージクラス、タグ、ラベル
- それ以外のものは編集できない
    - ロケーションや、ロケーションタイプ

### 権限

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1d18d8ea-71b7-413d-9c6b-a31d6d236ea9/Untitled.png)

- アクセス制御を変更できる

### 保護

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/177cdef3-47d4-402f-9dcb-da4c4933bbf5/Untitled.png)

- バージョニング等の変更が可能

### ライフサイクル

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/be981756-e03a-4434-99c3-68e2dd755093/Untitled.png)

- 「ルールを追加」
    - アクションを選択
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7f251a40-00fd-4a99-8811-5c4060bc286d/Untitled.png)
        
        - マルチパート アップロードを削除
            
            並列アップロードに失敗した不完全なファイルを削除する
            
    - オブジェクト条件の選択
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7942df12-bf02-4edf-9277-d2b0b1c43e7e/Untitled.png)
        
        - 経過日数、バージョンの数等設定できる

### オブザーバービリティ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f3c8575e-4bbe-48fd-bcbb-34735311fc5e/Untitled.png)

### **インベントリ レポート**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bed11334-0a3e-47d4-9c14-d4cf76d7c5be/Untitled.png)

> オブジェクトに関するメタデータ情報（オブジェクトのストレージ クラス、ETag、コンテンツ タイプなど）を含むインベントリ レポートを生成できます。この情報は、ストレージ費用の分析、オブジェクトの監査と検証、データ セキュリティとコンプライアンスの確保に役立ちます。インベントリ レポートをカンマ区切り値（CSV）ファイルとしてエクスポートし、[BigQuery](https://cloud.google.com/bigquery/docs?hl=ja#docs) などのツールでさらに詳しく分析できます。
>