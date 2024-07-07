## Resource Manager

---

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7b2e2623-f57e-4167-a48f-436517109cb5/Untitled.png)

- 組織、フォルダー、プロジェクト、リソースという階層構造
- 会社の組織構造と似ている
- ユースケース
    - 組織は会社単位、フォルダーは部署単位、プロジェクトは環境単位に相当する

### Organizaiton Policy(組織ポリシー)

- 組織に対して特定のアクションを許可するポリシー
- 下位の階層(フォルダー、プロジェクト、リソース)にも権限が継承される
- 組織を作るには個人アカウントではなく、GoogleWorkspaceやCloud Identityが必要

### 組織の計画に関するベストプラクティス

- 必要最低限の組織数にする
- 組織を使用して管理権限を明確にする
- セキュリティの観点
    - 最小権限の法則
        - 不要な権限を与えない
    - 管理オーバーヘッドを抑える
        - 不要な組織を作成しない
- テストに別の組織を使用する
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/3892a6cb-1465-4fa9-afa8-a6950d3cd420/Untitled.png)
    
    - 本番環境に影響を及ばさないようにするために、テスト、ステージング、本番環境は組織を分ける
- Google Cloud 組織全体の請求先アカウントを使用する
    - アカウントは最小数に絞る
    - 会計組織以外のアカウントは請求内容を閲覧できないようにする

## Deployment Manager(CDM)

---

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ceb74f0b-4476-4bf1-a328-bf7b1a94be6a/Untitled.png)

- Googleクラウド上のリソースのプロビジョニングと管理を行うサービス
- YAMLなどの形式で記述され、複雑なデプロイメントも一貫性と再利用制を保証する
- テンプレート例
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ea8ca1be-0e51-4d98-9d1e-9265ec594d2a/Untitled.png)
    
    type: デプロイされるリソースのタイプ
    
    properties: リソースのパラメーター
    
- コマンド
    
    set, create, update, deleteが一般的なコマンド(Associate Cloud Engineerでは出る)
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7e31c46f-23c3-4759-a68c-03225bda169e/Untitled.png)
    

## Cloud Function Toolkit(CFT)

---

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/40e8be5b-51b3-409d-a2fd-1f085b35934b/Untitled.png)

- GoogleCloudのリソースを管理するためのツールキットであり、Deployment Managerと同様Yamlファイルで作成する
- Deployment Managerとは、目的が異なる
    - 柔軟性
        - CFTは指定するリソースに縛りがないが、CDMは特定の種類のリソースを定義するために使用される
    - コードベース管理が容易
        - CFTはGitなどの外部バージョン管理システムに保存される
        - CDMはGoogleCloudコンソールで作成、および管理される
    - カスタマイズ性
        - CFTテンプレートは任意の関数や変数を定義することができるが、Deployment Mangaerは、GoogleCloudが提供している関数に限られる。
    - CFTはTeraform等にも対応している

## IAM(Identity and Access Management)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7045d10b-708c-4cc3-bce6-a535f0940ae8/Untitled.png)

- 一般的にユーザーやアクセス権限を管理するためのサービス
- IAMの変更履歴を外部にエクスポートできる
    - エクスポート先は、CloudStorageかBigQuery
- 親階層で強い権限を付与すると、子階層にも適用されてしまう
    - → 子階層で細かい権限を設定するのがプラクティス
- 体系
    - IAMポリシーはバインディングで定義される
        - ロールとメンバーをセットにしたもの
    - スライド
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7cb05e8b-fea7-472e-92a3-f64b69a81d1a/Untitled.png)
        

### 役割ベースのアクセス制御(Role-based access control)

- 役割(Role)を使用して特定リソースへのアクセスを制御する
- 2種類のロールがある
    - 事前定義されたロール(Predefined roles)
        - 特定のサービスやリソースに対する一般的な操作をカバーするためのロール
    - カスタムロールの2種類
        - 事前定義されたロールで不十分な場合に

### RBACとABAC

「アクセス制御」の異なる方法論やモデルを表す。

GoogleCloudでは、RBAC、ABMC、両方を実現することができる。(AWS Azuleでも可能)

- RBAC(Role-Based AccessControl)
    - ユーザーは特定のロールに関連づけられ、そのロールには特定の権限が割り当てられる。
    - ユーザーは割り当てられたロールを通して、リソースへのアクセス権限を持つ
- ABAC(Attribute-Based AccessControl)
    - ユーザー、リソース、環境などの属性を使用してアクセス権限を持つ
    - 属性はユーザーの部門やリソースの種類、時間帯など様々な要因に基づく

### CEL(Common Expresion Language)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/106b22be-1ef8-4b03-9eba-41e3eed886a4/Untitled.png)

GoogleCloudで定義される式言語。IAMロールを定義することができる

### 基本的なロール(Primitive roles)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4be17367-b9e3-4ccb-885c-0b6199aeb301/Untitled.png)

- 2022年11月非推奨、2023年11月完全削除

### Identity Platform

難しいログイン認証の流れを簡単に作成することができる。メール / パスワードのほか、Githubでも可能

### サービスアカウント

- アプリケーションなどからGoogleCloudへアクセスする際に用いられるアカウント
- ２種類ある
    - ユーザー管理のサービスアカウント
        - ユーザー自身で管理するアカウント
    - デフォルトサービスアカウント
        - GCE/GKEなどで自動作成されるアカウント

