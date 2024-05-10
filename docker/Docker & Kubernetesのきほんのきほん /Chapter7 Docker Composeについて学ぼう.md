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