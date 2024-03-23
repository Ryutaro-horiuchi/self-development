- SQLは「集合指向」と言う発想に基づいて設計された言語
    - ベン図を書いてみるのが効果的
    - 手続き型言語とは違う
        
        プログラムは一連の手順（手続き、関数、サブルーチンなどと呼ばれることもあります）によって構成され、手順が順番に実行されることで問題を解決するスタイル
        
- HAVING句は、何を持って集合とみなすのかに着目する
- この章では、HAVING句を通して、「集合単位の操作」という集合指向言語の特性を理解する

## データの歯抜けを探す

- テーブル: SeqTbl
    
    
    | seq | name |
    | --- | --- |
    | 1 | ディック |
    | 2 | アン |
    | 3 | ライル |
    | 5 | カー |
    | 6 | マリー |
    | 8 | ベン |
- 手続き型言語のアプローチ
    
    ```
    前提として、SeqTblをファイルとする
    
    1. 連番の昇順か降順にソートする
    2. ソートキーの昇順にループさせて、一行ずつ次の行とseq列の値を比較する
    ```
    
    - ファイルのレコードは順序を持つが、テーブルのレコードは順序を持たない
        - 代わりにテーブル(SQL)は複数行を集合とみなす
- 集合指向言語(SQL)のアプローチ
    
    ```sql
    -- 結果が返れば歯抜けあり
    SELECT '歯抜けあり' AS gap 
      FROM SeqTbl 
    HAVING COUNT(*) <> MAX(seq);
    ```
    
    - テーブル全体を一つの集合とみなす
    - 
- GROUP BY句がないHAVING句のSQL文は、テーブル全体が一行に集約される
    
    <aside>
    💡 現在の標準SQLでは、HAVING句を単独で使える
    → SELECT文で、元の列を使用できなくなるため、定数か集約関数を使用する
    
    </aside>
    

## HAVING句でサブクエリ - 最頻値を求める

- Ex. 卒業後の学生の収入の最頻値を求める (答えは20,000)
    - テーブル: Graduates (卒業生テーブル)
        
        
        | name(名前) | income(収入) |
        | --- | --- |
        | サンプソン | 400,000 |
        | マイク | 30,000 |
        | ホワイト | 20,000 |
        | アーノルド | 20,000 |
        | スミス | 20,000 |
        | ロレンス | 15,000 |
        | ハドソン | 10,000 |
    - SQL
        - 収入が同じ卒業生をひとまとめにする集合を作り、その集合群から要素数が最も多い集合を探す
        
        ```sql
        -- 最頻値を求めるSQL: その１ ALL述語の利用
        
        SELECT income, COUNT(*) AS cnt 
          FROM Graduates 
         GROUP BY income 
        HAVING COUNT(*) >= ALL ( SELECT COUNT(*) 
                                   FROM Graduates
                                  GROUP BY income);
        ```
        
    - 手続き型言語だと…
        
        収入でソートしてループ処理を行い、同じ収入の行数が前に数えた収入の行数より大きければ、その収入を変数に代入して保存するといった処理になる
        

## NULLを含まない集合を探す

- 前提としてCOUNT句は、引数にアスタリスクを取るとNULLも数の対象に含め、列名を引数に取るとNULLを除外して数を数える
- Ex. 全ての学生がレポート提出済みの学部を取得する
    - テーブル: Students
        
        
        | student_id(学生ID) | dpt(学部) | sbmt_date(提出日) |
        | --- | --- | --- |
        | 100 | 理学部 | 2018-10-10 |
        | 101 | 理学部 | 2018-09-22 |
        | 102 | 文学部 |  |
        | 103 | 文学部 | 2018-09-10 |
        | 200 | 文学部 | 2018-09-22 |
        | 201 | 工学部 |  |
        | 202 | 経済学部 | 2018-09-25 |
        - 提出が済んでいない学生はsbmt_dateにNULLが入る
    - SQL1:  COUNT関数の利用
        
        ```sql
        -- 提出日にNULLを含まない学部を選択する：その1 COUNT関数の利用
        SELECT dpt 
          FROM Students 
         GROUP BY dpt 
        HAVING COUNT(*) = COUNT(sbmt_date);
        ```
        
        - 学部ごとに部分集合を作り、COUNT(*)とCOUNT(sbmt_date)が同じ部分集合が、学生がレポート提出済みとみなすことができる
    - SQL2: CASE式の利用(特定関数)
        
        ```sql
        -- 提出日にNULLを含まない学部を選択する：その2 CASE式の利用
        SELECT dpt 
          FROM Students 
         GROUP BY dpt 
        HAVING COUNT(*) = SUM(CASE WHEN sbmt_date IS NOT NULL 
                                   THEN 1 ELSE 0 END);
        ```
        
        - ここでのCASE式は、特定の条件(sbmt_dateがNULLではないか)を満たす集合に含まれるかどうかを決める関数を表している。このような関数を特定関数と呼ぶ

## 全称量文をHAVING句(集合)で表現する

- [全称量化と存在量化](https://www.notion.so/66bf901cf6174355b6079a4663f7c243?pvs=21)
- Ex. 消防隊で全てのチームメンバーが「待機状態」であるチームを抽出する
    - テーブル: Teams
        
        
        | member(隊員) | team_id | status(状態) |
        | --- | --- | --- |
        | ジョー | 1 | 待機 |
        | ケン | 1 | 出勤中 |
        | ミック | 1 | 待機 |
        | カレン | 2 | 出勤中 |
        | キース | 2 | 休暇 |
        | ジャン | 3 | 待機 |
        | ハート | 3 | 待機 |
    - SQL: 集合で表現する
        
        ```sql
        -- 全称文を集合で表現する
        SELECT team_id
          FROM Teams
         GROUP BY team_id
        HAVING COUNT(*) = SUM(CASE WHEN status = '待機'
                                   THEN 1
                                   ELSE 0 END);
        ```
        
        - ちなみに、NOT EXISTを使用して表現すると以下のようになる。パフォーマンスでは優れているが、二重否定を使うため、わかりづらい
            
            ```sql
            -- 全称文を述語で表現する
            -- 待機中ではないメンバーが一人も存在しないに変換するため、わかりづらい
            SELECT team_id, member 
              FROM Teams T1 
             WHERE NOT EXISTS (SELECT * 
                                 FROM Teams T2 
                                WHERE T1.team_id = T2.team_id 
                                  AND status <> '待機 ' ); 
            ```
            

## 関係除算でバスケット分析

Ex. ディスカウントチェーンの商品マスタ(Items)テーブルの全ての商品を揃えている店舗を選択する

- 前提バスケット分析
    
    マーケティング分野で用いられる手法の一つ。頻繁に一緒に買われる商品の法則性を見つける
    
- テーブル: Items
    
    
    | item(商品) |
    | --- |
    | ビール |
    | 紙おむつ |
    | 自転車 |
- テーブル: ShopItems
    
    
    | shop(店舗) | item(商品) |
    | --- | --- |
    | 仙台 | ビール |
    | 仙台 | 紙おむつ |
    | 仙台 | 自転車 |
    | 仙台 | カーテン |
    | 東京 | ビール |
    | 東京 | 紙おむつ |
    | 東京 | テレビ |
- SQL:
    
    ```sql
    
    -- ビールと紙おむつと自転車を全て置いている店舗を検索する
    SELECT SI.shop 
      FROM ShopItems SI INNER JOIN Items I 
        ON SI.item = I.item 
     GROUP BY SI.shop 
    HAVING COUNT(SI.item) = (SELECT COUNT(item) FROM Items);
    ```