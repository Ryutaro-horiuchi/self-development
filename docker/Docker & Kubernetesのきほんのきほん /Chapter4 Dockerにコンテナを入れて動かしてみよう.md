## Dockerの起動と終了

- Docker Engineは自動起動の設定があるが、コンテナには自動起動の設定がない
    
    → サーバーを新たに起動させた時に、コンテナも自動起動させるには、スクリプトを用意しておく必要がある
    
- 自動起動設定 (Desktop アプリ)
    
    Docker Preferences → General → Start Docker Desktop when you log in のチェックボックス
    

## コマンドの操作 基本

---

```docker
% docker コマンド (オプション) 対象 (引数)
					  |
						 --- 上位コマンド + 副コマンド
```

### コマンドと対象

- コマンドは上位コマンド と副コマンドで構成されている
    - 上位コマンド: 何を
        - 対象の種類が入る 全部で12種類
        - Ex. container, image
    - 副コマンド: どうする
- 省略形でかけるコマンドもある
    - Ex. docker run (docker container run)
        - 慣例的に省略形で書くことが多いが、docker1.13より、コマンドが再編成され、省略しない書き方に統一された。

### オプションと引数

- オプション
    - コマンドに対して細かい設定を行う
    - 「-」と1文字の組み合わせのオプションは、まとめて書くことができる
        - Ex. `-d`, `-i`, `-t` をまとめて実行する
            
            `-dit`
            
- 引数: 対象に対して持たせたい値をかく
    - イメージの種類によって異なる
    - Ex. 文字コードの指定、ポート番号の指定
- Ex. バックグラウンドで実行する、モード1で実行する
    
    docker container run -d penguin —mode=1
    

## コマンド: コンテナの作成・削除と、起動・停止

---

### `docker container run`

- コンテナの作成(`docker container create`)、起動(`docker container start`)を一度に行うコマンド。イメージがなければ、イメージのダウンロード(`docker image pull`)も行う
- よく使われるオプション
    - - -name イメージ名
    - -p ポート番号
    - -v ボリュームをマウントする
    - - -net コンテナをネットワークに接続する
    - -d バックグラウンドで実行する
    - -dit
        - -d: バックグラウンドで実行するためのオプション
        - -i, -t: コンテナの中身を操作するためのオプション
        - どういう時に使用するか
            - デーモンとして動くコンテナに対し使用することが多い
                - デーモン: UNIXやLinuxで動くプログラムのうち、常に待ち受けにして、裏で動き続けるプログラムのこと
                - 一回限りの実行であれば、特にditをつけなくても良いが、デーモンとして動くコンテナは、プログラムを終了することがないため、実権を握るために-ditをつける
- Ex.
    
    ```bash
    % docker run --name apa000ex1 -d httpd
    
    # バージョン指定
    % docker run --name apa000ex1 -d httpd:2.2
    ```
    
    - httpd: Apacheのイメージ名。バージョンを指定しないと最新版が使用される

### `docker stop コンテナ名`

コンテナの停止

- Ex.
    
    ```docker
    % docker stop apa000ex1
    ```
    
- idを指定して、停止することもできる。(rmコマンドも同様)

### `docker rm コンテナ名`

コンテナの削除

- EX.
    
    ```docker
    % docker rm apa000ex1
    ```
    

### `docker psコマンド`

- 動いているコンテナの一覧を表示する
    
    ```bash
    % docker ps
    CONTAINER ID   IMAGE     COMMAND                   CREATED          STATUS          PORTS                 NAMES
    092bac936c0c   mysql     "docker-entrypoint.s…"   14 seconds ago   Up 13 seconds   3306/tcp, 33060/tcp   mysql000ex7
    ```
    
    - STATUS
        - UPだと稼働している
- -aオプション
    
    存在するコンテナの一覧を表示する
    

　　　

## コンテナと通信

---

- コンテナを外部からアクセスできる状態にするには、コンテナ作成時に設定する必要がある
- 外からアクセスできるように、ポートを設定する必要がある
    
    <aside>
    💡 ・コンテナ自体のポートを設定する
    ・母体となる物理的なマシンのポートと、設定したコンテナのポートを繋ぐ
    
    </aside>
    
- ポートの設定例
    
    ```bash
    -p 8080:80
    (-p ホストのポート番号:コンテナのポート番号)
    ```
    
- 複数のWebサーバーを並列で稼働させるには、ホストのポート番号をずらす必要がある

### コンテナの通信: ハンズオン

- ハンズオン
    1. runコマンドを実行する
        1. Apacheのイメージからコンテナを作成してサーバーを立てる
        
        ```bash
        % docker run --name apa000ex2 -d -p 8080:80 httpd
        ```
        
    2. psコマンドで稼働状況を確認する
        
        ```bash
        % docker ps
        CONTAINER ID   IMAGE     COMMAND              CREATED          STATUS          PORTS                  NAMES
        2b7edd728240   httpd     "httpd-foreground"   28 seconds ago   Up 27 seconds   0.0.0.0:8080->80/tcp   apa000ex2
        ```
        
    3. ブラウザでApacheにアクセスする
    4. stopコマンドで停止する
        
        ```bash
        % docker stop apa000ex2
        apa000ex2
        ```
        
    5. rmコマンドで削除する
        
        ```bash
        % docker rm apa000ex2
        apa000ex2
        ```
        
    6. コマンドに引数をつけて、コンテナの消去を確認する
        
        ```bash
        % docker ps -a
        CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
        ```
        

## 色々なコンテナ

---

### LinuxOSの入ったコンテナ

- 中に入って操作することが前提なので、引数にシェルコマンドを指定する
    - オプション
        
        -dを指定せずに-itのみを指定、引数に/bin/bashなどのシェルコマンドを指定する
        
- イメージ名
    - ubuntu, centos, debian

### webサーバーやDBサーバー用のコンテナ

- webサーバーは通信することが前提のため、オプションでポート番号を指定する
    - オプション
        
        -dを指定してバックグラウンドで実行。-pでポートを指定
        
    - イメージ名
        - httpd(Apache), nginx
- DBサーバーはルートパスワードの指定
    - オプション
        
        -dを指定。起動時に -e MYSQL_ROOT_PASSWORDでrootのパスワードを指定
        

### プログラミング言語の実行環境

- イメージ名 python
    - オプション
        
        -dを指定せずに引数にpythonコマンドを指定して実行する
        

## イメージの削除

- コンテナを削除してもイメージは残る
    
    → イメージを削除しないとストレージを圧迫するため、使わなくなったイメージは適宜削除する
    
- イメージを削除するには、イメージから作ったコンテナを全て消去する必要がある

### `docker image rm イメージ名`

イメージを削除する

```bash
% docker image rm イメージ名(:バージョン名)
% docker image rm イメージ1 イメージ2 イメージ3
```

- 半スペース区切りで複数削除するイメージを指定できる

### `docker image ls`

イメージの一覧

- 実行例
    
    ```bash
    % docker image ls
    REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
    mysql        latest    8251f0669c6e   3 days ago    623MB
    nginx        latest    7383c266ef25   10 days ago   188MB
    ```
    
    - TAG
        - バージョンを確認できる