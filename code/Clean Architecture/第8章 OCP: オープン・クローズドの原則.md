# 概要

- 「ソフトウェアの構成要素は拡張に対しては開かれていて、修正に対して閉じていなければならない」
    
    → ソフトウェアの振る舞いは、既存の成果物を変更せず拡張できるようにすべきである。
    
- ちょっとした拡張のために大量の書き換えが必要になるようなら、そのソフトウェアシステムのアーキテクトは大失敗への道を進んでいることになる
- OCPはクラスやモジュールを設計する際の指針となる原則だが、コンポーネントのレベルを考慮した時に、この原則はさらに重要なものとなる

# コンポーネントレベルのOCP

## Ex. 財務情報をWebページに表示するシステム

- 前提
    - ステークホルダーから、画面に出ている内容と同じものを印刷したいという要望が出たとする
    - レポートの作成は2つの異なる責務を負っている
        - 出力するデータの計算
        - web(印刷)向けの表示形式の作成

<aside>
💡

2つの異なる責務を分離するには、ソースコードの依存関係を調整し、一方に影響を与えることなく変更できるようにする必要がある

</aside>

### 処理をクラスに分割し、クラスをコンポーネントにまとめる

- マークの説明
    - <I>・・・インターフェイス
    - <DS>・・・データ構造
    - 通常の矢印・・・使用の関係
    - 白抜きの矢印・・・実装や継承の関係
    - 二重線・・・コンポーネント

![IMG_3640.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/b6bb89fd-0af6-48b1-b00b-135df3b15cbf/IMG_3640.jpeg)

- クラスAのコードからクラスBを知っているが、クラスBはクラスAのことを一切知らない。
    - FinancialDataMapper
        - 実装の関係によって、FinancialDataGatewayのことを知っているが、FinancialDataGatewayはFinancialDataMapperのことを一切知らない
- コンポーネントAがコンポーネントBの変更から保護されるべきならば、コンポーネントBからコンポーネントAに依存すべきである
    - クラスレベルだけでなく、コンポーネントレベル(二重線で囲まれた枠を超える線)も、すべて一方通行になっている
        - コンポーネント
            
            ![IMG_3641.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/d88133d9-51cd-43e5-816e-03b8aad45b9e/IMG_3641.jpeg)
            
            - Ex.
                - Presenterを変更した時に、Controllerを変更する必要をなくしたい
                - Viewを変更した時に、Presenterを変更する必要をなくしたい
                - 他の全てを変更した時にInteractorを変更する必要をなくしたい
            - Interactorはビジネスルールを含んでおり、アプリケーションの最上位レベルの方針を含んでいる。そのほかは周辺にある関心ごとである。
                - Controllerは、PresenterやViewに対して中心的な位置付けになる
            - 保護の階層ができている
                - Interactorは最上位レベルの概念なので、最も保護されるが、Viewは最下位レベルの概念なので、保護レベルは最も低くなる
                - 上位レベルにあるコンポーネントは、下位レベルのコンポーネントが変更されたとしても、変更する必要がない

### 情報の隠蔽

- FinancialReportRequesterインターフェイスの役割は、FinancialReportControllerがInteractorの内部を知りすぎないように保護すること
    - Controllerへの変更がInteractorに影響を及ぼさないようにすることを最優先としつつも、ControllerもまたInteractorの変更から保護しておきたい。そのために、Interactorの内部を隠蔽している
    - コード例
        - インターフェイス
            
            ```python
            from abc import ABC, abstractmethod
            
            class FinancialReportRequester(ABC):
                @abstractmethod
                def request_report(self, report_id: str) -> str:
                    pass
            ```
            
        - Interactor
            
            ```python
            class FinancialReportInteractor(FinancialReportRequester):
                def request_report(self, report_id: str) -> str:
                    # ビジネスロジックの詳細
                    return f"Financial Report for ID: {report_id}"
            ```
            
        - Controller(Interactorを利用するクラス)
            
            ```python
            class FinancialReportController:
                def __init__(self, requester: FinancialReportRequester):
                    self.requester = requester
            
                def get_report(self, report_id: str) -> str:
                    # Interactorの詳細を知らなくても、インターフェイスを通じてアクセス可能
                    return self.requester.request_report(report_id)
            
            ```
            
        - 使用例
            
            ```python
            interactor = FinancialReportInteractor()
            controller = FinancialReportController(interactor)
            
            # ControllerからInteractorを利用
            print(controller.get_report("12345"))
            ```