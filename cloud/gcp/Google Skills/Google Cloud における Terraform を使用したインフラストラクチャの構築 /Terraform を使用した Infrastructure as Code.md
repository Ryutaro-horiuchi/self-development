## TerraformとInfrastructure as Code

- **Infrastructure as Code（IaC）**は、インフラを手動操作ではなく、ファイルで定義・管理する方法。
- **Terraform**は、HashiCorpが開発したIaCツール。インフラの構築・変更・管理を、安全かつ再現可能な形で行う。
- *HCL（HashiCorp Configuration Language）**で希望するリソースを定義する。
- プロバイダを通じて、Google Cloud、AWS、GitHub、Dockerなどのリソースを管理できる。

## 基本的なワークフロー

1. **スコープを決める**：必要なリソースを確認する。
2. **構成を書く**：HCLで希望する状態を記述する。
3. **初期化する**：必要なプロバイダを取得する。
4. **プランを確認する**：作成・変更・破棄される内容を確認する。
5. **適用する**：実際の環境に変更を反映する。

```
terraform init
terraform plan
terraform apply
```

- 構成ファイルとして、`.tf`または`.tf.json`を使用する。
- 状態ファイルは、管理している環境の状態を記録し、構成との差分を判断するために使われる。
- `terraform show`で現在の状態を確認できる。

## 構成ファイルの主な要素

- **`terraform`ブロック**
    - 必要なプロバイダの取得元やバージョンを指定する。
    - Terraform Registry からダウンロードするプロバイダを Terraform に知らせるために必要
    
    ```
    terraform {
      required_providers {
        google = {
          source = "hashicorp/google"
          version = "3.5.0"
        }
      }
    }
    ```
    
    - プロバイダのバージョンを制限すると、破壊的変更を含むバージョンの意図しない取得を防げる。
- **`provider`ブロック**
    - 指定したプロバイダの構成に使用する
    - プロジェクト、リージョン、ゾーンなどを設定する。
    
    ```
    provider "google" {
    
      project = "qwiklabs-gcp-00-3a373e0573a4"
      region  = "us-east1"
      zone    = "us-east1-c"
    }
    ```
    
- **`resource`ブロック**：ネットワークやVMなど、管理するリソースを定義する。
    
    ```
    resource "google_compute_network" "vpc_network" {
      name = "terraform-network"
    }
    ```
    

## インフラの作成・変更・破棄

### リソースを作成する

- 構成ファイルにリソースを追加し、`terraform apply`を実行する。
    
    !terrfaform.png
    
    - `(known after apply)`は、作成後に確定する属性値を示す。
- 表示されたプランを確認し、`yes`を入力して適用する。
    - プランに正しくない内容や危険な内容が含まれていると思われる場合は、インフラストラクチャを変更せず、ここで中止するのが安全

### リソースを変更する

- 構成を書き換えると、希望する状態に到達するために必要な変更が計画される。
- 変更には、既存リソースを維持した更新と、破棄・再作成を伴う置き換えがある。

| プランの記号 | 意味 | ラボの例 |
| --- | --- | --- |
| `+` | 新規作成 | VPCやVMの追加 |
| `~` | 既存リソースをそのまま更新 | VMへのタグ追加 |
| `-/+` | 破棄して再作成 | VMのブートディスクイメージ変更 |
| `-` | 破棄 | VMやVPCの削除 |

### リソースを破棄する

```
terraform destroy
```

- 管理対象のインフラを破棄するプランが表示され、承認後に実行される。
- Terraformは依存関係から処理順序を判断する。
- 例：VMを破棄してから、そのVMが使用していたVPCを破棄する。
- 一部のリソースだけを削除する場合は、該当する`resource`ブロックを構成から削除し、`terraform apply`を実行する。

## リソースの依存関係

### 暗黙的な依存関係

- 他のリソースの属性を参照すると、Terraformが依存関係を自動的に認識する。
- 可能な限り、属性参照による依存関係を使用する。

静的IPを予約し、VMに割り当てる例：

```
resource "google_compute_address" "vm_static_ip" {
  name = "terraform-static-ip"
}
```

VMのネットワーク設定：

```
network_interface {
  network = google_compute_network.vpc_network.self_link

  access_config {
    nat_ip = google_compute_address.vm_static_ip.address
  }
}
```

- VMが静的IPの属性を参照しているため、Terraformは静的IPを先に作成してからVMへ反映する。

### 明示的な依存関係

- 属性参照では表れない依存関係は、`depends_on`で指定する。
- 例：VM内のアプリケーションがCloud Storageバケットを使用する場合。
    
    ```
    # New resource for the storage bucket our application will use.
    resource "google_storage_bucket" "example_bucket" {
      name     = "qwiklabs-gcp-00-3a373e0573a4"
      location = "US"
    
      website {
        main_page_suffix = "index.html"
        not_found_page   = "404.html"
      }
    }
    
    # Create a new instance that uses the bucket
    resource "google_compute_instance" "another_instance" {
      # Tells Terraform that this VM instance must be created only after the
      # storage bucket has been created.
      depends_on = [google_storage_bucket.example_bucket]
    
      name         = "terraform-instance-2"
      machine_type = "e2-micro"
    
      boot_disk {
        initialize_params {
          image = "cos-cloud/cos-stable"
        }
      }
    
      network_interface {
        network = google_compute_network.vpc_network.self_link
        access_config {
        }
      }
    }
    ```
    
- この指定により、バケット作成後にVMを作成する。
- 構成ファイル内でのリソースの記述順は、適用順序を決めない。

## 実行プランを保存する

```
terraform plan -out static_ip
terraform apply "static_ip"
```

- `terraform plan`は変更内容を表示し、実際のリソースは変更しない。
- プランを保存すると、確認したプランを指定して適用できる。

## プロビジョナー

- ファイルのアップロード、シェルコマンドの実行、他のソフトウェアの導入・起動などに使用する。
- インスタンスを事前構成する方法として、カスタムOSイメージやPackerも紹介されている。

### `local-exec`の例

```
provisioner "local-exec" {
  command = "echo ${self.name}: ${self.network_interface[0].access_config[0].nat_ip} >> ip_address.txt"
}
```

- `local-exec`は、Terraformを実行しているマシン上でコマンドを実行する。
- この例では、VM名と外部IPアドレスを`ip_address.txt`に追記する。
- `[0]`は、最初のネットワークインターフェースや`access_config`を参照する。

### 実行タイミングと失敗時の扱い

- ラボで使用する作成時プロビジョナーは、リソース作成時に実行される。
- 既存リソースにプロビジョナーを追加しただけでは、再作成や実行は行われない。
- ラボでは、次の操作でVMを再作成し、プロビジョナーを実行する。

```
terraform taint google_compute_instance.vm_instance
terraform apply
```

- `tainted`状態のリソースは存続するが、次回の適用で破棄・再作成の対象になる。
- 作成時のプロビジョニングに失敗した場合も、リソースが`tainted`として扱われ、再作成時に再試行される。
- 破棄時のみ実行するプロビジョナーも定義でき、クリーンアップやデータ抽出などに利用できる。