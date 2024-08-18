---
marp: true
paginate: true
theme: default
---
<style>
  section {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }
  ul {
    flex-basis: 60%;
  }
  li {
    font-size: 32px
  }
</style>

<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>

# Google Cloud Next Tokyo  に行ってきました

---

<style scoped>
  li {
    font-size: 36px;
  }
</style>

# アジェンダ
- 堀内　 「Gemini for Google Cloud で出来ること」
- 田中 

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>

# Gemini for Google Cloud で出来ること

--- 
<style scoped>
.hoge {
  display: flex;
  justify-content: space-around;
}
img {
 
}
</style>

# 参考

<div class="hoge">
  <img width="50%" src="/Users/ryutafolder/workspace/self-development/output/2024/08/Monosnap Next_Tokyo_24_Program_Guide 2024-08-18 16-38-31.png">
  <img style="margin-left: 8px;"height="80%" width="50%" src="/Users/ryutafolder/workspace/self-development/output/2024/08/Next1.jpeg">
</div>

---
<style scoped>
section {
  justify-content: flex-start;
}
</style>
# 参考

---
<style scoped>
section {
  display: flex;
  
}
.hoge {
  
}
</style>

# Gemini for Google Cloud 

- Google Cloud向けのGeminiが今年4月に新たに発表された。
- Googleの最新AIモデルである「Gemini」を用いた複数のサービスの統合的なブランド
  - コーディング支援のGemini Code Assistも傘下に加わっている


<img height="60%" width="60%" src="/Users/ryutafolder/workspace/self-development/output/2024/08/Monosnap Gemini for Google Cloud is here | Google Cloud Blog 2024-08-18 16-53-46.png">

<!-- この中から、主にGemini code Assist, Gemini in BigQueryについて取り上げます -->

---

# Gemini Code Assist 

---

<style scoped>
ul {
  flex-basis: 60%;
}
</style>

# Gemini Code Assist 
- コードの生成とコードの解説を行い、エンジニアの生産性を向上させる
- Visual Studio Codeなどの一般的なエディターで使用可能
- GitHub Copilotと競合するサービス

---


# Gemini Code Assist デモ



---

# Gemini Code Assist 新しい機能

<br>

## Repository-wide Context (プライベートプレビュー)

<br>

  - 単一のファイルを超え、コードベース全体を認識した上でコーディングアシストしてくれる
  - Gemini 1.5 Proを使用した100万トークンのサポートにより可能


---

# Gemini Code Assist 新しい機能

<br>

## Code Customization (プライベートプレビュー)

<br>

- プライベートのコードベースに基づくコンテキストを考慮したレスポンスに対応
- GitHub、GitLab、Bitbucketを含む複数のソースコードリポジトリにアクセスするための接続を提供しています


---
<style>
/* .hoge {
  flex-basis: 80%;
} */

</style>

# Gemini Code Assist と Github Copilotとの比較

<div class="hoge">

|  | トークン | ナレッジベース | コード管理 |
| --- | --- | --- | --- |
| Copilot (GPT-4 Turbo ) | 128,000 | Github | Github |
| Gemini  | 1,000,000 | Stack Overflow, Datadog、Redis、Datastax、Elastic、HashiCorp、Neo4j、Pinecone ...etc  | Github, GitLab, Bitbucker |

</div>

<!--
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

-->

---
# Gemini in BigQuery 

---

<style scoped>
  li {
    font-size: 28px
  }
</style>
# Gemini in BigQuery
BigQuery上で、自然言語を使用してSQLの生成や補完ができる

<br>

#### BigQuery data preparation(プレビュー)
  - 生成AIの補助のもと、BigQueryのデータのクレンジングができる仕組み。コンテキストを考慮した上で提案をしてくれる


#### BigQuery data canvas (プレビュー)
  - データエンジニア向けの機能。データの探索、クエリ、可視化を1箇所で行える


---
# BigQuery data canvas (プレビュー) デモ画像

---
<style scoped>
li {
  font-size: 24px
}
</style>

# Gemini for Google Cloud  その他

- Gemini Cloud Assist
    - AIとのチャットを通じて、ニーズに合わせたアーキテクチャ構成の生成やインシデント発生時の問題の診断と原因究明、解決の支援、さらにコスト削減や性能の最適化や可用性の強化などに関するアドバイスなどを提案。
- Gemini in Security
  - 既存製品のセキュリティサービスである、Security Command Centerなどに組み込まれる
  - チャットを通じて、セキュリティ上の問題に関するイベントデータの収集と要約、取るべきアクションの推奨を提案。
- Gemini in Looker (プレビュー)
  - 自然言語を使用してレポートや Google スライドのプレゼンテーションを作成できる
- Gemini in Databases
  - SQL生成機能やデータ要約機能、データベースの移行支援などをAIが提供する


---

# 引用





















