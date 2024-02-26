## ウインドウ関数 (OLAP関数) 概要

---

- OLAP - データベースを使って、リアルタイムにデータ分析を行う処理のこと
- サポート状況
    - MySQLは5.7時点で未サポートだったが、8.0にてサポートされるようになった
- ウインドウ関数は、GROUP BY句のカット機能とORDER BY句の順序づけの機能を持ち合わせている
    - GROUP BYと違って、集約の機能はない

### ウインドウ関数の構文

```sql
<ウインドウ関数> OVER ([PARTITION BY <列リスト>] // PARTITION BY句は省略可
　　　　　　　　　　　　　    ORDER BY <ソート用列リスト>)
```

- ウインドウ関数として使える関数の種類
    - 集約関数(Ex. SUM, AVG, COUNT)
    - ウインドウ専用関数(RANK, DENSE_RANK)
        - ウインドウ専用関数の引数は常に空っぽ
- PARTITION BYで区切られたレコードの集合をウインドウと呼ぶ
    - PARTITION BYを指定しないと、テーブル全体が一つの大きなウインドウとして扱われる
- 原則SELECT句でのみ使用する

### RANK関数

- レコードのランキングを算出する関数。同順位が複数レコード存在した場合、後続の順位が飛ぶ
    
    例) 1位が3レコードある場合: 1位、 1位、 1位、 4位…
    
- Ex. 商品分類ごとに販売単価を安い順にランクづけ
    
    ```sql
    SELECT shohin_mei, shohin_bunrui, hanbai_tanka,
           RANK () OVER (PARTITION BY shohin_bunrui
                             ORDER BY hanbai_tanka) AS ranking
      FROM Shohin;
    
    +-----------------------+--------------------+--------------+---------+
    | shohin_mei            | shohin_bunrui      | hanbai_tanka | ranking |
    +-----------------------+--------------------+--------------+---------+
    | フォーク              | キッチン用品       |          500 |       1 |
    | おろしがね            | キッチン用品       |          880 |       2 |
    | 包丁                  | キッチン用品       |         3000 |       3 |
    | 圧力鍋                | キッチン用品       |         6800 |       4 |
    | ボールペン            | 事務用品           |          100 |       1 |
    | 穴あけパンチ          | 事務用品           |          500 |       2 |
    | Tシャツ               | 衣服               |         1000 |       1 |
    | カッターシャツ        | 衣服               |         4000 |       2 |
    +-----------------------+--------------------+--------------+---------+
    ```
    

### DENSE_RANK関数とROW_NUMBER関数

- DENSE_RANK関数
    - ランキングを算出するが、同順位が複数レコード存在しても後続順位が飛ばない
    
    例) 1位が3レコードある場合: 1位、 1位、 1位、 2位…
    
- ROW_NUMBER関数
    - 一意な順番を付与する
    
    例) 1位が3レコードある場合: 1位、 2位、 3位、 4位…
    

### 集約関数をウインドウ関数として使用する

- 従来の集約関数と同様、ウインドウ関数として使用しても引数には列が入る
- 合計値は、自分より前のレコードの値を対象に求められており、類型と呼ばれる
- EX. SUM
    
    ```sql
    SELECT shohin_id, shohin_mei, hanbai_tanka,
           SUM (hanbai_tanka) OVER (ORDER BY shohin_id) AS current_sum
      FROM Shohin;
    
    +-----------+-----------------------+--------------+-------------+
    | shohin_id | shohin_mei            | hanbai_tanka | current_sum |
    +-----------+-----------------------+--------------+-------------+
    | 0001      | Tシャツ               |         1000 |        1000 | // 1000
    | 0002      | 穴あけパンチ          |          500 |        1500 | // 1000 + 500
    | 0003      | カッターシャツ        |         4000 |        5500 | // 1000 + 500 4000
    | 0004      | 包丁                  |         3000 |        8500 | // 1000 + 500 + 4000 + 3000
    | 0005      | 圧力鍋                |         6800 |       15300 |
    | 0006      | フォーク              |          500 |       15800 |
    | 0007      | おろしがね            |          880 |       16680 |
    | 0008      | ボールペン            |          100 |       16780 |
    +-----------+-----------------------+--------------+-------------+
    ```
    
