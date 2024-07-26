# ComputeEngine

Google Cloud Compute Engine（GCE）は、Google Cloud が提供する仮想マシン（VM）を提供するInfrastructure as a Service（IaaS）サービスである。

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c959f415-8b40-4035-9445-684cbe5a4404/Untitled.png)

### インスタンスの作成画面

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/95bc36bd-6bfa-45cf-b26b-2d27cd4a5d6b/Untitled.png)

### OSイメージの種類

様々な OS イメージが提供されており、Windows や Linux などのディストリビューションを選択して VM を起動できる。カスタムイメージを作成することも可能である。

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/89376b00-4f68-4c48-b46e-fbcbefde68b6/Untitled.png)

- 代表的なLinuxディストリビューション
    
    Linux ディストリビューションとは、Linux カーネル、システムユーティリティ、アプリケーション、ライブラリなどをパッケージ化し、配布・インストールが容易になるようにまとめられたものを指す。
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bd480bf3-7190-4638-a710-cc85cfe623f2/Untitled.png)
    

### 料金体系

料金従量制である。

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/137ad8a5-736a-4707-8a82-f8c546684171/Untitled.png)

- 継続利用割引（Sustained Use Discounts）
    - 仮想マシンを一定期間実行し続けると、割引が適用される。
    - 割引率はマシンタイプと実行期間によって異なる。
- 確約利用割引（Committed Use Discounts）
    - 1 か月、3 か月、1 年、3 年、5 年、7 年、10 年という期間にわたって、特定のマシンタイプとストレージを予約することで、割引が適用される。
    - 割引率は、マシンタイプ、ストレージ、予約期間によって異なる。
- 割引率一覧
    
    割引率は常に変わるため、実際に使用する際は最新のものを参照とのこと
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9c50bf9e-9f86-4403-a89a-e0a241319b8a/Untitled.png)
    
- その他
    - 秒単位の請求
        - 従来のクラウドコンピューティングサービスは時間単位で請求していたが、Compute Engine は秒単位の請求を可能にする。
    - Cloud Monitoring の Recommender 機能
        - 過去 8 日間の稼働実績にあわせて推奨サイズを提案
        - VM のマシンタイプだけでなく、インスタンスグループのマシンタイプ、アイドル状態の VM やリソースの検知も行う。

### Preemptable VM と Spot VM

中断の可能性がある代わりに、通常の VM に比べて大幅な割引を提供する。

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e99d08cf-9a79-4368-b00d-97f60e8cb535/Untitled.png)

- Spot VM
    - Google Cloudの余剰リソースから割り当てられる。余剰リソースが多いと割引率が高くなる
    - 余剰リソースが低くなると割引率が下がり、中断となる
    - サポートされるマシンタイプは今後増えていく可能性がある

### マシンファミリー

特定のワークロードに適したプロセッサとハードウェアから構成される一連のセット

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b0797177-27ba-4533-b4c9-70e1df2cf0c5/Untitled.png)

- 一覧(試験には出ないが、実務では最適なマシンタイプを設定する必要があるため参考に)
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1dc666e0-f510-4b0f-a854-9bee947386de/Untitled.png)
    
    - コンピューティング最適化
        - データ解析などで使用される
    - 
- バースト機能
    - バースト
        - 一時的に負荷がかかること
    - 突発的な CPU のパフォーマンス向上が可能な 「バースト」 機能を備えたマシンタイプが存在する。一時的に高い CPU 性能が要求されるシナリオで有用である。
    - バースト時、インスタンスが物理 CPU を追加する。
    - 追加料金なし
    - 継続時間
    • e2-micro: 30 秒
    • e2-small: 60 秒
    • e2-medium: 120 秒

### ストレージのオプション

- どのインスタンスもOS用のブートディスクを持っているが、さらにストレージ容量を増やしたい場合は下記より選択する
- 暗記する必要はない
    
    → ゾーンか、リージョンか。HDDかSSDかという分類の仕方だけ把握する
    

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ea5f96e3-5f95-47f4-8736-f7be20ad2492/Untitled.png)

