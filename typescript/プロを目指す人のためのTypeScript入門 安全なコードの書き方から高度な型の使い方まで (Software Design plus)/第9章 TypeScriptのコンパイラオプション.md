## tsconfig.jsonによるコンパイラオプションの設定

- TypeScriptの環境構築は1にpackage.json、2にtsconfig.json
- TypeScriptコンパイラは自動的にtsconfig.jsonを読み込んで、コンパイル時にその設定を使用してくれる
    - 違う名前のファイルをコンパイル時に参照させたい場合は、以下コマンド
        
        `tsc -p hoge.json`
        

### tsconfig.jsonの自動生成

- tsconfig.jsonを自動生成するコマンド
    - `npx tsc —init`
        - npxはnpmの付属コマンド。node_modulesの中にインストールされているパッケージを実行する

### ファイルのパス周りの設定

どのファイルをコンパイルするかという情報

- include
    
    ```json
    {
    	"include": ["./src/**/*.ts"]
    }
    ```
    
    - globパターンが使える
        - `**/`
            - 0個以上のディレクトリ階層を表す
        - `*.ts`
            - 拡張子.tsの任意のファイル
- exclude
    
    ```json
    {
    	"include": ["./src/**/*.ts"],
    	"exclude": ["./src/__tests__/**/*.ts"]
    }
    ```
    
    - include同様globパターンが使える。
    - includeで指定されたファイル群の中から一部のファイルを除外したい時に使用する
- files
    
    ```json
    {
    	"files": ["src/index.ts"]
    }
    	
    ```
    
    - 古くからある指定方法。globパターンが使えない

## チェックの厳しさに関わるオプション

### strictオプション

- strict系と呼ばれる複数のコンパイラオプションをまとめて有効にするもの。
    - 本書の解説内容はこれが有効に設定された状態の挙動
- tsc —initコマンドで新規でtsconfig.jsonが作成されたときは、デフォルトで有効になっている
- 後方互換性のためにオプションとして用意しており、新規プロジェクトでは有効で問題ない

### strictNullChecksオプション

- strict系の一つ
- オフにすると、型からundefinedが消える

### noImpilcitAnyオプション

- strict系の一つ
- TypeScriptでは、原則して関数の引数の型注釈は必須
    - このオプションをオフにすると、関数の引数の型を書かなくてもコンパイルエラーにならない
- 型が書かれていない引数は、noImpilcitAny無効下ではany型になる
- JavaScriptのプログラムをTypeScriptに移行する場合のみ無効にしておく

### noUncheckedIndexedAccessオプション

- デフォルトではfalseになっている
- インデックスシグネチャを常にオプショナルなプロパティのように扱われる(undefinedとのユニオン型になる)
    - [任意のプロパティ名を許容する型(インデックスシグネチャ)](https://www.notion.so/29f93db055548012be89e95af5113828?pvs=21)
- Ex.
    
    ```tsx
    type PriceData = {
      [key: string]: number;
    }
    const data: PriceData = {
      apple: 220,
      coffee: 120,
      bento: 500
    };
    
    const applePrice = data.apple; // 型推論でnumber
    const bananaPrice = data.banana; // こちらも型推論でnumberとなってしまう
    ```
    
    - オプションがオフだとオプショナルとして扱わないため、インデックスシグネチャはnumber型として扱われる。この時、存在しないプロパティも戻り値はnumber型となってしまう。
    - オンにすることで、`number | undefined`となり型安全性を担保する

### 新規プロジェクトでのおすすめ設定

- strictオプションは有効にする
- noUncheckedIndexedAccessも有効にする
- exactOptionalPropertyTypesも有効にする
    - [オプショナルプロパティの表現](https://www.notion.so/2ab93db0555480a39c38d5690b48de0e?pvs=21)