## Global UIテスト

### 前提: Context API(React)

- Toastコンポーネント Global UIでどこからでも呼び出せる、使用できるコンポーネント
    - Global UIを扱うためには、Propsだけでは実装に不便なことがある
        - React標準APIである、「ContextAPI」はこういったシーンで活用できる
            - Propsによる明示的な値私が不要になるため、子孫コンポーネントからルートコンポーネントが保持する「値と更新関数」に直接アクセスできる
- Ex.
    - Contextの定義
        
        ```tsx
        export type ToastStyle = "succeed" | "failed" | "busy";
        
        export type ToastState = {
          isShown: boolean;
          message: string;
          style: ToastStyle;
        };
        
        export const initialState: ToastState = {
          isShown: false,
          message: "",
          style: "succeed",
        };
        ```
        
    - Contextオブジェクトに付属しているProviderコンポーネントをレンダリングしている
        
        ```
        <ToastStateContext.Provider value={{ isShown, message, style }}>
              <ToastActionContext.Provider value={{ showToast, hideToast }}>
                {children}
                {/* isShown が true になった時、表示される */}
                {isShown && <Toast message={message} style={style} />}
              </ToastActionContext.Provider>
            </ToastStateContext.Provider>
        ```
        
        - 子孫コンポーネント(Toastコンポーネント)、をProvider(ToastStateContext.Provider, ToastActionContext.Provider)で囲むことで、valueに渡した変数や関数を、子孫コンポーネントで使用できるようにする

### Global UIテストの観点

- Providerが保持する状態に応じて表示が切り替わること
- Providerが保持する更新関数を経由し、状態を更新できること

### Global UIテスト手法例

- 例に使用するコンポーネントの概要
    - <Toast>コンポーネント: Viewを提供する
    - <ToastProvider>コンポーネント: 表示のための状態を保持する
    - useToastProvderフック: 表示ロジックを管理する
    - useToastActionフック: 子孫コンポーネントから呼び出す
- 2通りある
1. テスト用のコンポーネントを用意し、インタラクションを実行する
    
    ```tsx
    const user = userEvent.setup();
    
    const TestComponent = ({ message }: { message: string }) => {
      const { showToast } = useToastAction(); // <Toast> を表示するためのフック
      return <button onClick={() => showToast({ message })}>show</button>;
    };
    
    test("showToast を呼び出すと Toast コンポーネントが表示される", async () => {
      const message = "test";
      render(
        <ToastProvider>
          <TestComponent message={message} />
        </ToastProvider>
      );
      // 初めは表示されていない
      expect(screen.queryByRole("alert")).not.toBeInTheDocument();
      await user.click(screen.getByRole("button"));
      // 表示されていることを確認
      expect(screen.getByRole("alert")).toHaveTextContent(message);
    });
    ```
    
2. 初期値を注入し、表示確認をする
    
    ただ表示確認をするだけであれば、従来通りPropsを渡すだけで確認できる
    
    ```tsx
    test("Succeed", () => {
      const state: ToastState = {
        isShown: true,
        message: "成功しました",
        style: "succeed",
      };
      render(<ToastProvider defaultState={state}>{null}</ToastProvider>);
      expect(screen.getByRole("alert")).toHaveTextContent(state.message);
    });
    ```
    

## Next.js Routerの表示結合テスト

next-router-mockを使用する

- Jestで、Next.jsのRouterに関するテストをかけるようになる
- mockRouter.setCurrentUrlを実行して、対照テストの現在のURL状態を再現する
    
    ```tsx
    test("「Create Post」がカレント状態になっている", () => {
      **mockRouter.setCurrentUrl("/my/posts/create");**
      render(<Nav onCloseMenu={() => {}} />);
      const link = screen.getByRole("link", { name: "Create Post" });
      expect(link).toHaveAttribute("aria-current", "page");
    });
    ```
    

## セットアップ関数のテクニック