- HDDとSSD
    - HDD: 回転する円盤に磁気でデータを読み書きする
    - USBメモリーと同じように内蔵しているメモリーチップにデータの読み書き
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3e65bf96-4590-44c7-a580-fb3fb8d58777/Untitled.png)
    
- 性能による分類
    - スタンダード、バランス、SSD、エクストリームの4種類
        - → の方向に性能が高くなる
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0e703cb1-111c-4415-9947-74fefb02d3e9/Untitled.png)
    
- ロケーションと永続制による分類
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f16b5235-301c-4ebf-93a0-2036ccf389f5/Untitled.png)
    

### 仮想マシンのオプション

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4f5e8d38-3fa8-4e63-8ced-a2d6e8c01b9c/Untitled.png)

- コロケーションスペース
    - Google Cloud環境と同等のレイテンシにVMware環境を置くことができる
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1c5be7f0-766c-4023-9281-8a6be6a6b9b9/Untitled.png)
    
- Bare Metal Solution
    - Googleが物理サーバーを提供し、それをGoogle Cloudのデータセンター内に設置する
    - Googleがハードウェアの管理や保守を行うため、ユーザーはインフラ管理の負担を軽減し、アプリケーション開発に専念できる
- パブリッククラウド
    - インターネット経由で一般に提供されるクラウドサービス
- プライベートクラウド
    - 特定の組織専用のクラウド環境。高いセキュリティとカスタマイズ性を提供。リソースは専有される。
- ハイブリッドクラウド
    - パブリッククラウドとプライベートクラウドの利点を組み合わせて利用する方法

### IPアドレス

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9bd6e92e-94b8-4561-a340-45d865b6162a/Untitled.png)

- エフェメラルIPは、インスタンスを停止するとそのIPは解放される

### バックアップ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ecb24b1c-798c-4d61-8fce-da44dac0bbe7/Untitled.png)

- カスタムイメージのユースケース
    - あるリージョンで稼働中のイメージを、他のリージョンに移行したい場合
- 補足 バックアップの種類
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2000ffc4-417b-44c4-b6f5-84e573c2e959/Untitled.png)
    

### 移行の流れ - Migrate for Compute Engine

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4368072e-517a-40ee-b85e-7ed28071364b/Untitled.png)

### マネージドインスタンスグループ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/cbab013b-613b-4260-a9de-69df55d6d3b1/Untitled.png)

- オートスケーリングの設定
    1. インスタンステンプレートを作成する。
    2. インスタンステンプレートに基づき、MIG を作成する。
    3. Load Balancing を設定し、各 VM の状態をチェックする。
    4. オートスケールを設定する。
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bf390155-a6b7-426a-8d0d-3ddcc30ba3fa/Untitled.png)
    
    - 負荷が減ると、時間が経つにつれて、VMの数も下がっていることがわかる
- マネージドインスタンスグループと非マネージドインスタンスグループ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/426542f9-6f46-4328-bbec-db28b3142797/Untitled.png)


## 仮想マシンの作成とWebサーバーのインストール[ハンズオン]
### マシンタイプ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/106cca6f-94f4-4f52-8cf8-b956463fe4ec/Untitled.png)

- プリセット - あらかじめ用意されている
- コア - 自分でCPU、メモリなどを選択できる

### 可用性

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d5f077d7-da80-4f4b-9206-51d9dabf2aca/Untitled.png)

- SpotVMか、標準か

### ブートディスク

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/96bb76af-cfcd-475a-a3a9-49e6a2bf1497/Untitled.png)

- OSやバージョン、ブートディスクの種類を選択できる

### 自動化スクリプト

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ddbbb0b3-0853-41e2-b89f-bb4f1f4c3ee5/Untitled.png)

詳細オプション > 管理

- 自動化
    - GCEが立ち上がった時のスクリプトを記述できる

### SSH接続

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/05c2056b-70ef-4df7-a1a2-f991195bfd39/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8ea7c471-44f8-4b5b-8c0b-c1f56ec7333e/Untitled.png)

- コンソールからSSHでGCEの中にアクセスできる

