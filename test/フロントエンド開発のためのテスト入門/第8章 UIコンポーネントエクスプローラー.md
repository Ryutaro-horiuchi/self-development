## StorybookのUIコンポーネントテスト

- Jestを使用したUIコンポーネントテストとE2Eテストの中間に位置するテスト
    - Jest 実行速度が速く、忠実性が低い
    - E2E 実行速度が遅く、忠実性が遅い

## 環境構築

- npx storybook init
    - セットアップ用のコマンド。質問に答える形でセットアップする
- npm install
    - react react-dom(React環境)
- npm run storybook
    - storybookを立ち上げる

## Storybookの基本

### Storyを登録する

- Storyファイルの拡張子
    - `.stories.jsx`
    - Ex. Button.jsxコンポーネントのStoryファイルを作成するときは、Button.stories.jsファイルとなる
- Ex. ButtonStoryファイル
    - Button.jsx
        
        ```tsx
        import React from 'react';
        import PropTypes from 'prop-types';
        import './button.css';
        
        /**
         * Primary UI component for user interaction
         */
        export const Button = ({ primary, backgroundColor, size, label, ...props }) => {
          const mode = primary ? 'storybook-button--primary' : 'storybook-button--secondary';
          return (
            <button
              type="button"
              className={['storybook-button', `storybook-button--${size}`, mode].join(' ')}
              style={backgroundColor && { backgroundColor }}
              {...props}
            >
              {label}
            </button>
          );
        };
        
        Button.propTypes = {
          /**
           * Is this the principal call to action on the page?
           */
          primary: PropTypes.bool,
          /**
           * What background color to use
           */
          backgroundColor: PropTypes.string,
          /**
           * How large should the button be?
           */
          size: PropTypes.oneOf(['small', 'medium', 'large']),
          /**
           * Button contents
           */
          label: PropTypes.string.isRequired,
          /**
           * Optional click handler
           */
          onClick: PropTypes.func,
        };
        
        Button.defaultProps = {
          backgroundColor: null,
          primary: false,
          size: 'medium',
          onClick: undefined,
        };
        ```
        
    - Button.stories.js
        
        ```tsx
        import { Button } from './Button';
        
        export default {
          title: 'Example/Button',
        	component: Button,
        }
        ```
        
        - export default オブジェクトのcomponentプロパティに、コンポーネントを指定することで、コンポーネントに対するStoryファイルの定義となる
        
        ```tsx
        import { Button } from './Button';
        
        export default {
        	title: 'Example/Button',
        	...
        
        }
        
        export const Large = {
          args: {
            size: 'large',
            label: 'Button',
          },
        };
        
        export const Small = {
          args: {
            size: 'small',
            label: 'Button',
          },
        };
        ```
        
        - argsプロパティで、コンポーネントに渡すPropsを定義することができる
        - Large, Smallで別名でexportすることで、異なるサイズのStoryを登録することができる
        

### 3レベル設定のディープマージ

- 登録する一つ一つのStoryは、「Global, Component Story」の3レベルで定義された設定をマージしたものが採用される。
    - 共通で適用したい項目は適切なスコープで定義することで、DRYに設定することができる
        
        → 全てのStoryで適用したい設定はGlobal, コンポーネント単位であれば、Componentといった具合
        
- 3レベル
    - Global：全Storyの設定(.storybook/preview.js)
    - Component：Storyファイルごとの設定(export default)
    - Story：Storyごとの設定(export const)
    - 設定の優先度
        - Global < Component < Story

## Storybook必須アドオン

### storybook/addon-essentials

- storybookインストール時に標準でインストールされる
- Controlsパネルを使ったデバッグ
    - Propsの値を書き換えることで、表示がどうなるかリアルタイムでデバッグすることができる
        - 筆者は文字が長くなった場合に意図したレイアウトになっているかを確認


### actionsパネル(storybook/addon-actions)

