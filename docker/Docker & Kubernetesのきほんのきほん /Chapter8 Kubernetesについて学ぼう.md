# kubernetesとは

---

コンテナのオーケストレーションツール(システム全体の統括をし、複数のコンテナを管理できるもの)

- オーケストラと同じ楽団員を指揮者が指揮するように、複数のコンテナを管理するのがKubernetes。
- k8sと略すことも

## Kubernetesは、複数の物理的なマシンに複数のコンテナがあることが前提

- 1台1台の物理的なマシンの中に、複数のコンテナがある
    
    (物理的なマシンは、仮想マシンで構成することもある)
    
    - 複数のコンテナを1台ずつ作成したり、管理したりするのは大変なため、Kubernetesがある
    - 例えば 20個のコンテナを作ろうと思ったら、20回docker runコマンドを使用することになる

# マスターノードとワーカーノード

---

- Kubernetesはマスターノードと呼ばれるコントロールを司るノードとワーカーノードという実際に動かすノードで構成される
- ノードはおおよそ物理的なマシンと同じだと考える
    
    → クラスターの作り方によっては、物理的マシンではないこともある
    

## マスターノード

- ワーカーノード上のコンテナを管理する
    
    (現場監督のようなもので、大工で言えば棟梁に当たる。)
    
- マスターノード上ではコンテナは動かないため、Docker Engineなどのコンテナエンジンもインストールしない

## ワーカーノード

- 実際のサーバーに当たる部分でコンテナが動作するマシン。
- Docker Engineなどのコンテナエンジンもインストールされている必要がある

## クラスター

- マスターとワーカーで構成されたKubernetesのシステムの一群をクラスターと呼ぶ
- クラスターは自立して動くため、管理者のパソコンから直接ワーカーノードを管理することはない。
    
    → 管理者(人)はマスターノードの初期設定・調整のみ行う
    

## Kubernetesを使うには、Kubernetesのインストールが必要

---

Kubernetesは、Docker Engineなどのコンテナエンジンとは別のソフトウェア

### マスターノードとワーカーノード共通してインストールするもの

- Kubernetesのソフトウェア
- CNI(仮想ネットワークのドライバ)
    - 代表的なのはflannel、Calico、AWS VPC CNI

### マスターノードのみ

- コンテナなどの状態管理のためにetcdというDBを入れる

### ワーカーノードのみ

- Docker Engineなどのコンテナエンジンを入れる

### 管理者のPC

マスターノードの設定を行うのに、kubectl(クーべシーティーエル / クーべコントロール)を入れる

→ マスターノードにログインして初期設定を行ったり調整をする

## マスターノード 構成

---

マスターノードは、コントロールプレーン(制御盤)でワーカーノードを管理する

- コントロールプレーンは5つの部品で管理されている。
    
    
    | 項目 | 内容 |
    | --- | --- |
    | kube-apiserver | 外部とやり取りをするプロセス。kubectlからの命令を受け取って実行する |
    | kube-controller-manager | コントローラーを統括管理・実行する |
    | kube-scheduler | Podを、ワーカーノードへと割り当てる |
    | cloud-controller-manager | クラウドサービスと連携して、サービスを作る |
    | etcd | クラスター情報を全管理するデータベース |
    - etcd以外は、Kubernetesに入っているため、etcdとKubernetesをインストールすればすべて入る

## ワーカーノード 構成

---

- ワーカーノードは、kube-letとkube-proxyが動く。
    
    
    | 項目 | 内容 |
    | --- | --- |
    | kube-let | マスターノード側のkube-schedulerと連携して、ワーカーノード上にPod(コンテナとボリューム)を配置し実行する。また、実行中の状態を定期的に監視し、kube-scheduelrへ通知する |
    | kube-proxy | ネットワーク通信をルーティングする仕組み |

![IMG_1365.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a07a2b8c-8124-43de-ac1e-abaef324adac/IMG_1365.jpeg)

# Kubernetesは常に望ましい状態に保つ

---

- DockerComposeは、作成時のみオプションの指定によって、コンテナの数を指定できるが、監視はしていないため、「作って終わる」のに対し、Kubernetesは「その状態を維持する」
    - Ex. コンテナを4つとボリュームを4つをKubernetesでリリース
        - → コンテナが1つ壊れたら、そのコンテナを自動で削除して新しいコンテナを1つ作成する

## Kubernetesを使ったシステムのコンテナ削除

- 直接コマンドでコンテナを削除するのではなく、設定ファイルでコンテナ数を指定して削除を行う
    - → 直接コマンドでコンテナを削除すると、設定ファイルの「状態」と整合が取れず、新たにコンテナをKubernetesが作成してしまうため

## コラム

- 増減しやすい仕組みのことをスケーラビリティと呼ぶ
- Kubernetesの定義ファイルは、データベースとして管理される
    - 作成した定義ファイルは、etcdに書き込まれる

# Kubernetesの構成と用語

---

## Pod

