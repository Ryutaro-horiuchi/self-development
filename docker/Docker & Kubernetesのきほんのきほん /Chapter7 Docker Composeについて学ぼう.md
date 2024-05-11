p202

構築に関わるコマンド分の内容を一つのテキストファイルに画期混んで、一気に実行したり、停止したり破棄したりできるのが、Docker Compose

p203

upコマンドは、docker runコマンドに似ている。定義ファイルに従って、イメージをDLしたり、コンテナを作成・起動したりする

downコマンドは、コンテナとネットワークを停止・削除する。ボリュームとイメージはそのまま残る

stopコマンドは、コンテナとネットワークを停止のみ行う

p204

Docker ComposeとDockerfileの違い

Docker Compose - docker run コマンドの集合体で、作成するのは、コンテナとネットワークやボリュームといった周辺環境も合わせて作成できる

Dockerfile - イメージを作るもの。周辺環境は作成できない

p205

Docker Composeのインストールと使い方

Docker Engineとは別のソフトウェアであるため、別途インストールが必要

→ MacやWindowsのデスクトップアプリであれば、既に入っているためインストール作業がいらない

→ Linuxの場合は、Docker ComposeとPython3の実行環境と必要なツール(python3, python3-pip)をインストールする

- Docker Composeはpythonで書かれたプログラムであるため、pip3コマンドでインストールする

p206

定義ファイル名は、必ず「docker-compose.yml」

DockerComposeを使用するには、Dockerfileと同様、ホスト上にファルダを作成して、そこに定義ファイルを置く。定義ファイルはフォルダ内に一つのみおく。

フォルダには、コンテナ作成に必要な画像ファイルや、HTMLファイルなども置いておく

p207

Docker Composeでは、コンテナの集合のことを「サービス」と呼んでいる

p208

定義ファイル doker run コマンドの内容と似ている

p211

定義ファイルの記述例 yml

```yaml
version: 3
service:
  コンテナ名1:
  コンテナ名2:
networks:
  ネットワーク名1:
volumes:
  ボリューム名1:
  ボリューム名2:

```

コンテナの設定記述例

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

記述が一つの場合は、コロンの後に続けて書けば良い

記述が複数になる場合は、ハイフンで改行して記入する

p212

記述ルールまとめ

p213

定義ファイルの項目

depends_on: 他のサービスに依存することを示す。依存先のコンテナが作られてからコンテナを作成する

restart: コンテナが停止した時にどうするか

p215

ハンズオン

下記と同様のものをdocker-composeで作成する

[ハンズオン WordPressコンテナとMySQLコンテナを作成し、動かしてみよう](https://www.notion.so/WordPress-MySQL-145f081c660e42b38da8052f95f93da9?pvs=21) 

STEP2

```yaml
version: "3"
services:
networks:
volumes:
  
```

STEP3

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

step4

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

step5

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

p221

docker-composeコマンドを使用する

up, down, stopのコマンドをとりあえず覚えておけば良い。

コンテナや周辺環境を作成するコマンド docker-compose up

よく使う記述例

```bash
docker-compose -f 定義ファイルのパス up オプション
```

```bash
docker-compose -f /Users/ユーザー名/Documents/com_folder/docker-compose.yml up -d
```

- -d バックグラウンドで実行する

コンテナや周辺環境を削除するコマンド docker-compose down

```bash
docker-compose -f 定義ファイルのパス down オプション
```

コンテナを停止するコマンド docker-compose stop

```bash
docker-compose -f 定義ファイルのパス stop オプション
```

p226

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