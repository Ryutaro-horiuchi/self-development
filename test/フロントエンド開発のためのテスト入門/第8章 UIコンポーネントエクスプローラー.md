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
    - Storybook エクスプローラー
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/dd7a89a3-4721-4090-b7b9-781efd532f7a/Untitled.png)
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ac003c21-c819-46e9-98b5-d5ecbfc3f867/Untitled.png)
        

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
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/6c7c130b-6e8e-4aa5-8689-c5a9fd3d01a4/Untitled.png)