- EX. AVG
    
    ```sql
    SELECT shohin_id, shohin_mei, hanbai_tanka,
           AVG (hanbai_tanka) OVER (ORDER BY shohin_id) AS current_avg
      FROM Shohin;
    +-----------+-----------------------+--------------+-------------+
    | shohin_id | shohin_mei            | hanbai_tanka | current_avg |
    +-----------+-----------------------+--------------+-------------+
    | 0001      | Tシャツ               |         1000 |   1000.0000 | // 1000
    | 0002      | 穴あけパンチ          |          500 |    750.0000 | // (1000 + 500)/2
    | 0003      | カッターシャツ        |         4000 |   1833.3333 | // (1000 + 500 + 4000)/3
    | 0004      | 包丁                  |         3000 |   2125.0000 |
    | 0005      | 圧力鍋                |         6800 |   3060.0000 |
    | 0006      | フォーク              |          500 |   2633.3333 |
    | 0007      | おろしがね            |          880 |   2382.8571 |
    | 0008      | ボールペン            |          100 |   2097.5000 |
    +-----------+-----------------------+--------------+-------------+
    ```
    

### フレームを指定する - 移動平均

- ウインドウという部分集合をさらに範囲を細かく指定するオプション機能がある。オプションの集計範囲はフレームと呼ばれる
- ORDER BY句の後ろに専用のキーワードを用いてフレームを指定する
    - キーワード
        - ROWS - 行
        - PRECEDING - 前
        - FOLLOWING - 後
- EX. 2行前 ~ 現在の移動平均を算出する
    
    ```sql
    SELECT shohin_id, shohin_mei, hanbai_tanka,
           AVG (hanbai_tanka) OVER (ORDER BY shohin_id
                                    **ROWS 2 PRECEDING**) AS moving_avg
      FROM Shohin;
    
    +-----------+-----------------------+--------------+------------+
    | shohin_id | shohin_mei            | hanbai_tanka | moving_avg |
    +-----------+-----------------------+--------------+------------+
    | 0001      | Tシャツ               |         1000 |  1000.0000 |
    | 0002      | 穴あけパンチ          |          500 |   750.0000 |
    | 0003      | カッターシャツ        |         4000 |  1833.3333 | // (1000+500+4000)/3
    | 0004      | 包丁                  |         3000 |  2500.0000 |// (500+4000+3000)/3
    | 0005      | 圧力鍋                |         6800 |  4600.0000 |// (4000+3000+6800)/3
    | 0006      | フォーク              |          500 |  3433.3333 |
    | 0007      | おろしがね            |          880 |  2726.6667 |
    | 0008      | ボールペン            |          100 |   493.3333 |
    +-----------+-----------------------+--------------+------------+
    ```
    
    - ROWS 「行」、PRECEDING「前の」を使用して、〜行前までというフレーム指定をしている
        
        **`ROWS 2 PRECEDING`**は「2行前まで」というフレーム指定になる
        
    - 移動平均: 一定区間ごとの平均値を区間をずらしながら求めたもの
- Ex.  現在の前後の行を集計対象に含める
    
    ```sql
    SELECT shohin_id, shohin_mei, hanbai_tanka,
           AVG (hanbai_tanka) OVER (ORDER BY shohin_id
                                     **ROWS BETWEEN 1 PRECEDING** AND 
                                                  **1 FOLLOWING**) AS moving_avg
      FROM Shohin;
    ```
    
    - PRECEDING, FOLLOWINGを併用する

### 2つのORDER BY

- ウインドウ関数内のORDER BYは最終的な結果の並び順には影響しない
- 最終的な並び順を指定するには、従来通りSELECT句の行末でORDER BYを指定する
    
    ```sql
    SELECT shohin_mei, shohin_bunrui, hanbai_tanka,
           RANK () OVER (ORDER BY hanbai_tanka) AS ranking
      FROM Shohin
     ORDER BY ranking;
    ```
    

## GROUPING 演算子

---

- 前提: GROUP BYと集約関数では、小計と合計を同時に求めることはできない
    
    ```sql
    SELECT shohin_bunrui, SUM(hanbai_tanka)
      FROM Shohin
     GROUP BY shohin_bunrui;
    
    +--------------------+-------------------+
    | shohin_bunrui      | SUM(hanbai_tanka) |
    +--------------------+-------------------+
    | 衣服               |              5000 |
    | 事務用品           |               600 |
    | キッチン用品       |             11180 |
    +--------------------+-------------------+
    ```
    
    <aside>
    💡 GROUPING 演算子を使用することで、小計と合計を同時に求めることができる
    
    </aside>
    
- GROUPING 演算子は、`ROLLUP`, `CUBE`, `GROUPING SETS` の3種類がある