- Kubernetesでは、コンテナはPodという単位で管理される
- Podはコンテナとボリュームがセットになったもの
    - 基本的に1Pod 1コンテナだが、コンテナは複数にすることもできる
    - ここでのボリュームは、Podの中での複数のコンテナが情報を共有するために使用するものであり、作らないこともある

## Podを束ねるサービス

- 同一の構成のPodをまとめて管理する
    - Podを束ねる班長のようなもの
    - Podが複数のワーカーノード(マシン)に存在している場合でも、まとめて管理する
- ロードバランサーの役割を果たしている
    - サービス一つ一つに固有のIPアドレスが付与されており、通信をPodへ適切に振り分ける
        
        → 各々のワーカーノードへの振り分けは、本物のロードバランサーで行われる
        

## デプロイメントとレプリカセット

### レプリカセット

- サービスと同じく同一の構成のPodをまとめて管理するが、こちらはPodの数を管理する班長
    - Podが障害で一部停止してしまった場合に、足りない分を増やしたりする。定義ファイルのPodの数が変更されたら、その分数を変更する
- レプリカセットにより管理されている同一構成のPodをレプリカと呼ぶ
    - Podを増減することを、レプリカを増やす・減らすと言ったり、Podの数を決めることをレプリカの数を決めるとも言ったりする

### デプロイメント

- Podのデプロイを管理するもの、どのイメージを使うかなど
- イメージとして、レプリカセットが班長だとしたらデプロイメントはその上司

## リソース

Pod、サービス、デプロイメント、レプリカセットなどをリソースと呼ぶ。

リソースは50種類ぐらいあるが、実際に使うのは少ない

## Kubernetesの用語まとめ

![IMG_1366.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/cc15a1a4-51c5-4a6e-859b-7095e5a05a51/IMG_1366.jpeg)

# Kubernetesのインストールと使い方

## Kubernetesにはいくつか種類がある

---

- KubernetesはCloud Native Computing Foundation(CNCF)という団体で策定された規格
    - 元々Google社の技術だったが、Google社などがCNCFという団体を作成し、そこに寄贈した
- サードパーティーから、管理機能を充実させたものやコンパクトにしたものなど、Kubernetesの仕様に準拠したソフトウェアが提供されている
    - こうしたソフトウェアは互換性がある。「Cerficied Kubernetes」という認定を受けている

## どのKubernetesを使うのか

---

- 一から構築するのが大変。負担に対する利益が少ない
- 一般的に使うときは、AWSなどのクラウドコンピューティングサービスを使う
    - Ex. AWS
        - EC2かFargateをワーカーノードとして構築する。EKSでマスターノードとして管理する
        - 仮想サーバー
            - EC2: サーバー機能を提供するサービス
            - Fargate: コンテナの実行エンジンサービス
        - EKS(Amazon Elastic Kubernetes Service)
            - マスターノードに当たるサービス
- デスクトップ版は、あらかじめKubernetesがバンドルされている
    - Settings → Enable Kubernetesにチェックをつければ使用できる
    - etcdやCNIをわざわざ入れる必要はない
    - 1台のマシンにマスターノードとワーカーノードとしての機能を持たせることができる
    - とはいえ、あくまで学習用

## 物理的なマシンでのKuberntes構築とkubeadm

---

