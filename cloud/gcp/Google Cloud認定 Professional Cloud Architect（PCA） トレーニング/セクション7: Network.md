# 全体像

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6b3d6fcd-aea7-403c-89c3-4213ce797ed3/Untitled.png)

- 雲印
    
    インターネット環境
    
- VPC → Region → Subnet という順番
    - ゾーンはサブネットをまたげる
- OnPremisesからGoogleCloudへ接続するには、CloudRouterや、CloudVPNを使用する
- インターネットから、GoogleCloudへ接続するにはパブリックIPアドレスを使用する
- GoogleCloud内で接続するにはプライベートIPアドレスが必要


# VPC
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b7e9d578-d87a-484f-9ce1-0905d13d2e4e/Untitled.png)

## AWSとの比較

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7825121e-4255-48b7-be4b-a31244804f79/Untitled.png)

- AWSでは、ゾーンがサブネットをまたがることはない

## VPCピアリング

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/eb89beac-ac50-493e-b1d0-9410fa2f1725/Untitled.png)

- プロジェクトの同異に関わらず、異なるVPC間をインターネットやVPCを経由せず、高速かつ安全に接続できる
- 制限事項
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f544f3e1-9a65-45e0-b3cf-da1b61571d21/Untitled.png)
    

## 共有VPC

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/56f58fa3-6a5c-451a-9c82-57c01b4a5ff9/Untitled.png)

- 複数のGoogle Cloudプロジェクトが同じVPCネットワークとそのリソースを共有するための機能

## VPC Service Controls

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/940d69c5-ad2d-4311-9c9a-94d6c9ca9b69/Untitled.png)

## 限定公開のGoogleアクセス(Private Google Access)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/854b02ab-ec89-4138-a3eb-f59967b2d6d5/Untitled.png)

- 内部 IP アドレスしか持たない VM インスタンスが Google API とサービスの外部 IP アドレスにアクセスすることができる。
- AのVMは、パブリックIPはないが、Google Serviceへのアクセスが有効になっている
- Google Service
    - GCS、GKE、GCE、BigQueryなど

## 通信プロトコル

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/16ef0171-8d34-45d7-b80e-b785ddf0d9e6/Untitled.png)

# 接続サービス
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b1cbb10f-e16c-481b-985b-ac5ff6f7bc06/Untitled.png)

- VPN、専用線接続の違いは公共のインターネットを使用するかしないか

## Cloud VPN

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9963d32a-b91d-4cd6-a066-8f28e77fcd70/Untitled.png)

- Cloud VPN
    - 拠点と拠点を結ぶVPN
- クライアントVPN
    - サードパーティ製のVPNソリューションを使用する
    - 個人の端末に専用のソフトウェアをインストールし、接続する

### 2種類のゲートウェイ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4075c4a5-28aa-467c-b20b-3fd293d95894/Untitled.png)

- HA VPN
    - vpn-gateway
        - Google Cloudのネットワークとオンプレミスネットワークや他のクラウドネットワークをVPN接続する
- Classic VPN
    - target-vpn-gateway
        - Google CloudのVPCネットワーク内に存在し、VPNトンネルの終端

## Cloud Interconnect(専用線接続)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ce9373fe-7963-4ed8-ba69-bf861351812f/Untitled.png)

- Dedicated Interconnect
    - Google Cloudとオンプレミスとの環境間を、直接の物理的な接続を提供
- Partner Interconnect
    - サービスプロバイダを介して、GoogleCloudとオンプレミスとの環境間の接続を提供
    - 速度はサービスプロバイダ次第なので、 GoogleCloudからSLAは提供されていない


# ルーティングとファイアウォール
# FirewallとRouting

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/48002978-825b-4790-a3fb-895fadb49df9/Untitled.png)

- 事前に定義されたルール
    - ネットワークプロトコルやIPアドレスに基づいて

## Cloud Firewall

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9c3ed5ff-53d0-4ec0-8da7-7894d0db99a9/Untitled.png)

- 優先順位
    - 番号が低いほど優先順位が高い

### Cloud Firewall 設定画面

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/97940d77-8e83-413f-a449-b0acab460212/Untitled.png)

- デフォルトルール　65535

### FireWall Insights

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f14a587e-d496-4e99-a62e-4ba50348080d/Untitled.png)

- ファイアウォールの分析ができる
    - ルールの使用率
    - 変更履歴の追跡

## Cloud Armor

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4ce0d8e0-aa68-4aaf-8d7e-d0c4a87870d4/Untitled.png)

- Cloud FirewallはVPCへ流入するトラフィックの制御に特化していたのに対し、CloudArmorはHTTP/HTTPSトラフィックの制御に特化している

### DDoS 攻撃

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2dde2bc3-c06a-41be-b4f6-2a5e2a59f7ce/Untitled.png)

- DDoS攻撃
    - 対象のウェブサイトやサーバーに対して、複数のコンピューターから大量に行うことを指す
    - トラフィックそのものは正常であることが多いため、特別な対応が必要

