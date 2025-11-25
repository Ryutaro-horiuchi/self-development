# Components

## 自動インポート

- Nuxt.jsはcomponentsディレクトリ配下にあるコンポーネントを自動的にインポートする
    
    ```tsx
    -| components/
    ---| AppHeader.vue
    ---| AppFooter.vue
    
    app/app.vue
    <template>
      <div>
        <AppHeader />
        <NuxtPage />
        <AppFooter />
      </div>
    </template>
    ```
    

### コンポーネントの名前

- コンポーネント名は自身のファイルへのパスとファイル名に基づいて生成される。重複するセグメントは削除される
    - Ex.
        - ディレクトリ構造
            
            ```tsx
            -| components/
            ---| base/
            -----| foo/
            -------| Button.vue
            
            ```
            
        - コンポーネント名 `<BaseFooButton>`
            
            → コンポーネント名とファイル名を同一にすることを推奨
            
- コンポーネントをパスを考慮せず名前のみで自動インポートしたい場合は、設定オブジェクトの`pathPrefix`オプションをfalseにする
    
    ```tsx
    export default defineNuxtConfig({
      components: [
        {
          path: '~/components',
          pathPrefix: false,
        },
      ],
    })
    
    ```
    
    - これにより、例えば、`~/components/Some/MyComponent.vue` は `<SomeMyComponent>` ではなく `<MyComponent>` として使用可能になる

## 動的コンポーネント

- Vueの**`<component :is="someComputedComponent">`**構文を使用したい場合、下記のいずれかを実施する必要がある
    1. resolveComponentヘルパーを使用
    2. #componentsからコンポーネントを直接インポート
- Ex.
    
    ```tsx
    <script setup lang="ts">
    import { SomeComponent } from '#components'
    
    const MyButton = resolveComponent('MyButton')
    </script>
    
    <template>
      <component :is="clickable ? MyButton : 'div'" />
      <component :is="SomeComponent" />
    </template>
    
    ```
    
    - resolveComponentの引数はリテラル文字列のコンポーネント名

## グローバルオプション

- 推奨はされないが、全てのコンポーネントをグローバルに登録することも可能
    
    ```tsx
      export default defineNuxtConfig({
        components: {
    +     global: true,
    +     dirs: ['~/components']
        },
      })
    
    ```
    
- 一部のコンポーネントのみを選択的にグローバル登録することもできる
    - 下記いずれか
        1. ~/components/global ディレクトリに配置
        2. ファイル名に .global.vue サフィックスを付ける

## 動的インポート(遅延読み込み)

- コンポーネント名に「`Lazy`」プレフィックスを追加するだけで遅延読み込みになる
    - コンポーネントが常に必要でない時に有用
    - コンポーネントのコード読み込みを適切なタイミングまで遅らせることができ、JavaScriptバンドルのサイズ最適化に役立つ

```tsx
<script setup lang="ts">
const show = ref(false)
</script>

<template>
  <div>
    <h1>Mountains</h1>
    <LazyMountainsList v-if="show" />
    <button
      v-if="!show"
      @click="show = true"
    >
      Show List
    </button>
  </div>
</template>

```

## 遅延ハイドレーション(v4から)

### 前提

- 遅延コンポーネントは条件付きレンダリングされない限り、依然として積極的に読み込まれるため、常に実行時パフォーマンスを向上させるわけではない
    
    → アプリを最適化するには、一部のコンポーネントのハイドレーションを、表示されるまで、あるいはブラウザがより重要なタスクを完了するまで遅延させる必要がある
    
- ハイドレーションとは
    - SSRで出力されたただのHTMLに、Vueのイベント・状態管理・リアクティブ性などを紐付けて、有効化（hydration）するステップ

### 本題

- Nuxtは遅延ハイドレーションをサポートしており、コンポーネントがインタラクティブになるタイミングを制御できる
    - Nuxtはハイドレーション戦略を複数提供しており、コンポーネントに適用できる戦略は1つだけである
    - 遅延ハイドレーションされたコンポーネントのプロパティ変更は、直ちにハイドレーションをトリガーする

### ハイドレーション戦略

