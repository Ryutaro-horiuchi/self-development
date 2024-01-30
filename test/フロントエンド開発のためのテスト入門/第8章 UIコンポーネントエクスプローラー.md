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