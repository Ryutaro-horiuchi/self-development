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
    

### データ取得処理をまとめておけるuseAsyncData()

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
    - 
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
    ```
    
- 戻り値
    
    下記のデータが含まれたオブジェクトになる
    
    | プロパティ名 | 内容 |
    | --- | --- |
    | data | ハンドラの本来の戻り値 |
    | pending | データ取得が終了したかどうかを表すbool値 |
    | refresh | データを再取得する関数 |
    | error | データ取得失敗した時のエラーオブジェクト |