## Cloud Router

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/83b57463-91b4-4e0a-83d9-e96f8b898174/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/707a9f0c-bfbe-46b6-aace-f1a77ae883d3/Untitled.png)

- ネクストホップ
    - 次の経由点

## Cloud NAT

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f2da34d6-78c7-439b-9a11-dc49a4129d83/Untitled.png)

- VPC 内のリソースがインターネットや他の Google サービスにアクセスする際に、プライベート IP アドレスをパブリック IP アドレスに変換するサービス
- 複数のプライベートIPアドレスに対して、1つ(または複数)のパブリックIPアドレスを使用して変換することで、外部IPアドレスの消費を抑制する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1e1b5e67-9dca-4a24-9ecc-1804ab81b2d4/Untitled.png)

# LoadBalancer
## 概要

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5c2f7f70-4e3e-43bf-be6a-2ee0cdafa495/Untitled.png)

- プレウォーミング
    - Load Balancerや背後のリソースをあらかじめ準備しておく
        - Ex. GCEのインスタンスの立ち上げに1-2分時間がかかるが、ユーザーはこの部分を意識せずに使用することができる
- ヘルスチェック機能もある

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2eed9eab-26e2-4cc8-9591-ca0838e0003f/Untitled.png)

## 分類

### フォーマット

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/df220b51-0221-4fa7-8258-eab483088348/Untitled.png)

- 内部負荷分散か外部負荷分散か
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e2f1641f-f8e5-4799-b262-da4be79f98eb/Untitled.png)
    
- 地域による分類
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/591e7b06-85cf-44bb-9bf4-e9ca074b3956/Untitled.png)
    
- 価格帯
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5e27e840-4d0f-49a5-98f1-6145e07e4830/Untitled.png)
    
- プロキシ or パススルー
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d9874d35-dd7d-4c95-98fc-f170da58f0b1/Untitled.png)
    
    - プロキシ
        - 直接VMに接続せず、プロキシを経由して接続
    - パススルー
        - VMに直接接続する。(光回線がないと使用できないなどの制限がある)
- トラフィックの種類
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/08e6f513-bca5-4057-a471-467ae2445fad/Untitled.png)
    
    - TCP UDPをネットワークロードバランサ
    - HTTP HTTPSをアプリケーションロードバランサ

### 決定木

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8fc4dbd3-d412-45ce-b7ae-528571945b75/Untitled.png)

### ヘルスチェック

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/77685779-9e20-4084-83aa-380d5d4d32fc/Untitled.png)

- MIGと組み合わせることで、オートスケーリング機能が提供される

# ハンズオン　マネージドインスタンスグループを作成する

[インスタンステンプレートとマネージドインスタンスグループ](https://www.notion.so/ebbf1351dc5343279bc9b977e5759ec0?pvs=21) 

## トップ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c640800c-c425-4bbe-a3a0-c814bfb38059/Untitled.png)

「ロードバランシングを作成」をクリック

## ロードバランサの作成

### **ロードバランサのタイプ**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/94d64482-ceb8-427f-9dcb-1f049ab11552/Untitled.png)

- アプリケーション ロードバランサ（HTTP / HTTPS）を選択

### **インターネット接続または内部**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/679a3023-ce1d-4cad-8c82-deeeac6f788b/Untitled.png)

- インターネット接続（外部）を選択

### グローバルまたはシングル リージョンのデプロイ

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ed9bfe76-a7a2-467a-b937-881813ea397c/Untitled.png)

- グローバルを選択

### **ロードバランサの世代**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/dfc5a672-a664-4ed3-b56f-0c995691f36b/Untitled.png)

- 従来のだと、「フォールとインジェクション」や「リクエストヘッダー」と「レスポンスヘッダー」の変換などが対応していない
- 今回は新しいものを選択

### ロードバランサの作成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ca4dd6c3-60d8-45e8-8b03-a93135160fba/Untitled.png)

「構成」をクリック

## 構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e9671b65-68ea-48b6-8f5f-9a0017793d17/Untitled.png)

- フロントエンドはポート
- バックエンドはロードバランサーを介した背後のサービス

### フロントエンドの構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2c58d236-fa53-4cdc-844a-64b90e59b869/Untitled.png)

- 名前を入力して「完了」

### バックエンドの構成

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9117512c-2654-43de-bd73-e21a4cddd81d/Untitled.png)

- 「バックエンドバケットを作成」
    - GCSのバケットを設定できる
- 今回はマネージドインスタンスを割り当てるので、「バックエンドサービスを作成」
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/42abcd66-78c8-480d-bcfe-9af1fd8729f6/Untitled.png)
    
    - 名前入力
    - インスタンスグループ欄にて作成した、インスタンスグループを割り当てる
    - ポートは80
