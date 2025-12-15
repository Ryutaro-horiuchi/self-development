- `server/`ディレクトリは、アプリケーションに API やサーバーハンドラを登録するために使われます。
- Nuxt はこのディレクトリ配下のファイルを自動的にスキャンし、HMR（ホットリロード）対応の API / サーバーハンドラとして登録します。
    
    → Express や Fastify を自分で立てなくても「ファイルを置くだけで API が生える」仕組みです。
    

## ディレクトリ構造

```tsx
server/
 ├ api/        # /api 配下のエンドポイント
 ├ routes/     # /api なしのエンドポイント
 └ middleware/ # 全リクエスト共通のサーバーミドルウェア

```

| ディレクトリ | 役割 |
| --- | --- |
| `server/api` | `/api/*` として公開される API |
| `server/routes` | `/hello` など **/api なし**のルート |
| `server/middleware` | 全リクエスト前処理 |

## API / Server Handler(server/api) の基本

- 各ファイルは、`defineEventHandler()`（またはそのエイリアス）で定義された **default export の関数**を持つ必要があります。
    
    ```tsx
    export default defineEventHandler((event) => {
      return { hello: 'world' }
    })
    
    ```
    
    - return した値 → 自動で JSON レスポンスになる

### フロントエンドからの呼び出し

```tsx
const { data } = await useFetch('/api/hello')
```

- Nuxt が **サーバー or クライアントを意識せずに通信**してくれる

## Server Routes（/apiなしのルート）

- `/api` プレフィックスを付けずにサーバールートを追加したい場合は
server/routes に配置します
- Ex.
    - `server/routes/hello.ts`
        
        ```tsx
        export default defineEventHandler(() => 'Hello World!')
        ```
        

## Server Middleware

- **すべてのリクエストの前**に実行される
- 用途例
    - ログ出力
    - ヘッダ付与
    - 認証情報を `event.context` に追加
- レスポンスを返してはいけない
- Ex.
    - `server/middleware/auth.ts`
        
        ```tsx
        export default defineEventHandler((event) => {
        	event.context.auth = { user: 123 }
        })
        ```
        

## Server Plugins（Nitro Plugin）

- `server/plugins` に置いたファイルは Nitro プラグインとして登録され、
サーバーのライフサイクルにフックできる
- Ex.
    - `server/plugins/nitroPlugin.ts`
        
        ```tsx
        export default defineNitroPlugin((nitroApp) => {
          console.log('Nitro plugin', nitroApp)
        })
        
        ```
        

## Server Utilities

- server/utils に共通ユーティリティを置けます。API ハンドラをラップする関数などを定義可能。
    
    **→ API** の共通処理（ログ、例外処理）をまとめる場所