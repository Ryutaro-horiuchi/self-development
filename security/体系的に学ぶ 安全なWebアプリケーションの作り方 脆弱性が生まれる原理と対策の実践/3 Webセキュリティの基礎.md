## HTTPとセッション管理

### リクエストメッセージ

- ブラウザからWebサーバーに送られた要求
- 1行目はリクエストライン
    - Webサーバーに対する命令に相当する
    - メソッド、URL、プロトコルバージョンを空白で区切って表現する
        
        ```
        GET http://example.jp/31/31-001.php HTTP/1.1
        ```
        
- 2行目以降はヘッダ。名前と値をコロンで区切っている
    - 必須ヘッダはhostのみ。送信先のホスト名とポート番号(80の場合は省略可能)
- サンプル
    
    ```
    GET http://example.jp/31/31-001.php HTTP/1.1
    host: example.jp
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: ja,en-US;q=0.9,en;q=0.8
    Connection: keep-alive
    Referer: http://example.jp/31/
    Cookie: xx; roundcube_sessauth=xx
    ```
    

### レスポンスメッセージ

- 以下の構成
    - 1行目はステータスライン
        - プロトコルバージョン、ステータスコード、テキストフレーズ を空白区切り
        
        ```
        HTTP/1.1 200 OK
        ```
        
    - レスポンスヘッダ
        - 代表的なヘッダ
            - Content-Length
                - ボディのバイト数
            - Content-Type
                - MIMEタイプというリソースの種類を指定する
    - 空行
    - ボディ
- サンプル
    
    ```
    HTTP/1.1 200 OK
    Server: nginx/1.10.3
    Date: Tue, 24 Mar 2026 11:46:42 GMT
    Content-Type: text/html; charset=UTF-8
    Content-Length: 20
    Connection: keep-alive
    X-UA-Compatible: IE=edge
    
    <body>
    20:46</body>
    
    ```
    

### POSTメソッド

### メッセージボディ

- POSTメソッドによるリクエストメッセージにはボディが含まれる。レスポンスと同様、ヘッダと空行で区切る
- Content-Length, Content-TypeがPOSTにより送信される際に追加される
    - Content-Typeは送信する値のMIMEタイプで、HTMLのform要素で設定することができる。
    - 指定がない場合は「`application/x-www-form-urlencoded`」。これは名前=値の組を& で繋いだデータ形式。名前と値はパーセントエンコーディングされる

#### パーセントエンコーディング

- URL上で特別な意味を持つ記号や日本語などをURL上に記述する場合に用いる。
- 対象の文字を「%xx」という形式で表す。xxはバイトの16進数表記
    - Ex.
        
        
        | **ステップ** | **状態** | **具体的な中身** |
        | --- | --- | --- |
        | **元データ** | 文字 | あ |
        | **コンピュータの内部** | 2進数（3バイト分） | `11100011` `10000001` `10000010` |
        | **人間向けの表記** | 16進数（2文字×3個） | `E3` `81` `82` |
        | **URL用の表記** | **パーセント付与** | **`%E3%81%82`** |