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