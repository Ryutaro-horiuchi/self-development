## ルーティング

- Nuxtはファイルベースのルーティングを提供し、Webアプリケーション内にルートを作成する
    
    → app.vueのみを使用する場合、vue-routerは含まれない。ページシステムを強制するには、nuxt.configで`pages: true`を設定するか、router.options.tsを用意する
    

### 使用方法

- 拡張子
    - ページはVueコンポーネントであり、Nuxtがサポートする有効な拡張子（デフォルトでは.vue、.js、.jsx、.mjs、.ts、.tsx）を持つことが可能
- Nuxtは `~/pages/` ディレクトリ内のすべてのページに対して自動的にルートを作成する。
    - app/pages/index.vue
        - アプリケーションの/ルートにマッピングされる
    - app/app.vue
        
        ```html
        <template>
          <div>
            <!-- 全ページで共有されるマークアップ例：ナビゲーションバー -->
            <NuxtPage />
          </div>
        </template>
        ```
        
        - app.vueを使用する場合、現在のページを表示するには必ず`<NuxtPage/>`コンポーネントを使用する
- ページは単一のルート要素を持たせる

### 動的ルート

- 動的ルートを使いたい場合、ファイル名またはフォルダ名に 角括弧 [ ] を使う。
- Ex. `app/pages/users-[group]/[id].vue`
    - 例えばURL /`users-admins/123` のようなアクセス時にこのコンポーネントがマッチする。
    - Options API
        - このコンポーネント内では、groupとidを`$route`オブジェクトを介してアクセスできる
            
            ```tsx
            <template>
              <p>{{ $route.params.group }} - {{ $route.params.id }}</p>
              <!-- <p>admins - 123</p>　-->
            </template>
            ```
            
    - Composition API
        - グローバルな`useRoute関数`を利用
            
            ```tsx
            <script setup lang="ts">
            const route = useRoute()
            
            if (route.params.group === 'admins' && !route.params.id) {
              console.log('Warning! Make sure user is authenticated!')
            }
            </script>
            
            ```
            

## Catch-all Route

- キャッチオールルート
    - そのパス配下のすべてのルートにマッチさせる
- `[...]slug.vue` というファイルを作成する
- Ex. `app/pages/[...slug].vue`
    
    ```tsx
    <template>
      <p>{{ $route.params.slug }}</p>
    </template>
    ```
    
    - /hello/world にアクセスすると、以下がレンダリングされる
        
        ```tsx
        <p>["hello", "world"]</p>
        ```
        

## Nested Routes

- `<NuxtPage>`を使用してネスト構造のディレクトリに沿ったルートを表示することが可能
- Ex.
    - ディレクトリ構造
        
        ```tsx
        -| pages/
        ---| parent/
        -----| child.vue
        ---| parent.vue
        
        ```
        
    - 上記だと以下のルートを生成する
        
        ```tsx
        [
          {
            path: '/parent',
            component: '~/pages/parent.vue',
            name: 'parent',
            children: [
              {
                path: 'child',
                component: '~/pages/parent/child.vue',
                name: 'parent-child',
              },
            ],
          },
        ]
        
        ```
        
    - 子コンポーネント `child.vue` を表示するには、app/pages/parent.vue 内に `<NuxtPage>` コンポーネントを挿入する必要がある
        - pages/parent.vue
            
            ```tsx
            <template>
              <div>
                <h1>I am the parent view</h1>
                <NuxtPage :foobar="123" />
              </div>
            </template>
            
            ```
            
        - pages/parent/child.vue
            
            ```tsx
            <script setup lang="ts">
            const props = defineProps({
              foobar: String,
            })
            
            console.log(props.foobar)
            </script>
            ```
            

### Child Route Keys

`NuxtPage>` が いつ再レンダリング (再描画) されるか を制御するための仕組み。

- ページ遷移したとき／パラメータが変わったとき／フルパスが変わったとき」など、「どの変化を “新しいページに切り替えるべきトリガー” とみなすかを明示できるようにするためのキー。
- 二通りの方法がある
    1. 親コンポーネント側で、子コンポーネントの属性にpageKeyプロパティをつける
        
        ```tsx
        <template>
          <div>
            <h1>I am the parent view</h1>
            <NuxtPage :page-key="route => route.fullPath" />
          </div>
        </template>
        
        ```
        
    2. 子コンポーネント側でdefinePageMeta を使って key を定義
        
        ```tsx
        <script setup lang="ts">
        definePageMeta({
          key: route => route.fullPath,
        })
        </script>
        
        ```
        

## Route Groups

- ファイルベースのルーティングに影響を与えない方法で、一連のルートをグループ化したい場合に使用
- Ex.
    
    ```tsx
    -| pages/
    ---| index.vue
    ---| (marketing)/
    -----| about.vue
    -----| contact.vue
    
    ```
    
    これにより、アプリ内に /、/about、/contact ページが生成される。
    

## Special Metadata

- アプリ全体で独自に使用するメタデータを定義することは可能
- 種類(抜粋)
    - `ailas`
        
        異なるパス名で同じページにアクセスすることができる
        
    - `keepalive`
        
        Nuxt は自動的にページを Vue の `<KeepAlive>` コンポーネントでラップする。これは、例えば動的な子ルートを持つ親ルートで、ルート変更時にページ状態を保持したい場合に有用
        
        [KeepAliveタグ](https://www.notion.so/KeepAlive-fd8e981bdf804e069937b0b374e2ef4f?pvs=21) 
        

## Navigation

ナビゲーションアプリのページ間を移動するには、`<NuxtLink>` コンポーネントを使用する

- Ex
    
    ```tsx
    <template>
      <NuxtLink to="/">Home page</NuxtLink>
    </template>
    
    ```
    

### プログラムによるナビゲーション

`navigateTo()`ユーティリティメソッドを通じてプログラムによるナビゲーションが可能

- Ex
    
    ```tsx
    <script setup lang="ts">
    const name = ref('')
    const type = ref(1)
    
    function navigate () {
      return navigateTo({
        path: '/search',
        query: {
          name: name.value,
          type: type.value,
        },
      })
    }
    </script>
    
    ```
    

## 複数ページのディレクトリ

- デフォルトでは、すべてのページはプロジェクトのルートにある `app/pages` ディレクトリに配置する必要がある。
    
    → ただし、Nuxt Layers を使用してアプリのページのグループ化を作成できる
    
    - Ex.
        - ディレクトリ構造
            
            ```tsx
            -| some-app/
            ---| nuxt.config.ts
            ---| pages/
            -----| app-page.vue
            -| nuxt.config.ts
            
            ```
            
        - some-app/nuxt.config.ts
            
            ```tsx
            // some-app/nuxt.config.ts
            export default defineNuxtConfig({
            })
            ```
            
        - nuxt.config.ts
            
            ```tsx
            export default defineNuxtConfig({
              extends: ['./some-app'],
            })
            
            ```