### 説明で用いるShohinテーブル

```sql
+--------------------+-----------------------+--------------+------------+
| shohin_bunrui      | shohin_mei            | hanbai_tanka | torokubi   |
+--------------------+-----------------------+--------------+------------+
| 衣服               | Tシャツ               |         1000 | 2009-09-20 |
| 事務用品           | 穴あけパンチ          |          500 | 2009-09-11 |
| 衣服               | カッターシャツ        |         4000 | NULL       |
| キッチン用品       | 包丁                  |         3000 | 2009-09-20 |
| キッチン用品       | 圧力鍋                |         6800 | 2009-01-15 |
| キッチン用品       | フォーク              |          500 | 2009-09-20 |
| キッチン用品       | おろしがね            |          880 | 2008-04-28 |
| 事務用品           | ボールペン            |          100 | 2009-11-11 |
+--------------------+-----------------------+--------------+------------+
```

### ROLLUP - 合計と小計を一度に求める

- 合計行のレコードを、超集合行と呼ぶ
    - GROUP BYでは作られない合計の行のこと
    - 長集合行の集約キーは、デフォルトでNULLが使用される
- Ex1. 商品分類ごとの小計と全体の合計を求める
    
    ```sql
    SELECT shohin_bunrui, SUM(hanbai_tanka)
      FROM Shohin
     GROUP BY ROLLUP(shohin_bunrui);
    -- MySQL GROUP BY shohin_bunrui WITH ROLLUP;
    
    +--------------------+-----------+
    | shohin_bunrui      | sum_tanka |
    +--------------------+-----------+
    | キッチン用品       |     11180 |
    | 事務用品           |       600 |
    | 衣服               |      5000 |
    | NULL               |     16780 | // 超集合行
    +--------------------+-----------+
    
    ```
    
    - MySQLのみ `WITH ROLLUP`を使用する
    - ROLLUP演算子の役割は「集約キーの組み合わせが異なる結果を一度に計算する」
        - この例のケースでは、次の2つの組み合わせについての集約を一度に計算している
            - `GROUP BY()` - GROUP BYがないと同義。全体の合計行のレコードを生み出す
            - `GROUP BY(shohin_bunrui)`
    
- Ex2. 集約キーに「登録日」 を追加したケース
    
    ```sql
    -- ROLLUPなし
    SELECT shohin_bunrui, torokubi, SUM(hanbai_tanka) AS sum_tanka
      FROM Shohin
     GROUP BY shohin_bunrui, torokubi;
    
    +--------------------+------------+-----------+
    | shohin_bunrui      | torokubi   | sum_tanka |
    +--------------------+------------+-----------+
    | 衣服               | 2009-09-20 |      1000 |
    | 事務用品           | 2009-09-11 |       500 |
    | 衣服               | NULL       |      4000 |
    | キッチン用品       | 2009-09-20 |      3500 |　// 集約
    | キッチン用品       | 2009-01-15 |      6800 |
    | キッチン用品       | 2008-04-28 |       880 |
    | 事務用品           | 2009-11-11 |       100 |
    +--------------------+------------+-----------+
    ```
    
    ```sql
    --MySQL ROLLUPあり
    SELECT shohin_bunrui, torokubi, SUM(hanbai_tanka) AS sum_tanka
      FROM Shohin
     GROUP BY shohin_bunrui, torokubi WITH ROLLUP;
    
    +--------------------+------------+-----------+
    | shohin_bunrui      | torokubi   | sum_tanka |
    +--------------------+------------+-----------+
    | キッチン用品       | 2008-04-28 |       880 |
    | キッチン用品       | 2009-01-15 |      6800 |
    | キッチン用品       | 2009-09-20 |      3500 |
    | キッチン用品       | NULL       |     11180 | // 小計 キッチン用品
    | 事務用品           | 2009-09-11 |       500 |
    | 事務用品           | 2009-11-11 |       100 |
    | 事務用品           | NULL       |       600 | // 小計 事務用品
    | 衣服               | NULL       |      4000 |
    | 衣服               | 2009-09-20 |      1000 |
    | 衣服               | NULL       |      5000 | // 小計 衣服
    | NULL               | NULL       |     16780 | // 合計
    +--------------------+------------+-----------+
    ```
    
    - 次の3パターンの集約の異なる結果を表示している
        - `GROUP BY()` - 全体の合計行のレコードを生み出す
        - `GROUP BY(shohin_bunrui)` - 商品分類でまとめた合計行
        - `GROUP BY(shohin_bunrui, torokubi)` - 商品分類, 登録日でまとめた行
    - 合計行に当たるのは、`GROUP BY()`と`GROUP BY(shohin_bunrui)`に当たる行
    

