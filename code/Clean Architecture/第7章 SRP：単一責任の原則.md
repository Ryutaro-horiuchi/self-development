単一責任の原則は「どのモジュールもたった一つのことを行うべき」**ではない**

→ こういった原則はあるが、最下位のレベルのものに対して用いるものであり、SOLID原則の単一責任の原則(SRP)とは異なる

かつてSRPは以下のように語られてきた

```
モジュールを変更する理由はたったひとつだけであるべきである
```

ソフトウェアシステムに手を加えるのはユーザーやステークホルダーを満足させるため

→ ユーザーやステークホルダーこそが、SRPの指す「偏光する理由」である。つまり、以下のように言い換えられる

```
モジュールはたったひとりのユーザーやステークホルダーに対して責務を負うべきである
```

「たったひとりのユーザーやステークホルダーに対して」という表現は適切ではない。現実には複数のユーザーやステークホルダーがシステムを同じように変更したいと考えることもある。

変更を望む人たちを一つのグループとして「アクター」と呼ぶことにすると、SRPは以下のようになる

<aside>
💡

モジュールはたった一つのアクターに対して責務を負うべきである

</aside>

# 症例1: 想定外の重複

---

## 前提

給与システムにおけるEmployeeクラスがある

```mermaid
classDiagram
  direction TB
  class Employee {
    +calculatePay()
    +reportHours()
    +save()
  }
```

- メソッド
    - calculatePay()
        - 経理部門が規定する。報告先はCFO
    - reportHours()
        - 人事部門が規定する。報告先はCOO
    - save()
        - データベース管理者が規定する。報告先はCTO
- 上記メソッドを一つのEmployeeクラスに入れると、開発者はすべてのアクターを結合することになる。

## 本題

### 重複をなくした

calculatePay, reportHoursメソッド両方で、所定労働時間を算出していたとする

- 計算アルゴリズムが同じだったので開発者はコードの重複を嫌い、この部分をregularHoursメソッドに切り出した

```mermaid
flowchart TB
  node_1["calculatePay"]
  node_2["regularHours"]
  node_3["reportHours"]
  node_1 --> node_2
  node_3 --> node_2
```

### CFOチーム側で改修の必要が出てきた

その後、CFOチームが所定労働時間の算出方法に手を加える必要が出てきた

- 担当者はcalculatePayが、regularHoursを呼び出しているのを確認し、regularHoursを改修した。(regularHoursが、reportHoursからも呼ばれていることは確認できなかった)

### 問題の発覚

COOチームはCFOチーム側の改修を知ることなく、regularHoursから上がってきた数字を活用していた。やがて問題が発覚し、何百万ドルの損害でた

## 問題の原因

- 別々のアクター(CFOチーム、COOチーム)を一つにまとめてしまったこと
    
    <aside>
    💡
    
    SRPはアクターの異なるコードは分割すべきだという原則である
    
    </aside>
    

# 症例2: マージ

現状だとEmployeeクラスのスキーマを各チームが変更したい場合、変更が衝突することになる。

複数の人たちがそれぞれ別の理由で同じソースファイルを変更することに原因がある

# 解決策

様々な解決策があるが、いずれも関数を別のクラスに移動することは共通している

```mermaid
classDiagram
  direction LR
  class PayCalculator {
    + calculatePay()
  }
  class HourReporter {
    + reportHours()
  }
  class EmployeeSaver {
    + saveEmployee()
  }
  class EmployeeData{
  }
  PayCalculator --> EmployeeData
  HourReporter --> EmployeeData
  EmployeeSaver --> EmployeeData

```

Facadeパターン

```mermaid
classDiagram
  direction LR
  class EmployeeFacade {
    + calculatePay()
    + reportHours()
    + save()
  }
  class PayCalculator {
    + calculatePay()
  }
  class HourReporter {
    + reportHours()
  }
  class EmployeeSaver {
    + saveEmployee()
  }
  EmployeeFacade --> PayCalculator
  EmployeeFacade --> HourReporter
  EmployeeFacade --> EmployeeSaver 

  class EmployeeData　{
  }
  PayCalculator --> EmployeeData
  HourReporter --> EmployeeData
  EmployeeSaver --> EmployeeData
```