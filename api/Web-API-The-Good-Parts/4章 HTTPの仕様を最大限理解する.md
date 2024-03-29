HTTPをはじめインターネットで利用される仕様の多くはRFCと呼ばれる仕様書で定義されている

<br>
<br>

# ステータスコードを正しく使う

<br>

## 200番台: 成功

- 201 Created
    - リソースが作成された
- 202 Accepted
    - リクエストした処理が非同期で行われ、処理は受け付けたが完了はしていない時に使用される
- 204 No Content
    - レスポンスが空の時に返す。
    - DELETEメソッドでデータの削除を行い、何もリソースを返す必要がない時に使用される
        - DELETEの時にもリソースを返すべきだという主張もある
        - 筆者の考えではPUT,PATCHは200, DELETEは204
            - データがいらないため、削除していることが多く、その後データを受け取る必要性は低いから

<br>

## 300番台: 追加で処理が必要

- 301, 302, 303, 307の4つはリダイレクトに関する
    - 301, 302はリダイレクト前のHTTPメソッドを使用してリダイレクトするものであったが、ブラウザの多くが仕様に反してGETメソッドでリダイレクトしている
    - Locationというヘッダーでリダイレクト先のURIが返される
    - 301
        - コンテンツがこれから先ずっと移動したままである
    - 302
        - コンテンツが一時的に移動していることを伝える
    - 303
        - リダイレクト前のメソッドに依存せず、GETメソッドでリダイレクトする
    - 307, 308
        - 302, 301を厳密に定めたもの
        - HTTPメソッドの変更を許可していない
- 300 Multiple Choices
    - 指定したURIが取得するデータを一意に特定するには曖昧で、複数の可能性がある場合
- 304 Not Modified
    - 前回のデータ取得から更新していないことを知らせるもの
    - キャッシュの情報を返した時のみ

<br>

## 400番台: クライアントのリクエストに問題があった場合

- 400
    - 他の400番台のステータスコードでは表すことができないエラーに使用する
- 401 Unauthorized
    - 認証のエラー
- 403 Forbidden
    - 認可のエラー
- 404 NotFound
    - ただステータスコードを返すのではなく、正しい情報を送るのが吉のコンテキストでは、詳細な情報を返すべき
- 405 Method Not Allowed
    
    メソッドが許可されていない
    
- 406 Not Acceptable
    
    クライアントが指定してきたデータ形式にAPIが対応していない
    
- 408 Request Timeout
    
    リクエストタイムアウト
    

<br>

## 500番台: サーバーに問題があった場合

- 503
    
    メンテナンスなどで一時的に利用できない状態
    
<br>
<br>


# キャッシュとHTTPの仕様

<br>

## プロキシサーバーによるキャッシュ

- キャッシュについて考えるときは、クライアントとオリジンサーバーの中継役を担うプロキシサーバーについて考える必要がある
- オリジンサーバーが更新されたのにも関わらず、適切なリクエストを送らないと古いデータをプロキシサーバーが返してしまうことがある
- リバースプロキシ
    - サービス提供側がAPIへのアクセスを高速化するために配置する

<br>

## HTTPのキャッシュの仕組み

- HTTPでは、キャッシュが利用可能な状態を”fresh”(新鮮), そうでない状態を”stale”(新鮮ではない)と呼ぶ

<br>

### Expiration Model(期限切れモデル)

- あらかじめレスポンスデータに保存期限を決めておき、期限が切れたら再度アクセスをして取得を行う
- 二つのレスポンスヘッダを使用する方法がある
    - Expiresと Cache-Controlを同時に使用した場合はExpiresが優先される
    - Expires: 期限切れを絶対時間(RFC1123定義)で表す
        
        ```json
        Expires: Fri, 01 Jan 2016 00:00:00 GMT
        ```
        
    - Cache-Control max-age: 現在時間からの秒数で表す
        
        ```json
        Cache-Control: max-age=3600
        ```
        
        - Dateヘッダ(レスポンスが生成されたサーバー側の日時を示すヘッダ)
        - この日時からの経過時間がmax-ageの値を超えた場合には期限が切れたことを考えられる

### ValidationModel(検証モデル)

- 今持っているキャッシュが有効かどうかをサーバーに問い合わせる
- 条件付きリクエストに対応する
    
    「過去に取得したある時点でのデータ」をサーバーに伝え、更新されていた時にのみデータを返す。更新されていない時は、304を返し更新されていないことを伝える
    
