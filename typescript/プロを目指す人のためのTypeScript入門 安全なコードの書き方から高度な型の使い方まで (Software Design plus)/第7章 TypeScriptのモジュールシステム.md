# import宣言とexport宣言

## TypeScriptのimport

- 実際のソースファイルの拡張子は.tsだが、import宣言を使用する場合は.jsと書く

### インポート要点

- インポートした側のモジュールよりも、インポートされた側のモジュールの方が先に実行される
- import宣言がどこに書かれているかは実行の順番に関係ない。ファイルの先頭に書くのが慣習
    
    ```tsx
    console.log("uhyoの名前は${name}で年齢は${age}です")
    
    import { name, age } from "./uhyo.js"
    ```
    
    次のように書いてもuho.tsがconsole.logよりも先に実行される。
    
- モジュールの実体は1つ
    - 複数のファイルから同一のファイルAをインポートされていたとしても、Aが実行されるのは1回のみ
    - どのモジュールも実態は1つだけで、何度読み込まれても1回しか実行されず、全ての読み込み元には同じものが見えることになる

## 型のインポート・エクスポート

### エクスポート

1. export type 構文
    
    ```tsx
    export type Animal = {
      species: string;
      age: number;
    }
    ```
    
2. export {} 構文
    
    ```tsx
    type Animal = {
      species: string;
      age: number;
    };
    
    const tama: Animal = {
      species: "Felis silvestris catus",
      age: 1
    };
    
    export { Animal, tama };
    ```
    

### インポート

- 従来と同様の形でインポートできる
    
    ```tsx
    import { Animal, tama } from "./animal.js";
    
    const dog: Animal = {
      species: "Canis lupus familiaris",
      age: 2
    };
    
    console.log(dog, tama);
    ```
    

### export type {} と import type{}

- エクスポート(インポート)されたものは型として使用可能になる
- Ex. export type
    
    ```tsx
    type Animal = {
      species: string;
      age: number;
    };
    
    const tama: Animal = {
      species: "Felis silvestris catus",
      age: 1
    };
    // これはOK!
    export type { Animal, tama };
    ```
    
    - export typeされたものは、値として使うことが不可能になり、型としてのみ使える。
        - typeofキーワードと使うことが多い
- Ex. import type
    
    ```tsx
    import type { Animal, tama } from "./animal.js";
    
    // type構文を使用して変数と型を一度にインポートしたいとき
    // import { tama, type Animal } from "./animal.js";
    
    // エラー: 'tama' cannot be used as a value because it was imported using 'import type'.
    const myCat: Animal = { ...tama };
    
    // こちらはOK
    const otherCat: typeof tama = {
      species: "Felis silvestris catus",
      age: 20
    };
    ```
    

## 一括インポート

```tsx
uhyo.ts
export const name = "uhyo";
export const age = 26;

index.ts
import * as uhyo from "./uhyo.js";

console.log(uhyo.name); // "uhyo" と表示される
console.log(uhyo.age);  // 26 と表示される
```

- 型システム的には、uhyoは、`{name: “uhyo”; age: 26; }`型になる
- uhyo.tsにdefaultがあった場合は、defaultとしてアクセスできる

## スクリプトとモジュール

- TS, JSのファイルはスクリプトとモジュールの2種類に分類される
    - HTMLからJavaScriptを読み込んで実行する際は、script要素で`type="module"`という属性で読み込まれたものがモジュールとして扱われ、そうでないものはスクリプトとして扱われる
        - `type=”module”`を伴わずに読み込まれたファイルの中でimport, exportが使われていた場合は構文エラーになる
    - Node.jsの場合、package.jsonの”type”フィールドに”module”設定されているかどうかで決まる
- TypeScriptでは、プログラム中にimportやexportが含まれるものは自動的にモジュールとして扱われ、そうでないものはスクリプトとして扱われる

<aside>
⚠️

スクリプトでは、トップレベルに定義された変数や型のスコープがファイルの中だけではなく、プロジェクト全体に広がる点に注意

</aside>

# Node.jsのモジュールシステム

## Node.jsの組み込みモジュール

- Node.jsに最初から備わっているモジュールのこと。
- Ex. readline
    
    ```tsx
    import { createInterface } from "readline";
    ```
    
    - `from "readline";`
        - ./や、../などから始まらずいきなりモジュール名が書かれているものは、外部モジュールであるとみなされる
            - 外部モジュールは、「組み込みモジュール」と「npmでインストールされたモジュール」の2つに分類できる

## DefinitelyTypedと@types

### 前提

- npmで配布されているモジュールにはTypeScript向けの型定義が同梱されているものとそうでないものがあり、後者をTypeScriptから利用するためにサポートが必要。
- サポートするために運用されているのが`DefinitelyTyped`と`@types`パッケージ

### 型定義が同梱されていない時のエラー例

- express
    
    ```tsx
    Could not find adeclaration file for module 'express'.
    // expressの型定義ファイルが見当たらないというエラー
    ```
    

### 対応

@typesパッケージをインストールするのが1つの解決法

- 手順は`npm install -D @types/express`を実行して`@types/express`をインストール
    
    → expressモジュールの内容をTypeScriptが認識したことを意味している
    
- 上記のようにライブラリに型定義がない場合は@typesパッケージをインストールすることで型定義を補う
- 自分で型定義ファイルを作ることもできる
    - .d.tsという拡張子ファイルはTypeScriptコンパイラから型定義ファイルとして扱われる。実装は含まない
    - Ex.
        
        ```tsx
        declare module "express" {
        	const result: number;
        	export default result;
        }
        ```
        
        - declare moduleブロックにexport宣言を書くことで、そのモジュールから何がエクスポートされているかを明示できる

### DefinitelyTyped

- @typesパッケージの開発・運用はMicrosoftが運営するDefinitelyTypedというシステムに集約されている
- 実際に@typesパッケージの中身を作るのはコミュニティの有志