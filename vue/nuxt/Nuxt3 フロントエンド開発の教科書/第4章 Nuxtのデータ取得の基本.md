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


## データ取得処理を再実行するリフレッシュ

- refreshプロパティ
    - useAsyncDataと同じ処理を含んだ関数となっており、このプロパティを関数として実行するだけで、useAsyncData()関数が再実行される
    - refreshプロパティを関数として実行する際、関数内に新しいパラメーターを用意するコードがないと再実行の際に新しい情報は取得されない
    - Ex.
        
        ```tsx
        const asyncData = await useAsyncData(
        	(): Promise<any> => {
        		...
        		const response = $fetch(urlFull);
        		return response;
        	},
        	{
        		transform: (data: any): string => {
        			...
        		}
        	}
        );
        const pending = asyncData.pending;
        const weatherDescription = asyncData.data;
        const refresh = asyncData.refresh;
        
        const onCityChanged = () => {
        	selectedCity.value = cityList.value.get(selectedCityId.value) as City;
        	refresh();
        }
        ```
        
- watchオプション
    - refreshプロパティとは別の関数を再実行する仕組み
    - Ex.
        
        ```tsx
        const selectedCityId = ref(1853909);
        
        const asyncData = await useAsyncData(
        	(): Promise<any> => {
        		...
        		return response;
        	},
        	{
        		transform: (data: any): WeatherInfoData => {
        			...
        		},
        		watch: [selectedCityId]
        	}
        );
        ```
        
        - watchオプションに、配列として監視してほしいリアクティブ変数を渡すと、その値が変更されたときにリフレッシュが行われるようになっている

## コンポーザブル

よく使うコードを再利用する場合、別ファイルに記述してその関数をインポートして利用するという方法が一般的だが、Nuxtでは、これを自動化し、インポートを不要にする機能としてコンポーザブル(Composables)というものがある

### コンポーザブルの作り方

1. コンポーザブルを定義するファイルは、composablesフォルダ内に格納する
2. 1のフォルダ内にuse〇〇.tsというキャメル記法の名称のファイルを作成する
3. 2と同名のメソッドを定義しエクスポートする
4. 3のメソッド内に再利用したいコードを記述し、その結果をリターンする
- 構文
    
    ```tsx
    export const use〇〇 = (引数: 引数の型, ...) => {
    	return 戻り値
    }
    ```
    
- Ex. composables/useWeatherInfoFetcher.ts
    
    ```tsx
    export const useWeatherInfoFetcher = (city: City) => {
    	const config = useRuntimeConfig();
    	const asyncData = useLazyAsyncData(
    		...
    	);
    	return asyncData;
    };
    ```
    

### コンポーザブルの利用

- コンポーザブルはオートインポートであるため、単に関数を呼び出すだけ
    
    ```tsx
    ...
    const asyncData = useWeatherInfoFetcher(selectedCity.value);
    ...
    ```
    

## ランタイム設定の定義(Runtime Config)

プロジェクト全体で使われる定数値を設定情報としてまとめる機能がNuxtのランタイム設定

### ランタイム設定を記述 runtimeConfigプロパティ

- nuxt.config.tsに記述する
    - プロジェクトを作成すると自動で生成されている
    - Ex. nuxt.config.ts 初期値
        
        ```tsx
        // https://nuxt.com/docs/api/configuration/nuxt-config
        export default defineNuxtConfig({
          devtools: { enabled: true }
        })
        ```
        
- runtimeConfigプロパティ内にランタイム設定を記述する
    - Ex.
        
        ```tsx
        // https://nuxt.com/docs/api/configuration/nuxt-config
        export default defineNuxtConfig({
          devtools: { enabled: true },
        	runtimeConfig: {
        		public: {
        			weatherInfoUrl: "https://api.openweathermap.org/data/2.5/weather",
        			weathermapAppid: "xxxxxx"
        		}
        	}
        })
        ```
        
        - publicプロパティで定義しないと、private扱いになり、サーバーサイドレンダリングのみで使用はできるが、クライアントサイドレンダリングでは利用できなくなる
    
    ### ランタイム設定の利用
    
    - useRuntimeConfig()関数の戻り値オブジェクトからアクセスする
    - Ex.
        
        ```tsx
        export const useWeatherInfoFetcher = (city: City) => {
        	const config = useRuntimeConfig();
        	const params:{
        		lang: string;
        		q: string;
        		appid: string;
        	} =
        	{
        		lang: "ja",
        		q: city.q,
        		appid: config.public.weathermapAppid
        	}
        	const asyncData = useLazyFetch(
        		config.public.weatherInfoUrl,
        		...
        	);
        	return asyncData;
        };
        ```
        

### 環境変数の利用

- .envファイルでの環境変数とランタイム設定を自動対応させ、対応するものに関しては、値を上書きする仕組みがある
    - .env.localやenv.productionも同じように作用する
- Ex.
    - .env
        
        ```tsx
        NUXT_PUBLIC_WEATHERMAP_APPID = "xxxxx"
        ```
        
    - nuxt.config.ts
        
        ```tsx
        export default defineNuxtConfig({
        	...
        	runtimeConfig: {
        		public: {
        			weathermapAppid: ""
        		}
        	}
        })
        ```
        
        - weathermapAppidは、環境変数`NUXT_PUBLIC_WEATHERMAP_APPID`の値`xxxx`に上書きされる
- 対応関係
    - ランタイム設定の設定名を全て大文字のスネーク記法に変換し、先頭に`NUXT_`を付与する。publicのランタイム設定の場合は、`NUXT_PUBLIC_`とする