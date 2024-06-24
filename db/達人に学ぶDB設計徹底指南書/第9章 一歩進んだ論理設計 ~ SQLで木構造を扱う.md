- RDBは、「木構造」の取り扱いを苦手としている
- 本章では、木構造をRDBで扱う方法にどのようなものがあるか、選択肢を検討していく

# 木構造とは

---

「木」のようにデータが階層状の構造になっている

- イメージ
    
    ![IMG_1451.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c72a2899-8dd2-4ded-943d-2993e756cdaa/54495048-c41b-463d-8c5a-b3115e220891.png)
    
- 用語
    - ノード
        - 木の繋ぎ目(結節点)のこと。図では社員一人一人がノードに相当する
    - ルートノード
        - 木が始まるトップのノード
    - リーフノート
        - 自分よりも下位のノードを持たない「終着点」のノード
    - 内部ノード
        - ルートでもリーフでもない中間のノード
    - 経路
        - あるノードから別のノードへたどる道筋のこと

## 木構造の表現方法1 「隣接リストモデル」

- RDBで木構造を取り扱う際に最も古くから使われる手法
- ノードのレコードに親情報を持たせる
- イメージ
    
    ![IMG_1452.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/078746fc-8d8c-45f5-b0ab-e71e0834e070/8cf5d814-d285-4bd2-b57f-dfd106f4f0a0.png)
    
- 更新や検索のクエリが複雑でパフォーマンスが悪い

## 木構造の表現方法2-1  「入れ子集合モデル」

- ノードを点ではなく面積を持った「円」とみなし、円の包含関係によってノード間の階層関係を表す
- イメージ
    
    ![IMG_1453.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/ce118e8d-c1cf-4fbf-ad1a-73f62d80bbeb/IMG_1453.jpeg)
    
    ![IMG_1454.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/f81b9d20-a74f-4ea7-91cf-6539add71ca2/4ab68e84-cb0e-4791-800c-42c641848697.png)
    
- 「左端」と「右端」が要となる
    - 円の左端と右端の座標を表現している
    - 上司が部下の円をきちんと包含できるように、各円の座標を割り当てる必要がある
- 検索がシンプルになる
    - ルートの検索
        
        ```sql
        SELECT *
          FROM 組織図
         WHERE 左端 = 1;
        ```
        
    - リーフを求める
        
        ```sql
        SELECT * 
          FROM 組織図  AS 上司
         WHERE NOT EXISTS
           (SELECT *
              FROM 組織図 AS 部下
             WHERE 部下.左端 > 上司.左端
             　AND 部下.左端 < 上司.右端);
        ```
        
- 更新については問題を抱えている
    - イメージの組織図のイブに部下を加える場合、イブの座標は(2,3)であるため、整数値を扱う仕様だと、部下を置くことができない
        - イブの円を広げる必要が出てくる → 他の円も調整する必要が出てくる
            - クエリ
                
                ```sql
                -- 追加するノードの席を上げる
                UPDATE 組織図
                   SET 左端 = CASE WHEN 左端 WHEN 左端 > 3
                                            THEN 左端 + 2
                                            ELSE 左端 END,
                       右端 = CASE WHEN 右端 >= 3
                                   THEN 右端 + 2
                                   ELSE 右端 END
                 WHERE 右端 >= 3;
                
                -- 部下を追加
                INSERT INTO 組織図 VALUES ('イサク', 3, 4);
                ```
                
            - イメージ
                
                ![IMG_1455.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/a8356639-c9f6-4a46-8990-6cc3ba44d5c4/5ba8de4d-5f5a-43a3-8c40-db1e25a8f4c8.png)
                
                ![IMG_1456.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/fbeb7c88-7af2-4f2a-9322-1f9fb09997b1/63d9980e-1f4c-4255-b85d-5ad9207b5ebd.png)
                
    
    <aside>
    💡 更新対象と無関係な円の座標も連動して更新しなければならない点が最大の弱点
    
    </aside>
    
- 削除はレコードを削除するだけなので、簡単
    - 部下も一緒に削除する時も範囲指定で削除が用意

## 木構造の表現方法2-2 入れ子区間モデル

- 入れ子集合モデルの拡張版
- 取り扱える座標を整数から実数に広げた
    
    ![IMG_1457.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/10faea6f-328e-42ad-9726-9ea35cab09ed/97b02a8b-4668-443c-8d03-0fd0b8eafa91.png)
    
    <aside>
    💡 「入れ子集合モデル」の更新における問題を解決している
    
    </aside>
    
- 座標を求める計算式
    - 挿入対象としたい区間の左座標「plft」、右端座標を「prgt」とする
    
    ```
    追加したいノードの左端座標　(plft * 2 + prgt) / 3 
    追加したいノードの右端座標　(plft + prgt * 2) / 3
    ```
    
- 十分な実数の有効桁数が必要になるので、現時点でこのモデルを採用できるかどうかは未知数
    - データ型の物理的成約がなければ、RDBにおける検索 / 更新どちらにおいても最も優れている。著者的にはいますぐ採用していいものとしている

## 木構造の表現方法3 経路列挙モデル

- ノードをディレクトリとみなし、各ノードまでの経路を記述する
- イメージ
    
    ![IMG_1458.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/cb839663-438c-4ce2-884f-ec7e48f917c3/4c8ae035-e2a7-4cd4-a644-009d4c8cc549.png)
    
- 更新が少なく、大量データの高速検索が必要なケースに向いている
- メリット
    - 検索のパフォーマンスが良い
        
        経路がテーブル上で一意になるため、ユニークインデックスによる高速検索が可能
        
- デメリット
    - 経路に主キーを使うと、経路の文字列が非常に長大になる危険がある
    - パスに番号を使うと、ノードの削除、追加などの更新が複雑になる
- 検索の例
    - ルートを求める
        
        ```sql
        SELECT *
          FROM 組織図
         WHERE 社員 = REPLACE(経路, '/', '');
        ```
        
    - リーフを求める
        
        ```sql
        SELECT * 
          FROM 組織図 AS 親
         WHERE NOT EXISTS
            (SELECT *
                FROM 組織図 AS 子
                WHERE 子.経路 LIKE  親.経路 || '_%');
        ```
        
- 更新の例
    - いくらか複雑になる
    - イメージ図
        
        ![IMG_1460.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e000e946-cb8a-434c-b07d-c4765901a103/104b3229-0139-48c6-840f-7726dd95b7b0.png)
        
    - クエリ
        
        ![IMG_1461.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/bd92d37c-5271-43d9-b380-f91de4559400/924ae54d-e131-44f3-82ad-c7b6fb6bc0f7.png)
        
    
    <aside>
    💡 部分木となるパスを全て更新する必要が出てくる
    
    </aside>
    
- 削除の例
    
    ```sql
    DELETE FROM 組織図
     WHERE 経路 LIKE (SELECT 経路
                       FROM 組織図
                      WHERE 社員 = 'カイン') || '%';
    ```