- セットアップ関数内で、さまざまなインタラクション関数やスパイ関数を用意し、returnする
- テスト時には、セットアップ関数からContextに応じて必要な関数を使用しテストする
    - Ex.
        - セットアップ関数
            
            ```tsx
            function setup() {
              const onClickSave = jest.fn();
              const onValid = jest.fn();
              const onInvalid = jest.fn();
              render(
                <PostForm
                  title="新規記事"
                  onClickSave={onClickSave}
                  onValid={onValid}
                  onInvalid={onInvalid}
                />
              );
              async function typeTitle(title: string) {
                const textbox = screen.getByRole("textbox", { name: "記事タイトル" });
                await user.type(textbox, title);
              }
              async function saveAsPublished() {
                await user.click(screen.getByRole("switch", { name: "公開ステータス" }));
                await user.click(screen.getByRole("button", { name: "記事を公開する" }));
              }
              async function saveAsDraft() {
                await user.click(screen.getByRole("button", { name: "下書き保存する" }));
              }
              return {
                typeTitle,
                saveAsDraft,
                saveAsPublished,
                onClickSave,
                onValid,
                onInvalid,
              };
            }
            
            ```
            
        - セットアップ関数を使用したテスト
            
            ```tsx
            test("不適正内容で「下書き保存」を試みると、バリデーションエラーが表示される", async () => {
              const { saveAsDraft } = setup();
              await saveAsDraft();
              await waitFor(() =>
                expect(
                  screen.getByRole("textbox", { name: "記事タイトル" })
                ).toHaveErrorMessage("1文字以上入力してください")
              );
            });
            
            test("不適正内容で「下書き保存」を試みると、onInvalid イベントハンドラーが実行される", async () => {
              const { saveAsDraft, onClickSave, onValid, onInvalid } = setup();
              await saveAsDraft();
              expect(onClickSave).toHaveBeenCalled();
              expect(onValid).not.toHaveBeenCalled();
              expect(onInvalid).toHaveBeenCalled();
            });
            ```
            

### 似たようなインタラクションを抽象化する

- UIコンポーネントのテストは似たようなインタラクションが必要になることが多い
    - テストの「事前準備、レンダリング」だけでなく、操作対象を関数で抽象化することが良しとされる
    - Testing Library作者のKent C. Dodds氏の解説されているテクニック
    - Ex.
        
        ```tsx
        function setup(url = "/my/posts?page=1") {
          mockRouter.setCurrentUrl(url);
          render(<Header />);
          const combobox = screen.getByRole("combobox", { name: "公開ステータス" });
        
          **async function selectOption(label: string) {
            await user.selectOptions(combobox, label);
          }**
          return { combobox, selectOption };
        }
        
        test("公開ステータスを変更すると、status が変わる", async () => {
          // すでにある page=1 が消えていないこともあわせて検証
          **const { selectOption } = setup();**
          expect(mockRouter).toMatchObject({ query: { page: "1" } });
          await selectOption("公開");
          expect(mockRouter).toMatchObject({
            query: { page: "1", status: "public" },
          });
          await selectOption("下書き");
          expect(mockRouter).toMatchObject({
            query: { page: "1", status: "private" },
          });
        });
        
        ```
        

## MSW(モックサーバーライブラリ)

ネットワークレベルのモックを実現するライブラリ

- Jestでは、APIを呼び出している関数自体をモックしていた
- 発生したheaderやqueryの内訳が詳細に検証することができる
- BFFを含むフロントエンドの至る所で活用できる
- jsdomには、FetchAPIが用意されていない(2023年3月時点)
    - whatwg-fetchをインストールし、全てのテストで`import “whatwg-fetch”`を使用する
- Ex.
    
    ```tsx
    import { setupWorker, rest } from "msw";
    const worker = setupWorker(
      rest.get("/login", (req, res, ctx) => {
    		const { username } = await req.json();
        return res(
          ctx.json({
            username,
            firstname: "John"
          })
        );
      })
    );
    worker.start();
    ```
    
    - /loginというURLに対するPOSTリクエストがインターセプトされる
        - bodyに含まれるusernameを参照して`{username, firstName: “John”}`というjsonレスポンスが返却される

### Jestで使用する準備

