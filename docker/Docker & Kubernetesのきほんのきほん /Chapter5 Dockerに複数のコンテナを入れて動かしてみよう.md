# WordPress 環境構築

- WordPress
    
    Webサイトを作成できるソフトウェア
    
    Apache、DB、PHPの実行環境が必要
    
- WordPressのコンテナと、MySQLのコンテナを作成する
    - WordPressコンテナ: WordPress + Apache + PHPの実行環境
    - MySQLコンテナ: MySQL

## Docker ネットワークを作成・削除する

---

- コンテナ同士を繋ぐために、仮想的なネットワークを作成する

### `docker network create`

- 仮想ネットワークを作成する
    
    ```tsx
    docker network create ネットワーク名
    ```
    

### `docker network rm`

- 仮想ネットワークを削除する
    
    ```tsx
    docker network rm ネットワーク名
    ```
    

- 他`docker network`系のよく使われる副コマンド
    - connect
    - disconnect
    - inspect: ネットワークの詳細情報を表示する
    - ls
    - prume: 現在コンテナがつながっていないネットワークをすべて削除する

## MySQLコンテナ起動時のオプションと引数

- よく使う記述例
    
    ```bash
    % docker run
     --name コンテナ名
     -dit
     --net=ネットワーク名 
     -e MYSQL_ROOT_PASSWORD=MYSOLのrootパスワード
     -e MYSQL_DATABASE＝データベース領域名
     -e MYSQL_USER＝MYSQLのユーザー名
     -e MYSQL_PASSWORD=MYSQLのパスワード
     mysql
     --character-set-server=文字コード
     --co1lation-server= 照合順序
     --mysql_native_password=ON  
    ```
    
- オプション
    - - -net: ネットワークを紐付ける
    - -e: 環境変数を設定する
        - OSにおいて、様々な設定値を保存できる場所のこと
        - よく設定する環境変数
            - https://hub.docker.com/_/mysql  - **Environment Variables**
            - MYSQL_ROOT_PASSWORD
                - rootパスワード
                    - rootは全権のあるユーザー
                
                → セキュリティの観点で、権限を制御された一般ユーザーを作成するのが一般的
                
            - MYSQL_DATABASE
                - データベース名
            - MYSQL_USER
                - ユーザー名
            - MYSQL_PASSWORD
                - パスワード名
- 引数
    - --character-set-server=utf8mb4
        - 文字コードをUTF8にする
    - --collation-server=utf8mb4_unicode_ci
        - 照合順序をUTFにする
    - --mysql_native_password=ON
        - 以前の認証方式を使用する
            
            → MySQL5.7から、MySQL8になった際に外部からの認証方式が変更になった
            
- 各コンテナで設定できる環境変数は、あらかじめ定義されているっぽい
    
    https://hub.docker.com/_/mysql
    

      

## WordPressコンテナ起動時のオプションと引数

---

- よく使う記述例
    
    ```bash
    % docker run
    	--name コンテナ名
    	-dit 
    	--net=ネットワーク名
    	-p ポートの設定
    	-e WORDPRESS_DB_HOST=データベースのコンテナ名
    	-e WORDPRESS_DB_NAME=データベース領域名
    	-e MORDPRESS_DB_USER=データベースのユーザー名
    	-e WORDPRESS_DB_PASSWORD=データベースのパスワード
    	wordpress
    ```
    
- オプション
    - -dit
    - - -net
    - -e
        - 環境変数
            - WORDPRESS_DB_HOST
                - データベースのコンテナ名
            - WORDPRESS_DB_NAME
                - データベース領域名
            - WORDPRESS_DB_USER
                - データベースユーザー名
            - WORDPRESS_DB_PASSWORD
                - データベースのパスワード

## ハンズオン WordPressコンテナとMySQLコンテナを作成し、動かしてみよう

- ハンズオン
    1. network createコマンドでネットワークを作成する
        
        ```bash
        % docker network create wordpress000net1
        0afa1fd30654d7ed05d2bf15c233b477946e0df119062aa749e3fcbaf5e39935
        ```
        
    2. runコマンドを実行してMySQLコンテナを作成・起動する
        
        ```bash
        % docker run
        	--name mysql000ex11
        	-dit 
        	--net=wordpress000net1
        	-e MYSQL_ROOT_PASSWORD=myrootpass
        	-e MYSQL_DATABASE=wordpress000db
        	-e MYSQL_USER=wordpress000kun
        	-e MYSQL_PASSWORD=wkunpass
        	mysql
        	--character-set-server=utf8mb4
        	--collation-server=utf8mb4_unicode_ci
        	--mysql_native_password=ON
        ```
        
    3. runコマンドを実行してWordPressコンテナを作成・起動する
        
        ```bash
        % docker run
        	--name mysql000ex12
        	-dit 
        	--net=wordpress000net1
        	-p 8085:80
        	-e WORDPRESS_DB_HOST=mysql000ex11
        	-e WORDPRESS_DB_NAME=wordpress000db
        	-e MORDPRESS_DB_USER=wordpress000kun
        	-e WORDPRESS_DB_PASSWORD=wkunpass
        	wordpress
        ```
        
    4. psコマンドでコンテナの稼働を確認する
    5. ブラウザでWordpressを確認する
    6. 後始末をする
        - コンテナ、イメージの削除
            
            ```bash
            % docker stop wordpress000ex12 mysql000ex11
            % docker rm wordpress000ex12 mysql000ex11
            % docker image rm mysql wordpress
            ```
            
        - ネットワークの削除
            
            ```bash
            % docker network ls
            NETWORK ID     NAME               DRIVER    SCOPE
            908028eebee4   bridge             bridge    local
            149d6728929d   host               host      local
            9eface030ba2   none               null      local
            0afa1fd30654   wordpress000net1   bridge    local
            
            docker network rm wordpress000net1
            wordpress000net1
            ```