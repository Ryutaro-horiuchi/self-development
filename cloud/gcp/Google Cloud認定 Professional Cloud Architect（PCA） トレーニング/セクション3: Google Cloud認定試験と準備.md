## Google Cloud 導入

---

- Google Cloudの設計思想は、Every company is a data companyに基づいている
    
    全ての企業が自社でデータセンターを用意するのではなく、GoogleCloudのクラウドサービスを活用してデータ処理を行うことができるという考え方
    

- スライド
    
    !https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fa9c878a-198b-466c-9e8d-ee309e04bf5c/Untitled.png
    
    !https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/4d155009-8179-4282-8f05-b765adefca6e/Untitled.png
    
    !https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f6868bc9-38ca-4f87-b335-4f29cb9b8536/Untitled.png
    
    - ゾーン
        - SPOF ドメインである
            
            単一のドメインで障害が起こると、全てのサービスが停止してしまうようなドメインのこと
            
        - リージョンの中に3つのゾーンがあることによって、もし一つのゾーンが停止しても、別のゾーンでサービスを継続することができる
    
    !https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b8fee389-585c-4cb8-b453-b0746f2c3a11/Untitled.png
    
    - 最新のサービスはリージョンによって遅れて展開されることがある。GoogleCloudはカリフォルニアの企業のため、最新サービスは米国西部リージョンにリリースされることが通常
    
    !https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e2493500-ddc6-4759-9b23-698c6aa7edd0/Untitled.png
    
    - Ex. 仮想マシンはゾーンリソース

## Cloud Billing

---

### 予算アラートの設定

- GoogleCloudは従量課金制
- 期間、プロジェクト、サービス別に予算金額を指定することで、予算の一定の割合のタイミングでアラートを通知することができる

### Cloud Billing

- 支払い情報が確認できる
- 請求先アカウントを作成できる
- 左側のメニューにて詳細を確認できる
    - 費用管理
        - レポート
            - 期間やサービスをフィルタできる
            
            - イメージ
                
                ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/02e9129b-abce-4fc2-b3d7-b9cd1c8d3ea8/Untitled.png)
                
        - 予算とアラート
        - 課金データのエクスポート
            - 現在の利用料金をBigQueryにエクスポートして分析することができる
            - プロジェクト、タグ、サービス別に分析できる
    - 費用の最適化
        - CUD確約利用割引
            - サービスを使用する期間を前もって登録することで、そのサービスの割引を受けられる
            - 期間は1年、3年の長期利用