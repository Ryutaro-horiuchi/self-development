## Nuxtのサーバー機能の基本

Web API のデータ提供を行うNuxtのサーバー機能は、serverフォルダにファイルを作成することで利用できるようになる

### Nuxtエンドポイントの作成

- Ex.
    - server/api/getMemberList.ts
        
        ```
        import type {Member} from "@/interfaces";
        import {createMemberList} from "@/membersDB";
        
        export default defineEventHandler(
        	(event): Member[] => {
        		//membersDB.tsを利用して会員リスト情報Mapオブジェクトを生成。
        		const memberList = createMemberList();
        		//会員リスト情報Mapオブジェクトの値部分を取得。
        		const memberListValues =  memberList.values();
        		//会員リスト情報Mapオブジェクトの値部分を配列に変換。
        		const memberListArray = Array.from(memberListValues);
        		//会員リスト情報配列をリターン。
        		return memberListArray;
        	}
        );
        ```
        
        - membersDB
            
            ```tsx
            import type {Member} from "@/interfaces";
            
            export function createMemberList(): Map<number, Member> {
            	const memberListInit = new Map<number, Member>();
            	memberListInit.set(33456, {id: 33456, name: "田中太郎", email: "bow@example.com", points: 35, note: "初回入会特典あり。"});
            	memberListInit.set(47783, {id: 47783, name: "鈴木二郎", email: "mue@example.com", points: 53});
            	return memberListInit;
            }
            ```
            
- 解説
    - サーバーAPIエンドポイントの処理コードは、`defineEventHandler()`関数の実行結果をデフォルトエクスポートする
    - アロー関数の引数 event はhttpに関するイベントオブジェクト
    - 本来であればデータを返却するときに、JSON.stringify()メソッドを利用してJSONデータ化する必要があるが、これはdefineEventHandler()内で自動でJSONデータ化されるようになっており、不要である
    - `defineEventHandler()` は、Nuxtが内包するhttpフレームワークであるh3の関数

### Nuxtのエンドポイントからのデータ取得

```tsx
const asyncData = useLazyFetch("/api/getMemberList");
const memberList = asyncData.data;
const pending = asyncData.pending;
```

- 同一Nuxtプロジェクト内のサーバーAPIエンドポイントへのアクセスの場合は、プロトコル部分やホスト部分は省略でき、パス部分のみを記述するだけで問題ない

## GETリクエスト

### クエリパラメーターでの会員詳細情報の取得

- Ex.
    - pages/member/memberDetail/[id].vue
        
        ```tsx
        const route = useRoute()
        const asyncData = useLazyFetch(
        	"/api/getOneMemberInfo",
        	{
        		query: {id: route.params.id}
        	}
        );
        ```
        
        - queryプロパティでクエリパラメーターidとして、ルートパラメータで渡された値を付与する

### サーバーサイドでのクエリパラメーターの取得

- Ex.
    - server/api/getOneMemberInfo.ts
        
        ```tsx
        export default defineEventHandler(
        	(event): Member => {
        		//クエリパラメータを取得。
        		const query = getQuery(event);
        		//membersDB.tsを利用して会員リスト情報Mapオブジェクトを生成。
        		const memberList = createMemberList();
        		//クエリパラメータのidを数値に変換。
        		const idNo = Number(query.id);
        		//クエリパラメータに該当する会員情報オブジェクトを取得。
        		const member = memberList.get(idNo) as Member;
        		//取得した会員情報オブジェクトをリターン。
        		return member;
        	}
        );
        ```
        
- `getQuery(event)`を実行すると、イベントオブジェクト内に格納されたクエリパラメーターを取り出せる

## POSTリクエスト

リクエストボディでの新規会員情報の送信

### リクエストボディの取得

- Ex.
    
    ```tsx
    export default defineEventHandler(
    	async (event) => {
    		const body = await readBody(event);
    		console.log(body);
    		return {
    			result: 1,
    			member: body
    		};
    	}
    );
    ```
    
- `readBody(event)`を実行すると、リクエストボディを取得できる
    - この関数は非同期関数であるため、awaitを利用する必要がある点に注意

## サーバーサイドルーティング

### routesサブフォルダ

- pagesフォルダ配下にファイルを作成するとそのままルーティング化する仕組みが、サーバーサイドにもそのまま適用できる
    - server/api 配下に作成したファイルはそのまま/api配下のパスとして実行されるが、`routes`フォルダの場合はルーティングの仕組みが適用される

### HTTPメソッドは拡張子で指定する

- Ex.
    - パス: `/member-management/members`
    - HTTPメソッド:  `get`
        
        → `members.get.ts`になる。単純だが、postの時は`members.post.ts`
        

### ルートパラメーターの取得

- サーバーサイドでもルートパラメーターを含めたファイルの作成方法は、pagesフォルダ内のファイルの作成方法と同じである
- Ex.  ファイル作成
    - パス: `/member-management/members/32234`
    - HTTPメソッド: `get`
    
    ```tsx
    server/routes/member-management/members/[id].get.ts
    ```
    
- Ex. ルートパラメータ取得コード
    
    ```tsx
    export default defineEventHandler(
    	(event): ReturnJSONMembers => {
    		//ルートパラメータを取得。
    		const params = event.context.params;
    		//membersDB.tsを利用して会員リスト情報Mapオブジェクトを生成。
    		const memberList = createMemberList();
    		//ルートパラメータのidを数値に変換。
    		const idNo = Number(params!.id);
    		//ルートパラメータに該当する会員情報オブジェクトを取得。
    		const member = memberList.get(idNo) as Member;
    		//送信データオブジェクトをリターン。
    		return {
    			result: 1,
    			data: [member]
    		};
    	}
    );
    ```
    
    - event.context.params
        - ルートパラメーターを全て取得できる