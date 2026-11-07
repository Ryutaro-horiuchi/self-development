## **Terraform モジュールとは**

Terraform モジュールとは、Terraform 構成ファイルを 1 つのディレクトリ内に集めたものです。1 つのディレクトリに `.tf` ファイルが 1 つまたは複数だけという単純な構成でも、1 つのモジュール

- Ex.
    
    ```
    ├── LICENSE
    ├── README.md
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ```
    

## Terraform モジュールの目的

Terraform の構成が大きくなると、内容の把握や更新が難しくなり、変更による想定外の影響やコードの重複が生じやすくなる。モジュールは、こうした問題を解決するために構成をまとめる仕組み。

- **体系化**：関連する構成を論理的なコンポーネントにまとめる。
- **カプセル化**：構成を分離し、変更による意図しない影響や名前の衝突を抑える。
- **再利用**：環境・プロジェクト・チーム間で構成を共有し、作業時間とミスを減らす。
- **整合性の維持**：共通の構成やベストプラクティスを適用しやすくする。

## モジュールの基本

- **モジュール**：同じディレクトリに置かれた Terraform 構成ファイルの集まり。`.tf` ファイルが1つだけでも成立する。
- **ルートモジュール**：Terraform コマンドを直接実行する対象のディレクトリ。
- **子モジュール**：別の構成から `module` ブロックで呼び出されるモジュール。
- **ローカルモジュール**：ローカルファイルシステムから読み込む。
- **リモートモジュール**：Terraform Registry、バージョン管理システム、HTTP URL などから読み込む。

### 入力と出力

- `source`：モジュールの取得元を指定する。
- `version`：対応する取得元で、使用するモジュールのバージョンを指定する。
- **入力変数**：`module` ブロックの引数として渡す。デフォルト値がない変数は必須。
- **出力値**：モジュール内で `output` を定義し、呼び出し元から次の形式で参照する。

```hcl
module.<MODULE_NAME>.<OUTPUT_NAME>
```

## モジュールの標準的な構造

```
minimal-module/
├── LICENSE
├── README.md
├── main.tf
├── variables.tf
└── outputs.tf
```

- `LICENSE`：配布時の利用条件。
- `README.md`：モジュールの使い方。
- `main.tf`：主要なリソース構成。
- `variables.tf`：入力変数の定義。
- `outputs.tf`：出力値の定義。

この構造は慣例であり、すべてのファイルが必須というわけではない。

### 配布に含めないファイル

- `terraform.tfstate`、`terraform.tfstate.backup`：インフラストラクチャの状態を保存する。
- `.terraform/`：取得したモジュールやプラグインを保持する。
- `.tfvars`：モジュール単体の配布では通常不要。入力値は呼び出し元から渡す。

これらは、用途に応じてバージョン管理の対象から除外する。

## 実践1：Registry のモジュールを使う

Terraform Registry の Google Cloud ネットワークモジュールを使い、VPC と3つのサブネットを作成する。

1. サンプルリポジトリを取得し、`v6.0.1` に切り替える。
2. `examples/simple_project` の構成を編集する。
3. プロジェクト ID、ネットワーク名、サブネットのリージョンなどを入力変数で設定する。
4. モジュールの出力を、ルートモジュールの出力から参照する。
5. 初期化してリソースを作成する。

```bash
terraform init
terraform apply
```

- ネットワーク名は `example-vpc` に設定する。
- サブネットには `10.10.10.0/24`、`10.10.20.0/24`、`10.10.30.0/24` を使用する。
- Registry の **Inputs** と **Outputs** で、対応する入力変数と出力値を確認できる。
- 作業後は `terraform destroy` でリソースを削除する。

## 実践2：独自モジュールを作る

Cloud Storage バケットを管理するローカルモジュールを作成し、HTML ファイルを配置する。

### ディレクトリ構成

```
.
├── main.tf
├── variables.tf
├── outputs.tf
└── modules/
    └── gcs-static-website-bucket/
        ├── LICENSE
        ├── README.md
        ├── website.tf
        ├── variables.tf
        └── outputs.tf
```

### モジュール側の定義

- `website.tf` に `google_storage_bucket` リソースを定義する。
- バケット名、プロジェクト ID、ロケーションなどを入力変数にする。
- バージョニング、保持ポリシー、暗号化、ライフサイクルルールなどを設定可能にする。
- 作成したバケットを `output` として公開する。

### ルートモジュールからの利用

- `source = "./modules/gcs-static-website-bucket"` で呼び出す。
    
    ```
    module "gcs-static-website-bucket" {
      source = "./modules/gcs-static-website-bucket"
      
      ...
     }
    ```
    
- バケット名とプロジェクト ID を渡す。
- 例として、作成から365日経過したオブジェクトを削除するライフサイクルルールを指定する。
- バケット名はグローバルに一意にする。

### 作成・確認・削除

1. `terraform init` で初期化する。
2. `terraform apply` でバケットを作成する。
3. サンプルの `index.html` と `error.html` を取得する。
4. `gcloud storage cp` でバケットにアップロードする。
5. ブラウザから `index.html` にアクセスして表示を確認する。
6. `terraform destroy` でリソースを削除する。

## モジュール活用のベストプラクティス

- 構成を書き始める段階から、モジュール化を考える。
- ローカルモジュールで関連する構成を整理・分離する。
- Terraform Registry の既存モジュールを活用する。
- チームで使うモジュールを共有し、共通の構成を維持する。
- 新しいモジュールを追加したら、`terraform init` または `terraform get` で利用できる状態にする。