- 手順としては以下のステップを踏む
1. サーバー側で生成し、クライアント側にキャッシュと共に保持させる
    - 二通りの方法がある
    - Last-Modified (最終更新日付)
        - 一覧のような複数リソースの場合は、そのリソースの中で最後に更新されたリソースの最終更新日付
        - ユーザーIDのユーザー情報のような特定のリソースの場合は、リソース自体の最終更新日付
        
        ```json
        Last-Modified: Tue, 01 Jul 2014 00:00:00 GMT
        ```
        
    - ETag(エンティティタグ)
        - ある特定のリソースのバージョンを表す識別子。フィンガープリントである文字列
        - 最終更新日付やデータ全体をMD5や、SHA1などの関数を使用してハッシュ化して生成する
        
        ```json
        ETag: "ff39b31e285573....."
        ```
        
2. クライアントから条件付きリクエストを行う
    - 最終更新日付を使用する場合は、If-Modified-Sinceヘッダ
        
        ```json
        GET /v1/users/12345
        If-Modified-Since:  Tue, 01 Jul 2014 00:00:00 GMT
        ```
        
    - エンティティタグを使用する場合は、If-None-Matchヘッダ
        
        ```json
        GET /v1/users/12345
        If-None-Match: "ff39b31e285573....."
        ```
        
3. サーバ側で送られてきた情報と現在の情報をチェックし、変更がなければ304を、変更されていた場合は200というステータスコードとともに変更された内容を送る

<br>

## キャッシュを使用したくない場合

- Cache-Control: no-cache ヘッダーを使用する
    - キャッシュを使用して欲しくないことを明示的に伝えることができる
        
        → 厳密には「キャッシュをしないという訳ではなく、検証モデルを用いて必ず検証を行う」を意味する
        
- 機密情報などを含むデータで、中継するプロキシサーバーにはキャッシュして欲しくないことを要請するにはno-storeを使用する

<br>

## Varyでキャッシュの単位を指定する

- URI以外にどのリクエストヘッダの項目をデータを一意に特定するかを指定する
    - HTTPには、Accept-xxxx ヘッダの値によってレスポンスの中身を変更する仕組みがあるため(サーバー駆動型コンテントネゴシエーション)
        - Ex. Accept-Language 返すレスポンスの値の表示言語を指定する
    - Varyヘッダーを使用して、キャッシュするヘッダーを使用することで、返すレスポンスを最適にキャッシュすることができる
        
        ```json
        Vary: Accept-Language
        ```
        
<br>

## Cache-Controlヘッダ


- キャッシュをコントロールするためのヘッダ
- 列挙することが可能 `Cache-Control: public, max-age=3600`

### publicとprivate

- プロキシサーバーにおいてデータを共有できるか
- 全員に配信されるお知らせの情報などであれば、同じリソースにアクセスする人は同じ情報を取得するためpublicに指定する
- users/meなどで、自分のユーザー情報を取得できるようになっている場合は、ユーザーに応じて内容が変わるため、privateを使用する

### statle-while-revalidate

- max-ageを超えた後もキャッシュの内容を返す。その裏側で非同期にキャッシュの検証を行う
    - Ex.
        
        ```json
        Cache-Control: max-age=600, stale-while-revaliate=600
        ```
        
        - 新鮮なのは10分間だけだが、その後の10分間もキャッシュサーバーはクライアントのリクエストに対して、保持したキャッシュをそのまま返すことができる
        - その間、非同期でオリジンサーバーへキャッシュの検証を行う問い合わせを行う
            
            → 最大20分間はキャッシュされたデータを受け取ることになるが、突然キャッシュが切れるのではなく、キャッシュ切れが起こった際に非同期でキャッシュの更新を可能にし、クライアントへ効率よく返すことができる
            
    
<br>
<br>

# メディアタイプ

- 送信するデータ本体の形式を表すためにメディアタイプ(データの形式)を指定する
    - レスポンス時にはレスポンスボディに含まれるメディアタイプはなにかを指定する
    - リクエスト時には、クライアントがどのようなメディアタイプを理解することができるのかを指定する

<br>

## レスポンス時のメディアタイプ

- Content-Typeヘッダを使用する
    
    ```json
    Content-Type: application/json
    ```
    
    - application/jsonのようなメディアタイプはMIMEタイプとも呼ばれる
        - 元々Content-Typeヘッダの仕様は、電子メールの仕様の由来している
    - メディアタイプの指定は以下のフォーマット
        
        ```json
        トップレベルタイプ名 / サブタイプ名 [ ; パラメーター]
        
        // Ex.
        // application/json
        // text/html
        ```
        
        - トップレベルタイプは大別して、テキストなのか画像なのかといったカテゴリを表す
        - サブタイプは、具体的なデータ形式を表す
        - パラメーターは省略可能で、テキストデータの場合のcharsetのように付加情報をつけたい時に使用する

