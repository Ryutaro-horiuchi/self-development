## 初めに

業務でDjangoアプリケーション上で時間がかかる処理をCloudRunジョブに移行し、バックグラウンド化しました。初めて触った部分でもあるので、備忘録として残しておきたいと思います。

## 前提

### 対象読者

- CloudRunの基本的な理解
- Python, Djangoの基本的な理解

### 記事で触れること

- PythonからCloudRunジョブを実行する
- ジョブ実行時にオプションをつけてオーバーライドする

### 記事で触れないこと

- Python, Django周辺知識

## 本題

### CloudRunジョブについて

CloudRunはサービスとジョブとに分かれていますが、ジョブはタスクを実行するだけであり、サービスと違いHTTPリクエストはリッスンしません。任意のタイミング、スケジュールに沿った実行が可能です。

詳細は公式のページをご確認ください

[ジョブを作成する  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/create-jobs?hl=ja)

### コード

- カスタムコマンドを作成
    
    CloudRunジョブ用にカスタムコマンドを作成します。例なので、簡単な内容としては実際にはバックグラウンド化したい重たい処理を呼び出します
    
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
        
    - これで、python [manage.py](http://manage.py) job —id={id}の形でコマンド実行できます
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
        
        - CloudRunを実行するために、専用のgoogle-cloud-runをインストールします
    
- CloudRunJobで実行するか