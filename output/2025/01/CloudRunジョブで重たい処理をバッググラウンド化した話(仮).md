## 初めに

業務でDjangoアプリケーション上で時間がかかる処理をCloudRunジョブに移行しました。初めて触った部分でもあるので、備忘録として手順を残しておきたいと思います。

## 前提

### 対象読者

- CloudRunサービスは知っているけど、CloudRunジョブは触ったことがない方
- CloudRunジョブをコードから実行する方法を知りたい方

### 記事で触れること

- Python(Django)からCloudRunジョブを実行する
- オプションをカスタムして実行する

### 記事で触れないこと

- Python, Django周り
- デプロイ周り

## 本題

### CloudRunジョブについて

CloudRunはサービスとジョブとに分かれていますが、ジョブはタスクを実行するだけであり、サービスと違いHTTPリクエストはリッスンしません。任意のタイミング、スケジュールに沿った実行が可能です。

詳細は公式のページをご覧ください

[ジョブを作成する  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/create-jobs?hl=ja)

### コード

- カスタムコマンドを作成
    
    CloudRunジョブ用にカスタムコマンドを作成します。例のコードはオプションidを受け取り出力するだけの簡単な処理にしていますが、実際にはバックグラウンド化したい重い処理を呼びだします
    
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
        
    - これで、`python [manage.py](http://manage.py) job —id={id}`の形でコマンド実行できます
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
                        - コンテナごとのオーバーライド指定になります。今回は`args`にて、リクエストから受け取ったidで上書きする構成にしています。
                        他に`env`や`clear_args`を用いて環境変数を上書きしたり、元々設定されている引数を消去できます。詳細は以下をご覧ください

[Class ContainerOverride (0.10.14)  |  Python client library  |  Google Cloud](https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.RunJobRequest.Overrides.ContainerOverride)

### イメージを保存

- ArtifactRegistryにイメージを保存します。詳細は割愛しますが、Dockerfileを用意し、`gcloud builds submit`コマンドを使用することで、イメージを保存することができます。詳細は以下をご覧ください
    
    [CLI と API を使用してビルドを送信する  |  Cloud Build Documentation  |  Google Cloud](https://cloud.google.com/build/docs/running-builds/submit-build-via-cli-api?hl=ja#submit_builds_with_storage_source)
    

### CloudRunジョブを作成

![1.image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/0eb85480-81ba-4753-bd28-4a48308320e4/1.image.png)

コンソールからCloudRunジョブを作成します。イメージは先ほど作成したものを使用してください

![2.image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/50f559b7-5cfa-4492-8523-6851e18d808a/2.image.png)

画像の通りの設定にします。idはデフォルトで1とします。

作成後実行を確認し、成功とログでメッセージを確認できればokです

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/849cf71d-9bcd-4dbf-9331-e8e92730195a/image.png)

### CloudRunサービスから検証

ClouRunと同様の手順でサービスもデプロイします。

デプロイ後、用意したエンドポイントjob/{id}を叩き、CloudRunジョブのタスクが新しく実行されていること、引数が上書きされていることが確認できます。

画像はjob/2で叩いて確認したものになります

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/aca51744-8f13-435b-be38-c43eb09bb41a/image.png)

今回はわかりやすいように引数についてログ出力しましたが、コンソール側からでも各タスクごとに引数や環境変数がどういった構成で実行されたのか確認することができます

![Monosnap 履歴 – cloud…bs-sample – Task 0 logs – Cloud Run ジョブ – PCA-Udemy – Google Cloud コンソール 2025-01-24 09-49-26.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/9afc480d-52aa-4db0-8d19-40b36c912a84/Monosnap_%E5%B1%A5%E6%AD%B4__cloudbs-sample__Task_0_logs__Cloud_Run_%E3%82%B7%E3%82%99%E3%83%A7%E3%83%95%E3%82%99__PCA-Udemy__Google_Cloud_%E3%82%B3%E3%83%B3%E3%82%BD%E3%83%BC%E3%83%AB_2025-01-24_09-49-26.png)