- しきい値の設定
    - 分散モードの説明
        
        > ロードバランサがバックエンド インスタンス グループ間または NEG 間でリクエストをどのように分散するかを指定します。HTTP(S) の場合、サポートされている分散モードは、使用率（インスタンス グループのバックエンド向け）、レート（インスタンス グループと NEG 向け）です。バックエンドの使用率またはレートが構成済みの最大値に達すると、ロードバランサは構成済みの最大値に達していない他のバックエンドに新しいリクエストを振り向けます。すべてのバックエンドが構成済みの最大値に達した場合は、ロードバランサは最大値を超えることになります。
        > 
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ab90395b-0d4f-4b5f-9f1c-ba4694f6bd52/Untitled.png)
    
    - 今回はデフォルトのまま
- CDN
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2c5678f4-fe9a-4be0-96ed-4436c30c4333/Untitled.png)
    
    - 今回はデフォルトのまま
- ヘルスチェック、セキュリティ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/18e52955-1b43-47c0-a3f5-575ee9eade8b/Untitled.png)
    
    - ポート: 80、タイムアウト: 5 秒、チェック間隔: 10 秒、異常しきい値: 3 回の試行
    - セキュリティは今回設定しない

### ルーティングルール

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/86e80639-05e8-4f2b-a8ca-bbe93ba560c2/Untitled.png)

- ホスト、パスに応じてトラフィックを転送できる
- 今回は設定なし

### 作成

「作成」をクリック

# 挙動の確認

## ロードバランサー コンソール画面

![Monosnap Monosnap 2024-08-03 22-24-45.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8376a20f-815d-4d33-822f-4fd970c08e1f/Monosnap_Monosnap_2024-08-03_22-24-45.png)

- フロントエンド、バックエンド別に確認できる

## VMの確認

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2e5f1a0a-20d2-4e29-b196-3b3f1478878a/Untitled.png)

- マネージドインスタンスグループの設定によって、VMマシンが2つ作成されている
- 負荷がないため、この内部IPのいずれかにロードバランサーによって振り分けられる

### リソースの削除の注意

- ロードバランサーに関連づけられているマネージドインスタンスグループは削除することはできない
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/83bc3976-69b1-45e7-83f0-7d3b6344deb7/Untitled.png)
    
- VMも直接は削除できない
- → ロードバランサーを削除後、インスタンスグループを削除する

# CDN(Content Delivery Network)
## 概要

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5827f875-01a9-4c66-a699-e5d31d11a201/Untitled.png)

- クライアントとオリジンの間にキャッシュを配置して、オリジンの負荷低減とレスポンス向上を目指す
- CDNの文脈
    - clients と CDN間のやり取り
        - Viewer Request, Viewer Response
    - clients と Originとのやり取り
        - Origin Request, Origin Response

## 生存期間の設定

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/7bbd2cc0-4a84-49cb-abc0-d4b2dea671db/Untitled.png)

- 生存期間の設定が大事
- コンテンツの鮮度とオリジンサーバーの負荷はトレードオフの関係にある
    - 上記加味しながら、適切に設定する

## キャッシュキーの調整

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e731a5b1-0822-4ed8-b43d-6403f99d4ea0/Untitled.png)

### キャッシュキーの設定例

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f4b11a99-290d-40e2-b49d-266b444640cd/Untitled.png)

- 優先順位
    - Cache-Control > Expires

### ロードバランサーでアクセスログを取得する

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/69e6ed1e-048e-4e78-9d9c-8664590b8c51/Untitled.png)

# DNS(Domain Name System)
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0d675d39-bce9-4d32-be26-74a9e08f6da7/Untitled.png)

- ドメイン名をIPアドレスに変換するシステム
- ドメインの問い合わせをする際、キャッシュDNSサーバー、権威DNSサーバーの2段階で問い合わせをする

## 主要なレコード

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fb78c5f8-5429-4915-95e7-a90bfebf61ea/Untitled.png)

- レコード
    - ドメインとIPアドレスの組み合わせ
- Aレコード、　CNAMEレコードは一般常識として覚えておく

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a8917407-7057-4103-aac7-2b7c65f849fb/Untitled.png)

# API

# Apigee(アピジー)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/5d2db184-f1cd-482a-b4ea-eac39f983061/Untitled.png)

## 例 オンラインの書籍販売システム

### 書籍の追加 API

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/15dd1229-6ac7-42c8-b555-3b30b8b714da/Untitled.png)

- Ex. オンラインの書籍販売システム
    1. ApigeeにはあらかじめエンドポイントとしてIngressを登録しておく
- 処理の流れ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/17b898f9-a4d4-4e05-97d5-5547e96b7f39/Untitled.png)
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d6d7d034-ca14-419c-a736-c5a7a5b3993e/Untitled.png)
    

### 書籍の情報取得

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/952a784c-b4f5-425b-a26f-56923acd1f1f/Untitled.png)

- 書籍の流れ
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0640aa0e-c381-4f8c-bef5-f1241625b2ae/Untitled.png)
    
    - 認証情報を含める
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/da796d20-ba97-4784-baa4-dc250dcd4b3d/Untitled.png)
        

# 負荷対策も優れている

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/8d759c78-ad21-4aad-a51f-7220f3c3bd93/Untitled.png)

通常は大量のリクエストを送られると429を返すが、Apigeeは自動的にスケーリングを行い処理をする