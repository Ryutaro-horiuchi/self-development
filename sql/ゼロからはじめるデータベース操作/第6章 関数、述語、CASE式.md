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