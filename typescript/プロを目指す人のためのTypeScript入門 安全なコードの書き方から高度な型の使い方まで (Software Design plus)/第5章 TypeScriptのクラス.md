## TypeScriptのクラス宣言

### プロパティの宣言

```tsx
class User {
	name: string = "";
	age: number = 0
	readonly address: string = "" // 読み取り専用プロパティ
	gender?: number; // オプショナルなプロパティ
	
}
```

- コンストラクタを定義していないため、オプショナルなプロパティをのぞき型に沿った初期値が必要

### コンストラクタ

```tsx
class User {
	name: string;
	age: number;

	constructor(name: string, age: number) {
		this.name = name;
		this.age = age;
	}
	
	...
}

const uhyo = new User("uhyo", 26)
```

- コンストラクタを宣言しているので、nameとageには初期値が不要

### 静的プロパティ・静的メソッド

- プロパティ、メソッドに`static`をつけることで定義できる
    - 静的プロパティ・静的メソッド: クラスそのものに属するプロパティやメソッド
    - Ex.
        
        ```tsx
        class User {
        	static adminName: string = "uhyo";
        	static getAdminUser() {
        		return new User(User.adminName, 26);
        	}
        }
        ```
        
- 静的プロパティ・静的メソッドはインスタンスからは呼び出せない

### 3種のアクセシビリティ修飾子

- プロパティ、メソッドには`public`, `protected`, `private`の3種類の修飾子をつけられる
- `public`は何も修飾子をつけない時と同じ動作
- `private`はクラスの内部からのみアクセスできる
- `protected`はクラスの内部およびそのクラスを継承するクラスからもアクセスできる
- Ex.
    
    ```tsx
    class User {
      name: string;
      private age: number;
    
      constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
      }
    
      public isAdult(): boolean {
        return this.age >= 20;
      }
    }
    
    const uhyo = new User("uhyo", 26);
    console.log(uhyo.name);      // "uhyo" が表示される
    console.log(uhyo.isAdult()); // true が表示される
    console.log(uhyo.age); // エラー: Property 'age' is private and only accessible within class 'User'.
    ```