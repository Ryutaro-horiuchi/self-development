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