### Apache(Webサーバー)のインストール

コマンド一覧

- sudo su
    - 管理者の権限に切り替える
- apt update
    - パッケージ管理リポジトリを最新に
- apt install apache2
    - continue ? → Y
- ls /var/www/html
    - index.htmlの確認
- echo "Hello World!" > /var/www/html/index.html
    - htmlの中に文字列を挿入

# 静的IPアドレスと動的IPアドレス


## 前提

- 動的IPアドレス
    
    インスタンスを停止すると、IPアドレスが解放される
    
    → 次回起動するときは、違うIPアドレスを使用する
    

- 静的IPアドレス
    
    停止しても、IPアドレスを変更
    
    何も関連づけられていないと課金される。使っていない時は、必ず削除をする
    

## ハンズオン 静的IPアドレスを作成する

1. GCEの適当なVMインスタンスを作成
2. VPCネットワーク > IPアドレス
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7794f775-d322-4a45-9284-828031003384/Untitled.png)
    
    - 作成したIPアドレスは、種類欄よりエフェメラル(動的)であることがわかる
3. 「外部静的アドレスを予約します」をクリック
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fb052b36-4094-4dc8-8180-e5fb6c3e6357/Untitled.png)
    
    - 作成したインスタンスと同じリージョンにする
    - 接続先を作成したインスタンスに紐づける
4. 静的アドレスが作成されていることがわかり、VMインスタンス紐付けされていることがわかる
    
    ![Monosnap IP アドレス – VPC Network – PCA-Udemy – Google Cloud コンソール 2024-07-19 10-19-52.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/381f395a-968d-41c3-96ea-8843d1d7d31f/Monosnap_IP_%E3%82%A2%E3%83%88%E3%82%99%E3%83%AC%E3%82%B9__VPC_Network__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-07-19_10-19-52.png)
    
    ![Monosnap VM インスタンス – Compute Engine – PCA-Udemy – Google Cloud コンソール 2024-07-19 10-21-07.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ba9dd98c-0e87-4f97-83e8-ee2f674d2bdb/Monosnap_VM_%E3%82%A4%E3%83%B3%E3%82%B9%E3%82%BF%E3%83%B3%E3%82%B9__Compute_Engine__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-07-19_10-21-07.png)
    
5. 停止しても外部IPアドレスが変わらないことがわかる
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2c00edc1-ebbe-44c5-8dca-b32c99da3fee/Untitled.png)
    
6. 静的アドレスを解放する際は、VMインスタンスを削除してから、解放する必要がある
    - VMインスタンス削除前は解放できない
        
        ![Monosnap IP アドレス – VPC Network – PCA-Udemy – Google Cloud コンソール 2024-07-19 10-23-41.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/58179a2d-8fa5-43a6-a645-a851bfeba60b/Monosnap_IP_%E3%82%A2%E3%83%88%E3%82%99%E3%83%AC%E3%82%B9__VPC_Network__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2024-07-19_10-23-41.png)
        
    - VMインスタンスを削除後、使用リソースがなしになり、静的アドレスを解放できるようになっている
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3356184f-27ff-46df-9695-4281426a623a/Untitled.png)


# インスタンステンプレートとマネージドインスタンスグループ
## インスタンステンプレートの作成

### テンプレートの作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2ac627ba-2fe7-45bf-a7fc-49e6075da32a/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2a5ec79e-913c-4dd7-bc2a-e953304398d8/Untitled.png)

- 名前は適当なもの
- マシンの構成を一番安いもの
    - E2
- プリセットは、micro
- ファイアウォール
    - HTTPトラフィックを許可
- 管理 > 起動スクリプト
    
    ```markdown
    #!/bin/bash
    apt update
    apt -y install apache2
    echo "Hello World! $(hostname -i)" > /var/www/html/index.html
    ```
    

テンプレートが出来上がる

## VMインスタンスを作成する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e8e487b0-7935-4df4-8257-b5101224f8f7/Untitled.png)

VMを作成を開くと、新たにVMを作成する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ae706b3c-f01f-4ccb-a34d-23b9a383e1a9/Untitled.png)

