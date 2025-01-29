## 初めに

業務で Django + CloudRun の環境を使用しており、時間がかかる処理をCloudRunジョブに移行することで、効率的にバックグラウンド処理を行えるようにしました。本記事では、その構築手順を解説します。CloudRunジョブを初めて触る方でも、この記事を参考に実装できるように説明しています。

### 対象読者

- CloudRunサービスは知っているけど、CloudRunジョブは触ったことがない方
- Django(Python)からCloudRunジョブを実行する方法を知りたい方

### 記事で触れること

- Django(Python)からCloudRunジョブを実行する
- ジョブ実行時のコマンド引数をカスタムして実行する

### 記事で触れないこと

- Python、Djangoの基本操作
- デプロイ周りの詳細

<br>

## CloudRunジョブについて

CloudRunはサービスとジョブの2種類に分かれています。ジョブは一連のタスクを実行する非同期処理の機能で、サービスとは異なりHTTPリクエストをリッスンしません。任意のタイミングやスケジュールに沿った実行が可能で、特に長時間実行する処理やバッチタスクに適しています。

詳細については公式ドキュメントをご覧ください
[ジョブを作成する  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/create-jobs?hl=ja)

<br>

## システム要件

システム要件は以下とします

- エンドポイント`job/{id}`でCloudRunジョブを実行することができる
    - `id`は任意の数値を指定可能。`id`をCloudRunジョブに引数として渡す
- CloudRunジョブは、渡された引数`id`をログ出力する

<br>

## 実装
### カスタムコマンドを作成

CloudRunジョブで実行するDjangoのカスタムコマンドを作成します。

- app/management/commands/job.py
    
    ```python
    from django.core.management.base import BaseCommand, CommandError
    
    class Command(BaseCommand):
      def add_arguments(self, parser):
        parser.add_argument('--id', type=int, required=True)
    
      def handle(self, **kwargs):
        id = kwargs['id']
        print(f'ジョブを実行しています。引数id: {id}が渡されました')
    ```
    
- このカスタムコマンドは、以下のように実行できます。
    
    ```python
    python manage.py job —-id={id}
    ```

### CloudRunジョブを実行するエンドポイントを用意

DjangoアプリケーションからCloudRunジョブを実行するエンドポイントを用意します

- urls.py
    
    ```python
    from django.urls import path
    from app import views
    
    urlpatterns = [
        path('job/<int:id>', views.run_job) 
    ]
    ```
    
- views.py
    
    ```python
    from django.http import HttpResponse
    from django.conf import settings
    
    from google.cloud import run_v2
    
    def run_job(self, id):
      overrides = run_v2.types.RunJobRequest.Overrides(
          container_overrides=[
              run_v2.types.RunJobRequest.Overrides.ContainerOverride(
                  args=['manage.py', 'job', f'--id={id}'],
              )
          ]
      )
      request = run_v2.RunJobRequest(
          name=f'projects/{settings.PROJECT_ID}/locations/asia-northeast1/jobs/{settings.JOB_NAME}',
          overrides=overrides
      )
      client = run_v2.JobsClient()
      client.run_job(request=request)
    
      return HttpResponse('CloudRunジョブを実行しました。')
    ```
    
    - [google-cloud-run](https://cloud.google.com/python/docs/reference/run/latest)**ライブラリのインストール**
    - ポイント
        - `RunJobRequest`でジョブ名と引数を指定
        - `client.run_job`でジョブの実行をトリガー
    :::details 詳細
    - `client.run_job`
      ジョブ実行をトリガーできます。この時、ジョブ実行を作成するためのパラメーター `request`を引数に取ります
    - request(`run_v2.RunJobRequest`)
        - name
          CloudRunJobのジョブ名を指定します。フォーマットは`projects/{project}/locations/{location}/jobs/{job}`になります
        - overrides(`run_v2.types.RunJobRequest.Overrides`)
          - ジョブの仕様を上書きします。
          - container_overrides(シーケンス[`run_v2.types.RunJobRequest.Overrides.ContainerOverride`])
                        - コンテナごとのオーバーライド指定になります。今回は`args`にて、リクエストから受け取ったidで上書きする構成にしています。
                        他に`env`や`clear_args`を用いて環境変数を上書きしたり、元々設定されている引数を消去できます。詳細は以下をご覧ください
        [Class ContainerOverride (0.10.14)  |  Python client library  |  Google Cloud](https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.RunJobRequest.Overrides.ContainerOverride)
    :::

### Dockerイメージを作成・保存

ArtifactRegistryにイメージを保存します。
1. Dockerfileの準備
2. ビルドと保存
        
    ```python
    gcloud builds submit --region={region-name} --tag gcr.io/{PROJECT_ID}/{IMAGE_NAME} .
    ```
        
    - 詳細は公式ドキュメントをご覧ください
      [CLI と API を使用してビルドを送信する  |  Cloud Build Documentation  |  Google Cloud](https://cloud.google.com/build/docs/running-builds/submit-build-via-cli-api?hl=ja#submit_builds_with_storage_source)

### CloudRunジョブを作成
Google Cloud ConsoleからCloudRunジョブを作成します。保存したDockerイメージを使用し、デフォルトコマンド引数として先ほど作成したカスタムコマンドを登録します
![](https://storage.googleapis.com/zenn-user-upload/b01b6ae3dfa2-20250126.png)

作成後、ジョブを実行して、ログで成功メッセージを確認します。
```
ジョブを実行しています。引数id: 1が渡されました
```
![](https://storage.googleapis.com/zenn-user-upload/ba3a30ff846a-20250126.png)

### 検証
- CloudRunジョブと同様の手順でサービスもデプロイします。
- デプロイ後、サービスのエンドポイント`/job/{id}`にリクエストを送信し、CloudRunジョブが正しく実行されていることを確認します。

例: `/job/2`を実行した場合、ログに以下のメッセージが出力されることを確認できます。
```
ジョブを実行しています。引数id: 2が渡されました
```
![](https://storage.googleapis.com/zenn-user-upload/cb856a113a42-20250126.png)

### 補足

バックグラウンド処理を行う他の選択肢として、GCPのCloud Functionsがありますが、以下の違いがあります。

- CloudRunジョブ
    - 最大実行時間: 24時間
    - バッチ処理や重たいタスクに適している
- Cloud Functions
    - 最大実行時間: 9分（HTTPトリガーは最大60分）
    - 軽量なイベント駆動型の処理に適している

<br>

## 終わりに

CloudRunジョブを活用することで、処理のバックグラウンド化を比較的簡単に実現できることが分かりました。特に、長時間実行が必要な重たい処理には非常に適しており、他の選択肢よりも柔軟性があります。

この記事が、Djangoアプリでのバックグラウンド化において少しでも参考になれば幸いです。

最後までお読みいただき、ありがとうございました！

<br>

## 参考

https://cloud.google.com/run/docs/create-jobs?hl=ja

https://cloud.google.com/run/docs/execute/jobs?hl=ja

https://cloud.google.com/run/docs/configuring/jobs/containers?hl=ja