- Propsに渡されたイベントハンドラーがどのように呼び出されたのかをログ出力する機能
- 初期設定では、.storybook/preview.js上にて、接頭辞「on」で始まるイベントハンドラーが自動でactionsに出力されるようになっている
    
    ```tsx
    export const parameters = {
      actions: { argTypesRegex: "^on[A-Z].*" },
    }
    ```
    
- Ex.
    - Story
        
        ```tsx
        export const FailedSaveAsDraft: Story = {
          play: async ({ canvasElement }) => {
            const canvas = within(canvasElement);
            await user.click(canvas.getByRole("button", { name: "下書き保存する" }));
            const textbox = canvas.getByRole("textbox", { name: "記事タイトル" });
            await waitFor(() =>
              expect(textbox).toHaveErrorMessage("1文字以上入力してください")
            );
          },
        };
        ```

### レスポンシブレイアウトに対応するViewport設定

- スマートフォンレイアウトでStoryを登録したい場合、`parameters.viewport`を設定する必要がある
- Ex.
    
    ```tsx
    export const SPLoggedIn: Story = {
      parameters: {
        viewport: {
          viewports: INITIAL_VIEWPORTS,
          defaultViewport: "iphone6",
        },
      },
    ```
    
- 全storyで共通で使用する場合、設定ファイルにparameterを持たせておく
    - story
        
        ```tsx
        export const SPLoggedIn: Story = {
          parameters: {
            ...SPStory.parameters,
          },
        ```
        
    - 設定ファイル
        
        ```tsx
        export const SPStory = {
          parameters: {
            viewport: {
              viewports: INITIAL_VIEWPORTS,
              defaultViewport: "iphone6",
            },
            screenshot: {
              ...
            },
          },
        };
        ```
        

## WebAPIに依存したStoryの登録

### アドオンを設定する

- mswと、msw-storybook-addon をインストールする
- .storybook/preview.jsにて設定する
    
    ```tsx
    import { initialize, mswDecorator } from "msw-storybook-addon";
    
    export const decorators = [mswDecorator];
    
    initialize();
    ```
    
    - initialize()関数で有効化
    - mswDecoratorも全てのStoryで必要になるため、exportで設定しておく
- パブリックディレクトリの場所を宣言する
    
    ```tsx
    $ npx msw init <PUBLIC_DIR>
    ```
    
- Storybookにも、パブリックディレクトリの場所を明記しておく
    
    ```tsx
    const path = require("path");
    
    module.exports = {
    	...
      staticDirs: ["../public"],
    }
    ```
    

### リクエストハンドラーを変更する

- 認証のリクエストなど、全てのStoryで使用する場合はGlobal(.storybook/preview.js)に設定しておく
    
    ```tsx
    import { **handleGetMyProfile** } from ..
    
    export const parameters = {
    	msw: { handlers: [**handleGetMyProfile**()] },
    	...
    }
    ```
    
    src/services/client/MyProfile/__mock__/msw.ts
    
    ```tsx
    export function handleGetMyProfile(args?: {
      mock?: jest.Mock<any, any>;
      status?: number;
    }) {
      **return rest.get(path(), async (_, res, ctx) => {
        args?.mock?.();
        if (args?.status) {
          return res(ctx.status(args.status));
        }
        return res(ctx.status(200), ctx.json(getMyProfileData));
      });**
    }
    ```
    
- Story 使用例
    
    ```tsx
    import { handleGetMyProfile } from "@/services/client/MyProfile/__mock__/msw";
    import { Login } from "./";
    
    export default {
      component: Login,
      parameters: {
        nextRouter: { pathname: "/login" },
        msw: { handlers: [**handleGetMyProfile({ status: 401 })**] },
      },
      decorators: [BasicLayoutDecorator],
    } as ComponentMeta<typeof Login>;
    
    ...
    ```
    

## Router依存したStoryの登録

### アドオンを設定する

