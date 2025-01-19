## リスコフの置換原則(LSP)

> S型のオブジェクトo1の各々に、対応するT型のオブジェクトo2が1つ存在し、Tを使って定義されたプログラムPに対してo2の代わりにo1を使ってもPの振る舞いが変わらない場合、SはTの派生型であると言える
> 

### 継承の使い方の指針

- Ex. GOOD Licenseクラス
    
    ```mermaid
    classDiagram
      direction LR
      class Billing {
      }
      class License {
        + calcFee()
      }
      Billing --> License
      class PersonalLicense {
    
      }
      class BusinessLicense {
    
      }
      PersonalLicense --|> License
      BusinessLicense --|> License
    
    ```
    
    - Billingアプリケーションは派生型に依存していないため、どちらの派生型もLicense型に置き換えて使用することができる
- Ex. BAD 正方形・長方形問題
    
    ```mermaid
    classDiagram
      direction LR
      class User {
      }
      class Rectangle {
        + setH()
        + setW()
      }
      class Square {
        + setSide()
      }
    
      User --> Rectangle
      Square --|> Rectangle
    ```
    ```
    
    - Square(正方形)は、Rectangle(長方形)の適切な派生型とは言えない。
        - Rctangleは幅と高さを独立して変更できるが、Squareは両方同時に変更する必要がある
        - Userが下記のようなコードで、…をSquareのインスタンスを作っていると、最後のアサーションは失敗する
            
            ```python
            Rectangle r = ...
            r.setW(5)
            r.setH(2)
            assert(r.area() == 10);
            ```
            

## リスコフの置換原則とアーキテクチャ

- LSPは継承の指針だけでなう、インターフェイスと実装に関するソフトウェア設計の原則になっている
- ユーザーは定義されたインターフェイスに依存し、そのインターフェイスが置換可能である必要がある
- Ex.  ダメな例
    - 様々なタクシー会社の中からタクシーを手配するシステム
        - ユーザーが運転手を選択した際に、運転手データベースから対象の運転手を呼び出すURIを取得する
        - この時各タクシー会社のURIは一律であり、置換可能である必要があるが、一部がこれに準拠しないと、別途対応が必要となり、複雑な仕組みを追加することとなる