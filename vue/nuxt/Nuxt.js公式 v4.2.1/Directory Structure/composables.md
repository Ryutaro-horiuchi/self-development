composablesディレクトリ配下のVueコンポーザブルを自動インポートする

## 使用方法

### 定義

1. 名前付きエクスポート
    
    ```tsx
    export const useFoo = () => {
      return useState('foo', () => 'bar')
    }
    ```
    
2. デフォルトエクスポート
    
    ```tsx
    // It will be available as useFoo() (camelCase of file name without extension)
    export default function () {
      return useState('foo', () => 'bar')
    }
    ```
    

### 使用

.js, .ts, .vueファイルで自動インポートされたコンポーザブルを使用できるようになる

```tsx
<script setup lang="ts">
const foo = useFoo()
</script>

<template>
  <div>
    {{ foo }}
  </div>
</template>

```

## ネストされたコンポーザブル

- 自動インポートを使用して、コンポーザブルを別のコンポーザブル内で使用できる
    
    ```tsx
    export const useFoo = () => {
      const nuxtApp = useNuxtApp()
      const bar = useBar()
    }
    ```
    

### [プラグイン](https://nuxt.com/docs/4.x/directory-structure/app/plugins#providing-helpers)へアクセス

```tsx
export const useHello = () => {
  const nuxtApp = useNuxtApp()
  return nuxtApp.$hello
}

```

## ファイルのスキャン方法

- Nuxtはapp/composables/ディレクトリの最上位にあるファイルのみをスキャンする
- ネストされたモジュールは対象外となるため、再エクスポート(推奨)するか、スキャナーの設定でネストされたディレクトリを含めるようにする
- Ex. 再エクスポート
    
    ```tsx
    // Enables auto import for this export
    export { utils } from './nested/utils.ts'
    ```