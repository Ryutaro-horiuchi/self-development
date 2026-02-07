## 2種のデプロイ先

- Node.js環境かWebサーバーのどちらか
    - Node.js環境: `npm run build`
    - Webサーバー: `npm run generate`

## Nuxtが対応しているホスティングプロバイダ

- Nuxtの実行環境をあらかじめ用意してくれるサービスがある
- 表9-1 p279

### Netlify

- Node.jsのホスティングサービス
- GitHubなどのホスティングサービスでソースコードから、自動で取得・デプロイを行なってくれる
- データベースなどのデータ保存部分は別でサービスを利用する必要がある

## Nuxt Devtools

- Nuxt用のデバッグツール
- 画面最下部にある下記のアイコンを押下すると確認できる
    
    ![image.png](attachment:333f93d0-47e2-48b5-ae9b-0c37fe298b92:image.png)
    
- 初期画面
    
    ![image.png](attachment:ab9abfd2-a40d-4195-a2ca-e24598ad2fd1:image.png)
    

### Nuxt Devtoolのアイコンと表示される情報

![IMG_9726.jpeg](attachment:d62fa914-0b62-4139-ba46-db9e7730e30e:IMG_9726.jpeg)

### Pages

![image.png](attachment:2f862fba-a528-44eb-bca4-39c7428d38be:image.png)

- プロジェクトのルーティング情報が見れる

### Components

![image.png](attachment:4ce7bb1e-0024-4088-9fdd-33fb94417cba:image.png)

- プロジェクト内のコンポーネントが確認できる
- グラフのボタンを押下すると、コンポーネントの関連をグラフで表示してくれる
    
    ![image.png](attachment:a859d21c-5a9f-4931-92b8-b97bfa0961d1:image.png)
    

### Imports

![image.png](attachment:bb864e07-89ad-4f3d-90db-8dae179ac581:image.png)

### Modules

### Plugins

### Runtime Configs