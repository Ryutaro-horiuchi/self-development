## TypeScriptの関数宣言

```tsx
function range(min: number, max: number): number[] {
	...
}
```

### 返り値がない関数を作る

`void型`を使用する

- Ex.
    
    ```tsx
    function helloWorldTimes(n: number): void {
    	for(let i=0; i < n; i++) {
    		console.log("Hello World")
    	}
    }
    ```
    
- 早期リターンで戻り値がないときもvoid側を使用

## 関数式

- Ex.
    
    ```tsx
    type Human = {
      height: number;
      weight: number;
    };
    const calcBMI = function(human: Human): number {
      return human.weight / human.height ** 2;
    };
    ```
    
- 関数宣言との違いは巻き上げが発生しない

## アロー関数式

- Ex.
    
    ```tsx
    type Human = {
     ...
    };
    
    const calcBMI = ({height, weight}: Human): number => {
      return weight / height ** 2;
    };
    ```
    
- 省略形
    - 式が一つであれば、`{}`と`return`を省略できる
    
    ```tsx
    // 普通の書き方
    const calcBMI = ({height, weight}: Human): number => {
      return weight / height ** 2;
    };
    
    // 省略形
    const calcBMI = ({height, weight}: Human): number => weight / height ** 2;
    ```
    

## メソッド記法

```tsx
const obj = {
  // メソッド記法
  double(num: number): number {
    return num * 2;
  },
  // 通常の記法 + アロー関数
  double2: (num: number): number => num * 2,
};

console.log(obj.double(100));  // 200 と表示される
console.log(obj.double2(-50)); // -100 と表示される
```

## 可変長引数の宣言

- 関数が任意の数の引数を受け取れるようにする。
- …引数名: 型という構文
    
    ```tsx
    const sum = (base: number, ...args: number[]): number => {
     ...
    }
    ```
    

### 関数呼び出し時にスプレッド構文(rest)を使用する

```tsx
const sum = (...args: number[]): number => {
  ...
};

const nums = [1, 2, 3, 4, 5];

console.log(sum(...nums));
// console.log(sum(1,2,3,4,5));と同義
```

## デフォルト値を指定しないオプショナルな引数の宣言

- `引数名?: 型`という構文を使用する
- Ex
    
    ```tsx
    const toLowerOrUpper = (str: string, upper?: boolean): string => {
      ...
    }
    ```
    
    - オプショナルな引数が省略された場合はundefinedになる。よって、上記のupperの型はbooleanとundefinedのUnion型になる

  # 関数の型

TypeScriptでは関数も値であるため、関数を表す型がある。それが関数型である。

## 関数型の記法

- 構文
    - `(引数リスト) ⇒ 帰り値の型`
- Ex.
    
    ```tsx
    type F = (repeatNum: number) => string;
    
    const xRepeat: F = (num: number): string => "x".repeat(num);
    ```
    
    - 関数型には引数名が存在するが、これは型チェックには影響しない
        - 例でもrepeatNumとnumは一致しないが問題ない

## 返り値の型注釈は省略すべきか

- 返り値の型は明示する
    - メリット
        1. 反対に関数が長く戻り値を返すのに中身を読み込む場合はすぐに、渡す引数と戻り値の型がわかるためメリットが大きい
        2. 関数内部で返り値の型に対してがたチェックを働かせることができる
    - デメリット
        - 書く量が多くなる。特に短い場合は中身を見ればすぐにわかるため、メリットが小さい
- 明示する場合としない場合とでは、”真実の源”が変わってくる
    - 明示した場合はその型が絶対的な真実として見なされる
        - → 基本的に返り値の型を明示した方が、エラーの内容から瞬時に原因を突き止められるため有利であり、返り値の型を必ず書くという派閥もある
    - 明示しなかった場合は、返り値の型は型推論によって関数の中身が絶対的な真実として見なされる
    
    <aside>
    💡
    
     関数の返り値の型を明示するかどうかは”真実の源”がどこにあるかを考えながら決めると良い
    
    </aside>

## 引数の型注釈が省略可能な場合

- 返り値と違い引数の型を気軽に省略することはできないが、”逆方向の型推論”が働く場合に省略することができる
- 逆方向の型推論
    - 式の型が先にわかっている場合に、それを元に式の内部に対して推論が働くことを指す
    - Ex. 変数宣言の時に変数に型注釈がある
        
        ```tsx
        type F = (arg: number) => string;
        // この関数式は引数の型を書かなくてもOK
        const xRepeat: F = (num) => "x".repeat(num);
        ```
        
        F型の変数(xRepeat)に代入されるということは、関数式の変数numのがたはnumber型であると推論することができる
        
    - 他に、関数引数(filterメソッドなど)の場合など

