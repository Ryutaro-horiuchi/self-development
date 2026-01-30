## クッキーを利用する際の関数 useCookie()

- 構文
    
    ```tsx
    const 変数　= useCookie<データ型>("クッキー名", オプションオブジェクト)
    ```
    
- Ex.
    
    ```tsx
    //ログインユーザ情報をクッキーに格納。
    const loginUserCookie = useCookie<User|null>("loginUser");
    loginUserCookie.value = asyncData.data.value.user;
    ```
    
- useCookieを使用したクッキーオブジェクトはリアクティブな変数であるため、.valueプロパティに値を代入する
- 本来クッキーに格納できるのは文字列だけだが、useCookieが用意したクッキーオブジェクトに代入する際、自動的にJSON.stringifyによるエンコードが行われるため、エンコードの処理は不要になっている
- [オプションオブジェクト](https://nuxt.com/docs/4.x/api/composables/use-cookie#parameters)
- 値がない場合はnullとなるため、型は必ずnullを含める必要がある

## ルートミドルウェア

画面遷移の途中で処理を挟み込むのをルートミドルウェアと呼ぶ。Nuxtでは3種類のものがある

### インラインミドルウェア

- 構文
    
    ```tsx
    definePageMeta({
      middleware: (to, from) => {
    	  ルートミドルウェア処理
    	}
    })
    ```
    
    - 引数はどちらもRouteLocationNormalizedオブジェクトであり、第一引数toが遷移先のルート、第二引数fromが遷移元のルートに関するデータが格納されている
    - 戻り値は以下いずれか
        
        
        | コード | 内容 |
        | --- | --- |
        | return; | 画面遷移処理を続行 |
        | return navigateTo(遷移先パス) | 画面遷移処理を中断し指定の画面へ遷移 |
        | return abortNavigation(); | 画面遷移処理を中断。404エラー |
        | return abortNavigation(エラーオブジェクト); | 画面遷移処理を中断し、エラーを発生。500エラー |
- Ex.
    
    ```tsx
    <script setup lang="ts">
    import type {User} from "@/interfaces";
    
    definePageMeta({
      middleware: (to, from) => {
    	const loginTokenCookie = useCookie<string|null>("loginToken");
    	const loginUserCookie = useCookie<User|null>("loginUser");
    	if(loginTokenCookie.value  == null || loginUserCookie.value == null) {
    		return navigateTo("/login");
    	}
    	else {
    		return;
    	}
    }
    });
    </script>
    
    ```
    
    - 挙動としてログイン状態の場合は問題なくトップ画面が表示されるが、ログアウト状態の場合はログイン画面へ強制的に遷移される
        - 上記処理はコンポーネントのレンダリングが行われる前に、実行される

### ミドルウェアを再利用できる名前付きミドルウェア

- ミドルウェアファイルの作成
    - 名前付きミドルウェアは、その処理が記述されたファイルをmiddlewareフォルダ内に格納する
    - ファイル名の記法はケバブ記法となっている
    - Ex.
        - middleware/loggedin-check.ts
            
            ```tsx
            import type {User} from "@/interfaces";
            
            export default defineNuxtRouteMiddleware(
            	(to, from) => {
            		const loginTokenCookie = useCookie<string|null>("loginToken");
            		const loginUserCookie = useCookie<User|null>("loginUser");
            		if(loginTokenCookie.value == null || loginUserCookie.value == null) {
            			return navigateTo("/login");
            		}
            		else {
            			return;
            		}
            	}
            );
            ```
            
            - 名前付きルートミドルウェアを定義する場合は、`defineNuxtRouteMiddleware()`関数の実行をデフォルトエクスポートするだけ
            - 中身はインラインミドルウェアと同じ
- 名前付きミドルウェアの適用
    - index.vue
    
    ```tsx
    <script setup lang="ts">
    ...
    definePageMeta({
    	middleware: **["loggedin-check"]**
    	// middleware: "loggedin-check"
    })
    ...
    </script>
    ```
    
    - middlewareプロパティに対して、middleware内のファイル配列型式か文字列で記述するだけ
- ミドルウェアの実行順序は配列の順序
    - 1つ目のミドルウェアでreturn以外が返されると、その後のミドルウェアは実行されなくなる

### 全てのルーティングに適用されるグローバルミドルウェア

- ミドルウェアのファイルの拡張子を.global.tsとするだけで、自動的にグローバルミドルウェアとなり、全ての画面遷移に適用されるようになる


## サーバーミドルウェア

サーバーAPIエンドポイント側の処理が行われる前に処理を挟み込める

### サーバーミドルウェアの作り方

- server/middlewareフォルダ内に作成する
- Ex. server/middleware/logging.ts
    
    ```tsx
    export default defineEventHandler(
    	(event) => {
    		console.log(`リクエスト情報: ${event.node.req.url}`);
    	}
    );
    ```
    
    - サーバーミドルウェアの構文はサーバーAPIエンドポイント処理の構文と同じ
    - [Nuxtエンドポイントの作成 defineEventHandler](https://www.notion.so/Nuxt-defineEventHandler-2ed93db0555480ff9873c72656722dd3?pvs=21)

### 注意点

- 戻り値は記述できない
- 必ずグローバルで適用される

## Column

- データベースや認証などバックエンドに必要な機能を提供するサービスをBaaSと呼ぶ
- GoogleのFirebaseが有名だが、最近人気なのがSupabase
    - 大きな違いはFirebaseはNoSQLなのに対し、SupabaseはPostgreSQLを利用したRDBである点