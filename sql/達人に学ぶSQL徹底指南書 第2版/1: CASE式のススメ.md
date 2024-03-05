## CASE式の注意点

- 各分岐が返すデータ型の統一
- ENDを書き忘れない
- ELSE句は必ず書く

## CASE式　応用

---

### 既存のコード体系を新しい体系に変換して集計する

- 既存のコード体系から、分析用のコード体系に変換して、その単位で集計したいという要件
    - Ex.  県単位から地方単位に集計したい
        - 集計元の表
            
            
            | pref_name(県名) | population(人口) |
            | --- | --- |
            | 徳島 | 100 |
            | 香川 | 200 |
            | 愛媛 | 150 |
            | 福岡 | 300 |
            | 佐賀 | 100 |
            | 長崎 | 200 |
            | 東京 | 50 |
        - 求めたい集計
            
            
            | 地方名 | population(人口) |
            | --- | --- |
            | 四国 | 650 |
            | 九州 | 600 |
            | その他 | 450 |
        - SQL (SELECT句とGROUP BY句に同じCASE式を書く)
            
            ```sql
            -- 県名を地方名に再分類する
            SELECT CASE pref_name
                      WHEN '徳島' THEN '四国'
                      WHEN '香川' THEN '四国'
                      WHEN '愛媛' THEN '四国'
                      WHEN '高知' THEN '四国'
                      WHEN '福岡' THEN '九州'
                      WHEN '佐賀' THEN '九州'
                      WHEN '長崎' THEN '九州'
                    ELSE 'その他' END AS district,
                   SUM(population)
              FROM PopTbl
             GROUP BY CASE pref_name
                        WHEN '徳島' THEN '四国'
                        WHEN '香川' THEN '四国'
                        WHEN '愛媛' THEN '四国'
                        WHEN '高知' THEN '四国'
                        WHEN '福岡' THEN '九州'
                        WHEN '佐賀' THEN '九州'
                        WHEN '長崎' THEN '九州'
                      ELSE 'その他' END AS district,
            ```
            
        - SQL (ASキーワードを使用して、CASE式を一つにする)
            
            ```sql
            SELECT CASE pref_name
                      WHEN '徳島' THEN '四国'
                      WHEN '香川' THEN '四国'
                      WHEN '愛媛' THEN '四国'
                      WHEN '高知' THEN '四国'
                      WHEN '福岡' THEN '九州'
                      WHEN '佐賀' THEN '九州'
                      WHEN '長崎' THEN '九州'
                    ELSE 'その他' END AS district,
                   SUM(population)
              FROM PopTbl
             GROUP BY district
            
            ```
            
            - PostgreSQLとMySQLでは使用できる
                - SELECT句のリストを先にスキャンして、列の計算を事前に行なっている

### 異なる条件の集計を1つのSQLで行う

- Ex.  県別・性別に人口を集計したい
    - 集計元の表
        
        
        | pref_name(県名) | sex(性別) | population(人口) |
        | --- | --- | --- |
        | 徳島 | 1 | 100 |
        | 徳島 | 2 | 120 |
        | 香川 | 1 | 200 |
        | 香川 | 2 | 180 |
        | 愛媛 | 1 | 150 |
        | 福岡 | 2 | 300 |
        | 佐賀 | 1 | 100 |
        | 長崎 | 2 | 200 |
    - 求めたい集計
        
        
        | pref_name(県名) | 男 | 女 |
        | --- | --- | --- |
        | 徳島 | 100 | 120 |
        | 香川 | 200 | 180 |
        | 愛媛 | 150 | 0 |
        | 福岡 | 0 | 300 |
        | 佐賀 | 100 | 0 |
        | 長崎 | 0 | 200 |
    - 普段だとWHERE句を使用。2回SQLを発行する
        
        ```sql
        -- 男性の人口
        SELECT pref_name,
               population
          FROM PopTbl2
         WHERE sex = '1';
        
        -- 女性の人口
        SELECT pref_name,
               population
          FROM PopTbl2
         WHERE sex = '2';
        ```
        
    - CASE式、集約関数を使用して、1回SQLを発行する
        
        ```sql
        SELECT pref_name,
               --男性の人口
               SUM( CASE WHEN sex = '1' THEN population ELSE 0 END) AS cnt_m,
               --女性の人口
               SUM( CASE WHEN sex = '2' THEN population ELSE 0 END) AS cnt_f
          FROM PopTbl2
         GROUP BY pref_name;
        
        ```
        
        - 行持ち(行のデータ)から列持ちに展開している

<aside>
💡 WHERE句で条件分岐させるのは素人のやること。プロはSELECT句で分岐させる

</aside>

### CHECK制約で複数の列を定義する

- Ex. 会社の人事テーブルにて、女性である場合給与は20万円以下という制約
    
    ```sql
    CONSTRAINT check_salary CHECK
       ( CASE WHEN sex = '2'
              THEN CASE WHEN salary <= 200000
                        THEN 1 ELSE 0 END
         ELSE 1 END = 1 )
    ```
    
    - CONSTRAINT
        
        このキーワードは、データベースのテーブルに適用される制約を定義するために使用されます
        
    - CHECK
        
        テーブルの列に対する条件を指定します。
        
    - 「条件法」と呼ばれる条件式に当たる
        - PならばQである → 「社員の性別が女性ならば、給料は20万円以下である」

### 条件を分岐させてアップデートする

