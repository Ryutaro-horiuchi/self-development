### 依存関係逆転の原則(DIP)

- ソースコードの依存関係が具象ではなく、抽象だけを参照しているもの。それが最も柔軟なシステムである
- DIPを考える時は、OSやプラットフォーム周りの具象モジュールに依存することは許容とする。
    - Ex. JavaのStringクラス等
        - 具象ではあるが、他のクラスと比べて非常に安定しており、変更されることはほとんどなく、あったとしてもきちんとコントロールされている
- 依存したくないのは、開発中のモジュールなど、変化しやすい具象要素

## 安定した抽象

- 抽象インターフェイスの変更は、それに対する具象実装の変更につながる。
- 一方、具象実装を変更しても、インターフェイスの変更が必要にはならない。

<aside>
💡

インターフェイスは実装よりも、変化しにくい

</aside>

- 優れたソフトウェアアーキテクトは、インタフェイスの変動性をできるだけ抑えようとし、新しい機能を実装するときも、できる限りインターフェイスの変更なしで済ませられるようにする

### 安定したソフトウェアアーキテクチャは、変化しやすい具象への依存を避け、安定した抽象インターフェイスに依存するべきである

- プラクティス
    - 変化しやすい具象を参照しない
        - 代わりに抽象インターフェイスを参照すること。一般的には、**Abstarct Factoryパターン**を使うことになる
    - 変化しやすい具象クラスを継承しない
        - 継承は一種の依存である
    - 具象関数をオーバーライドしない
    - 変化しやすい具象を名指しで参照しない
    

## **Abstarct** Factory

- プラクティスに従おうとすると、具象オブジェクトを生成する際に、特別な処理が必要になる。
    - 具象オブジェクトを生成する際には、そのクラス名や生成方法を明示的に記述する必要があるため、ソースコードがその具象定義に依存する形となる。これを完全に避けることはできないため
    - オブジェクト指向言語では、Abstract Factoryパターンを使って望まざる依存性を管理する
- Abstract Factoryパターン クラス図
    
    ![IMG_3657.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/2a4c91e1-6fe9-4b48-b594-42a9394d5556/IMG_3657.jpeg)
    
    - クラスの説明
        - **Application**
            - `Service Factory`を通じて必要な`Service`を取得する
        - **Service Factory（インターフェース）**:
            - `makeSvc`メソッドを定義する抽象的なファクトリー。
            - `Application`はこのインターフェースに依存し、具体的な実装には直接依存しない
        - **Service Factory Impl（実装クラス）**:
            - `Service Factory`の実装クラス。
            - `makeSvc`を実際に実装し、具体的な`Service`インスタンス（`Concrete Impl`）を生成します。
        - **Service（インターフェース）**:
            - サービスのインターフェース。
            - `Application`はこのインターフェースを通じて、具体的なサービスの機能を使用します。
    - 処理の流れ
        1. `Application`は`Service Factory`インターフェースに依存し、`makeSvc`メソッドを呼び出します。
        2. `Service Factory Impl`が`Service Factory`を実装し、`makeSvc`を通じて具体的な`Service`インスタンス（`Concrete Impl`）を生成します。
        3. `Application`は`Service`インターフェースを通じてサービスを利用します。
    - 結果どうなったのか
        - **依存性の分離**: `Application`は具体的なサービスの実装（`Concrete Impl`）に直接依存せず、抽象インターフェース（`Service`や`Service Factory`）を通じて操作します。
        - **柔軟性の向上**: 新しいサービス実装が追加されても、`Application`のコードを変更する必要がなく、`Service Factory`の実装を差し替えるだけで対応できます。
        - **モジュール化**: 依存関係が明確に分離され、コードの可読性と保守性が向上します。
    - 曲線は抽象と具象の区切り。
        - 曲線を横切るソースコードの依存性は、全て具象側から抽象側へと向かっている
        - 曲線を横切る処理の流れは、ソースコードの依存性と逆向きになる。だからこそ「依存関係逆転の法則」と名付けられた
- Abstract Factoryパターン コード例
    
    ```python
    from abc import ABC, abstractmethod
    
    # 1. Service インターフェース
    class DatabaseService(ABC):
        @abstractmethod
        def connect(self):
            pass
    
    # 2. Concrete Impl（具体的な実装クラス）
    class MySQLDatabaseService(DatabaseService):
        def connect(self):
            return "Connected to MySQL Database"
    
    class PostgreSQLDatabaseService(DatabaseService):
        def connect(self):
            return "Connected to PostgreSQL Database"
    
    # 3. Service Factory インターフェース
    class DatabaseServiceFactory(ABC):
        @abstractmethod
        def make_service(self) -> DatabaseService:
            pass
    
    # 4. Service Factory Impl（具体的なファクトリー実装クラス）
    class MySQLDatabaseServiceFactory(DatabaseServiceFactory):
        def make_service(self) -> DatabaseService:
            return MySQLDatabaseService()
    
    class PostgreSQLDatabaseServiceFactory(DatabaseServiceFactory):
        def make_service(self) -> DatabaseService:
            return PostgreSQLDatabaseService()
    
    # 5. Application（クライアントコード）
    class Application:
        def __init__(self, factory: DatabaseServiceFactory):
            self.factory = factory
    
        def run(self):
            # Factoryを使ってServiceを生成し、利用する
            service = self.factory.make_service()
            print(service.connect())
    
    # 6. 実行例
    if __name__ == "__main__":
        # MySQLを使用する場合
        mysql_factory = MySQLDatabaseServiceFactory()
        app_mysql = Application(mysql_factory)
        app_mysql.run()
    
        # PostgreSQLを使用する場合
        postgres_factory = PostgreSQLDatabaseServiceFactory()
        app_postgres = Application(postgres_factory)
        app_postgres.run()
    ```