- storybook-addon-next-router をインストールする
- .storybook/main.jsと.storybook/preview.jsに設定をする
    - main.js
        
        ```jsx
        module.exports = {
          stories: ["../src/**/*.stories.@(js|jsx|ts|tsx)"],
          addons: [ "storybook-addon-next-router",],
        	...
        }
        ```
        
    - preview.js
        
        ```jsx
        import { RouterContext } from "next/dist/shared/lib/router-context";
        
        nextRouter: {
          Provider: RouterContext.Provider,
        },
        ```
        
- Story
    
    ```jsx
    export const RouteMyPosts: Story = {
      parameters: {
        nextRouter: { pathname: "/my/posts" },
      },
    };
    ```
    

## Play functionを利用したインタラクションテスト

Storybook上でユーザーの操作を再現できる

### アドオンを設定する

- インストール
    
    ```jsx
    $ npm install @storybook/testing-library @storybook/jest @storybook/addon-interactions --save-dev
    ```
    
- .storybook/main.jsに設定を追加する
    
    ```jsx
    module.exports = {
      stories: ["../src/**/*.stories.@(js|jsx|ts|tsx)"],
    	addons: ["@storybook/addon-interactions"],
    	features: {
    		interactionsDebugger: true,
    	}
    	...
    }
    ```
    

### インタラクションを与える

StoryにPlay関数を使用する

- Ex.
    - Story
        
        ```jsx
        import { userEvent as user, waitFor, within } from "@storybook/testing-library";
        
        export const SucceedSaveAsDraft: Story = {
          **play:** async ({ canvasElement }) => {
            const canvas = within(canvasElement);
            await **user.type(**
              canvas.getByRole("textbox", { name: "記事タイトル" }),
              "私の技術記事"
            );
          },
        };
        ```
        
        - インタラクション自体の記述はtesting-library+jsdomの書き方と同様

## アクセシビリティテスト

- アクセシビリティについて
    
    [Webアクセシビリティとアクセシブルネーム](https://www.notion.so/Web-b1c65f7d5c8e449da9802c06fc21fe43?pvs=21) 
    
- Storybookを活用してコンポーネント単位でのアクセシビリティ検証が行える

### アドオンを設定する

- @storybook/addon-a11y —save-dev
- .storybook/main.jsに追加する
    
    ```jsx
    module.exports = {
    	addons: [
    		"@storybook/addon-a11y",
    	]
    }
    ```
    

### 検証を確認する

- StoryエクスプローラーのAccessibilityタグで検証される
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/1746ebec-51f2-431b-a42e-76f9c97f0f82/Untitled.png)
    
    - Violations 違反
    - Passes パス
    - Incomplete 修正すべき

### 一部のルール違反を無効化する

- ケースに応じて無効化したい場合がある。こちらも他と同様、Global, Component, Storyの3つのレベルで設定できる
    - Ex.  Componentレベルで設定
        
        ```jsx
        export default {
          component: Switch,
          parameters: {
            **a11y: {
              config: { rules: [{ id: "label", enabled: false }] },
            },**
          },
        } as ComponentMeta<typeof Switch>;
        ```
        

### アクセシビリティ検証を無効化にする

- Ex. Componentレベルで設定
    
    ```jsx
    export default {
      component: Switch,
      parameters: {
        **a11y: { disable: true }**
      },
    } as ComponentMeta<typeof Switch>;
    ```
    

## Storybookのスモークテスト (Test runner)

- スモークテスト
    - Storybookが壊れていないか、ざっくり検証するテストのこと
- Storybook自体をテスト化する
    - JestとPlaywrightで実行される
- ライブラリのインストール
    
    ```jsx
    npm install @storybook/test-runner --save-dev
    ```
    
- package.jsonにスクリプトを登録しておくと便利
    
    ```jsx
    {
     "scripts": {
    		"test:storybook": "test-storybook"
      }
    }
    ```
    

### Viewportの設定が反映されない課題の回避策(2023年3月時点)

