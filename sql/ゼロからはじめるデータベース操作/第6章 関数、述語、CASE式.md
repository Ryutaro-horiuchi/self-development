# 関数

- NULLに対しては、ほとんどの関数がNULLを返す決まりになっている

## 算術関数

---

### ABS - 絶対値を返す

```sql
ABS(数値)
```

### MOD - 剰余(あまり)

```sql
MOD(被除数, 除数)
```

```sql
mysql> select MOD(7,3);
+----------+
| MOD(7,3) |
+----------+
|        1 |
+----------+
```

- SQL Serverだけ使えない

### ROUND - 四捨五入

```sql
ROUND(対象数、丸めの桁数)
```

```sql
mysql> select ROUND(3.14159265, 3);
+----------------------+
| ROUND(3.14159265, 3) |
+----------------------+
|                3.142 |
+----------------------+
```

## 文字列関数

### || - 連結

```sql
文字列1 || 文字列2
```

- SQL ServerとMySQLでは使えない
    - MySQLでは、CONCAT関数を使用する
    
    ```sql
    SELECT CONCAT('あいう', 'えお') as CONCAT;
    +-----------------+
    | CONCAT          |
    +-----------------+
    | あいうえお        |
    +-----------------+
    ```
    

### LENGTH - 文字の長さ

```sql
LENGTH(文字列)
```

- 1文字の長さを2以上とするLENGTH関数もある
    - 何の単位で1と数えるかで変わってくる
        - MySQLでは、バイト数を数えている
            - 半角英語は1バイト、日本語の全角文字は2バイトとなるため、文字数とバイト数が合わないことになる

### LOWER - 小文字

- アルファベットの文字列を全て小文字にする

```sql
LOWER(文字列)
```

### UPPER - 大文字

- アルファベットの文字列を全て大文字にする

```sql
UPPER(文字列)
```

### REPLACE - 文字列の置換

```sql
REPLACE(対象文字列, 置換前の文字列, 置換後の文字列)
```

```sql
SELECT REPLACE('山田太郎です', '山田', '佐藤') AS 'REPLACE';
+--------------------+
| REPLACE            |
+--------------------+
| 佐藤太郎です         |
+--------------------+
```

### SUBSTRING - 文字列の切り出し

```sql
SUBSTRING(対象文字列 FROM 切り出し開始位置 FOR 切り出す文字数)
```

```sql
SELECT SUBSTRING('山田太郎です' FROM 3 FOR 4) AS 'REPLACE';
+--------------+
| REPLACE      |
+--------------+
| 太郎です     |
+--------------+
```

- PostgreSQL, MySQLのみ使用できる

## 日付関数

---

### CURRENT_DATE - 現在の日付

```sql
SELECT CURRENT_DATE;
```

```sql
SELECT CURRENT_DATE;
+--------------+
| CURRENT_DATE |
+--------------+
| 2024-02-20   |
+--------------+
```

### CURRENT_TIME - 現在の時間

```sql
SELECT CURRENT_TIME;
```

```sql
SELECT CURRENT_TIME;
+--------------+
| CURRENT_TIME |
+--------------+
| 06:57:08     |
+--------------+
```

### CURRENT_TIMESTAMP - 現在の日時

```sql
SELECT CURRENT_TIMESTAMP;
```

```sql
SELECT CURRENT_TIMESTAMP;
+---------------------+
| CURRENT_TIMESTAMP   |
+---------------------+
| 2024-02-20 06:58:20 |
+---------------------+
```

### EXTRACT - 日付要素の切り出し

```sql
EXTRACT(日付要素 FROM 日付)
```

```sql
SELECT CURRENT_TIMESTAMP AS NOW, EXTRACT(YEAR FROM NOW);
```

```sql
SELECT CURRENT_TIMESTAMP AS NOW, EXTRACT(YEAR FROM CURRENT_TIMESTAMP) AS YEAR;
+---------------------+------+
| NOW                 | YEAR |
+---------------------+------+
| 2024-02-20 07:00:39 | 2024 |
+---------------------+------+
```

## 変換関数

---

### 型変換 - CAST

```sql
CAST(変換前の値 AS 変換するデータ)
```

