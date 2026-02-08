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

- Virtual Filesはver0.6.7だと下記アイコン
    
    ![image.png](attachment:39d83558-9ca8-4e22-9e5d-40fd49215326:image.png)
    

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

- オートインポートの各コンポーザブルの利用状況が確認できる
- 「Show used only」をONにすると、使用しているもののみ表示される
    
    ![image.png](attachment:cc1af60a-7c1e-44bb-a4f5-6707849d8dc5:image.png)
    

### Modules

![image.png](attachment:e91c18f6-4939-4628-bc30-7768f84d6dde:image.png)

- インストールしたすべてのモジュールと、モジュールの github リポジトリ、ドキュメント、バージョンなどの情報が表示されます。

### Plugins

- プロジェクトで使用しているすべてのプラグインと、プラグインの初期化時間などの情報が表示されます。

![image.png](attachment:2e1d0261-5857-4f0d-80ae-cb08e5584e79:image.png)

### Runtime Configs

- ランタイム設定タブにはプロジェクトのすべてのランタイム設定が表示され、編集が可能です。

### Payload

- useState()によるステートの利用と、useAsyncData()によって取得したデータの両方が含まれている

### Hooks

- ライフサイクルフックなどの各種フックが実行された処理時間が表示されており、画面表示のパフォーマンス改善に利用できる

### VirtulaFiles

- Nuxtによって生成されたファイル類がリスト表示されている

### Inspect

- コーディングした各ファイルがViteによってどのように変換されているかの過程を確認することができる