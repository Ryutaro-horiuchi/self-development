## npm runのオプション

### buildオプション

- 本運用で動作するファイル一式が作成される
- 作成されたビルドファイル一式は、この構成のままNode.js上で動作するように作成されている
    - .output/serverフォルダ内に生成されたindex.mjsファイルを下記コマンドで実行することで、プロジェクトが動作する
        
        ```tsx
        node .output/server/index.mjs
        ```
        

### previewオプション

- ビルドされたプロジェクトの実行コマンド`node .output/server/index.mjs`とほぼ同じ動きをする
- 違いは `.env`の扱い
    - previewオプションだと、.envファイルの環境変数を読み込んでくれる。
        - → 本番運用により近いはnodeコマンドによる実行である

### generateオプション

- 静的ファイル一式が作成される
    - 各ページごとに静的ファイルとその相方となるjsファイル(_nuxtフォルダ内)を作成する
- 制約
    - serverフォルダ内の処理には対応できない
    - 外部APIへのアクセスが含まれたコードもgenerateコマンド実行したタイミングでAPIを取得し静的HTMLを生成するため、画面が表示されたタイミングでの実行ではなくなる
- ブラウザでのプレビューコマンド
    
    ```tsx
    npx serve .output/public
    ```
    

## Nuxtのレンダリング

NuxtにはCSR, SSR, SSG, ISGの4種のレンダリングモードがある。これらの違いを実際のコードと検証ツールを踏まえ確認する

### 前準備

下記準備

|  | パス | プロジェクト内パス | レンダリングモード |
| --- | --- | --- | --- |
| 1 | / | pages/index.vue | 指定なし |
| 2 | /spa | pages/spa.vue | CSR |
| 3 | /universal | pages/universal.vue | SSR |
| 4 | /ssg | pages/ssg.vue | SSG |
| 5 | /isg | pages/isg.vue | ISG |
- index.vueを除く各コンポーネントの共通コード
    
    ```tsx
    <script setup lang="ts">
    const now = new Date();
    const nowTime = ref(now.toLocaleTimeString());
    </script>
    
    <template>
    	<p>現在の時刻: {{nowTime}}</p>
    	<p>
    		<NuxtLink v-bind:to="{name: 'index'}">
    			戻る
    		</NuxtLink>
    	</p>
    </template>
    
    ```
    
    画面イメージ
    
    ![名称未設定.png](attachment:f6ddf225-3393-4bbc-83a6-8da74ae9cfba:名称未設定.png)
    

### レンダリングモードの設定

nuxt.config.ts

```tsx
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	devtools: { enabled: true },
	routeRules: {
		"/spa": {ssr: false},
		"/ssg": {prerender: true},
		"/isg": {swr: 60}
	}
});

```

- `routeRulesプ`ロパティを使用する。設定値は以下フォーマット
    
    ```tsx
    "パス": { レンダリングモード設定 }
    ```
    
    - パスは`/members/**`のようなmembers配下にあるファイル全てを対象といったワイルドカードを使用した指定も可能
    - レンダリングモード設定
        
        
        | 設定記述 | 内容 |
        | --- | --- |
        | ssr: false | レンダリングモードをCSRに設定 |
        | prerender: true | レンダリングモードをSSGに設定 |
        | swr: 数値 | レンダリングモードをISGに設定し、指定した数値の秒数ごとに再レンダリング |
        | isr: true | レンダリングモードをCDNにも対応したISGに設定 |
        - SSRを基本としたユニバーサルレンダリングがNuxtではデフォルトになっているため、SSRでレンダリングするときは何も設定する必要がない

### CSRの挙動

- /spaに遷移し「ページのソースを表示」
    
    ```tsx
    
    <!DOCTYPE html>
    <html>
    ...
    <body><div id="__nuxt"><svg class="nuxt-spa-loading" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 37 25" fill="none" width="80">...</script></body>
    </html>
    ```
    
    - __nuxt内には、時刻の表示や戻るリンクに関するタグは記述されていない
- CSRイメージ

### SSRの挙動

- /universalに遷移し、「ページのソースを表示」
    
    ```tsx
    <!DOCTYPE html>
    <html>
    ...
    <body ><div id="__nuxt"><!--[--><p>現在の時刻: 21:46:34</p><p><a href="/" class=""> 戻る </a></p><!--]--></div><script type="application/json" id="__NUXT_DATA__" data-ssr="true">[["Reactive",1],{"data":2,"state":3,"_errors":4,"serverRendered":5,"path":6},{},{},{},true,"/universal"]</script><script>window.__NUXT__={};window.__NUXT__.config={public:{},app:{baseURL:"/",buildAssetsDir:"/_nuxt/",cdnURL:""}}</script><script type="module" src="/_nuxt/entry.58b6f3a7.js" crossorigin></script></body>
    </html>
    ```
    
    - CSRとは違い、サーバーからレスポンスが送信された段階で、すでにdivタグ内にレンダリングされていることがわかる
- SSRイメージ


### SSGとISGの挙動

<aside>
💡

まだ発展途上である

</aside>

- /ssgに遷移し、　ページのソースを表示
    
    ```tsx
    <html >
    ...
    <body ><div id="__nuxt"><!--[--><p>現在の時刻: 6:29:42</p><p><a href="/" class=""> 戻る </a></p><!--]--></div><script type="application/json" id="__NUXT_DATA__" data-ssr="true">[["Reactive",1],{"data":2,"state":3,"_errors":4,"serverRendered":5,"path":6,"prerenderedAt":7},{},{},{},true,"/ssg",1770240582821]</script><script>window.__NUXT__={};window.__NUXT__.config={public:{},app:{baseURL:"/",buildAssetsDir:"/_nuxt/",cdnURL:""}}</script><script type="module" src="/_nuxt/entry.58b6f3a7.js" crossorigin></script></body>
    </html>
    ```
    
    - 何回リロードしても時刻は変わらない
    - 発展途上な点
        - サーバーサイド側ではSSGの挙動として問題ないが、フロント側では画面をリロードするとJSが実行されて、表示時刻が更新されてしまう
        - SSGがまともに動作する環境は限定的で、NetlifyとVercelのみとアナウンスされている
- /Isgに遷移
    
    ```tsx
    <html >
    ...
    <body ><div id="__nuxt"><!--[--><p>現在の時刻: 6:34:45</p><p><a href="/" class=""> 戻る </a></p><!--]--></div><script type="application/json" id="__NUXT_DATA__" data-ssr="true">[["Reactive",1],{"data":2,"state":3,"_errors":4,"serverRendered":5,"path":6,"prerenderedAt":7},{},{},{},true,"/ssg",1770240582821]</script><script>window.__NUXT__={};window.__NUXT__.config={public:{},app:{baseURL:"/",buildAssetsDir:"/_nuxt/",cdnURL:""}}</script><script type="module" src="/_nuxt/entry.58b6f3a7.js" crossorigin></script></body>
    </html>
    ```
    
    - 一定時間(60秒)過ぎてから更新すると、時刻が更新される