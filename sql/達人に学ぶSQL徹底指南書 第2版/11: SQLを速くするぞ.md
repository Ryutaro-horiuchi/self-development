## 効率の良い検索を利用する

---

### サブクエリを引数に取る場合、INよりもEXISTSを使う

- IN
    
    ```sql
    -- 遅い
    SELECT * 
    	FROM Class_A
    WHERE id IN (SELECT id FROM Class_B);
    ```
    
    - サブクエリの実行結果を一時的なワークテーブルに格納した後、全件走査する。
        - 一般的にワークテーブルにはインデックスが存在しない
- EXISTS
    
    ```sql
    -- 速い
    SELECT * 
    	FROM Class_A A
    WHERE EXISTS
    	(SELECT *
    		FROM Class_B B
    	WHERE A.id = B.id);
    ```
    
    - EXISTSの方が早い理由
        - ワークテーブルを作成しない
        - 結合キー(この場合はid)にインデックスが貼られていれば、Class_Bテーブルの実表は見に行かず、インデックスを参照するのみで済む
        - EXISTSは1行でも条件に合致する行を見つけたら、そこで検索を打ちきるので、INのように全表探索する必要がない
- とはいえ、INを使った場合でもパフォーマンスが上がるように改善を図る動きが出ている

### サブクエリを引数に取る場合、INよりも結合を使用する

```sql
-- INを結合で代用
SELECT A.id, A.name
	FROM Class_A A INNER JOIN Class_B B
	ON A.id = B.id;
```

- サブクエリがなくなったため、ワークテーブルを作成しない
- 片方のインデックスを使用する
- 両者インデックスがない場合は、EXISTSに群杯

## ソートを回避する

---

- ソートは暗黙理に行われている
    - ソートが発生する代表的な演算
        - GROUP BY
        - ORDER BY
        - 集約関数(SUM、COUNT、AVG、MAX、MIN)
        - DISTINCT
        - 集合演算子(UNION、INTERSECT、EXCEPT)
        - ウインドウ関数(RANK、ROW_NUMBER等)
- ソート処理がメモリでは足らず、ストレージを使うようになると、パフォーマンスが大きく低下する。
    
    → 無駄なソートは極力排除すべき
    

### 集合演算子は重複しないことがわかっている場合は、ALLオプションを付与する

- 集合演算子(UNION、INTERSECT、EXCEPT)は普通に使用すると、必ず重複排除のためのソートを行なっている
- 重複を気にしない、あらかじめ重複が発生しないことがわかっている場合はALLオプションを使用する

### DISTINCTを、EXISTSで代用する