- 型変換を行う背景
    - 型が合わないデータを演算したりするときに、型が不一致であるが故のエラーが生じたり、暗黙の型変換を生じさせて処理速度を低下させるといった不都合が起きるため

### COALESCE(コアレス) - NULLを値へ変換

```sql
SELECT str2 from SampleStr;
+-----------+
| str2      |
+-----------+
| えお      |
| def       |
| 太郎      |
| NULL      |
| あああ    |
| NULL      |
...
|           |
+-----------+

SELECT COALESCE(str2, 'NULLです')   FROM SampleStr;
+------------------------------+
| COALESCE(str2, 'NULLです')   |
+------------------------------+
| えお                         |
| def                          |
| 太郎                         |
| NULLです                     |
| あああ                       |
| NULLです                     |
| NULLです                     |
| NULLです                     |
| abc                          |
| abc                          |
| ッ                           |
+------------------------------+
```

# 述語

戻り値が真理値になる関数のこと

比較演算子も、述語の一つ(述語)

## LIKE述語 - 文字列の部分一致検索

### 特殊記号

- `%` : 0文字以上の任意の文字列を表す
- `_` : 任意の1文字を表す

### 前方一致

```sql
SELECT *
  FROM SampleLike
 WHERE strcol LIKE 'ddd%';
```

### 中間一致

```sql
SELECT *
  FROM SampleLike
 WHERE strcol LIKE '%ddd%';
```

### 後方一致

```sql
SELECT *
  FROM SampleLike
 WHERE strcol LIKE '%ddd';
```

## BETWEEN述語 - 範囲検索

- Ex. 販売単価が100 ~ 1000円の商品を取得する
    
    ```sql
    SELECT shohin_mei, hanbai_tanka
      FROM Shohin
     WHERE hanbai_tanka BETWEEN 100 AND 1000;
    ```
    
    - この場合、hanbai_tankaが100と1000のレコードも含まれる

## IS NULL述語 / IS NOT NULL述語

ある列がNULLであるか、ないかを取得するには、IS NULL と IS NOT NULLを使用する

```sql
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IS NULL;
```

## IN述語 - ORの便利な省略形

- OR構文を簡潔に書けるようになる
    
    ```sql
    SELECT shohin_mei, shiire_tanka
      FROM Shohin
     WHERE shiire_tanka IN (320, 500, 5000);
    ```
    
- 引数にサブクエリを使用することができる
    
    ```sql
    SELECT shohin_mei, hanbai_tanka
      FROM Shohin
     WHERE shohin_id IN (SELECT shohin_id 
                           FROM TenpoShohin
                          WHERE tenpo_id = '000C');
    ```
    
- `NOT IN` を用いて「否定」することも可能

## EXISTS述語 - レコードの存在有無を調べる

- ある条件に合致するレコードの存在有無を調べる
- レコードが存在すれば真、存在しなければ偽を返す
- EXISTSの引数は常に相関サブクエリを使用する
    - サブクエリで、SELECT * とするのは慣習
- `NOT EXISTS`を用いて「否定」することも可能
- Ex.
    
    ```sql
    SELECT shohin_mei, hanbai_tanka
      FROM Shohin AS S
      WHERE EXISTS (SELECT *
                     FROM TenpoShohin AS TS
                    WHERE TS.tenpo_id = '000C'
                      AND TS.shohin_id = S.shohin_id);
    +-----------------------+--------------+
    | shohin_mei            | hanbai_tanka |
    +-----------------------+--------------+
    | カッターシャツ        |         4000 |
    | 包丁                  |         3000 |
    | フォーク              |          500 |
    | おろしがね            |          880 |
    +-----------------------+--------------+
    ```
    

# CASE式

- 条件分岐で結果を得たいときに使用する
- 単純CASE式と検索CASE式の2種類に分かれる
- ELSEとENDの書き漏れに気をつける
    - (ELSE句読点は省略可能だが、可読性の観点で省略しない)
- select文の結果を柔軟に得るときに使用可能

## 検索CASE式

---

