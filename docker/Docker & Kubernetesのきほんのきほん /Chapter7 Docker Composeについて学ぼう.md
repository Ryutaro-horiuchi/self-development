# Docker Composeとは

構築に関わるコマンド分の内容を一つのテキストファイルに書き込み、一気にコンテナを作成・実行・廃棄することができる

## Docker Compose 仕組み

---

- 構築に関する設定を記述した定義ファイルをYAML形式で用意し、upやdownコマンドを使用して操作する

### コマンド

- upコマンド
    
    docker runコマンドに似ている。定義ファイルに従って、イメージをDLしたり、コンテナ・ネットワーク・ボリュームを作成・起動したりする
    
- downコマンド
    
    コンテナとネットワークを停止・削除する。(ボリュームとイメージはそのまま残る)
    
- stopコマンド
    - コンテナとネットワークを停止する

### Docker ComposeとDockerfileの違い

- Docker Compose
    
    docker run コマンドの集合体で、コンテナと周辺環境(ネットワークやボリューム)を作成する
    
- Dockerfile
    
    イメージを作る。周辺環境は作成できない。
    

### Docker ComposeとKubernetesの違い

- Docker Compose
    
    コンテナを作っては消す作業のみで、管理はできない
    
- Kubernetes
    
    Dockerコンテナを管理する
    

# Docker Composeのインストールと使い方

- Docker Engineとは別のソフトウェアであるため、別途インストールが必要
    
    <aside>
    💡 MacやWindowsのデスクトップアプリであれば、既に入っているためインストール作業がいらない
     Linuxの場合は、Docker ComposeとPython3の実行環境と必要なツール(python3, python3-pip)をインストールする。(Docker Composeはpythonで書かれたプログラムであるため、pip3コマンドでインストールする)
    
    </aside>
    

## Docker Composeの使い方

- Dockerfileと同様に、ホスト側にフォルダを作りそこに定義ファイルを置く
    - フォルダには、コンテナ作成に必要な画像ファイルや、HTMLファイルなども置いておく
- 定義ファイル名は、必ず「`docker-compose.yml`」
    - 実行するコマンドは、これまでと同様にDocker Engineに対して行われ、コンテナが作成されるのはDocker Engine上。
        
        人が手打ちで送るコマンド文を、Docker Composeが代理で打ち込んでいるイメージ
        
    - 定義ファイルは一つのフォルダに一つしか置かない
- Docker Composeでは、コンテナの集合のことを「サービス」と呼んでいる
    - 公式では、サービスとコンテナが混在しているが、全てコンテナとと読み替えてしまってほぼ問題ないとのこと

# Docker Composeファイルの書き方

## docker runコマンドとDocker Composeファイルは似ている

---