- [EXISTSは1行でも条件に合致する行を見つけたら、そこで検索を打ちきるので、INのように全表探索する必要がない](https://www.notion.so/EXISTS-1-IN-554e404296684dcca50aa7f47ade1fc0?pvs=21)
- SQL DISTINCT
    
    ```sql
    SELECT DISTINCT I.item_no
    	FROM Items I INNER JOIN SalesHistory SH
    		ON I.item_no = SH.item_no;
    
    item_no // 1対多なので重複を取り除くためにDISTINCTを使用する
    -----
    10
    20
    30
    ```
    
- SQL
    
    ```sql
    SELECT item_no
    	FROM Items I
    WHERE EXISTS (SELECT *  
    								FROM SalesHistory SH
    							WHERE I.item_no = SH.item_no)
    
    item_no // 条件に合致するものが見つかれば、検索を打ち切るので重複が発生しない
    -----
    10
    20
    30
    ```
    

## 極値関数(MAX / MIN)でインデックスを使う

---

インテックスを使用している列を極値関数の引数に使用すれば、インデックスのスキャンで済ませて、実表への検索を回避できる

## WHRE句で書ける条件はHAVING句には書かない

---

- GROUP BY句による集約はソートの処理を行うため、事前にWHERE句で行数を絞り込んだ方が良い
- WHERE句では、インデックスが利用できるが、HAVING句時に使用する集約されたビューは元テーブルのインデックスまでは引き継がないケースが多い

## インデックスが本当に使用されているか

---

### 索引列に加工を行わない

- 列に加工を行なってしまうと、インデックスが使用できなくなる。インデックスを利用するときは、検索条件の右側で値の計算を行うようにする
- NG
    
    ```sql
    SELECT * FROM SomeTable WHERE col_1 * 1.1 > 100;
    ```
    
- OK
    
    ```sql
    SELECT * FROM SomeTable WHERE col_1 > 100 / 1.1;
    ```
    

### インデックス列にNULLが存在する

IS NULLや、IS NOT NULLを使用するとインデックスが利用されなかったりする

### 否定系を使っている

以下、否定系はインデックスを使用できない

- <>
- !=
- NOT IN

### ORを使っている

- col1,col2にそれぞれのインデックス、あるいは(col1, col2)に複合インデックスを使用しているいずれの場合も、ORを使って条件を結合すると、インデックスが使用できなくなる

```sql
SELECT * FROM SomTable WHERE col_1 > 100 OR col_2 = 'abc';
```

### 複合索引の場合に、列の順番を間違えている

- (col1, col2, col3)の順番で複合インデックスを使用している場合、作成されたインデックスの列の順番が重要
    - ○ `SELECT * FROM SomeTable WHERE col_1 = 10 AND col_2 = 100 AND col_3 = 500;`
    - ○ `SELECT * FROM SomeTable WHERE col_1 = 10 AND col_2 = 100;`
    - × `SELECT * FROM SomeTable WHERE col_1 = 10 AND col_3 = 500;`
    - × `SELECT * FROM SomeTable WHERE col_2 = 100 AND col_3 = 500;`
- 順番が崩れていてもインデックスを利用できるDBはあるが、正しい場合と比較するとパフォーマンスが落ちる

### 後方一致、または中間一致のLIKE述語を用いている

- LIKE述語は前方一致検索のみインデックスが使用される

### 暗黙の型変換を行なっている

- 暗黙の型変換はオーバヘッドを発生させるだけでなく、インデックスまで使用不可になる
    
    →  明示的な型変換を行う
    
- Ex. 文字列型 col_1に対する条件
    - × `SELECT * FROM SomeTable WHERE col_1 = 10;`
    - ○ `SELECT * FROM SomeTable WHERE col_1 = '10';`
    - ○`SELECT * FROM SomeTable WHERE col_1 = CAST(10, AS CHAR(2));`

## 中間テーブルを減らせ

### IN述語で複数のキーを利用する場合は、一箇所にまとめる

- BAD: IN述語に複数のサブクエリを使用している
    
    ```sql
    SELECT id,state,city
    	FROM Address1 A1
    WHERE state IN (SELECT state
    								 FROM Addresses2 A2
    								WHERE A1.id = A2.id)
    AND city IN (SELECT city
    							FROM Addresses2 A2
    						 WHERE A1.id = A2.id);
    ```
    
- GOOD キーを結合してサブクエリを一つにする
    
    ```sql
    SELECT *
    	FROM Address1 A1
    WHERE id || state || city IN (SELECT id || state || city
    																FROM Addresses2 A2);
    ```
    

### ビューの利用は計画的に

- 安易に複雑なビューを定義するとパフォーマンス低下につながる
- 以下のような演算が含まれている場合、非効率なSQLになる
    - 集約関数(SUM, MIN, MAX, AVG, COUNT)
    - 集合演算子(UNION, INTERSECT, EXCEPT等)
    
    <aside>
    💡 ビューで集約をしていたら要注意
    
    </aside>
    

## まとめ

- パフォーマンスチューニングの大事な点
    - ボトルネックを見つけて、重点的に解消すること
- 最大のボトルネック
    - ストレージ(ハードディスク)へのアクセス
        - アクセスしないように、メモリの増設などを検討する