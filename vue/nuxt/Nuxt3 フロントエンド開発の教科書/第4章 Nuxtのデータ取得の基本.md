## Nuxtのデータ取得処理

### $fetch

- URLを渡すだけでGETリクエストする
- Ex.
    
    ```tsx
    //実際にアクセスするURLを生成。
    const urlFull = `${weatherInfoUrl}?${queryParams}`;
    
    //URLに非同期でアクセスしてデータを取得。
    const response = await $fetch(urlFull) as any;
    ```
    
- 内部ではofetchを使用しており、第二引数のオプションのオブジェクトの指定によって、POSTリクエストを送ることも可能
    
    ```tsx
    $fetch(url, {method: "POST", body: {...}})
    ```
    

## データ取得処理をまとめておけるuseAsyncData()

- キャッシュの利用などよしなにやってくれる
- 構文
    
    ```tsx
    useAsyncData(
    	キー文字列,
    	(): Promise<取得データのデータ型> => {
    		データ取得処理
    		return 取得データ;
    	},
    	オプションオブジェクト
    );
    ```
    
    - 第一引数のキー文字列が同じuseAsyncData()関数の実行結果はキャッシュされ、再利用されるようになっている
        - 省略した場合は「ファイル名 +  行番号」
- Ex.
    
    ```tsx
    const asyncData = await useAsyncData(
    	`/WeatherInfo/${route.params.id}`,
    	(): Promise<any> => {
    		const weatherInfoUrl = "https://api.openweathermap.org/data/2.5/weather";
    		const params:{
    			...
    		} =
    		{
    			...		
    		}
    		const queryParams = new URLSearchParams(params);
    		const urlFull = `${weatherInfoUrl}?${queryParams}`;
    		const response = $fetch(urlFull);
    		return response;
    	},
    );
    
    const data = asyncData.data;
    const weatherArray = data.value.weather;
    const weather = weatherArray[0];
    weatherDescription.value = weather.description;
    ```
    
- 戻り値
    
    下記のデータが含まれたオブジェクトになる
    
    | プロパティ名 | 内容 |
    | --- | --- |
    | data | ハンドラの本来の戻り値 |
    | pending | データ取得が終了したかどうかを表すbool値 |
    | refresh | データを再取得する関数 |
    | error | データ取得失敗した時のエラーオブジェクト |

### pickオプション

- データ項目を絞り込めるオプション
- Ex.
    
    ```tsx
    const asyncData = await useAsyncData(
    	`/WeatherInfo/${route.params.id}`,
    	(): Promise<any> => {
    		const weatherInfoUrl = "https://api.openweathermap.org/data/2.5/weather";
    		...
    		const urlFull = `${weatherInfoUrl}?${queryParams}`;
    		const response = $fetch(urlFull);
    		return response;
    	},
    	{
    		pick: ["weather"],
    	}
    );
    const data = asyncData.data;
    ...
    ```
    
    - pick: 配列型式で必要なプロパティを列挙することで、戻り値のdata プロパティには指定したデータのみが含まれる

### transform オプション

- データを加工できるオプション
- Ex.
    
    ```tsx
    const asyncData = await useAsyncData(
    	`/WeatherInfo/${route.params.id}`,
    	(): Promise<any> => {
    		const weatherInfoUrl = "https://api.openweathermap.org/data/2.5/weather";
    		...
    		const urlFull = `${weatherInfoUrl}?${queryParams}`;
    		const response = $fetch(urlFull);
    		return response;
    	},
    	{
    		transform: (data: any): string => {
    			const weatherArray = data.weather;
    			const weather = weatherArray[0];
    			return weather.description;
    		}
    	}
    );
    const weatherDescription = asyncData.data;
    ```
    
    - transformの引数はuseAsyncData()の戻り値

## useAsyncData()と$fetchを簡潔に書けるuseFetch()

- useAsyncData()と$fetch()の組み合わせをより簡潔にかける関数として、`useFetch`が用意されている
- 戻り値はuseAsyncData()と同じ
- 構文
    
    ```tsx
    useFetch(
    	アクセス先URL,
    	オプションオブジェクト
    );
    ```
    
    - useAsyncData()と違い$fetchに渡していたURLを引数として渡せるため、簡潔な構文になっている
    - 第2引数のオプションオブジェクトは、useAsyncData()と同じものが指定できる一方でuseFetch()独自のオプションもある([公式](https://nuxt.com/docs/4.x/api/composables/use-fetch#parameters))
        - Ex. key, method, query, params, body, headers, baseURLなど
- Ex.
    
    ```tsx
    const params:{
    	lang: string;
    	q: string;
    	appid: string;
    } =
    {
    	lang: "ja",
    	q: selectedCity.value.q,
    	appid: "xxxxxx"
    }
    
    const asyncData = await useFetch(
    	"https://api.openweathermap.org/data/2.5/weather",
    	{
    		key: `/WeatherInfo/${route.params.id}`,
    		query: params,
    		transform: (data: any): string => {
    			const weatherArray = data.weather;
    			const weather = weatherArray[0];
    			return weather.description;
    		}
    	}
    );
    const weatherDescription = asyncData.data;
    ```
    
    - keyオプション useAsyncData()の第1引数と同じもの
    - queryオプション クエリパラメーターの設定

## ページ遷移を優先するLazy

- APIのレスポンスが遅いと、useFetch()などのアプローチではデータを取得するまでに画面が遷移せずユーザー体験が悪くなる
    - 処理順序を変更して、まずレンダリングを実行して画面表示を行い、その後データ取得処理を行うようにするのがlazyオプション
    - イメージ
        - p127

### lazyオプションがデフォルトのuseLazyAsyncData()

- Ex.
    
    ```tsx
    const asyncData = useLazyAsyncData(
    	`/WeatherInfo/${route.params.id}`,
    	...
    	const response = $fetch(urlFull);
    	return response;
    );
    ```
    
    - useAsyncDataをuseLazyAsyncDataに変更し、awaitを削除するだけでlazy版に変更できる

### 読み込み途中の表示に便利なpending

- useLazyAsyncData(useAsyncData)関数の戻り値オブジェクトのpendingプロパティはデータ取得が終了したかどうかを表すbool値であるため、読み込み途中の表示の出しわけに最適
- pendingプロパティの戻り値はリアクティブ変数である
- Ex.
    
    ```tsx
    <script lang="ts">
    ...
    const asyncData = useLazyAsyncData(
    	`/WeatherInfo/${route.params.id}`,
    	...
    	const response = $fetch(urlFull);
    	return response;
    );
    const weatherDescription = asyncData.data;
    const pending = asyncData.pending;
    </script>
    
    <template>
    	<p v-if="pending">データ取得中…</p>
    	<section v-else>
    		<h2>{{selectedCity.name}}の天気</h2>
    		<p>{{weatherDescription}}</p>
    	</section>
    	<p>リストに<NuxtLink v-bind:to="{name: 'index'}">戻る</NuxtLink></p>
    </template>
    ```