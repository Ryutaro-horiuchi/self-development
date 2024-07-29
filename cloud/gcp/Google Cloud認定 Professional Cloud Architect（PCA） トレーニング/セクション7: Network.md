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
## FirewallとRouting

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/48002978-825b-4790-a3fb-895fadb49df9/Untitled.png)

## Cloud Firewall

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9c3ed5ff-53d0-4ec0-8da7-7894d0db99a9/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/97940d77-8e83-413f-a449-b0acab460212/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f14a587e-d496-4e99-a62e-4ba50348080d/Untitled.png)

## Cloud Armor

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4ce0d8e0-aa68-4aaf-8d7e-d0c4a87870d4/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2dde2bc3-c06a-41be-b4f6-2a5e2a59f7ce/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/83b57463-91b4-4e0a-83d9-e96f8b898174/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f2da34d6-78c7-439b-9a11-dc49a4129d83/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1e1b5e67-9dca-4a24-9ecc-1804ab81b2d4/Untitled.png)