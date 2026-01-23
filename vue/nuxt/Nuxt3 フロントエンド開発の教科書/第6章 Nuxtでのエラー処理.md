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
    -