## Terraformとは

- インフラストラクチャを安全かつ効率的に構築・変更・バージョン管理するツール。
- 構成ファイルに希望する状態を記述すると、必要な操作を実行プランとして作成し、適用できる。
- 構成を変更した場合は、変更内容に応じた増分の実行プランを作成する。
- VM、ストレージ、ネットワークから、DNSエントリやSaaS機能まで管理できる。

## 主な機能

- **Infrastructure as Code**
  - インフラ構成をコードとして記述し、バージョン管理・共有・再利用できる。
- **実行プラン**
  - 適用時に行う操作を事前に確認し、予想外の変更を防ぐ。
- **リソースグラフ**
  - リソース間の依存関係を把握し、依存しないリソースの作成・変更を並行して実行する。
- **変更の自動化**
  - 変更内容と適用順序を整理し、少ない手作業で複雑な変更を適用できる。

## リソースの定義

`instance.tf`の`resource`ブロックで、作成するリソースを定義する。

```hcl
resource "google_compute_instance" "terraform" {
  project      = "qwiklabs-gcp-04-eb3b8d7a3d28"
  name         = "terraform"
  machine_type = "e2-medium"
  zone         = "us-east1-d"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

- リソースタイプ：`google_compute_instance`
- リソース名：`terraform`
- タイプの接頭辞`google`は、Googleプロバイダに対応する。
- この例では、Debian 12を使用する`e2-medium`のVMを定義している。

## インフラ構築の流れ

### 1. 初期化する

```bash
terraform init
```

- 新しい構成や、バージョン管理から取得した構成で最初に実行する。
- ローカル設定・データを初期化し、必要なプロバイダのプラグインをダウンロード・インストールする。

### 2. 実行プランを確認する

```bash
terraform plan
```

- 希望する状態にするために必要な操作を確認する。
- 実際のリソースを変更せず、意図した変更になっているかを検証できる。

### 3. 変更を適用する

```bash
terraform apply
```

- 構成ファイルと同じディレクトリで実行する。
- 表示された実行プランを確認し、問題がなければ`yes`を入力して適用する。
- 承認前の時点では、インフラはまだ変更されていない。

実行プランの表示例：

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

- `+`：リソースの新規作成。
- `<computed>`や`(known after apply)`：作成後に値が確定する属性。
- プランに誤りや危険な変更がある場合は、適用を中止する。

### 4. 現在の状態を確認する

```bash
terraform show
```

- 管理しているリソースの現在の状態や属性を確認する。
- 取得した値は、追加リソースや出力の構成に利用できる。

## 状態ファイル

- Terraformは、リソースの情報を`terraform.tfstate`に記録する。
- 状態ファイルは、作成したリソースのIDを追跡し、Terraformが管理対象を把握するために重要。