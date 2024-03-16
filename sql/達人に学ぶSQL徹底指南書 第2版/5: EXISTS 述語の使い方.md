## 理論編

---

### 述語の定義

- 関数。戻り値が真理値になるもの

### 存在の階層

- `=`, `BETWEEN`, とEXISTSを比較すると大きな違いは引数が単一の値か集合か
    - `=`, `BETWEEN`は単一の値(スカラ値)のみ引数に取る (Ex. `age = 13`, `age BETWHEEN 6 AND 13`)
    - EXISTSは行の集合を引数にとる
        
        ```sql
        SELECT id
        	FROM Foo AS F
        WHERE EXISTS
        	( SELECT *
        			FROM Bar AS B
        		WHERE F.id=B.id
        	);
        ```
        
- 述語論理では上記のように入力のレベルに応じて、分類している
    - `=`, `BETWEEN`のように、一行を入力する述語を「一階の述語」
    - EXISTSのように行の集合を入力とする述語を「二階の述語」

### 全称量化と存在量化

量化とは、全称量子化と存在量子化の二つに分類される

- 全称量子化
    - 「全てのx(行)が条件Pを満たす」という文を書くための道具
    - SQLには全称量子化に対応する術語が存在しない
- 存在量子化
    - 「条件Pを満たすx(行)が(少なくともひとつ)存在する」という文を書くための道具
    - EXISTS術語はこれにあたる
- SQLで、全称量子化を存在量子化にするには
    - 「全ての行が条件Pを満たす」のを、「条件Pを満たさない行は存在しない」へ変換する必要がある

## 実践編

---

### テーブルに存在「しない」データを探す

- テーブルに存在するデータのうち、何らかの条件を満たすものを選択するのが一般的なケースだが、時に「存在しないデータ」を探さなければならないケースがある
- Ex. 各会議に出席していない人物を求める
    - Meetingテーブル
        
        
        | meeting | person |
        | --- | --- |
        | 第一回 | 伊藤 |
        | 第一回 | 水島 |
        | 第一回 | 坂東 |
        | 第二回 | 伊藤 |
        | 第二回 | 宮田 |
        | 第三回 | 水島 |
        | 第三回 | 坂東 |
        | 第三回 | 宮田 |
    - データが存在するか否かを表す、次数の高い問題設定となっている
    - SQL
        - 考え方として、全員が出席した集合を作成しそこから現実的に出席した集合を引き算すれば良い
        - 全員が出席した集合
            
            ```sql
            
            SELECT DISTINCT M1.meeting, M2.person
              FROM Meetings M1 CROSS JOIN Meetings M2;
            ```
            
        - 実際の出席した集合を引き算する
            
            ```sql
            -- 欠席者だけを求めるクエリ：その１ 存在量化の応用
            SELECT DISTINCT M1.meeting, M2.person
              FROM Meetings M1 CROSS JOIN Meetings M2
             WHERE NOT EXISTS -- NOT EXISTSで、実際の出席した集合に存在しない集合とtなる
                    (SELECT *　-- 実際の出席した集合
                       FROM Meetings M3
                      WHERE M1.meeting = M3.meeting
                        AND M2.person = M3.person);
            ```
            
        
        <aside>
        💡 NOT EXISTSは差集合演算としての機能を持っている
        
        </aside>
        

### 全称量化に慣れる

- SQLでは「全ての行について~」という全称量の表現を、「~でない行が一つも存在しない」という二重否定文の存在量の表現へ変換する必要がある
- Ex に使用する TestScoresテーブル
    
    
    | student_id | subject | score |
    | --- | --- | --- |
    | 100 | 算数 | 100 |
    | 100 | 国語 | 80 |
    | 100 | 理科 | 80 |
    | 200 | 算数 | 80 |
    
    …
    
- Ex. 全ての教科で、50点以上取っている生徒を抽出する
    
    存在量子化に置き換えると、「50点未満である教科が一つも存在しない」になる
    
    ```sql
    
    SELECT DISTINCT student_id
      FROM TestScores TS1
     WHERE NOT EXISTS -- 以下の条件を満たす行が存在しない
            (SELECT *
               FROM TestScores TS2
              WHERE TS2.student_id = TS1.student_id
                AND TS2.score < 50); --50点未満の強化
    ```
    
- Ex.「 算数の点数が80点以上、国語の点数が50点以上」の生徒を抽出する
    - 一見すると全称量化に見えないが、次のように読み替えてみると全称量化であることが判明する
        
        *「ある学生の全ての行について、教科が算数ならば80点以上であり教科が国語であれば50点以上である」*
        
        →条件を分岐させた量化
        
        - 二重否定の存在量子化
            - *教科が算数ならば80点未満か、国語であれば50点未満の学生の行は一つも存在しない*
    - SQL
        
        ```sql
        SELECT student_id
          FROM TestScores TS1
         WHERE subject IN ('算数', '国語')
           AND NOT EXISTS　-- 算数が80点未満か国語が50点未満の生徒に属さない生徒
                (SELECT *
                   FROM TestScores TS2
                  WHERE TS2.student_id = TS1.student_id
                    AND 1 = CASE WHEN subject = '算数' AND score < 80 THEN 1
                                 WHEN subject = '国語' AND score < 50 THEN 1
                                 ELSE 0 END)
         GROUP BY student_id
        ```
        

p101

列と値を入れ替える IN句

p102

まとめ

EXISTのみ、行の集合を引数に取る

高階関数の一種と見做せる

全称量子化に相当する演算子がない。