- 何台もの物理マシンを使った本格的なKubernetesを使用方法について
    - 物理的なマシン、仮想的なマシンを必要数分用意し、UbuntuなどのLinuxOSを用意する
    - kubeadmという構築ツールを使用して、[マスターノードとワーカーノード共通してインストールするもの](https://www.notion.so/cdf9c3bacdb7443289cd0722e14d7d18?pvs=21) で挙げられている必要なソフトウェアをインストールする
    - マスターワーカーそれぞれでマシンが何を担当するのかを設定する
        - マスターで`kubeadm initで`初期設定をする
        - ワーカーで`kubeadm join`を実行するとマスターとワーカーが繋がる

# 定義ファイルの書き方

- Kubernetesで使うPodやサービスに関する設定をマニフェストと呼び、記述したファイルをマニフェストファイルと呼ぶ
- 形式はyaml形式。Docker Composeと異なりファイルは任意の名前で良い。

## 定義ファイルはリソース単位で記述する

---

- 定義ファイルはリソース単位で記述する
    - 初心者はリソースの項目として使うのは「デプロイメント」と「サービス」ぐらい
    - デプロイメントがレプリカセットとPodを内包しているため、「Pod」「レプリカセット」という項目を単独で記述することは少ない
- 定義ファイルは分けても良い
    - リソースごとに分けてもまとめて書いても良い
        - まとめて書く場合は、リソースごとに書く

### 記述例 大項目のみ

```yaml
apiVersion:
kind:
metadata:
spec:
```

### リソースの指定 APIグループと種類

- APIグループ(apiVersion)と種類(kind)で指定する
- よく使うリソースのAPIグループと種類
    
    
    | リソース | APIグループ / バージョン | 種類(kind) |
    | --- | --- | --- |
    | Pod | core/v1(v1) | Pod |
    | サービス | core/v1(v1) | Service |
    | デプロイメント | apps/v1 | Deployment |
    | レプリカセット | apps/v1 | ReplicaSet |

### メタデータとスペック

- メタデータ(metadata)
    - リソースの名前やラベルを記述する
    - ラベル
        - キーと値のペアでメタデータとして設定する。ラベルをつけると、セレクター機能を使用して特定のラベルがついたPodだけを配置するなど、Podを選択して設定できる
    - 主なメタデータ(一部)
        
        
        | 項目 | 内容 |
        | --- | --- |
        | name | リソースの名前 |
        | namespace | リソースが細分化されるDNS互換のラベル |
        | uid | 一意に識別する番号 |
        | resourceVersion | リソースのバージョン |
        | labels | 任意のラベル |
- スペック(spec)
    - どんなリソースを作るのか。
    - リソースの種類によって書き方が異なる

## メタデータとスペックの書き方 Pod編

- フォーマット
    
    ```yaml
    apiVersion:
    kind:
    metadata:
      name:
      labels:
    spec:
      containers:
        - name:
          image:
          ports:
    ```
    
    - metadata name
        - Pod(コンテナ+ボリューム)の名前
        - アイドルグループのグループ名(Ex. Twice)
    - containers name
        - コンテナ名前
        - アイドルグループに所属している個々のアイドル名(Ex. mina)

p265

ハンズオン(1)

step2

```yaml
apiVersion:
kind:
metadata:
spec:
```

step3

```yaml
apiVersion: v1
kind: Pod
metadata:
spec:
```

step4

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: apa000pod
  labels:
    app: apa000kube
spec:
```

step5

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: apa000pod
  labels:
    app: apa000kube
spec:
  containers:
    - name: apa000ex91
      image: httpd
      ports:
      - containerPort: 80
```

p266

ハンズオン(2)

- Podがアイドルのグループ、コンテナがアイドルだとすると、デプロイメントは所属事務所のようなもの
- selector
    - 管理対象を指定する
    - ラベルを指定する。templateの中のmetadata
- replica
    - Pod数を幾つに保つか
- template
    - 作成するPodの情報を書く
        - metadata, specが項目になる

step2

```yaml
apiVersion:
kind:
metadata:
spec:
```

step3

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
spec:
```

step4

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apa000dep
spec:
```

step5

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apa000dep
spec:
  selector:
    matchLabels:
      app: apa000kube
  replicas: 3
```

step6

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apa000dep
spec:
  selector:
    matchLabels:
      app: apa000kube
  replicas: 3
  template:
    metadata:
      labels:
        app: apa000kube
    spec:
      containers:
        - name: apa000ex91
          image: httpd
          ports:
          - containerPort: 80
```

templateのmetadata内のnameはいらない

p272 ハンズオン(3)

typeの設定

- Serviceの種類。外部とサービス間の通信を、どのIPアドレス(もしくはDNS)でアクセスするかを設定するもの
- 業務で使うときは、LoadBalancerを設定するケースがほとんど。
- NodePortはそのワーカーノードに直接アクセスするためのもの。
- Externalname
    - 中から外に通信したい時に使用する

p273

ポートの設定

- サービスのポート、ワーカーノードへのポート、コンテナへのポートをそれぞれ設定する

(p274の図は写真をとる)

p274

セレクターの設定

デプロイメントの時と違い、matchLabelsは書いてはダメ

デプロイメントは、ラベルセレクターというものを使用して、この条件に合うときなどの指定ができる

step2

```yaml
apiVersion:
kind:
metadata:
spec:
```

step3

```yaml
apiVersion: v1
kind: Service
metadata:
spec:
```

step4

```yaml
apiVersion: v1
kind: Service
metadata:
  name: apa000ser
spec:
  
```

step5

```yaml
apiVersion: v1
kind: Service
metadata:
  name: apa000ser
spec:
  type: NodePort
  ports:
  - port: 8099 # サービスのポート
    targetPort: 80 # コンテナのポート
    protocol: TCP
    nodePort: 30080 # ノードのポート
  selector:
    app: apa000kube
```

p278

Kubernetesのコマンド

kubectlコマンドを使って操作する

```yaml
kubectl コマンド オプション
```

コマンド一覧

太字のもののみ押さえる

ハンズオン(1)定義ファイルでPodを作る

step1

デプロイメントの定義ファイルを読み込ませる

```yaml
kubectl apply -f /Users/
```

p284

定義ファイルでPodを増やす

apa000dep.ymlのreplicasを3から5に変更する

```yaml
apiVersion: apps/v1
...
spec:
  selector:
    matchLabels:
      app: apa000kube
  replicas: 5
  template:
    ...
```

p286

イメージをApacheからnginxに変える

```yaml
apiVersion: apps/v1
...
spec:
	...
  template:
		...
    spec:
      containers:
        - name: apa000ex91
          image: nginx
          ports:
          - containerPort: 80
```

p288

手動でPodを削除する

p290

デプロイメントとサービスを削除する