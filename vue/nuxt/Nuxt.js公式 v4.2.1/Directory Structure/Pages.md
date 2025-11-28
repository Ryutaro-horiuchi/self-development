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