## 導入

### 重複行を残すALLオプションをつけるとパフォーマンスが向上する

- [重複行を残す集合演算 - ALLオプション](https://www.notion.so/ALL-d2f3cc2c216e4140b202e05ff8c7817f?pvs=21)
- ALLオプションをつけないと、重複行を削除するために内部でソート処理が発生する
    
    → ALLオプションをつけると重複を削除しないため、ソートが行われずパフォーマンスが向上する
    

### 演算の順番に優先順位がある

UNIONとINTERSECTでは、INTERSECTが先に実行される。UNIONを先に実行したい場合は、括弧で明示的に演算の順序を指定する

## テーブル同士を比較する - 集合の相当性チェック[基本編]

- 2つのテーブルが正しいかを比較する
    - バックアップと最新環境を比較する場合など
    - Ex. テーブル名は違うが、中身が同じ(行数も列も値も)
        - tbl_A
            
            
            | key | col_1 | col_2 | col_3 |
            | --- | --- | --- | --- |
            | A | 2 | 3 | 4 |
            | B | 0 | 7 | 9 |
            | C | 5 | 1 | 6 |
        - tbl_B
            
            
            | key | col_1 | col_2 | col_3 |
            | --- | --- | --- | --- |
            | A | 2 | 3 | 4 |
            | B | 0 | 7 | 9 |
            | C | 5 | 1 | 6 |
- SQL: UNIONを用いる
    
    ```sql
    SELECT COUNT(*) AS row_cnt
      FROM ( SELECT * 
               FROM   tbl_A 
             UNION
             SELECT * 
               FROM   tbl_B ) TMP;
    ```
    
    - tbl_A, tbl_Bと合計の行数とクエリの結果の行数が同じであれば中身が同じである
        
        → 仮にtbl_Bのkey,Bの列が一つでも違ければ、4が返ってくる
        
    - 列名列数を知る必要がなく、比較することができる
    - UNIONには冪等性がある
        
        ```sql
        S * S = S
        ```
        
        冪等性: 繰り返し処理を実行しても一度だけ実行した場合と結果が同じになる
        

## テーブル同士を比較する - 集合の相当性チェック[応用編]

- 基本編は事前に2つのテーブルの行数を調べる必要があったが、応用編ではこの事前チェックなしで正しいかどうか確認する
- 集合論 相当性を調べる公式
    - (A⊆B) かつ (A⊇B)  <=> A=B
        
        <aside>
        💡 AがBを含み、かつBがAを含むなら、両者は等しい
        
        </aside>
        
    - (A∪B) =  (A∩B) <=> A=B
        
        <aside>
        💡 ABの集合の和とABの集合の交差が等しいなら、両者は等しい
        
        </aside>
        
- SQL
    - `(A UNION B) EXCEPT (A INTERSECT B)`の結果が空集合になっていれば、二つのテーブルは等しい
    
    ```sql
    -- 二つのテーブルを比較して正しければ「等しい」、そうでなければ「異なる」を返すクエリ
    SELECT CASE WHEN COUNT(*) = 0 
                THEN '等しい'
                ELSE '異なる' END AS result
      FROM ((SELECT * FROM  tbl_A
             UNION
             SELECT * FROM  tbl_B) 
             EXCEPT
            (SELECT * FROM  tbl_A
             INTERSECT 
             SELECT * FROM  tbl_B)) TMP;
    ```
    
    - 処理が高度になった分、パフォーマンスはUNIONの時と比べて落ちる
    - INTERSECT, EXCEPTがないMySQLでは使えない
    - 相違した行を出力する
        
        ```sql
        /* テーブル同士のdiff */
        (SELECT * FROM  tbl_A
           EXCEPT
         SELECT * FROM  tbl_B)
         UNION ALL
        (SELECT * FROM  tbl_B
           EXCEPT
         SELECT * FROM  tbl_A);
        ```
        

## 差集合で関係除算を表現する

Ex. 社員の技術情報テーブル Skillsのテーブルのskillを全て持っている社員をEmpSkillsから取得したい

- テーブル
    - Skills
        
        
        | skill |
        | --- |
        | Oracle |
        | UNIX |
        | Java |
    - EmpSkills
        
        
        | emp | skill |
        | --- | --- |
        | 相田 | Oracle |
        | 相田 | UNIX |
        | 相田 | Java |
        | 相田 | C# |
        | 上崎 | UNIX |
        | 上崎 | ORacle |
        | 上崎 | PHP |
        
- SQL
    
    ```sql
    -- 差集合で関係除算 (剰余を持った除算)
    SELECT DISTINCT emp
      FROM EmpSkills ES1
     WHERE NOT EXISTS
            (SELECT skill
               FROM Skills
             EXCEPT
             SELECT skill
               FROM EmpSkills ES2
              WHERE ES1.emp = ES2.emp);
    ```
    

## 等しい部分集合を見つける

Ex. 供給業者と取り扱っている部品テーブルから、全く同じ部品と数を取り扱っている業者を取得する

- テーブル
    
    
    | sup(供給業者) | part(部品) |
    | --- | --- |
    | A | ボルト |
    | A | ナット |
    | A | パイプ |
    | B | ボルト |
    | B | パイプ |
    | C | ボルト |
    | C | ナット |
    | C | パイプ |
    | D | ボルト |
    | D | パイプ |
    | E | ヒューズ |
    | E | ナット |
    | E | パイプ |
    | F | ヒューズ |
    
    - AとC、BとDが同じ
    
- SQL
    
    ```sql
    SELECT SP1.sup, SP2.sup
      FROM SupParts SP1, SupParts SP2 
     WHERE SP1.sup < SP2.sup              /* 業者の組み合わせを作る(結合) */
       AND SP1.part = SP2.part            /* 条件1. 同じ種類の部品を扱う */
    GROUP BY SP1.sup, SP2.sup 
    HAVING COUNT(*) = (SELECT COUNT(*)    /* 同数の部品を扱う */
                         FROM SupParts SP3 
                        WHERE SP3.sup = SP1.sup)
       AND COUNT(*) = (SELECT COUNT(*) 
                         FROM SupParts SP4 
                        WHERE SP4.sup = SP2.sup);
    ```
    
    - SQL 途中処理イメージ 条件1. 同じ種類の部品を扱う
        
        ```sql
        SELECT SP1.sup, SP2.sup
          FROM SupParts SP1, SupParts SP2 
         WHERE SP1.sup < SP2.sup              /* 業者の組み合わせを作る(結合) */
           AND SP1.part = SP2.part            /* 条件1. 同じ種類の部品を扱う */
        ```
        
        | SP1.sup | SP1.part | SP2.sup | SP2.part |
        | --- | --- | --- | --- |
        | A | ボルト | B | ボルト |
        | A | ボルト | C | ボルト |
        | A | ボルト | D | ボルト |
        | A | ナット | C | ナット |
        | A | ナット | E | ナット |

## 重複行を削除する高速クエリ

- イメージテーブル 果物と値段
    
    
    | りんご | 50 |
    | --- | --- |
    | みかん | 100 |
    | みかん | 100 |
    | みかん | 100 |
    | バナナ | 80 |
- SQL
    - 差集合で求める
        
        ```sql
        -- 重複行を削除する高速なクエリ1: 補集合をEXCEPTで求める
        
        DELETE FROM Products
         WHERE rowid IN ( SELECT rowid
                            FROM Products 
                          EXCEPT
                          SELECT MAX(rowid)
                            FROM Products 
                           GROUP BY name, price);
        ```
        
    - NOT IN演算子を使用する
        
        ```sql
        -- 重複行を削除する高速なクエリ２: 補集合をNOT INで求める
        
        DELETE FROM Products 
         WHERE rowid NOT IN ( SELECT MAX(rowid)
                                FROM Products 
                               GROUP BY name, price);
        ```
UNION ALLは冪等ではない