### GROUPING関数 - 超集合行かを見分ける

- 「長集合行の集約キーは、デフォルトでNULLが使用される」仕様のため、集約キーが元々NULLのものが混じっていると、どれが超集合行なのかが一瞬でわからない
    - Ex. 集約キーに「登録日」 を追加したケースにて、一部引用して説明
        
        ```sql
        +--------------------+------------+-----------+
        | shohin_bunrui      | torokubi   | sum_tanka |
        +--------------------+------------+-----------+
        | キッチン用品       | 2008-04-28 |       880 |
        ...
        | キッチン用品       | NULL       |     11180 | // 小計 キッチン用品
        | 事務用品           | 2009-09-11 |       500 |
        ...
        | 事務用品           | NULL       |       600 | // 小計 事務用品
        | 衣服               | NULL       |      4000 | // これはレコードの登録日がNULLであったものを集約した行であり、超集合行ではない
        | 衣服               | 2009-09-20 |      1000 |
        | 衣服               | NULL       |      5000 | // 小計 衣服
        | NULL               | NULL       |     16780 | // 合計
        +--------------------+------------+-----------+
        ```
        
- 超集合行のNULLを判別するために、`GROUPING関数`を用意している
    - 引数にとった列の値が超集合行のために生じたNULLであれば1を、それ以外の値なら0を返す
    - Ex.
        
        ```sql
        SELECT GROUPING(shohin_bunrui) AS shohin_bunrui,
               GROUPING(torokubi) AS torokubi, SUM(hanbai_tanka) AS sum_tanka
        FROM Shohin
        GROUP BY shohin_bunrui, torokubi WITH ROLLUP;
        
        +---------------+----------+-----------+
        | shohin_bunrui | torokubi | sum_tanka |
        +---------------+----------+-----------+
        |             0 |        0 |       880 |
        |             0 |        0 |      6800 |
        |             0 |        0 |      3500 |
        |             0 |        1 |     11180 |
        |             0 |        0 |       500 |
        |             0 |        0 |       100 |
        |             0 |        1 |       600 |
        |             0 |        0 |      4000 |
        |             0 |        0 |      1000 |
        |             0 |        1 |      5000 |
        |             1 |        1 |     16780 |
        +---------------+----------+-----------+
        ```
        
- GROUPING関数を使用すれば、超集合行のキーに適当な文字列を埋め込むことも可能になる
    
    ```sql
    
    ```
    

### CUBE  全ての可能な組み合わせを算出する

- CUBE演算子の役割は「全ての可能な組み合わせを算出する」
    - Ex.のケースでは、次の4つの組み合わせについての集約を一度に計算している
        - `GROUP BY()` - GROUP BYがないと同義。全体の合計行のレコードを生み出す
        - `GROUP BY(shohin_bunrui)`
        - `GROUP BY(torokubi)`  (ROLLUPからさらに追加された)
        - `GROUP BY((shohin_bunrui, torokubi)`
- MySQL8.0ではサポートされていない
- EX.
    
    ```sql
    SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
                THEN '商品分類 合計'
                ELSE shohin_bunrui END AS shohin_bunrui,
           CASE WHEN GROUPING(torokubi) = 1
                THEN '登録日 合計'
                ELSE torokubi END AS torokubi,
           SUM(hanbai_tanka) AS sum_tanka
      FROM Shohin
     GROUP BY CUBE(shohin_bunrui, torokubi);
    ```
    

### GROUPING SETS 欲しい組み合わせだけ取得する

- CUBE演算子を使って求めた結果の一部だけ求めたい時に使用する
- Ex.のケースでは、次の2つの組み合わせについての集約を一度に計算している
    - `GROUP BY(shohin_bunrui)`
    - `GROUP BY(torokubi)`
- Ex.
    
    ```sql
    SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
                THEN '商品分類 合計'
                ELSE shohin_bunrui END AS shohin_bunrui,
           CASE WHEN GROUPING(torokubi) = 1
                THEN '登録日 合計'
                ELSE CAST(torokubi AS VARCHAR(16)) END AS torokubi,
           SUM(hanbai_tanka) AS sum_tanka
      FROM Shohin
     GROUP BY GROUPING SETS (shohin_bunrui, torokubi);
    ```
    
- MySQL8.0ではサポートされていない