- [runコマンドを実行する](https://www.notion.so/run-07983fa7c9c84d308e09e3e03e5a10c0?pvs=21)
    
    ```bash
    % docker run --name apa000ex2 -d -p 8080:80 httpd
    ```
    
- 上記のDocker Composeファイル
    
    ```yaml
    version: "3"
    
    services:
    	apa000ex2
    		image: httpd
    		ports:
    			- 8080:80
    		restart: always
    ```
    

## 定義ファイルの書式

---

- 定義ファイルの記述例 大項目のみ
    
    ```yaml
    version: 3
    services:
      コンテナ名1:
      コンテナ名2:
    networks:
      ネットワーク名1:
    volumes:
      ボリューム名1:
      ボリューム名2:
    
    ```
    
    - 最初にバージョンを書く
    - servicesはコンテナのこと
        - Kubernetesでも同様に、コンテナの集合体のことをServiceと呼ぶ
    - 字下げはタブを使用するのは禁止。半角スペースを使用する

- 定義ファイルの記述例 設定を書く
    
    ```yaml
    version: 3
    service:
      コンテナ名1:
    	  image: イメージ名
    	  networks:
    	    - ネットワーク名1
    	  ports:
    	    - ポートの設定
    ```
    
    - 記述が一つの場合は、コロンの後に続けて書けば良い
    - 記述が複数になる場合は、ハイフンで改行して記入する

### 定義ファイル（YAML形式）の記述ルールまとめ

- まとめ
    - 最初にDocker Composeのバージョンを書く
    - 大項目「services」「networks」「volumes」に続いて設定内容を書く
    - 親子関係はスペースで字下げして表す
    - 字下げのスペースは、同じ数の倍数とする
    - 名前は、大項目の下に字下げして書く
    - コンテナの設定内容は、名前の下に字下げして書く
    - 「一」が入っていたら複数指定できる
    - 名前の後ろには「：」をつける
    - 「：」の後ろには空白が必要（例外的にすぐ改行するときは不要）
    - コメントを入れたい場合は＃を使う（コメントアウト）
    - 文字列を入れる場合は、「’（シングルクォート）」「"（ダブルクォート）」のどちらかでくくる

### 定義ファイルの項目

- 大項目
    
    
    | 項目 | 内容 |
    | --- | --- |
    | services | コンテナに関する定義をする |
    | networks | ネットワークに関する定義をする |
    | volumes | ボリュームに関する定義をする |
- よく使われる定義内容
    
    
    | 項目 | docker runでの対応 | 内容 |
    | --- | --- | --- |
    | image | イメージ引数 | 利用するイメージを指定する |
    | networks | —net | 接続するネットワークを指定する |
    | volumes | -v, —mount | 記憶領域のマウントを設定する |
    | ports | -p | ポートのマッピングを設定する |
    | environment | -e | 環境変数を設定する |
    | depends_on | なし | 別のサービスに依存することを示す(依存先のコンテナが作られてからコンテナを作成する) |
    | restart | なし | コンテナが停止したときの再試行ポリシーを設定する |
- その他の定義項目
    
    
    | 項目 | docker runでの対応 | 内容 |
    | --- | --- | --- |
    | command | コマンド引数 | 起動時の規定コマンドを上書きする |
    | cotainer_name | —name | 起動するコンテナ名を明示的に指定する |
    | dns | —dns | カスタムなDNSサーバーを明示的に設定する |
    | env_file | なし | 環境設定情報を書いたファイルを読み込む |
    | entrypoint | —entrypoint | 起動時のENTRYPOINTを上書きする |
    | external_links | —link | 外部リンクを設定する |
    | extra_hosts | —add-host | 外部ホストのIPアドレスを明示的に指定する |
    | logging | —log-driver | ログ出力先を設定する |
    | network_mode | —network | ネットワークモードを設定する |

### ハンズオン 定義ファイルを作成する

- 下記と同様のものをdocker-composeで作成する
    
    [ハンズオン WordPressコンテナとMySQLコンテナを作成し、動かしてみよう](https://www.notion.so/WordPress-MySQL-145f081c660e42b38da8052f95f93da9?pvs=21) 
    
- ハンズオン
    1. docker-compose.ymlを作成する
        
        適切な場所に作った「com_folder」内に「docker-compose.yml」ファイルを作成する
        
    2. 大項目を並べる
        
        ```yaml
        version: "3"
        services:
        networks:
        volumes:
          
        ```
        
    3. 名前を書く
        
        ```yaml
        version: "3"
        services:
          mysql000ex11:
          wordpress000ex12:
        networks:
          wordpress000net1:
        volumes:
          mysql000vol11:
        ```
        
    4. MySQLコンテナの定義を行う
        
        ```yaml
        version: "3"
        services:
          mysql000ex11:
            image: mysql
            networks:
              - wordpress000net1
            volumes:
              - mysql000vol11:/var/lib/mysql
            restart: always
            command: mysqld --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --mysql_native_password=ON
            environment:
              MYSQL_ROOT_PASSWORD: myrootpass
              MYSQL_DATABASE: wordpress000db
              MYSQL_USER: wordpress000kun
              MYSQL_PASSWORD: wkunpass
          wordpress000ex12:
        networks:
          wordpress000net1:
        volumes:
          mysql000vol11:
          wordpress000vol12:
          
        ```
        
    5. WordPressコンテナの定義を行う
        
        ```yaml
        version: "3"
        services:
          mysql000ex11:
            ...
          wordpress000ex12:
            depends_on:
              - mysql000ex11
            image: wordpress
            networks:
              - wordpress000net1
            volumes:
              - wordpress000vol12:/var/www/html
            ports:
              - 8085:80
            restart: always
            environment:
              WORDPRESS_DB_HOST: mysql000ex11
              WORDPRESS_DB_NAME: wordpress000db
              WORDPRESS_DB_USER: wordpress000kun
              WORDRESS_DB_PASSWORD: wkunpass
        networks:
          wordpress000net1:
        volumes:
          mysql000vol11:
          wordpress000vol12:
        ```
        
    6. 保存する

# Docker Composeを実行してみる

## Docker Composeの操作コマンド

---

- Docker Composeはdocker-composeコマンドを使用する
- up, down, stopのコマンドをとりあえず覚えておけば良い。

### コンテナや周辺環境を作成するコマンド docker-compose up

- よく使う記述例
    
    ```bash
    docker-compose -f 定義ファイルのパス up オプション
    ```
    
- 記述例
    
    ```bash
    docker-compose -f /Users/ユーザー名/Documents/com_folder/docker-compose.yml up -d
    ```
    
    - -d バックグラウンドで実行する

### コンテナや周辺環境を削除するコマンド docker-compose down

- よく使う記述例
    
    ```bash
    docker-compose -f 定義ファイルのパス down オプション
    ```
    

### コンテナを停止するコマンド docker-compose stop

- よく使う記述例
    
    ```bash
    docker-compose -f 定義ファイルのパス stop オプション
    ```
    

### Docker Composeでのコンテナ名と複数起動(scaleオプション)

- Docker Composeでコンテナを作成すると、コンテナ名が勝手に変わる
    - com_folderフォルダにpenguinという名のコンテナを作成すると、「com_folder_penguin_1」というコンテナ名になる
    - 名前は変わるが、Docker Composeでコンテナを指定するときは、元のコンテナ名(定義ファイルに記入した名前)で良い
    - 変更された名前は、Docker Engineから使用するときと、同じ構成のコンテナを複数起動したいとき(scaleオプション)に使用する

## ハンズオン Docker Composeを実行してみよう

---

- ハンズオン
    1. 定義ファイルを適切な場所に置く
        
        [ハンズオン 定義ファイルを作成する](https://www.notion.so/d4a4d93c5ba14171876a3c0a98ab6288?pvs=21) にて作成した「com_folder」と「docker-compose.yml」を使用する
        
    2. 定義ファイルの内容を実行する
        
        ```bash
        % docker-compose -f /Users/ユーザー名/Documents/com_folder/docker-compose.yml up -d
        ```
        
        ```bash
        % docker-compose -f /Users/ryutafolder/Documents/com_folder/docker-compose.yml up -d
        WARN[0000] /Users/ryutafolder/Documents/com_folder/docker-compose.yml: `version` is obsolete 
        [+] Running 3/33
         ⠴ wordpress000ex12 [⣿⣿⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀] Pulling                                                                                                                                                                                  5.6s 
           ✔ b0a0cf830b12 Already exists                                                                                                                                                                                                     0.0s 
           ✔ c93478d47932 Pull complete                                                                                                                                                                                                      0.9s 
           ⠙ e74cc574d0d2 Downloading  [>                                                  ]  539.9kB/104.4MB                                                                                                                                1.1s 
           ✔ e4782e138a90 Download complete                                                                                                                                                                                                  0.9s 
           ⠙ cfeec87621ae Waiting                                                                                                                                                                                                            1.1s 
           ⠙ c1badcd002c0 Waiting                                                                                                                                                                                                            1.1s 
        [+] Running 3/336 Waiting                                                                                                                                                                                                            1.1s                                                                                                                                                                                                         1.2s  
        ....
        
        ```
        
    3. ブラウザでWordPressにアクセスできることを確認する
        
        http://localhost:8085/ にアクセスする
        
    4. コンテナとネットワークを停止・削除する
        
        ```bash
        docker-compose -f /Users/ユーザー名/Documents/com_folder/docker-compose.yml down 
        ```
        
    5. 後始末をする
        
        イメージとボリュームはdownコマンドで削除されないため、手動で削除する