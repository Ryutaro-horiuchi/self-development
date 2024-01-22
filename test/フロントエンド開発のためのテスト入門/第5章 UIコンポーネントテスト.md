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