- Nuxtアプリケーションのメインコンポーネント
- app/pages/ディレクトリが存在する場合、app.vueファイルは任意
- 独自のapp.vueの追加や、カスタマイズすることも可能

## 最小限の使用

- app/pagesディレクトリはオプションであり、ない場合はvue-rotuerの依存関係を含まない
- app/app.vue
    
    ```tsx
    <template>
      <h1>Hello World!</h1>
    </template>
    ```
    

## Pagesでの使用

- app/pagesディレクトリがある場合、現在のページを表示するには`<NuxtPage>`コンポーネントを使用する
    
    [pages](https://www.notion.so/pages-2b993db055548082b19ded302ee4ca66?pvs=21) 
    
- app/app.vue
    
    ```tsx
    <template>
      <NuxtPage />
    </template>
    
    ```
    

## Layoutsでの使用

- アプリケーションで異なるページ、異なるレイアウトが必要な場合は`<NuxtLayout>`コンポーネントと`app/layouts`ディレクトリを使用する
    - [layouts](https://www.notion.so/layouts-2bb93db055548056bad2f86b05106693?pvs=21)
- app/app.vue
    
    ```tsx
    <template>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </template>
    
    ```