### Cloud Identity

組織のユーザーやデバイスの管理に関連する機能を提供する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/79a0aa45-12ca-480f-aa10-f436e6870c5b/Untitled.png)

### Google Workspace

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6899fb6f-4787-4f4f-872e-d83ff1123a12/Untitled.png)

## Operation Suite(運用監視ツール)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0f3068cf-fce0-4c55-854b-ba26ca016b33/Untitled.png)

- システム監視とは　スライド
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/97453943-3ea9-4c93-8312-9b3e8312056f/Untitled.png)
    
    - 特定多数のユーザーがリソースに対してアクセス、変更を加える際、「誰が、いつ、何をした」 といった証跡を取ることで、問題が発生したときに適切なアクションを取ることができ、また原因究明、再発防止策を打つことができる
- 歴史 スライド
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fa0bd99d-8da0-4999-ba41-d96798f3e367/Untitled.png)
    

### Cloud Logging

Cloud Logging は、Google Cloud のユーザーがクラウドリソースのログデータを収集、表示、分析するためのフルマネージド型サービス

- 機能
    - ログエクスプローラ（ログビューア）
        - 集約されたログに対してクエリ（フィルタリング）を実行
        - クエリの例：Load Balancer で WARNING を検知
        
        ```
        resource.type=“http_load_balancer”
        severity>=WARNING
        jsonPayload.enforcedSecuritypolicy.configuredAction !=“DENY”
        ```
        
    - ログベースの指標（Log-Based metrics）
    • Cloud Logging で収集されたログをもとにカスタムメトリクスを作成する機能である。
    • 特定のログイベントやログの内容に基づくメトリクスを作成、監視することができる。
        - ユースケース
            
            特定のログエントリが一定期間中に、あらかじめ設定した閾値を超過したかを監視するメトリクス（エラーが 1 時間に
            100 回以上記録されたら警告を出す）
            
    - ログルーター
        - Cloud Logging API に送信されたログに対し、保存・破棄・宛先指定などのルール適用
    - ログストレージ
        - ログを集約するログバケット（下図）の管理
            
            ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d5154877-486a-47a4-87ec-9335da4fac7b/Untitled.png)
            
    - 監査ログ
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7edd9a5d-486c-467d-8a4f-da500d09a8ee/Untitled.png)
        
        - 管理アクティビティ監査ログ
            - リソースの設定変更など管理タスクを監視するための重要なツール
        - ポリシー拒否監査ログ
            - GoogleCloudのサービスがIAMポリシーによって拒否されたリクエストに関する情報を提供する
            - → 不正なアクセスや設定のミスを迅速に特定することができる
    

## サービスレベル

- SLO（Service Level Objective、サービスレベル目標）
    - サービスの品質やパフォーマンスに関する具体的な目標を示す
        - Ex. あるクラウドサービスが 「月のアップタイム（稼働時間）が99.9%」 を目標として設定した場合、それはサービスが1 ヶ月のうち約 43.2 分以内（365日×0.1%、ただし計画停止は除く）しか停止しないことを意味する。
- SLA (Service Level Agreement、サービスレベル契約 もしくは 合意）
    - サービス提供者と顧客の間での正式な書面による契約または合意
    - SLO（サービスの品質や性能の目標）だけでなく、それを達成できなかった場合のペナルティや補償、その他の契約条件なども含まれることが多い。

## Cloud Monitoring

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6229f50a-2b63-4c5a-9b27-3e3cd70441b5/Untitled.png)

- アプリケーションおよびインフラストラクチャのパフォーマンスと健全性を監視、警告、視覚化するための Google Cloud のサービス
- Google Cloud だけでなく、AWS などの他クラウドや、およびオンプレミスのリソースの監視もサポートする
- Google Cloud 以外のマシン（オンプレミスのマシン、他クラウドプロバイダ）を監視するためには、エージェント（Monitoring Agent）をインストールする必要がある。
    - エージェントのインストールにより、特定のアプリケーション（例: MySQL、Nginx、Apache）に関する詳細なメトリクスも取得することができる
    - ただし、エージェントを使用せずとも、Cloud Monitoring API を通じて任意のメトリクスを送信して監視することも可能
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/58f69207-862a-4a94-8624-9962a0ba9201/Untitled.png)
    

## Cloud Trace

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/18751c3a-1f23-46dd-8f4d-ac4f6aef7419/Untitled.png)

- Google Cloud上で動作するアプリケーションのパフォーマンスのボトルネックや遅延の原因を特定するための分散トレーシングサービス
- Cloud Trace を使用することで、各サービス間でのリクエストの流れや遅延の原因を迅速に特定できる
    
    → パフォーマンスの問題の解決やシステムの最適化が容易に
    
- レイテンシ
    - あるプロセスが開始してから終了するまで
- マイクロサービスアーキテクチャ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ae7ba6eb-7f42-40a4-a1ba-aaeed14dca16/Untitled.png)
    
    - 一般的なクラウドサービスシステムでは、マイクロサービスアーキテクチャが推奨されている

### Cloud Service Health

- 特定のクラウドサービスの稼働状態やインシデント、メンテナンス情報などをユーザーに通知
するためのダッシュボードや通知システム

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1736494a-03ec-473d-83ac-3bed4c583081/Untitled.png)

- 緑色は使用可能だが、それ以外は何かしらの障害や通知事項がある