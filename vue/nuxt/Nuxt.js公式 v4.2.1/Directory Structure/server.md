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
    

## 動的ルート（Route Parameters）

- pages と同じ `[param]` 記法が使用できる
- Ex. URL: `/api/hello/nuxt`
    
    ```tsx
    server/api/hello/[name].ts
    
    // コード
    const name = getRouterParam(event,'name')
    ```
    

## HTTP Method ごとのハンドラ

- `test.get.ts,` `test.post.ts`
- ファイル名に `.get`, `.post` を付けることでHTTP メソッドごとに処理を分けられる

## Catch-all Route

- マッチしなかったすべてのルートを拾うためのハンドラ。
    - `[...slug].ts`
        
        ```tsx
        event.context.params.slug
        // 'bar/baz'
        
        ```
        

## Body / Query / Cookie

- `readBody(event)`
- `getQuery(event)`
- `parseCookies(event)`

## エラーハンドリング

```tsx
throwcreateError({
	statusCode:400,
	statusMessage:'Bad Request',
})

```

- throw すれば HTTP エラーとして返る
- uncaught error → 500

## Runtime Config

サーバー専用の環境変数を安全に扱える仕組み。

- `.env`
- `nuxt.config.ts`
- デプロイ先の環境変数を統合的に扱う。

```tsx
const config = useRuntimeConfig(event)
```

## event.$fetch（文脈引き継ぎ）

サーバー内で fetch する際、元のリクエストのヘッダ・コンテキストを引き継ぐための fetch。

## event.waitUntil（レスポンス後処理）

レスポンスを即返しつつ、裏で非同期処理（ログ・キャッシュ）を最後まで実行させる仕組み。

## 個人的な調査

### DBからデータの取得 も可能

- prismaを使えば可能っぽい
    
    ```tsx
    // server/api/users.get.ts
    import { prisma } from '~/server/db/prisma'
    
    export default defineEventHandler(async () => {
      const users = await prisma.user.findMany()
      return users
    })
    ```
    
    - 対応
        - MySQL / PostgreSQL / SQLite
        - Prisma / Drizzle / 生SQL
        - Redis / KV

### 向いていること

- BFF（画面専用API）
- DB CRUD
- 認証（セッション / JWT）
- 管理画面用 API
- SSR データ取得
    - Ex.
        
        ```tsx
        const { data } = await useFetch('/api/users')
        ```
        
        - SSR
            - 同一プロセス(HTTPを経由せずに)でサーバーハンドラ(defineEventHandler)を直接実行する
        - CSR
            - ブラウザからHTTPリクエストとしてserver/配下のapi/users/エンドポイントにアクセスする

### 向いていないこと

- 巨大なモノリス API
- 重いバッチ処理

### 実務でのよくある使い分け

- 小~中規模 Nuxt serverだけで完結
- BFFとして使う
    
    ```tsx
    Nuxt(server)
       ↓
    既存API（Rails / Go / etc）
    ```
    
- 本格バックエンドと分離

## まとめ

- Nuxt の server は「UIと同居できる軽量バックエンド（BFF）」
- Railsなどのバックエンドのフレームワークの代替というより、
    - フロントに最適化されたサーバー
    - SSR と密結合
    
    という立ち位置