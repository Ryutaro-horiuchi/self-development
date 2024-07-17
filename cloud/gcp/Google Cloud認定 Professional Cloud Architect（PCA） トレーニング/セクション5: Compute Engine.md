## ComputeEngine

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