- インスタンステンプレートで定義した設定がデフォルトで反映されている
- 作成すると、外部IPからHello Worldが確認できる

## マネージドインスタンスグループを作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/15691d28-c5db-4596-a149-2da2818d3a37/Untitled.png)

### グループの種類

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/95a40d3e-e637-48a2-95ed-bca8b42725ee/Untitled.png)

- 種類
    - stateless
        - バッジ処理やステートレスサービスを使う時
    - stateful
        - DBなどの永続的なデータを使用する
    - unmanaged(非インスタンスグループ)
        - 別の種類のインスタンスをグループ化
        - オートスケーリングなどの設定ができない
- 今回はstatelessを選択

### 自動スケーリング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1c9eb42b-76c4-4521-825e-faf937b50508/Untitled.png)

- 自動スケーリングモード
    - オン
        - 負荷が高い時にインスタンスを追加、負荷が低いときはインスタンスを削除する
    - スケールアウト
        - 負荷が高い時にインスタンス追加のみを行う
    - オフ
- 今回はオン。インスタンスの最小数を2, 最大数を3にする

### シグナル

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/242055c8-3fae-42e4-b433-b27ed7b14706/Untitled.png)

- Edit signal
    - CPU使用率
        - 60にすると、使用率が60を超えたらスケールアウトする
    - 今回はCPU使用率 60
- Predictive autoscaling
    - 予測自動スケーリング。少なくとも3日間稼働させたデータの結果から予測を行うもの
    - 今回はオフ

### 初期化期間

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3aab2750-befb-471c-a430-32401ab6a244/Untitled.png)

- 初期化にかかる時間を設定することができる
- 今回は60に設定

### スケールインの制御

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6e680c1c-99cd-43f3-b769-c125efdb2218/Untitled.png)

- スケールインをした直後に、トラフィックが急増し負荷が高くなることがある
- 上記のリスクをヘッジするため、特定の時間で減少するインスタンス数を制御する
- 今回は無効にする

### 自動修復

- ヘルスチェック
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d7cb0aea-3b5b-4bcf-9f73-09b0fd4af14c/Untitled.png)
    
    - 今回
        - プロトコルをHTTPにする
        - ヘルス条件を画像の通りにする
- 初期遅延
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bed19f77-56db-4758-b2d4-e495d0cef6ad/Untitled.png)
    
    - インスタンスが起動して、完全に立ち上がるまでの時間を指定する
    - 今回は30に設定
- 作成する
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3cab250b-de3b-41c2-aa62-2d9dc76f84c7/Untitled.png)
    

### インスタンスグループ詳細

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d25cd2af-a1ae-40d8-aafe-4d54c92e0b03/Untitled.png)

- VMインスタンスの最小数を2としたため、2つ立ち上がっていることが確認できる

### 補足

- 自動スケーリング
    - 最大数は1以上にする必要がある
    - インスタンスグループのインスタンスを削除しようとしても自動スケーリングの際は、インスタンスがまた立ち上がるため、VMインスタンスは削除できないようになっている
        - → 削除するには、インスタンスグループを削除する必要がある
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/da6b9ce7-3abf-4949-a29d-79e91bb92c89/Untitled.png)

# Container

# コンテナとは

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5a838bcb-a7ef-4610-b54a-55e8cf2066cd/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/196f94b3-283b-4248-84f9-483b30790406/Untitled.png)

