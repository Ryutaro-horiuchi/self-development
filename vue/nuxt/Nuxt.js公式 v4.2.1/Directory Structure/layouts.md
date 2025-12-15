- 複数のページ (routes) に共通する UI 部分 (たとえばヘッダー／サイドバー／フッター／共通レイアウト構造など) を “レイアウト (layout)” としてまとめておける仕組みを提供している。
- **`app/layouts/`** ディレクトリに置く
    - このディレクトリに配置されたコンポーネントは、使用時に非同期インポートによって自動的に読み込まれる

## レイアウトの有効化

- app.vueに`<NuxtLayout>`を追加することで有効化されます
- Ex. app/app.vue
    
    ```tsx
    <template>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </template>
    
    ```
    

## デフォルトのレイアウト

- `app/layouts/default.vue` ファイルがデフォルトのレイアウトとして使用できる
- Ex. `app/layouts/default.vue`
    
    ```tsx
    <template>
      <div>
        <p>Some default layout content shared across all pages</p>
        <slot />
      </div>
    </template>
    
    ```
    
    - ページの内容は`<slot />`コンポーネント内で表示される

## 名前付きレイアウト

- Ex.
    - ディレクトリ構造
        
        ```tsx
        -| layouts/
        ---| default.vue
        ---| custom.vue
        
        ```
        
    - ページ内で`custom`レイアウトを指定できる
        
        ```tsx
        <script setup lang="ts">
        definePageMeta({
          layout: 'custom',
        })
        </script>
        
        ```
        
    - `<NuxtLayout>`の`name`プロパティを使用して、全てのページのデフォルトレイアウトを上書きできる
        
        ```tsx
        <script setup lang="ts">
        const layout = 'custom'
        </script>
        
        <template>
          <NuxtLayout :name="layout">
            <NuxtPage />
          </NuxtLayout>
        </template>
        ```
        

## レイアウトを動的に変更する

- setPageLayoutヘルパーを使用する
    
    ```tsx
    <script setup lang="ts">
    function enableCustomLayout () {
      setPageLayout('custom')
    }
    definePageMeta({
      layout: false,
    })
    </script>
    
    <template>
      <div>
        <button @click="enableCustomLayout">
          Update layout
        </button>
      </div>
    </template>
    
    ```
    

## **ページごとにレイアウトを自由に制御する**

- pages 機能を使っている場合、`layout: false`を指定すると Nuxt による自動レイアウト適用を無効化できる
- その上で、ページコンポーネントの中で`<NuxtLayout>`を自分で配置することで、どのレイアウトをどこで使うかを完全にコントロールできる
- Ex.
    - app/pages/index.vue
        
        ```tsx
        <script setup lang="ts">
        definePageMeta({
          layout: false,
        })
        </script>
        
        <template>
          <div>
            <NuxtLayout name="custom">
              <template #header>
                Some header template content.
              </template>
        
              The rest of the page
            </NuxtLayout>
          </div>
        </template>
        
        ```
        
    - app/layouts/custom.vue
        
        ```tsx
        <template>
          <div>
            <header>
              <slot name="header">
                Default header content
              </slot>
            </header>
            <main>
              <slot />
            </main>
          </div>
        </template>
        
        ```