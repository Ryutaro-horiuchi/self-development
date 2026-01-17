Nuxtでは、Vue Routerを内部に含みながら、より簡単にVue Routerを利用できる仕組みになっている

## Nuxtルーティングの基本

### ルーティング表示領域を設定するNuxtPageタグ

- Ex
    
    ```tsx
    <template>
    	<header>
    		<h1>ルーティングサンプル</h1>
    	</header>
    	<main>
    		<NuxtPage/>
    	</main>
    </template>
    ```
    
- ルーティングに応じた画面表示領域を設定する。
- Vue Routerでは`RouterView`タグだが、Nuxtでは`NuxtPage`タグである
- NuxtPageはルートタグとしては使えない
    - → templateタグ直下に置くことができない

### Nuxtはファイルシステムルーター

- 画面用コンポーネントは全てpages配下に格納する。
    
    → 格納するファイルパス構造がそのままルーティングパスとなっている
    
    - ルートに該当するファイルは`index.vue`となっている
- Ex.
    - ルート `/member/memberList` → `pages/member/memberList.vue`

### リンク生成はNuxtLinkタグ

- Ex.
    
    ```tsx
    <NuxtLink v-bind:to="{name: 'member-memberList'}">
    
    # 直接パスを記述しても問題なく動作する
    <NuxtLInk to="/member/memberList">
    ```
    
    - 筆者曰く通常は柔軟性やメンテナンス性の観点でv-bindディレクティブを使用するケースが多いとのこと
    - v-bindディレクトリのnameプロパティを使用する際、ハイフン区切りのコンポーネントファイルパスとなる
        - トップ画面は`name: ‘index’`となる

## ルートパラメーターとルーティング制御

### ルートパラメーターは`[]`のファイル名

- pagesディレクトリ内で`[]`で囲まれたファイル名のコンポーネントファイルは、ルートパラメーターとして扱うルールになっている
    - ユーザーの詳細情報などで、会員IDを含めたパスを設定したいときなどに使用
- 構文
    
    ```tsx
    pages/・・・/[ルートパラメーター名].vue
    ```
    

### ルートパラメーターの取得はルートオブジェクトから

- Ex
    - pages/member/memberDetail/[id].vue
        
        ```tsx
        <script setup lang="ts">
        /ルートオブジェクトを取得。
        const route = useRoute();
        //会員情報リストをステートから取得。
        const memberList = useState<Map<number, Member>>("memberList");
        //会員情報リストから該当会員情報を取得。
        const member = computed(
        	(): Member => {
        		const id = Number(route.params.id);
        		return memberList.value.get(id) as Member;
        	}
        	
        </script>
        ```
        