- コマンド
    - [`docker container run`](https://www.notion.so/docker-container-run-633fd0c29a1341809a4d00b6ecff3848?pvs=21)
    - docker build
        - [コマンド](https://www.notion.so/131b0650a9944942ab81fc440b23271f?pvs=21)
    - docker commit
        - 現在のコンテナの状態を新しいイメージに保存する
    - docker push
        - コンテナイメージからレジストリに保存する
- Dockerfile
    - [Dockerfileでイメージを作成する](https://www.notion.so/Dockerfile-f1d9aed101ba4ca59b7e204068d8d931?pvs=21)

# Kubernetes

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2367bf35-64f4-4be4-8a6d-9ba80235f3c1/Untitled.png)

[Kubernetesとは](https://www.notion.so/Kubernetes-611917bff1274225978c93a89cc2af3f?pvs=21) 

# GKE

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/931a1334-ad77-4848-88b6-6b06e7ee491f/Untitled.png)

- Kubernetesの特徴と一部重複している

## 構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e4cd858b-02ff-436a-99c4-d147a57ad5c0/Untitled.png)

- kubectl
    - Kubernetesクラスターをコマンドラインで操作するツール
- Node
    - GKEでは、ノードはGCEが動作している

## 2つのクラスタモード

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f1c4dcf8-ca21-4ef4-9b6d-361ecda3997e/Untitled.png)

- 標準ではユーザーが管理
- AutopilotはKubernetesの管理を簡略化

## コマンド

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bc526399-9dd0-4fc8-aa2d-50f000e210c9/Untitled.png)

- クラスタに対しては、gcloudコマンドを使用する

## 定義ファイル(マニフェスト)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/eb47b80e-fcc2-43e2-9f0f-6cefc8bfb60c/Untitled.png)

[定義ファイルの書き方](https://www.notion.so/ddb664a0c2034dda8aa091003e4d693b?pvs=21) 

## レプリカセット・デプロイメント等

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f31247d4-b1f1-4426-b394-6377bba367b6/Untitled.png)

[デプロイメントとレプリカセット](https://www.notion.so/71dd7de91e4f4ee69d8f7bd68d226318?pvs=21) 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6b7c09a0-25ee-4565-8db0-91ead18dc7dd/Untitled.png)

- 環境の移行がスムーズにできる

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8f0cbf8b-1727-4b37-a87f-704eb9e5656a/Untitled.png)

[typeの設定](https://www.notion.so/type-e38add02a95f4a03801ec1f9a4e4211c?pvs=21) 

## GKEの冗長構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/045abd76-7303-4f66-98bc-cabc939dd2bf/Untitled.png)

## GKEの各種機能

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c0f88d14-6cc4-4a8c-986f-717644e895fa/Untitled.png)

- Tipsが重要そう

## デプロイ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d2b9c855-263b-4652-a6d6-5fa0974e9c36/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/08637233-b821-4016-ba0d-c0fa59690408/Untitled.png)

- Container Registryに保存しているイメージを指定

## GCEとGKEの比較

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6cb45937-5179-4568-bfeb-412c39787edb/Untitled.png)

## ベストプラクティス

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/004a2566-69f4-42db-90af-0f12c4a9b545/Untitled.png)

# Container Registry

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6fbb04a4-8e53-458f-b838-d87ebb24e5eb/Untitled.png)

- アーティファクト
    - ソースコードのビルドによって生成されたバイナリファイルやパッケージを含む一連のファイル群

# ハンズオン
## GKEを使ったサンプルアプリケーションの構築
## クラスタを作成する

### クイックスタートを使用して、チュートリアルで作成する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6165ce6b-02ac-4347-8ab1-bffa8694fcbe/Untitled.png)

### オートパイロットモードで作成する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b0b85324-f9d0-49b0-8783-eeb7b5b482a4/Untitled.png)

### フリート登録が新しくできている

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6dc6fe38-e8e3-4673-b5d9-44552c17a63d/Untitled.png)

https://cloud.google.com/kubernetes-engine/fleet-management/docs?hl=ja

### ネットワーキング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a9b4f497-fc31-47ad-bb22-65d3e985b02f/Untitled.png)

- ネットワーク アクセス
    - 一般公開かプライベートか選択できる
- コントロールプレーン global access
    
    クラスタのリージョンに関係なく、GCPリージョンやオンプレミス環境からコントロールプレーンのプライベートエンドポイントにアクセスできる
    

### 詳細設定

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a6d1e4fa-6c57-4a35-9013-d2fdc31c5065/Untitled.png)

- 自動化
    - メンテナンスを行う時間を設定できる
- セキュリティ
    - Binary Authorization の有効化
        - イメージが特定の署名要件を満たしているかを検証
    - 暗号鍵の設定
