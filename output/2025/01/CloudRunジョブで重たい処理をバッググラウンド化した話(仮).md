## 初めに

業務でDjangoアプリケーション上で時間がかかる処理をCloudRunジョブに移行しました。初めて触った部分でもあるので、備忘録として残しておきたいと思います。

## 前提

### 対象読者

- CloudRunサービスは知っているけど、CloudRunジョブは触ったことがない方
- CloudRunジョブをコードから実行する方法を知りたい方

### 記事で触れること

- PythonからCloudRunジョブを実行する
- オプションをカスタムして実行する

### 記事で触れないこと

- Python, Django周辺知識

## 本題

### CloudRunジョブについて

CloudRunはサービスとジョブとに分かれていますが、ジョブはタスクを実行するだけであり、サービスと違いHTTPリクエストはリッスンしません。任意のタイミング、スケジュールに沿った実行が可能です。

詳細は公式のページをご覧ください

[ジョブを作成する  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/create-jobs?hl=ja)

### コード

- カスタムコマンドを作成
    
    CloudRunジョブ用にカスタムコマンドを作成します。例のコードはオプションidを受け取り出力するだけの簡単な処理にしていますが、実際にはバックグラウンド化したい重たい処理を呼びだします
    
    - app/management/commands/job.py
        
        ```python
        from django.core.management.base import BaseCommand, CommandError
        
        class Command(BaseCommand):
          def add_arguments(self, parser):
            parser.add_argument('--id', type=int, required=True)
        
          def handle(self, **kwargs):
            id = kwargs['id']
            print(f'id: {id}が渡されました')
        ```
        
    - これで、`python [manage.py](http://manage.py) job —id={id}`の形ででコマンド実行できます
- CloudRunジョブを実行するエンドポイントを用意
    
    アプリケーションからCloudRunジョブを呼び出すエンドポイントを用意します
    
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
        
          return HttpResponse()
        ```
        
        - 専用ライブラリ [google-cloud-run](https://cloud.google.com/python/docs/reference/run/latest)をインストールします
        - `client.run_job`
            - ジョブ実行をトリガーできます。この時、ジョブ実行を作成するためのパラメーター `request`を引数に取ります
        - request
            - name
                - CloudRunJobのジョブ名を指定します。フォーマットは`projects/{project}/locations/{location}/jobs/{job}`になります
            - overrides
                - ジョブの仕様を上書きします。
                    - `run_v2.types.RunJobRequest.Overrides.ContainerOverride`
                        - コンテナごとのオーバーライド指定になります。今回は`args`にて、引数をオーバーライドしていますが、他に`env`や`clear_args`を用いて環境変数を上書きしたり、元々設定されている引数を消去できます。詳細は以下をご覧ください
                            
                            [Class ContainerOverride (0.10.14)  |  Python client library  |  Google Cloud](https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.RunJobRequest.Overrides.ContainerOverride)
                            
    
- CloudRunJobをコンソールで作成する