## コールシグネチャによる関数型の表現

- オブジェクト型の中で使用できる構文
    - `(引数リスト): 返り値の型;`
    - → そのオブジェクト型には「関数である」という意味が付与される
- コールシグネチャを用いることで、「プロパティを持った関数」の型を表現することができる
- Ex.
    
    ```tsx
    type MyFunc = {
      isUsed?: boolean;
      (arg: number): void;
    };
    
    const double: MyFunc = (arg: number) => {
      console.log(arg * 2)
    };
    
    // doubleはisUsedプロパティを持つ
    double.isUsed = true;
    console.log(double.isUsed);
    // doubleは関数として呼び出せる
    double(1000);
    ```
    
    - isUsedプロパティを持つオブジェクトであると同時にnumber側を受け取る関数でもあるような値の型


## 関数型の部分型関係

[部分型関係](https://www.notion.so/2a193db0555480299d34e6b856201660?pvs=21) 

- Ex.
    - オブジェクトの部分型関係 (復習)
        
        ```tsx
        type HasName = { name: string };
        type HasNameAndAge = { name: string; age: number };
        
        // オブジェクトの部分型関係
        // HasNameAndAge の値は HasName の条件をすべて満たす。
        // よって HasNameAndAge の値は、HasName 型の変数に代入できる。
        const p: HasNameAndAge = { name: "Alice", age: 20 };
        const q: HasName = p; // ✅ OK
        ```
        
        - `HasNameAndAge`は`HasName`の部分型である
            - プロパティが多い方が部分型である
    - 関数型の部分型関係
        
        ```tsx
        type HasName = { name: string };
        type HasNameAndAge = { name: string; age: number };
        
        // 関数型
        type F1 = (arg: HasName) => void;
        type F2 = (arg: HasNameAndAge) => void;
        ```
        
        - **`F1(** HasName を受け取る関数**)` は `F2(**　HasNameAndAge **を受け取る関数)` の部分型** になる
            - → オブジェクトの型の関係と逆なのは、関数の引数型は反変（contravariant）だから
            - 引数が少ない方が部分型である

### 引数の数による部分型関係

ある関数型Fの引数リストの末尾に新たな引数を追加して関数型Gを作った場合、FはGの部分型となる

```tsx
type UnaryFunc = (arg: number) => number;
type BinaryFunc = (left: number, right: number) => number;

const double: UnaryFunc = arg => arg * 2;
const add: BinaryFunc = (left, right) => left + right;

// UnaryFuncをBinaryFuncとして扱うことができる
const bin: BinaryFunc = double;
// 20 が表示される
console.log(bin(10, 100));
```

# ジェネリックス

- 型引数を受け取る関数を作る機能のこと
    - [型引数を持つ型](https://www.notion.so/2a193db0555480c28a14f39480f8f494?pvs=21)

## 使い方

- 構文
    - 定義: 関数名<型引数リスト>(仮引数群)という構文を付け足す
    - 呼び出し: 関数<型引数群>(引数群)
- 「入力の値によって出力の値が決まる」ような時がジェネリックスの基本的なユースケース
- Ex.
    
    ```tsx
    function repeat<T>(element: T, length: number): T[] {
      const result: T[] = [];
      for (let i = 0; i < length; i++) {
        result.push(element);
      }
      return result;
    }
    
    // ["a", "a", "a", "a", "a"] が表示される
    console.log(repeat<string>("a", 5)); 
    // [123, 123, 123] が表示される
    console.log(repeat<number>(123, 3)); 
    ```
    
- Ex.2 関数の記法別
    
    ```tsx
    // function関数式
    const repeat = function<T>(element: T, length: number): T[] {
      ...
    }
    // アロー関数
    const repeat = <T>(element: T, length: number): T[] => {
      ...
    }
    // メソッド記法
    const utils = {
      repeat<T>(element: T, length: number): T[] {
    		...
      }
    }
    ```
    

## 関数の型引数は省略することができる

```tsx
function repeat<T>(element: T, length: number): T[] {
  ...
}

// 省略なし 
console.log(repeat<string>("a", 5)); 
// 省略。型推論
console.log(repeat("a", 5)); 
```

## 型引数を持つ関数型

関数定義時と同様、型を定義する際も`<型引数リスト>`を使用して型を定義できる

```tsx
type Func = <T>(arg: T, num: number) => T[];
```