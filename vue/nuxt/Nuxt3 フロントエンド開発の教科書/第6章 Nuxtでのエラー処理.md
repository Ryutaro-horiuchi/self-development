## Nuxtのエラー発生とエラー処理タグ

### エラーを発生させるcreateError()

- Nuxtでは効率よくエラーを発生させる仕組みとして、createError()関数が用意されている
- Ex.
    
    ```tsx
    throw createError("エラー発生")
    ```
    

### エラー時の表示を実現するNuxtErrorBoundaryタグ

- Ex.
    
    ```tsx
    <template>
    	<NuxtErrorBoundary>
    		<ErrorGeneratorBasic/>
    		<template v-slot:error="errorProps">
    			<p>エラーが発生しました!</p>
    			<p>{{errorProps.error}}</p>
    			<button v-on:click="onResetButtonClick(errorProps.error)">エラーを解消</button>
    		</template>
    	</NuxtErrorBoundary>
    </template>_
    ```
    
    - 子コンポーネントでエラーが発生した際の表示内容を記述し、v-slot:errorディレクティブのtemplateタグで囲む。
    - 属性値は任意。そのerrorプロパティにエラー内容が入っている


## 画面を遷移するnavigateTo

```tsx
const onResetButtonClick = async (error: Ref): Promise<void> => {
	await navigateTo("/");
	error.value = null;
}
```

## エラー画面

- エラー画面に遷移させたい時は、NuxtErrorBoundaryを使用しない

### 擬似的な500エラー

- createErrorの引数オブジェクトfatal: trueを渡すとクライアントサイドでも500エラーをスローできる
    
    ```tsx
    const onThrowsErrorClick = (): void => {
    	throw createError({
    		message: "致命的な擬似エラー発生。",
    		fatal: true
    	});
    };
    ```
    
    - これにより、エラー画面へ遷移する

### エラー画面のカスタマイズ

- プロジェクト直下にerror.vueを置く
- Ex. error.vue
    
    ```tsx
    <script setup lang="ts">
    interface Props {
    	error: {
    		statusCode?: string;
    		statusMessage?: string;
    		message?: string;
    		stack?: string;
    	};
    }
    defineProps<Props>();
    
    const onBackButtonClick = () => {
    	clearError({redirect: "/"});
    }
    </script>
    
    <template>
    	<h1>障害が発生しました!</h1>
    	<h2>{{error.statusCode}}: {{error.statusMessage}}</h2>
    	<p>{{error.message}}</p>
    	<p>{{error.stack}}</p>
    	<button v-on:click="onBackButtonClick">戻る</button>
    </template>
    ```
    
    - エラー内容がPropsとして渡ってくる
        - 全てオプションであることに注意
    - clearError
        - 現時点で発生しているエラーをクリアし、指定したページの遷移を行なってくれる関数

## サーバーAPIエンドポイントのエラー処理

```tsx
<script setup lang="ts">
const onThrowsErrorClick = async (): Promise<void> => {
	const asyncData = await useFetch("/api/generateError");
	const errorValue = asyncData.error.value;
	if(errorValue != null) {
		throw createError({
			message: `サーバでエラーが発生しました: ${errorValue.message}`,
			statusCode: errorValue.statusCode,
			statusMessage: errorValue.statusMessage,
			fatal: true
		});
	}
};
</script>

<template>
	<section>
		サーバでエラーを<button v-on:click="onThrowsErrorClick">発生</button>
	</section>
</template>

```

- useFetchにてエンドポイントにアクセスしエラーが返ってきた場合、戻り値オブジェクトのerrorプロパティにエラー内容が格納される。エラーがない場合はnull(リアクティブ変数であるため、.valueでアクセス)
- エラーがあった場合createErrorに渡すことで、エラー画面を表示させている

### 余談

- httpbin
    - エラーを擬似的に発生してくれるWebサービスが存在する
    - Ex.
        
        ```tsx
        https://httpbin.org/status/500
        ```