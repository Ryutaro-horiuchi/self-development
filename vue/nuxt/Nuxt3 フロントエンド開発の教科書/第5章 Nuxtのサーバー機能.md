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