## MPAとSPAの違い

- MPA
    - 複数のHTMLページとHTTPリクエストで構築される従来のアプリケーション
- SPA
    - 単一のHTMLページ上で、Ajaxを使用して動的にページを書き換えるアプリケーション

## 必要なライブラリ

### UIコンポーネントのテスト環境準備 DOM API(jsdom)

- 表示されたUIを操作するためにDOM APIが必要になる
- Jest環境のNode.jsには、標準でDOM APIが用意されていないため、`jsdom`を使用してテスト環境をセットアップする
    
    ```tsx
    unittest/jest.config.ts
    
    export default {
      ...
      testEnvironment: "jest-environment-jsdom",
    }
    ```
    

### Testing Library

- 「テストがソフトウェアの使用方法に似ている」ことを推奨している
    - クリック、マウスオーバー、キーボード入力など
- React環境のTesting Library
    - @testing-library/react
        - 中核となるAPIは、どのUIフレームワークも同一のもの(@testing-library/dom)を使用している
    - Vueにも、`'@testing-library/vue'`があるっぽい？
        - [参考記事](https://devblog.thebase.in/entry/vue2-testing-library)

### UIコンポーネント用のマッチャー

- DOMの状態の検証をサポートする`@testing-library/jest-dom`をインストール

### ユーザー操作をシミュレートするライブラリ

- 実際のユーザー操作により近いシミューレトを行うことができる`@testing-library/user-event`を追加する

## UIコンポーネントテスト

- テスト対象コンポーネント
    
    ```tsx
    Form.tsx
    
    type Props = {
      name: string;
      onSubmit?: (event: React.FormEvent<HTMLFormElement>) => void;
    };
    export const Form = ({ name, onSubmit }: Props) => {
      return (
        <form
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit?.(event);
          }}
        >
          <h2>アカウント情報</h2>
          <p>{name}</p>
          <div>
            <button>編集する</button>
          </div>
        </form>
      );
    };
    ```
    

### 基本

- Testing Libraryのrender関数を使用して、テスト対象のUIコンポーネントをレンダリングする
- レンダリングした内容から特定DOM要素を取得するために、`screen.getByText`を使用する
- `@testing-library/jest-dom`で拡張したカスタムマッチャーを使用する(toBeInTheDocument)
- テスト
    
    ```tsx
    import { render, screen } from "@testing-library/react";
    import { Form } from "./Form";
    
    test("名前の表示", () => {
      render(<Form name="taro" />);
      expect(screen.getByText("taro")).toBeInTheDocument();
    });
    ```
    

### 要素の取得

- 特定のDOM要素をロールで取得する
    - Testing Libraryには、特定のDOM要素を取得する`screen.getByRole`がある
    - buttonタグは暗黙的に`role=”button”`が付与されているため、次のテストは成功する
        
        ```tsx
        test("ボタンの表示", () => {
          render(<Form name="taro" />);
          expect(screen.**getByRole("button")**).toBeInTheDocument();
        });
        ```
        
- h1, h2などの見出しタグを使用している場合は、`getByRole(”heading”)`で取得することができる
- テスト `getByRole(”heading”)` で要素を取得しテキストを検証する
    
    ```tsx
    test("見出しの表示", () => {
      render(<Form name="taro" />);
      expect(screen.getByRole("heading")).toHaveTextContent("アカウント情報");
    });
    ```
    

### イベントハンドラーのテスト

- イベントをPropsで指定するコンポーネントのテストは、第4章の時と同様、モック関数を利用して検証する
- テスト
    
    ```tsx
    test("ボタンを押下すると、イベントハンドラーが呼ばれる", () => {
      const mockFn = jest.fn();
      render(<Form name="taro" onSubmit={mockFn} />);
      fireEvent.click(screen.getByRole("button"));
      expect(mockFn).toHaveBeenCalled();
    });
    ```
    

## ケース別

### 一覧表示のテスト

一覧表示(ul)が表示されているかの検証

- ul要素は暗黙のロールとしてlistを持つため、getByroleを使用して以下のように書く
    
    ```tsx
    test("items の数だけ一覧表示される", () => {
      render(<ArticleList items={items} />);
      **const list = screen.getByRole("list");
      expect(list).toBeInTheDocument();**
    });
    ```
    

### within関数で対象を絞り込む

- ページ全体(screen)でロールを使用して対象DOMを取得しようとすると、大きいコンポーネントでは対象外のDOMも取得されてしまうことがある
    
    → within関数を使用して、対象を絞り込んで要素を取得する
    
    ```tsx
    test("items の数だけ一覧表示される", () => {
      ...
    	**const list = screen.getByRole("list");**
      **expect(within(list).getAllByRole("listitem")).toHaveLength(3);**
    });
    ```
    
    - listitemは、liタグの暗黙のロール

### 要素を持たなかった時のテスト

- getByRoleや、getByLabelTextは存在しない要素を取得しようとしたときは、エラーが起こる
- 存在しないことを確認したいときは、queryBy接頭辞を持つAPIを使用する
    
    ```tsx
    test("一覧アイテムが空のとき「投稿記事がありません」が表示される", () => {
      render(<ArticleList items={[]} />);
      **const list = screen.queryByRole("list");**
      expect(list).not.toBeInTheDocument();
      expect(list).toBeNull();
      expect(screen.getByText("投稿記事がありません")).toBeInTheDocument();
    });
    ```
    

### 属性のテスト

- toHaveAttributeを使用する
    
    ```tsx
    const item: ItemProps = {
      id: "howto-testing-with-typescript",
      title: "TypeScript を使ったテストの書き方",
      body: "テストを書く時、TypeScript を使うことで、テストの保守性が向上します…",
    };
    
    test("ID に紐づいたリンクが表示される", () => {
      render(<ArticleListItem {...item} />);
      expect(screen.getByRole("link", { name: "もっと見る" }))**.toHaveAttribute**(
        "href",
        "/articles/howto-testing-with-typescript"
      );
    });
    ```
    

### userEventで文字を入力する

- @testing-library/user-eventを使用する
    - userEvent.setup()で、APIを呼び出すuserインスタンスを作成する
    - user.type関数で入力を表現する。非同期処理のため、awaitを用いる
- Ex.
    
    ```tsx
    import { render, screen } from "@testing-library/react";
    import userEvent from "@testing-library/user-event";
    import { InputAccount } from "./InputAccount";
    
    **const user = userEvent.setup();**
    
    test("メールアドレス入力欄", async () => {
      render(<InputAccount />);
      const textbox = screen.getByRole("textbox", { name: "メールアドレス" });
      const value = "taro.tanaka@example.com";
      **await user.type(textbox, value);**
      expect(screen.getByDisplayValue(value)).toBeInTheDocument();
    });
    ```
    

### パスワードを入力する

- `input type="password"`は、暗黙的なrole属性を持たないため、getByRoleで取得することができない
    - HTML要素者は与えられた属性によって、暗黙のロールが変化する
- 代わりにgetByPlaceholderTextでパスワード欄を特定する
    
    ```tsx
    test("パスワード入力欄", async () => {
      render(<InputAccount />);
      **expect(() => screen.getByPlaceholderText("8文字以上で入力")).not.toThrow();
      expect(() => screen.getByRole("textbox", { name: "パスワード" })).toThrow();**
    });
    ```
    

### ボタンの活性、非活性のテスト

- `toBeEnabled();`, `toBeDisabled()`を使用する
    
    ```tsx
    test("「サインアップ」ボタンは非活性", () => {
      render(<Form />);
      expect(screen.getByRole("button", { name: "サインアップ" })).toBeDisabled();
    });
    
    test("「利用規約の同意」チェックボックスを押下すると「サインアップ」ボタンは活性化", async () => {
      render(<Form />);
      await user.click(screen.getByRole("checkbox"));
      expect(screen.getByRole("button", { name: "サインアップ" })).toBeEnabled();
    });
    ```
    

### formにアクセシブルネームを使用して、formロールで取得できるようにする

- form要素単独だと、formロールが付与されず取得することはできない
- aria-labelledby属性に見出しのidを付与することで、ロールで取得できるようになる
    
    ```tsx
    <form aria-labelledby={headingId}>
          <h2 id={headingId}>新規アカウント登録</h2>
    			...
    </form>
    ```
    

### 反復するユーザーインタラクションは関数化させる

- フォーム入力などのテストは、同じインタラクションを何度も書く必要が出てくる
    - 何度も繰り返されるテストは、関数にまとめておくと良い
- Ex.
    
    ```tsx
    async function inputDeliveryAddress(
      inputValues = {
        postalCode: "167-0051",
        prefectures: "東京都",
        municipalities: "杉並区荻窪1",
        streetNumber: "00-00",
      }
    ) {
      await user.type(
        screen.getByRole("textbox", { name: "郵便番号" }),
        inputValues.postalCode
      );
      await user.type(
        screen.getByRole("textbox", { name: "都道府県" }),
        inputValues.prefectures
      );
      await user.type(
        screen.getByRole("textbox", { name: "市区町村" }),
        inputValues.municipalities
      );
      await user.type(
        screen.getByRole("textbox", { name: "番地番号" }),
        inputValues.streetNumber
      );
      return inputValues;
    }
    ```
    

### スパイを使用してイベントを検証する

```tsx

// スパイ
function mockHandleSubmit() {
  const mockFn = jest.fn();
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data: { [k: string]: unknown } = {};
    formData.forEach((value, key) => (data[key] = value));
    mockFn(data);
  };
  return [mockFn, onSubmit] as const;
}

...
test("入力・送信すると、入力内容が送信される", async () => {
    const [mockFn, onSubmit] = mockHandleSubmit();
    **render(<Form onSubmit={onSubmit} />);**
    const contactNumber = await inputContactNumber();
    const deliveryAddress = await inputDeliveryAddress();
    await clickSubmit();
    expect(mockFn).toHaveBeenCalledWith(
      expect.objectContaining({ ...contactNumber, ...deliveryAddress })
    );
  });
```

### 非同期処理を含むUIコンポーネントテスト

- [WebAPIのモック](https://www.notion.so/WebAPI-b64f672534bf4aaeaef13bb59dbc96aa?pvs=21) を使用して、WebAPIクライアントのモック関数を用意する

```tsx
function mockPostMyAddress(status = 201) {
  if (status > 299) {
    return jest
      .spyOn(Fetchers, "postMyAddress")
      .mockRejectedValueOnce(httpError);
  }
  return jest
    .spyOn(Fetchers, "postMyAddress")
    .mockResolvedValueOnce(postMyAddressMock);
}

test("成功時「登録しました」が表示される", async () => {
  const mockFn = mockPostMyAddress();
  render(<RegisterAddress />); 

	// formを入力して「送信」ボタンを押すインタラクションをまとめた関数
	// 戻り値は入力した値のオブジェクト
  const submitValues = await fillValuesAndSubmit();

  expect(mockFn).toHaveBeenCalledWith(expect.objectContaining(submitValues));
  expect(screen.getByText("登録しました")).toBeInTheDocument();
});
```

## AAAパターンを意識して、可読性を上げる

- 「準備、実行、検証」の3ステップにまとめられたテストコードを、Arrange-Act-Assert(AAA)パターンと呼ばれる
- 

## スナップショットテスト

### 基本

- UIコンポーネントのスナップショットテストを実行すると、ある時点のレンダリング結果をHTML文字列として外部ファイルに保存することができる
- 対象としたいUIコンポーネントのテストファイルで、次のようにtoMatchSnapshotを含んだアサーションを実行する
    - テストファイルと同階層に__snapshots__が作成され、対象テストファイルと同名称の.snapファイルが出力される
        
        → .git管理対象としてコミットする
        
    
    ```tsx
    test("Snapshot: アカウント名「taro」が表示される", () => {
      const { container } = render(<Form name="taro" />);
      expect(container).toMatchSnapshot();
    });
    ```
    
- 2回目以降の実行では、コミット済みの.snapファイルと現時点でのスナップショットを比較して差分があると失敗するようになる

### 更新する

- 改修により表示内容を変更した場合、コミット済みのスナップショットを更新する
    
    ```bash
    $ npx jest —updateSnapshot
    # npx jest -u でも可
    ```
    

## ロールとWRI-ARIA

- role属性はWeb技術標準化を定めているW3Cの「WRI-ARIA」の仕様の1つ
- 「WRI-ARIA」は、マークアップだけでは不足している情報を補助したり、意図した通りの意味を伝えることができる
    
    → 「WRI-ARIA」由来のテストを書くことで、スクリーンリーダーなどの支援技術を使用しているユーザーにも、期待通りにコンテンツが届いているかを検証できる
    

### ロールと要素は1対1ではない

要素が持つ暗黙のロールは、要素と一対一ではない

暗黙のロールは要素に与える属性に応じて変化する

- Ex.
    
    ```html
    <!-- role="textbox" -->
    <input type="text" />
    
    <!-- role="checkbox" -->
    <input type="checkbox" />
    
    <!-- role="radio" -->
    <input type="radio" />
    
    <!-- role="spinbutton" -->
    <input type="number" />
    ```
    

### aria属性値を使った絞り込み

- headingが複数ある場合、第二引数にlevelオプションを使用することで見出しレベルを指定して取得することができる
    
    ```html
    getByRole("heading", { level: 1 })
    ```
    

### Webアクセシビリティとアクセシブルネーム

- ユーザーの心身特性に隔てなくWebが利用できる水準を**「Webアクセシビリティ」**と呼ぶ
    - マウスを動かして視覚的にWebを利用するものもいれば、スクリーンリーダーなどの支援技術を使用して利用するものもいる。どのユーザーも平等にwebを利用できるのが望ましい
- アクセシブルネーム
    - 支援技術が使用するノードの名称
    - 「送信」と書かれているボタンと、アイコンで送信の意味を担うボタン
        
        ```html
        <button>送信</button>
        <button><img alt="送信" src="path/to/img.png" /></button>
        <!-- alt="送信"がないとスクリーンリーダーに読み上げられない -->
        ```
        
    - alt属性を付与することで、どちらも送信ボタンとしてスクリーンリーダーに読み上げられる

### ロールアクセシブルネームの確認

2つ方法がある

- ブラウザの開発者ツール / 拡張機能を使用する
- テストコード上で、レンダリング結果からロールとアクセシブルネームを確認する方法
    
    @testing-library/reactのlogRoles関数を実行する
    
    ```tsx
    test("logRoles: レンダリング結果からロール・アクセシブルネームを確認", () => {
      const { container } = render(<Form name="taro" />);
      logRoles(container);
    });
    ```
    

## クエリー(要素取得API)の優先順位

- 「ユーザー操作を限りなく再現する」が、Testing LIbraryのコーディング原則。この原則にならい要素取得APIは次の順序で使用することを推奨
    1. 誰でもアクセスできるクエリー
        - 視覚的認知とスクリーンリーダーなどによる認知が同等であることを証明になる
        - getByRole, getByLabelText, getByPlaceholderText, getByText, getByDisplayValue
    2. セマンティッククエリー
        - 標準仕様に則った属性に基づくクエリー。
        - ブラウザ、支援技術によって大きく異なる
        - getByAltText
        - getByTitle
    3. テストID
        
        テストのためだけに与えられる符号。role属性などによるクエリが困難、もしくは意図的に意味を持たせたくない時に限り使用が推奨される
        
        - getByTestId