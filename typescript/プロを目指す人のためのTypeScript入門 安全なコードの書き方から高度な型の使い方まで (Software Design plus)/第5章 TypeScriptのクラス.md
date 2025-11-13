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

  ### コンストラクタ引数でのプロパティ宣言(TypeScript特有)

- 修飾子を活用することで、コンストラクタ引数でプロパティ宣言ができ、簡略化できる
- Ex.
    - 簡略化前
        
        ```tsx
        class User {
        	name: string;
        	private age: number;
        
        	constructor(name: string, age: number) {
        		this.name = name;
        		this.age = age;
        	}
        }
        ```
        
    - 簡略化
        
        ```tsx
        class User {
        	constructor(public name: string, private age: number) {}
        ```
        
        - この宣言で、簡略化前の`this.name = name;`に相当する処理が自動的に行われる
        - コンストラクタの引数名は、引数名であると同時にプロパティ名として扱われる
        - 
- TypeScript特有の機能であるため、この構文を使わないタイプの人も多い

### クラス式でクラスを作成する

- 構文
    - `class {…}`
- Ex.
    
    ```tsx
    const User = class {
      name: string;
      age: number;
    
      constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
      }
    
      public isAdult(): boolean {
        return this.age >= 20;
      }
    };
    ```
    
- privateやprotectedなどの修飾子は使用できない

### JavaScriptのプライベートプロパティ

- `#プロパティ名`のように、先頭に#をつけるとprivateになる
    - ES2015以降
- privateとは違い、コンパイルの時のみのチェックではなく、ランタイム上でもprivateとして動作する

```tsx
class User {
	name: string;
	#age: number;

	constructor(name: string, age: number) {
		this.name = name;
		this.#age = age:
	}
	...
}

```

### 静的初期化ブロック

- クラス宣言の中にstatic { … }という構文で、クラス宣言の評価の最中に実行される処理を記述できる
- Ex.
    
    ```tsx
    class User {
      static adminUser: User;
      static {
        this.adminUser = new User();
        this.adminUser.#age = 9999;
      }
    
      #age: number = 0;
      getAge() {
        return this.#age;
      }
      setAge(age: number) {
        if (age < 0 || age > 150) {
          return;
        }
        this.#age = age;
      }
    }
    
    console.log(User.adminUser.getAge()); // 9999 と表示される
    ```

### 型引数を持つクラス

- クラスも型引数を持つことができる
- Ex.
    
    ```tsx
    class User<T> {
      name: string;
      #age: number;
      readonly data: T;
    
      constructor(name: string, age: number, data: T) {
        this.name = name;
        this.#age = age;
        this.data = data;
      }
    
      public isAdult(): boolean {
        return this.#age >= 20;
      }
    }
    
    // uhyoはUser<string>型
    const uhyo = new User<string>("uhyo", 26, "追加データ");
    // dataはstring型
    const data = uhyo.data;
    
    // johnはUser<{ num: number; }>型
    const john = new User("John Smith", 15, { num: 123 })
    // data2は{ num: number; }型
    const data2 = john.data;
    ```
    
    - 型引数は省略もできる。その時は引数の値から推論される

## クラスの型

- クラス宣言はクラスオブジェクトという値を作るものであると同時に、インスタンスの型を宣言するものである
- Ex.
    
    ```tsx
    class User {
    	name: string = "";
    	age: number = 0;
    
    	isAdult(): boolean {
    		return this.age >= 20;
    	}
    }
    
    // これはもちろんOK
    const uhyo: User = new User();
    // これもOK!
    const john: User = {
      name: "John Smith",
      age: 15,
      isAdult: () => true
    };
    
    ```
    
    - Userという型も生成されている
    - 例ではname, ageというプロパティとisAdultというメソッドを持っていれば、`new User();`という構文で作成されなくてもUser型として扱える

### newシグネチャによるインスタンス化可能性の表現

- 前提
    - クラスオブジェクトそのものの型はどんなものか
        - `class User {…}`と宣言したならば、変数Userが持つ型はどのように表現できるか
    - new (引数リスト) ⇒ インスタンスの型という記法で型を表現できる
    - Ex.
        
        ```tsx
        class User {
          name: string = "";
          age: number = 0;
        }
        
        type MyUserConstructor = new () => User;
        
        // UserはMyUserConstructor型を持つ
        const MyUser: MyUserConstructor = User;
        // MyUserはnewで使用可能
        const u = new MyUser();
        // uはUser型を持つ
        console.log(u.name, u.age);
        ```
        
- 本題: newシグネチャ
    - コールシグネチャの亜種
        - [コールシグネチャによる関数型の表現](https://www.notion.so/2a593db0555480528217e55c14f58dab?pvs=21)
    - newで呼び出せると同時に、それ自身もプロパティやメソッドを持つというオブジェクトを表現したい場合に使用できる
    - Ex.
        
        ```tsx
        type MyUserConstructor = {
          new (): User;
        };
        ```