- Storyごとに設定したViewportsがTest Runnerに適用されない問題が報告されている
- issueに習い一時的に問題への回避策として、.storybook/test-runner.jsに次の設定を施している
    
    ```jsx
    module.exports = {
      async preRender(page, context) {
        **if (context.name.startsWith("SP")) {
          page.setViewportSize({ width: 375, height: 667 });
        } else {
          page.setViewportSize({ width: 1280, height: 800 });
        }**
      },
      ...
    };
    ```
    

### Test runnerによるアクセシビリティテスト

- インストール
    
    ```jsx
    $ npm install axe-playwright --save-dev
    ```
    
- .storybook/test-runner.jsに設定を追記する
    
    ```jsx
    module.exports = {
      async preRender(page, context) {
        ...
        **await injectAxe(page); // axeを使用した検証のセットアップ**
      },
      async postRender(page, context) {
        ...
        **await checkA11y(page, "#root", {
          includedImpacts: ["critical"], // Violations相当のみのエラーを計上**
          detailedReport: false,
          detailedReportOptions: { html: true },
          axeOptions: storyContext.parameters?.a11y?.options,
        });
      },
    };
    ```
    

## Storyを結合テストとして再利用する

- Storyで使用した**「状態の準備」**を結合テストで再利用する
- インストール
    
    ```jsx
    $ npm install --save-dev @storybook/testing-react
    ```
    
- Ex.
    - Story(状態の準備)
        
        ```jsx
        import { composeStories } from "@storybook/testing-react";
        import { render, screen } from "@testing-library/react";
        import * as stories from "./index.stories";
        
        const { Default, CustomButtonLabel, ExcludeCancel } = composeStories(stories);
        
        describe("AlertDialog", () => {
          test("Default", () => {
            render(<Default />);
            expect(screen.getByRole("alertdialog")).toBeInTheDocument();
          });
        
          test("CustomButtonLabel", () => {
            render(<CustomButtonLabel />);
            expect(screen.getByRole("button", { name: "OK" })).toBeInTheDocument();
            expect(
              screen.getByRole("button", { name: "キャンセル" })
            ).toBeInTheDocument();
          });
        
          test("ExcludeCancel", () => {
            render(<ExcludeCancel />);
            expect(screen.getByRole("button", { name: "OK" })).toBeInTheDocument();
            expect(
              screen.queryByRole("button", { name: "CANCEL" })
            ).not.toBeInTheDocument();
          });
        });
        ```
        
    - Storyを用いた結合テスト
        
        ```jsx
        import { composeStories } from "@storybook/testing-react";
        import { render, screen } from "@testing-library/react";
        **import * as stories from "./index.stories";**
        
        **const { Default, CustomButtonLabel, ExcludeCancel } = composeStories(stories);**
        
        describe("AlertDialog", () => {
          test("Default", () => {
            **render(<Default />);**
            expect(screen.getByRole("alertdialog")).toBeInTheDocument();
          });
        
          test("CustomButtonLabel", () => {
            **render(<CustomButtonLabel />);**
            expect(screen.getByRole("button", { name: "OK" })).toBeInTheDocument();
            expect(
              screen.getByRole("button", { name: "キャンセル" })
            ).toBeInTheDocument();
          });
        
          test("ExcludeCancel", () => {
            **render(<ExcludeCancel />);**
            expect(screen.getByRole("button", { name: "OK" })).toBeInTheDocument();
            expect(
              screen.queryByRole("button", { name: "CANCEL" })
            ).not.toBeInTheDocument();
          });
        });
        ```
        

### storybook/test-runnerとの違い

- テストとStoryの登録を一度に行い、工数を削減するアプローチは、Test runnnerによるアプローチと似ている。どちらが適しているかは、目的や甲乙を比較して検討する
- JestでStoryを使用する
    - モジュールモックやスパイが必要なテストをかける
    - 実行速度が速い(ヘッドレスブラウザを使用しない)
- Test runnerの方が優れている
    - テストファイルを別途用意する必要がない
        
        → Storyファイルだけで
        
    - 忠実性が高い(ブラウザを使用するため、CSSが再現される)