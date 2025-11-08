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