### `x-`で始まるメディアタイプ

前提

- IANA
    - インターネットに関連する番号を管理する組織

本題

- `x-`で始まるメディアタイプはIANAに登録されていないことを意味する
- 現在はIANAに登録済みでも歴史的経緯で残っているものもある
    - `x-`から始まるメディアタイプを使用する際は他に代用のものがないか確認する
- 例外的に`applciation/x-www-form-urlencoded`(HTMLのフォームデータを送信する際に使用される)はIANAに正式に登録されているメディアタイプである

### 自分でメディアタイプを作成する

- `x-`から始まるものを定義するべきではないとRFC6838では述べられている
- サブタイプ名に接頭辞をつけて作成する
    - 筆者曰く、vndが最も適しているとのこと
    - フォーマットとしては、接頭辞の後に会社名、その後データ形式とするのを推奨
    
    ```json
    // フォーマット例
    application/vnd.companyname.awesomeformat
    ```
    
    - vnd (Vendor tree ベンダーツリー)
        - 特定の企業や団体が管理しているもの
    - prs (Personal tree パーソナルツリー)
        - 公に公開されることのない製品においてのみ使用される
    - x.(Unregistered tree 未登録ツリー)
        - ローカル環境、プライベート環境でのみ使用されることを想定しているが、prsでカバーされるため、推奨はされていない

### メディアタイプは正しく指定すること

- JSON形式なのに、text/htmlで返された場合、直接ブラウザからURIを叩いて取得すると画面にデータが表示されてしまう

<br>

## リクエスト時のメディアタイプ

以下のヘッダを主に使用する

- Content-Type
    - リクエスト時の同様、リクエストボディの中身がどんなデータ形式なのかを指定する
    - フォームのPOSTメソッドでは、ファイル添付など複数のデータを混在させる場合には、multipart/form-dataを指定する
- Accept
    - クライアントがどんなメディアタイプを受け入れ可能かをサーバーに伝えるために指定する
    - 複数のメディアタイプを列挙することができる
        
        ```json
        Accept: text/html, application/xhtml+xml;,application/xmlx;q=0.9,
        ```
        
        - q(QualityValue(品質))
            - そのメディアタイプを利用する優先度を指定する
            - 指定されていなければ、1とみなされ最優先になる
    

### 同一生成元ポリシーとクロスオリジンリソース共有(CORS)

- 同一生成元ポリシー(Same Origin Policy)
    - 生成元ポリシーは、同じ生成元(オリジン)からの読み込みのみ許可する
        - URI中のスキーム、ホスト、ポート番号の組み合わせが同じであれば許可
    - XHTTPRequestでは、異なるドメインに対してアクセスを行い、レスポンスデータを読み込むことができない
- クロスオリジンリソース共有(CORS)
    - 異なる生成元にアクセスする手法のこと
    - 基本的なやりとり
        - クライアントから、Originというリクエストヘッダを送る
            
            ```
            Origin: http://www.example.com
            ```
            
        - サーバー側では、あらかじめアクセスを許可する生成元の一覧を保持しておいて、Originヘッダーで送られてきた生成元が一覧に含まれているかをチェックする
            - 含まれていない場合は、403を返す
            - 含まれていた場合は、`Access-Control-Allow-Origin`レスポンスヘッダに、Originリクエストヘッダと同じ生成元を入れて返す
                
                ```
                Access-Control-Allow-Origin: http://www.example.com
                
                全部許可
                Access-Control-Allow-Origin: *
                ```
                
- プリフライトリクエスト
    - 生成元をまたいだリクエストを行う前に、そのリクエストが受け入れられるかを事前にチェックする
    - 通常はブラウザが自動的に発行するものであり、通常は開発者が作成する必要はない
- CORSとユーザー認証情報
    - CORSでは、ユーザー認証情報を送信する際には追加のHTTPレスポンスヘッダを発行する必要がある
    - CookieやAuthenticationヘッダを使用して、認証情報をクライアントが送ってきた場合、サーバーは以下のようにAccess-Control-Allow-Credentialsヘッダにtrueをセットして、返す必要がある
        
        ```
        Access-Control-Allow-Credentials: true
        ```
        
        → これがないとブラウザは受け取ったレスポンスを拒否する
        
<br>
<br>

# 独自のHTTPヘッダ

- `x-`という接頭辞をつける
- 続きにサービスやアプリケーション名、その後つけたいヘッダ名とするのが一般的
- パスカルケースとケバブケースが一般的
- Ex. Github
    
    ```
    X-Github-Request-ID: 729448F8: ...
    ```