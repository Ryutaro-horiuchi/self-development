## 前提

- NULLが列に含まれていると、意図しない結果を得ることがある
- RDBはNULLを持ちこんだことにより、3値論理にならざるを得なかった(true, false, unknown)

## 理論編

---

NULLには2種類

- 未知
    - 今はわからないけれど、条件がそろえば分かるもの
    - Ex. サングラスをかけた人の目の色
- 適用不能(不明、論理的に不可能)
    - どう頑張ってもわからないもの
    - Ex. 冷蔵庫の目の色。男性の出産回数

### NULLは等号を使えない

- NULLに比較述語を使用すると、結果は全てUNKNOWNになる
    - 比較述語は値のみ使用できる
    - NULLは値ではなく、「値がない」ことを示す視覚的なマークに過ぎないため
- `WHERE col1 = NULL`と書けないのは、WHERE句が条件に合致したtrueの値を返すもののみ、抽出するため。この書き方だと、全てUNKNOWNとなり、何も返さない
    
    → `WHERE col1 is NULL` と書く
    

### unknown, 第三の真理値

- 3値論理の真理表(NOT)
    
    
    | x | NOT x |
    | --- | --- |
    | true | false |
    | unknown | unknown |
    | false | true- |
- 3値論理 AND, ORの優先順位
    - ANDの場合 `false > unknown > true`
    - ORの場合 `true > unknown > false`

## 実践編

---

### SQLの世界では排中律が成立しない

- 排中律とは
    - 命題とその否定をまたはつなげてできる命題は全て真であるという命題を、2値論理で排中律と呼ぶ
        - Ex. ジョンは20歳か、20歳でないかどちらかである
        - SQL
            
            ```sql
            -- 年齢が20歳か、20歳でない生徒を選択する
            SELECT *
            	FROM Students
            WHERE age = 20 OR age <> 20;
            
            ```
            
- SQLの世界で、下記のStudentテーブルがあるとして、ジョンの年齢がnullだと排中律が成立しない
    
    
    | name | age |
    | --- | --- |
    | ブラウン | 22 |
    | ジョン |  |
    | ボキー | 21 |
    - `WHERE age = 20 OR age <> 20;`
        - →ジョンのテーブルを判定するときは、`WHERE NULL = 20 OR NULL <> 20`、となり、`unknown`が返ってくるため、ジョンのレコードは抽出されない
    - NULLを含めるには、次の条件を追加する必要がある
        - `age IS NULL`
    - 上記のような問題に対してNULLを値として扱う述語が用意されている
        - 標準SQLでは、`IS DISTINCT FROM`
        - MySQLでは、`<=>`の比較演算子

### NOT IN と NOT EXISTは同値変換できない

- NOT INの選択肢にNULLがあると、結果は常に空になる
    - Ex. 学校のClassテーブル
        - Class_A
        
        | name | age | city |
        | --- | --- | --- |
        | ブラウン | 22 | 東京 |
        | ラリー | 19 | 埼玉 |
        | ボギー | 21 | 千葉 |
        - Class_B
            
            
            | name | age | city |
            | --- | --- | --- |
            | 齊藤 | 22 | 東京 |
            | 田尻 | 23 | 東京 |
            | 山田 | NULL | 東京 |
            | 和泉 | 18 | 千葉 |
            | 石川 | 19 | 神奈川 |
    - SQL: Bクラスの東京在住の生徒と年齢が一致しないAクラスの生徒を選択する
        - このSQLだと結果は空で、一行も返されない
            
            ```sql
            SELECT *
            	FROM Class_A
            WHERE age NOT IN
            		( SELECT age
            				FROM Class_B
            			WHERE city = '東京');
            ```
            
        - 処理の流れ
            
            ```sql
            1.サブクエリを実行して、年齢のリストを取得
            SELECT *
            FROM Class_A
            WHERE age NOT IN (22, 23, NULL);
            ```
            
            ```sql
            2. NOT INをNOTとINを使って同値変換
            SELECT *
            FROM Class_A
            WHERE NOT age IN (22, 23, NULL);
            ```
            
            ```sql
            3．IN述語をORで同値変換
            SELECT *
            FROM Class_A
            WHERE NOT ( (age = 22) OR (age = 23) OR (age = NULL) );
            ```
            
            ```sql
            4．ド・モルガンの法則を使って同値変換
            FROM Class_A
            WHERE NOT (age = 22) AND NOT(age = 23) AND NOT (age = NULL);
            ```
            
            ```sql
            5.NOTと＝を<>で同値変換
            SELECT *
            FROM Class_A
            WHERE (age <> 22) AND (age <> 23) AND (age <> NULL);
            ```
            
            ```sql
            6.NULLに<>を適用するとunknownになる
            SELECT *
            FROM Class_A
            WHERE (age <> 22) AND (age <> 23) AND unknown;
            ```
            
            ```sql
            7.ANDの演算にunknownが含まれると結果がtrueにならない（理論編のマトリックス参照）
            SELECT *
            FROM Class_A
            WHERE false
            -- または unknown
            ```
            

- p72
    
    NOT EXISTSは、trueかfalseしか返さない
    

p74

ALL述語, 極値関数

p76

NULLがある列に等号を用いるとunknownが帰る

unknownが論理演算に紛れ込むと、SQLが直感に反する動作をする

対処するには、段階的なステップに分けてSQLの動作を追うことが有効

→ 極力NULLは排除する

p81

OracleDBでは、NULLと文字列連結が標準SQLと仕様が違う