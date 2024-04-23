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