- useRoute()関数を実行することで、現在のルートに関する情報が格納されたルートオブジェクトを取得できる
    - ルートオブジェクトは[`RouteLocationNormalized`](https://router.vuejs.org/api/interfaces/RouteLocationNormalizedGeneric.html)型
        - ルーティング名やパス、#以降の文字列や、クエリパラメーター、ルートパラメーターを取得できる
- templateでは、`$route`と記述するだけで取得できる
    
    ```tsx
    <section>
    	<p>{{ $route.paramas }}</p>
    </section>
    ```
    

### ルートパラメーターを含むNuxtLinkタグ

- ルートパラメーターはparamsプロパティを使用する
- nameプロパティは、[]を取り除いたパス名になる
- Ex.
    
    ```tsx
    <NuxtLink v-bind:to="{name: 'member-memberDetail-id', params: {id: id}}">
    	IDが{{id}}の{{member.name}}さん
    </NuxtLink>
    ```
    

### ルーティングを制御するルーターオブジェクト

- 特定の画面への遷移や履歴の一つ前の画面へ遷移するなどルーティングを制御するのがルーターオブジェクトであり、`useRouter()`を実行して取得する
- Ex.
    
    ```tsx
    //フォームがサブミットされた時の処理。
    const onAdd = (): void => {
    	memberList.value.set(member.id, member);
    	router.push({name: "member-memberList"});
    };
    ```
    
- Routerオブジェクトのメソッド
    
    
    | メソッド | 内容 |
    | --- | --- |
    | push() | 指定パスに遷移する |
    | replace() | 現在のパスを置き換える |
    | back() | 履歴上の一つ前の画面に戻る |
    | forward() | 履歴上の一つ次の画面に進む |
    | go() | 履歴上の指定の画面に進む |

### ルートパラメーターのバリエーション

- 複数パラメーター
    - Ex. `pages/member/[name]/[points]/.vue`
        - リンク例 /member/search/suzuki/45
- ハイフンを使ったパラメーター
    - Ex. `pages/member/[name]-san/.vue`
        - リンク例 /member/yamamoto-san
            
            → この時、yamamotoがルートパラメーターとして使用される
            
    - `[ ]`と普通の文字を繋げられるのはハイフンのみ
- 省略可能パラメーター
    - `[[ ]]` と二重で使用すると省略可能なパラメーターになる
    - Ex. `pages/member/show/[name]/[[points]].vue`
    - リンク例
        - pages/member/show/suzuki/34
        - pages/member/show/tanaka
- 可変長パラメーター
    - スプレッド演算子を使用した可変長なルートパラメーター
    - Ex. `pages/member/call/[…id].vue`
    - リンク例
        - /member/call
        - /member/call/14/24/65

## ネストされたルーティング

- App.vueとは別の画面内でルーティング表示領域(ページが切り替わる領域)がある状態のこと
    - イメージ
        
        p86 画像
        

### ネストされたルーティングを実現するパス

- 例えば memberList.vue内でルーティング表示領域を設けたいとする場合、同階層にmemberListというフォルダを作成し、ネストして表示するコンポーネントをそのフォルダに格納する
- Ex.
    - pages/member/memberList.vue
        
        ```tsx
        <template>
        ...
        	<section>
        		<h2>会員リスト</h2>
        		...
        		<section>
        			...
        		</section>
        		<NuxtPage/>
        	</section>
        ```
        
    - pages/member/memberList配下に、memberList.vue内で表示させたいコンポーネントw用意すればあとはOK

## レイアウト機能

- 個々のページに適用する共通部分のレイアウトを定義できる
- ページに応じて使用するレイアウトを変えるなど柔軟な対応が可能

### レイアウトコンポーネントではslotを利用

- Nuxtのレイアウト機能を使用するときは、layoutsフォルダ内にコンポーネントを作成することになっている
    - デフォルトで適用させるコンポーネント名は`default.vue`とすることになっている
- これまでApp.vueでNuxtPageを利用していた部分をlayoutではslotを使用する
- Ex. layouts/default.vue
    
    ```tsx
    <template>
    	<header>
    		<h1>レイアウトサンプル</h1>
    	</header>
    	<main>
    		<slot/>
    	</main>
    </template>
    ```
    

### レイアウトの適用は NuxtLayout タグ

- レイアウトを適用させるためには、NuxtLayoutタグを使用する必要がある
- Ex. app.vue
    
    ```tsx
    <template>
    	<NuxtLayout>
    		<NuxtPage/>
    	</NuxtLayout>
    </template>
    ```
    

### デフォルト以外のレイアウト

- 複数のレイアウトファイルを作成することで、共通部分の切り替えが可能になる
- カスタムレイアウトの適用例
    - カスタムレイアウトファイル `layouts/member.vue`
        
        ```tsx
        <template>
        	<header>
        		<h1>レイアウトサンプル</h1>
        	</header>
        	<main>
        		<h1>会員管理</h1>
        		<slot/>
        	</main>
        </template>
        
        ```
        
    - カスタムレイアウトを適用するには、`definePageMeta`を使用する
        
        ```tsx
        <script>
        ...
        definePageMeta({
        	layout: "member"
        	// layout: false
        });
        </script>
        ```
        
        - falseを使用するとレイアウトを何も適用しない

## ヘッダ情報の変更機能

### ヘッダ情報を変更する [useHead()](https://nuxt.com/docs/4.x/api/composables/use-head)

- ヘッダ情報を設定する場合はuseHead()関数を使う
- Ex. タイトルタグの設定
    - pages/member/memberList.vue
        
        ```tsx
        <script setup lang="ts">
        const PAGE_TITLE = "会員リスト";
        
        useHead({
        	title: PAGE_TITLE
        });
        </script>
        ```
        
- 公式の例
    
    ```tsx
    <script setup lang="ts">
    useHead({
      title: 'My App',
      meta: [
        { name: 'description', content: 'My amazing site.' },
      ],
      bodyAttrs: {
        class: 'test',
      },
      script: [{ innerHTML: 'console.log(\'Hello world\')' }],
    })
    </script>
    ```
    

### titleのテンプレートを記述できるtitleTemplate

- タイトルタグを動的に変更したいとき
    - 下層ページで「ページタイトル | サイトタイトル」としたいなど
    - titleTemplateを使用する
- Ex.
    - app.vue
        
        ```tsx
        <script setup lang="ts">
        const SITE_TITLE = "ヘッダ変更サンプル";
        
        useHead({
        	// title: SITE_TITLE,
        	titleTemplate: (titleChunk: string|undefined): string => {
        		let title = SITE_TITLE;
        		if(titleChunk != undefined) {
        			title = `${titleChunk} | ${SITE_TITLE}`;
        		}
        		return title;
        	}
        	// titleTemplate: `%s | ${SITE_TITLE}`
        });
        </script>
        ```
        
    - `titleChunk`
        - 各ページに設定されているtitleプロパティが渡される
            - titleプロパティが設定されていない場合もあるため、undefined型とのユニオン型である
    - `%s`
        - titleChunkの値が自動で設定される
    - このコードによりタブに「会員リスト | ヘッダ変更サンプル」と表示される