- Ex.
    - msw/nodeのsetUpServer関数を使用して、Jest向けのセットアップ関数を用意する
        
        ```tsx
        src/tests/jest.ts
        import type { RequestHandler } from "msw";
        import { setupServer } from "msw/node";
        
        export function setupMockServer(...handlers: RequestHandler[]) {
          const server = setupServer(...handlers);
          beforeAll(() => server.listen());
          afterEach(() => server.resetHandlers());
          afterAll(() => server.close());
          return server;
        }
        ```
        
        - setUpServer関数にリクエストハンドラーを可変長引数で渡すことで、インターセプトが有効になる
        - beforeAll(), afterEach(), afterAll()のフックを使用することで、テストごとにサーバーを初期化し、異なるテスト間で干渉しないようにする
    
    - リクエストハンドラーを定義しする
        
        ```tsx
        src/client/MyPosts/__mock__/msw.ts
        
        import { rest } from "msw";
        
        export function handleCreateMyPosts(spy?: jest.Mock<any, any>) {
          return rest.post(path(), async (req, res, ctx) => {
            const data: ApiMyPosts.PostInput = await req.json();
            spy?.({ body: data, headers: req.headers.get("content-type") });
            if (data.title === "500") {
              const err = new HttpError(500).serialize();
              return res(ctx.status(err.status), ctx.json(err));
            }
            return res(ctx.json(createMyPostsData(data.title)));
          });
        }
        export const handlers = [handleCreateMyPosts()];
        ```
        
    
    - 実際のテストアップで、セットアップする
        
        ```tsx
        MyPostsCreate/index.test.tsx
        
        import * as MyPosts from "@/services/client/MyPosts/__mock__/msw";
        import { setupMockServer } from "@/tests/jest";
        
        setupMockServer(...MyPosts.handlers, ...MyProfile.handlers));
        ```
        

### MSWを使用したテスト例

- セットアップ関数
    
    ```tsx
    async function setup() {
      const { container } = render(<Default />);
      const { selectImage } = selectImageFile();
      async function typeTitle(title: string) {
        const textbox = screen.getByRole("textbox", { name: "記事タイトル" });
        await user.type(textbox, title);
      }
      async function saveAsPublished() {
        await user.click(screen.getByRole("switch", { name: "公開ステータス" }));
        await user.click(screen.getByRole("button", { name: "記事を公開する" }));
        await screen.findByRole("alertdialog");
      }
      async function saveAsDraft() {
        await user.click(screen.getByRole("button", { name: "下書き保存する" }));
      }
      async function clickButton(name: "はい" | "いいえ") {
        await user.click(screen.getByRole("button", { name }));
      }
      return {
        container,
        typeTitle,
        saveAsPublished,
        saveAsDraft,
        clickButton,
        selectImage,
      };
    }
    ```
    
- テスト
    
    ```tsx
    setupMockServer(...MyPosts.handlers, ...MyProfile.handlers);
    beforeEach(() => {
      mockUploadImage();
      mockRouter.setCurrentUrl("/my/posts/create");
    });
    
    describe("AlertDialog", () => {
      test("公開を試みた時、AlertDialog が表示される", async () => {
        const { typeTitle, saveAsPublished, selectImage } = await setup();
        await typeTitle("201");
        await selectImage();
        await saveAsPublished();
        expect(
          screen.getByText("記事を公開します。よろしいですか？")
        ).toBeInTheDocument();
      });
    
      test("「いいえ」を押下すると、AlertDialog が閉じる", async () => {
        const { typeTitle, saveAsPublished, clickButton, selectImage } =
          await setup();
        await typeTitle("201");
        await selectImage();
        await saveAsPublished();
        await clickButton("いいえ");
        expect(screen.queryByRole("alertdialog")).not.toBeInTheDocument();
      });
    
      test("不適正内容で送信を試みると、AlertDialog が閉じる", async () => {
        const { saveAsPublished, clickButton, selectImage } = await setup();
        // await typeTitle("201");　タイトルが入力されていない
        await selectImage();
        await saveAsPublished();
        await clickButton("はい");
        await waitFor(() =>
          expect(
            screen.getByRole("textbox", { name: "記事タイトル" })
          ).toBeInvalid()
        );
        expect(screen.queryByRole("alertdialog")).not.toBeInTheDocument();
      });
    });
    ```

## 画像選択テスト

jsdomでは、画像選択関連のインタラクションが整備されていない

- 下記仕様の関数を用意する
    - ダミーの画像ファイルを作成する
    - 画像インタラクションを再現する
    
    ```tsx
    import userEvent from "@testing-library/user-event";
    
    export function selectImageFile(
      inputTestId = "file",
      fileName = "hello.png",
      content = "hello"
    ) {
    	// userEventの初期化
      const user = userEvent.setup();
    	// ダミーの画像ファイルを作成
      const filePath = [`C:\\fakepath\\${fileName}`]; 
      const file = new File([content], fileName, { type: "image/png" });
    
    	// renderしたコンポーネントに含まれるdata-testid="file"相当のinput要素を取得
      const fileInput = screen.getByTestId(inputTestId);
    
    	// このkな数を実行すると、画像選択が再現される
      const selectImage = () => user.upload(fileInput, file);
      return { fileInput, filePath, selectImage };
    }
    ```