- 主キーを変更させるときに活用できる
    - ユニーク系を一部のRDBMS入れ替えも可能。
        - CASE式の分岐による更新は「一気に」行われるため重複しない
        - PostgreSQL, MySQLはエラーとなる
    - Ex. CASE式を使わない。3回SQLを発行する
        
        ```sql
        --1. aをワーク用の値dへ避難
        UPDATE SomeTable
           SET p_key = 'd'
         WHERE p_key = 'a';
        
        --2. bをaへ変換
        UPDATE SomeTable
           SET p_key = 'a'
         WHERE p_key = 'b';
        
        --3. dをbへ変換
        UPDATE SomeTable
           SET p_key = 'b'
         WHERE p_key = 'd';
        
        ```
        
    - Ex. CASE式を使う。1回SQLを発行する
        
        ```sql
        -- CASE式で主キーを入れ替える
        
        UPDATE SomeTable
           SET p_key = CASE WHEN p_key = 'a'
                            THEN 'b'
                            WHEN p_key = 'b'
                            THEN 'a'
                       ELSE p_key END
         WHERE p_key IN ('a', 'b');
        ```
        

### テーブルのマッチング

- Ex.  資格予備校で各講座が各月で実施されているか集計する
    - 集計元の表
        - CourseMaster
            
            
            | course_id | course_name |
            | --- | --- |
            | 1 | 経理入門 |
            | 2 | 財務知識 |
            | 3 | 簿記検定開講講座 |
            | 4 | 税理士 |
        - OpenCourses
            
            
            | month | course_id |
            | --- | --- |
            | 201806 | 1 |
            | 201806 | 3 |
            | 201806 | 4 |
            | 201807 | 4 |
            | 201808 | 2 |
            | 201808 | 4 |
    - 求めたい集計
        
        
        | course_name | 6月 | 7月 | 8月 |
        | --- | --- | --- | --- |
        | 経理入門 | ○ | × | × |
        | 財務知識 | × | × | ○ |
        | 簿記検定開講講座 | ○ | × | × |
        | 税理士 | ○ | ○ | ○ |
- Ex. CASE式 IN述語
    
    ```sql
    -- テーブルのマッチング: IN述語の利用
    SELECT course_name,
           CASE WHEN course_id IN
                        (SELECT course_id FROM OpenCourses
                          WHERE month = 201806) THEN '○'
                ELSE '×' END AS "6月",
           CASE WHEN course_id IN
                        (SELECT course_id FROM OpenCourses
                          WHERE month = 201807) THEN '○'
                ELSE '×' END AS "7月",
           CASE WHEN course_id IN
                        (SELECT course_id FROM OpenCourses
                          WHERE month = 201808) THEN '○'
                ELSE '×' END AS "8月"
      FROM CourseMaster;
    
    ```
    
- Ex. CASE式 EXISTS述語
    
    ```sql
    SELECT CM.course_name,
           CASE WHEN EXISTS
                      (SELECT course_id FROM OpenCourses OC
                        WHERE month = 201806
                          AND OC.course_id = CM.course_id) THEN '○'
                ELSE '×' END AS "6月",
           CASE WHEN EXISTS
                      (SELECT course_id FROM OpenCourses OC
                        WHERE month = 201807
                          AND OC.course_id = CM.course_id) THEN '○'
                ELSE '×' END AS "7月",
           CASE WHEN EXISTS
                      (SELECT course_id FROM OpenCourses OC
                        WHERE month = 201808
                          AND OC.course_id = CM.course_id) THEN '○'
                ELSE '×' END AS "8月"
      FROM CourseMaster CM;
    
    ```
    
- パフォーマンスはINより、EXISTSの方が高い
    - サブクエリでは主キーのインデックスが使えるため

### CASE式の中で集約関数を使う

- Ex. 学生クラブ
    - 集計元の表　StudentClub
        
        
        | std_id | club_id | club_name | main_club_flug |
        | --- | --- | --- | --- |
        | 100 | 1 | 野球 | Y |
        | 100 | 2 | 吹奏楽 | N |
        | 200 | 2 | 吹奏楽 | N |
        | 200 | 3 | バトミントン | Y |
        | 200 | 4 | サッカー | N |
        | 300 | 4 | サッカー | N |
        | 400 | 5 | 水泳 | N |
        | 500 | 6 | 囲碁 | N |
        - 複数のクラブを掛け持ちしている学生は、主なクラブがどれかを表すmain_club_flugにYかNの値が入る
        - 一つのクラウに専念している学生は、main_club_flugにNの値が入る
    - 集計元の表から、以下取得したい
        - 1つだけのクラブに所属している学生は、そのクラブIDを取得する
        - 複数のクラブを掛け持ちしている学生については、主なクラブIDを取得する
    - Ex. CASE式を使わない。HAVING句、WHERE句を使用して2回SQLを発行する
        
        ```sql
        -- 条件1: 1つのクラブに専念している学生を選択
        SELECT std_id, MAX(club_id) AS main_club
          FROM StudentClub
         GROUP BY std_id
        HAVING COUNT(*) = 1;
        
        -- 条件2: クラブを掛け持ちしている学生を選択
        SELECT std_id, club_id AS main_club
          FROM StudentClub
         WHERE main_club_flg = 'Y';
        ```
        
    - Ex. CASE式を使って、1回SQLを発行する
        
        ```sql
        SELECT std_id,
               CASE WHEN COUNT(*) = 1 -- 1つのクラブに専念する学生の場合
                    THEN MAX(club_id)
                    ELSE MAX(CASE WHEN main_club_flg = 'Y'
                                  THEN club_id
                                  ELSE NULL END) END AS main_club
          FROM StudentClub
         GROUP BY std_id;
        ```
        

<aside>
💡  HAVING句で条件分岐させるのは素人のやること。プロはSELECT句で分岐させる

</aside>

## まとめ

- CASE式は列名や定数を書ける場所には常に書くことができる
- CASE式を駆使することで、複数のSQL文を一つにまとめられ、可読性もパフォーマンスをも向上していいことづくし