- フォーマット
    
    ```sql
    CASE WHEN <評価式>  THEN  式
        WHEN <評価式>   THEN  式
        WHEN <評価式>   THEN  式
        ...
        ELSE <式>
    END
    ```
    
    - 最初のWHEN句から評価が始まる
        - 真になればTHEN句で指定された式が戻されてCASE式全体が終了する
        - 偽であれば、次のWHEN句の評価にうつる
        - 最後のWHEN句まで繰り返して、真にならなかった場合はELSE句で指定された式が戻されて終了となる
- Ex. 商品分類列の結果に接頭辞アルファベットをつける
    
    ```sql
    SELECT shohin_mei,
           CASE WHEN shohin_bunrui = '衣服'         THEN 'A：' || shohin_bunrui
                WHEN shohin_bunrui = '事務用品'     THEN 'B：' || shohin_bunrui
                WHEN shohin_bunrui = 'キッチン用品' THEN 'C：' || shohin_bunrui
                ELSE NULL
           END AS abc_shohin_bunrui
      FROM Shohin;
    
    +-----------------------+------------------------+
    | shohin_mei            | abc_shohin_bunrui      |
    +-----------------------+------------------------+
    | Tシャツ               | A：衣服                |
    | 穴あけパンチ          | B：事務用品            |
    | カッターシャツ        | A：衣服                |
    | 包丁                  | C：キッチン用品        |
    | 圧力鍋                | C：キッチン用品        |
    | フォーク              | C：キッチン用品        |
    | おろしがね            | C：キッチン用品        |
    | ボールペン            | B：事務用品            |
    +-----------------------+------------------------+
    ```
    
- Ex. 行を列に変換する
    
    ```sql
    --商品分類ごとに販売単価を合計した結果を行列変換する
    SELECT SUM(CASE WHEN shohin_bunrui = '衣服'         THEN hanbai_tanka ELSE 0 END) AS sum_tanka_ihuku,
           SUM(CASE WHEN shohin_bunrui = 'キッチン用品' THEN hanbai_tanka ELSE 0 END) AS sum_tanka_kitchen,
           SUM(CASE WHEN shohin_bunrui = '事務用品'     THEN hanbai_tanka ELSE 0 END) AS sum_tanka_jimu
      FROM Shohin;
    ```
    

## 単純CASE式

---

- フォーマット
    
    ```sql
    CASE <式>
    		WHEN <式>  THEN  式
        WHEN <式>   THEN  式
        WHEN <式>   THEN  式
        ...
        ELSE <式>
    END
    ```
    
    - 検索CASE式と違う点は、最初のCASE式で評価対象になる式を先に決めてしまう点
- Ex. 商品分類列の結果に接頭辞アルファベットをつける(単純CASE式)
    
    ```sql
    SELECT shohin_mei,
           CASE shohin_bunrui
                WHEN '衣服'         THEN 'A：' || shohin_bunrui
                WHEN '事務用品'     THEN 'B：' || shohin_bunrui
                WHEN 'キッチン用品' THEN 'C：' || shohin_bunrui
                ELSE NULL
            END AS abc_shohin_bunrui
      FROM Shohin;
    
    +-----------------+-------------------+----------------+
    | sum_tanka_ihuku | sum_tanka_kitchen | sum_tanka_jimu |
    +-----------------+-------------------+----------------+
    |            5000 |             11180 |            600 |
    +-----------------+-------------------+----------------+
    ```
    
    - 検索の時と違い、shohin_bunruiをWHEN句で再度書く必要がない

## CASE式の方言

---

- MySQLでは、IF文を使用できる
- Ex. 商品分類列の結果に接頭辞アルファベットをつける(IF文)
    
    ```sql
    SELECT  shohin_mei,
            IF( IF( IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL)
                	    IS NULL AND shohin_bunrui = '事務用品', CONCAT('B：', shohin_bunrui), 
                	IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL))
                        IS NULL AND shohin_bunrui = 'キッチン用品', CONCAT('C：', shohin_bunrui), 
                        IF( IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL)
                	    IS NULL AND shohin_bunrui = '事務用品', CONCAT('B：', shohin_bunrui), 
                	IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL))) AS abc_shohin_bunrui
      FROM Shohin;
    ```
    
    - 記述できる条件がCASE式よりも狭いためメリットがない。CASE式の方言を使わないことを推奨