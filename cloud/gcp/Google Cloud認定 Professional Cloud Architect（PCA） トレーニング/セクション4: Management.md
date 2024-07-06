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