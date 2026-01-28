## クッキーを利用する際の関数 useCookie()

- 構文
    
    ```tsx
    const 変数　= useCookie<データ型>("クッキー名", オプションオブジェクト)
    ```
    
- Ex.
    
    ```tsx
    //ログインユーザ情報をクッキーに格納。
    const loginUserCookie = useCookie<User|null>("loginUser");
    loginUserCookie.value = asyncData.data.value.user;
    ```
    
- useCookieを使用したクッキーオブジェクトはリアクティブな変数であるため、.valueプロパティに値を代入する
- 本来クッキーに格納できるのは文字列だけだが、useCookieが用意したクッキーオブジェクトに代入する際、自動的にJSON.stringifyによるエンコードが行われるため、エンコードの処理は不要になっている