- `hydrate-on-visible`
    - コンポーネントがビューポート内で可視化された際にハイドレーションを実行
- `hydrate-on-idle`
    - ブラウザがアイドル状態になった際にコンポーネントをハイドレートする。最大タイムアウトとして数値を渡すことも可能
- `hydrate-on-interaction`
    - 指定されたインタラクション（例：クリック、マウスオーバー）後にコンポーネントをハイドレートします。
- `hydrate-on-media-query`
    - ウィンドウがメディアクエリに一致した際にコンポーネントをハイドレートします
- `hydrate-after`
    - 指定した遅延時間（ミリ秒単位）後にコンポーネントをハイドレートします
    - 特定の待機時間を許容できるコンポーネント向け
- `hydrate-when`
    - ブール値の条件に基づいてコンポーネントをハイドレートします。
    - 常にハイドレーションが必要でないコンポーネントに最適
- `hydrate-never`
    - コンポーネントをハイドレートしません。

### ハイドレーションイベントのリスニング

- `@hydrated`イベントを発行する

### 注意点とベストプラクティス

1. 表示領域内のコンテンツを優先
    
    重要な、画面上部のコンテンツには遅延ハイドレーションを避けてください。すぐに必要とされないコンテンツに最適です。
    
2. 条件付きレンダリング
    
    `v-if=「false」` を使用する場合、遅延ハイドレーションは不要かもしれません。通常の遅延コンポーネントを使用できる
    
3. 共有状態
    
    複数コンポーネント間で共有される状態（v-model）に注意。1コンポーネントでモデルを更新すると、そのモデルにバインドされた全コンポーネントでハイドレーションがトリガーされる可能性があります。
    

## 直接インポート

Nuxtの自動インポート機能を回避したい場合や必要に応じて、`#components` からコンポーネントを明示的にインポートする

```tsx
import { LazyMountainsList, NuxtLink } from '#components'
```

## カスタムディレクトリ

- デフォルトでは、~/componentsのみがスキャン対象。以下の例のように他のディレクトリの追加やスキャン方法を変更することができる

```tsx
export default defineNuxtConfig({
  components: [
    // ~/calendar-module/components/event/Update.vue => <EventUpdate />
    { path: '~/calendar-module/components' },

    // ~/user-module/components/account/UserDeleteDialog.vue => <UserDeleteDialog />
    { path: '~/user-module/components', pathPrefix: false },

    // ~/components/special-components/Btn.vue => <SpecialBtn />
    { path: '~/components/special-components', prefix: 'Special' },

    // `~/components` のサブディレクトリに適用したいオーバーライドがある場合、
    // これを最後に記述することが重要です。
    // ~/components/Btn.vue => <Btn />
    // ~/components/base/Btn.vue => <BaseBtn />
    '~/components',
  ],
})

```

## npm パッケージからコンポーネントを読みこむ

npmパッケージからコンポーネントを自動インポートしたい場合、ローカルモジュール内で`addComponent`を使用して登録できる

```tsx
import { addComponent, defineNuxtModule } from '@nuxt/kit'

export default defineNuxtModule({
  setup () {
    // import { MyComponent as MyAutoImportedComponent } from 'my-npm-package'
    addComponent({
      name: 'MyAutoImportedComponent',
      export: 'MyComponent',
      filePath: 'my-npm-package',
    })
  },
})

```

## Client Components

- コンポーネントをクライアントサイドでのみレンダリングしたい場合、コンポーネント名に `.client` サフィックスを追加できます。
- 比較
    
    
    | 種類 | SSR HTML | Hydration | 実行場所 |
    | --- | --- | --- | --- |
    | **Server Components**（デフォルト） | 生成される | あり | 主にサーバー（＋一部クライアント） |
    | **Client Components** | ❌ 生成されない | ❌ ない | クライアントのみ |
    - ブラウザAPIを使うコンポーネントがあるときに有用
- Ex.
    
    ```tsx
    | components/
    --| Comments.client.vue
    
    ```
    
    ```tsx
    <template>
      <div>
        <!-- this component will only be rendered on client side -->
        <Comments />
      </div>
    </template>
    
    ```