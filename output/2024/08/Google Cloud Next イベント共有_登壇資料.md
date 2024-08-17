- 執筆
    - はじめに
        - Google Cloud Nextに行ってきました
        - アジェンダ
    - 堀内
        - こちらの基調講演を軸に
            - 画像
        - Gemini for Google Cloud
            - Google Cloud向けのGeminiが今年4月に新たに発表された。
                - https://cloud.google.com/blog/products/ai-machine-learning/gemini-for-google-cloud-is-here?hl=en
                - この中から、主にGemini code Assist, Gemini in BigQuery, Gemini in Lookerについて取り上げます
            - Gemini code Assist (プライベートプレビュー)
                - 概要
                    - コードの生成とコードの解説を行い、エンジニアの生産性を向上させる
                    - Visual Studio Codeなどの一般的なエディターで使用可能
                    - GitHub Copilotと競合するサービス
                - デモ画像(動画も検討)
                    - エディター内で生成
                    - テストコードを生成
                    - コードの説明
                - Copilotとの違い
                    - トークンの量 チャットでクエリおよび生成できるコードの量
                        - Github Copilot (GPT-4 Turbo ) は128,000 トークンほどらしい
                        - Gemini 1.5 Proは1,000,000トークン
                    - ナレッジデータベース
                        - Github Copilotは、GitHub のデータを使用
                        - Gemini
                            - Stack Overflowをはじめとする下記パートナーからのデータと知識ソースを使用して、改良をしている
                            - Datadog、Datastax、Elastic、HashiCorp、Neo4j、Pinecone、Redis、Singlestore、Snyk
                    - コードリポジトリサービスとの連携
                        - CopilotはGithubのみ
                        - Gemini は GitLab、GitHub、Bitbucket など
                - 今後の新機能(プレビュー)
                    - Repository-wide Context
                        - コードベース全体を認識した上で、コーディングアシストしてくれる
                        - Gemini 1.5 Proを使用した100万トークンのサポートにより可能
                            - トークン チャットでクエリおよび生成できるコードの量
                    - 
                    - Code Transformation
                    - Code Customization
                - 他の生成AIとの比較
                    
                    
                    |  |  |
                    | --- | --- |
                    |  |  |
                    |  |  |
                - デモ
                    - インラインでコメントでプロンプトを入力
                    - テストコードの生成
                    - コードの説明
                - これから
                    - コードベース全体を認識 (Repositry-wide Context) (プライベートプレビュー)
                        - 登壇上ではGemini自体の学習に使用されることはない
                    - コードを分析し、リファクタリング、最適化して変換 (Code Transformation) (パブリックプレビュー)
                    - プライベートのコードベースのコンテキストに応じたレスポンス対応(Code Customization)  (プライベートプレビュー)
            - Gemini in BigQuery (プレビュー
                - 専用のボタンを押してプロンプトを入力することや、クエリエディタ内でプロンプトを入力してそのまま実行することも可能
                - デモ
                - BigQuery data canvas (プレビュー)
                    - デモ
                - BigQuery data preparation(プレビュー)
                    - 
            - Gemini in Looker (プレビュー)
                
                https://support.google.com/looker-studio/answer/15067516
                
                - データの可視化や、レポート作成のための複雑な操作を自然言語で行えるようになる
                - 自然言語を使用した、グラフの生成
                - 1clickで、Google Slideの自動生成
                - レポート生成
    - イベント自体の感想
        - (一旦ざっくり)
            - Gemini関連が多かった
            - 資格取得者用のラウンジがあった
            - オライリーなどの技術書籍が20%引き
        - 写真とか載せれるものがあれば
- 参考になりそうなもの
    - https://cloud.google.com/gemini/docs/overview?hl=ja
    - https://cloud.google.com/blog/products/ai-machine-learning/gemini-for-google-cloud-is-here?hl=en
    - https://note.com/takuma_yoshida/n/nb00699cfd8f0
    - ([Gemini for Google Cloud: コード アシスタントからデータ分析まで、AI が
    あなたのワークフローを加速](https://www.notion.so/Gemini-for-Google-Cloud-AI-b82743ab31fb41e0aee9c11d59551c00?pvs=21) )