- メタデータ
    - ラベルの追加

## サンプルアプリを作成して、クラスタにデプロイする

### エディタを開く

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bc7f0875-5fda-4682-951d-57334530047c/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e7171642-2a9b-4596-a451-8500037b1238/Untitled.png)

### 必要なサンプルアプリを取得する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/17a71013-239a-4923-b621-04f0a8eb5106/Untitled.png)

- 右のチュートリアルに沿って進める
- サンプルコード
https://github.com/GoogleCloudPlatform/bank-of-anthos

### クラスタに接続する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6399247c-cb1e-4b29-ade3-b74fb9603c1f/Untitled.png)

- チュートリアル 3 -  5の手順

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c7d72be5-73c9-45e2-ad05-19020999e4a7/Untitled.png)

### クラスタにアプリケーションをデプロイする

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6de10330-ce85-4f5d-95b2-1f7cf2596755/Untitled.png)

コマンドを実行する

```bash
$ kubectl apply -f \
    ./extras/jwt/jwt-secret.yaml # JWTトークン
kubectl apply -f \
    ./kubernetes-manifests # マニフェストファイルのパス
```

- apply
    - マニフェストファイルに基づいてリソースの作成や更新を行う

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d5d7abff-671d-4c57-9340-27794de8af21/Untitled.png)

Podが作成されている

## コンソールから確認

### ワークロード

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/986a1c08-77bd-4cb8-a270-d9d129fb02ae/Untitled.png)

### ネットワーキング > Gateway.. > サービス

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/49bbc6de-2aad-4011-a84a-547758055795/Untitled.png)

frontendのエンドポイントをクリックするとアクセスできる


# PaaS
## App Engine

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c6f86a4f-face-47ae-b216-296ebb778dc3/Untitled.png)

### 環境の違い

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/cc6e62e4-ce66-4a14-91ea-4ad5b1b7bacf/Untitled.png)

- 最小インスタンス
    - スタンダードは0で、フレキシブルは1
- フレキシブル環境はGCE上のDockerコンテナ内で実行される

### スケーリング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6463cebd-8b8a-403b-be49-ad04e58204ad/Untitled.png)

### そのほかの特徴

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4ab13960-d28b-4635-a4cf-e1081896e27a/Untitled.png)

- Blue/Greenデプロイメントに対応
    - アプリケーションに接続できない時間が最小限に抑えられる
    - コストは高くなる

## Cloud Functions

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0fa1fcab-d86b-4560-99c2-3a69d41329bb/Untitled.png)

- オートスケーリング機能がある
- 下記からデプロイが可能
• ソースリポジトリ（GitHub や Bitbucket など）
• ローカルマシン（gcloud コマンドを使用）
• Cloud Console
• Cloud Functions API

### イベント駆動型とは

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c2f5d974-b6d1-4189-8e10-8f339baf7fcf/Untitled.png)

### 実行時間の制限と料金項目

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/97956cd9-8039-4ec6-9dbc-09f6fd566546/Untitled.png)

## Cloud Run

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/de5b3e2a-1c6c-4a54-8d76-e73256dd98d4/Untitled.png)

- サーバーレス
    - インフラ管理やサーバーの設定は自動で行ってくれる
    - イベント駆動型(HTTPリクエスト)で、インスタンスが起動される
        - リクエストがない時は、0になるため無駄なコストは省ける
- Dockerをデプロイするためのもの

### デプロイ方法

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/de62b76d-2f83-4930-97f1-a24cccb1c92b/Untitled.png)

- Cloud Build
    - コードの変更があったときに自動でイメージをビルド・デプロイする

### Cloud Run for Anthos

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/aed8e61d-7d52-4e2f-a50c-f87d9435908e/Untitled.png)

- for Anthos
    - GKEの機能に準ずる

## コンテナデプロイサービスの違い

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/27ef06c7-3a73-4519-a57f-255ea74deea0/Untitled.png)

- 管理レベルが高い - ユーザーの負担が少ない

## PaaSの分類

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4b31efd3-84c8-46c7-ad23-8aead271e876/Untitled.png)