---
marp: true
theme: default
paginate: true
---
<style>
  section {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }
  h1 {
    /* flex: 1 0 10%; */
  }
  /* h1 {
      position: absolute;
      left: 50px;
      top: 50px;
  }
  h3 {
      position: absolute;
      left: 50px;
      top: 150px;
  } */
</style>

<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
  p {
    text-align: center;
    font-weight: bold;
  }
  /* section {
      text-align: center;
  }
  h4 {
      position: absolute;
      bottom: 200px;
      right: 50px;
  } */
</style>

# RDBのNULLはアンチパターン

堀内 龍太朗
エンジニア勉強会
2024.07.18

---

# NULLについてどのような印象？

癖がある・・・
  - 四則演算にNULLが混じると、全てNULLになる
  - 集約関数は基本的にNULLを除外する
    - COUNT(*)のみNULLを除外しない

**→ NULLの挙動をきちんと理解しないと、思いもしないところでバグにつながる可能性も**

<!--  
・リレーショナルDBのNULLについてどのような印象をお持ちでしょうか？
・初めてNULL周りについて見た時は、だいぶ癖があるなぁという印象でした
・四則演算にNULLが混じっていると全てNULLになるであったり、集約関数の時は基本的にNULLは除外されて計算するけれど、COUNTに関しては引数がアスタリスクだとNULLを除外しないだったり
・注意してクエリを書かないと、思わぬバグに繋がりそうだなという印象でした
-->


---
<style scoped>
.hoge {
 display: flex;
 justify-content: center;
}
</style>

# 参考

<div class="hoge">
  <img src="達人から学ぶSQL徹底指南書.jpg" width=35% />
</div>

<!--  
直近こちらの書籍を読みまして、そういったバグに繋がる事例も書かれていたんですが、別でNULLに関する理論的なところも書かれていてすごく参考になったので、こちらを中心にご紹介したいと思っています。
タイトルのアンチパターンについても、この書籍では「NULLは極力排除しましょう」という指針で、自分自身も読み終わった後にNULLの使用はできるなら、避けたいなぁと感じたのでつけました。
-->

---

<style scoped>
ol {
  flex-basis: 70%;
}

</style>
# アジェンダ

1. NULLを使用するにあたって ~NULLと3値論理~
  1-1. 理論編
  1-2. 実例編
  1-3. 他に考慮すべき点
2. NULLとどう向き合うのか
3. まとめ

<!--  
アジェンダです。
最初はNULLを使用するにあたって、押さえておきたい3値論理という概念について触れます

この3値論理によって、だいぶややこしいことになっていて、直感に反した結果が返ってくることがあるので、そちらを実例編として取り上げます。

その後は、タイトルの通りで、他に考慮すべき点と、じゃあどういうふうにNULLと向き合うのか。まとめという形で進めていきます。
-->

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>

# 1. NULLを使用するにあたって ~NULLと3値論理~

---
<style scoped>
  h3 {
    position: absolute;
    top: 90px;
    left: 70px;

  }
  p {
    flex-basis: 40%;
    /* align-self: center;
    text-align: center */
  }
</style>

# 1-1.理論編

##### 3値論理とは？

真理値型(BOOLEAN)の話
　→ **プログラミング言語とSQLの真理値型には違いがある**

<!--  
さっきから3値論理と言っているんですけど、なんの話かというと、BOOLEANの話です。

で、この真理値がプログラミング言語とSQLとでは、ちょっと中身が違っています。
-->

---

# プログラミング言語の真理値

- 真「true」 偽「false」で表すことができる

```javascript
  const name = 'taro'

  if (name === 'taro') {
    console.log('名前はtaroです')
  } else {
    console.log('名前はtaroじゃありません')
  }

```

  <br>

→ これを**2値論理**と呼ぶ

<!--  
普段使用しているプログラミング言語においては、真理値は真「true」 偽「false」だけですと。これを2値論理と呼びます
-->

---

# SQLの真理値

- 真「true」、偽「false」 の他に **不明「unknown」** がある


→ これを**3値論理**と呼ぶ

3値論理を持ち込んだことよって、直感に反する振る舞いを見せる(バグを生みやすい)

<!--  
SQLでは、真「true」、偽「false」 の他に 不明「unknown」あります。3つ値を使用しているので、3値論理と呼んでいます。これをSQLの世界に持ち込んだことによって、だいぶ複雑でバグを生みやすいような仕様になっているなぁと思ってます。
-->

---
# どういう時にunknownになるのか

**NULLに比較述語を使用したとき、常にunknownになる**

```sql
-- 以下の式は全部unknownになる
1 = NULL
2 > NULL
3 < NULL
4 <> NULL
NULL = NULL
NULL > NULL
NULL < NULL
NULL <> NULL
```


<!--  
どういう時にunknownになるのかというと、これは単純にNULLを比較したら常にunknownが返ってきます。NULL同士の比較もNULLになります。
-->

---
# なぜ = NULLではなく、IS NULLと書かなくてはならないのか

```sql
-- 取得に失敗するSQL
SELECT *
  FROM table_a
 WHERE name = NULL;
```

```sql
-- 取得に成功するSQL
SELECT *
  FROM table_a
 WHERE name IS NULL;

```
- WHERE句は条件の評価がtrueのみ返される
- name = NULL はunknownが返ってくる

<!--
SQL勉強し初めの時に、NULLの行を抽出する際は = NULLではなく、IS NULLと書かなくてはならないのが、不便だなと思ってました。これの理由も「NULLを比較をするとunknownが返される仕様」で、WHERE句はtrueのみ抽出するからということがわかると思います。
-->
---



# AND ORを使用した時の優先順位
- 2値論理
    - AND
        - false > true
    - OR
        - true  > false

- 3値論理
    - AND
        - false > unknown > true
    - OR
        - true > unknown > false

<!--
この後実例編に移るんですが、その前に簡単に押さえていただきたいのが、ANDやORを使用した複数の条件が並んだときの優先順位です。
と言っても、2値論理の時の優先順位の間にunknownが入るイメージを持っていただければと思います。
trueとunknownがANDで並んでいれば、unknownの方が優先になるので、unknownが返されますし、ORで並んでいれば、trueが返されるようになります。
-->


---
<style scoped>
ul {
  flex-basis: 60%;
}
</style>
# 1-2. 実例編

<br>

unknown絡みの直感に反したクエリ
- NOT IN
- 限定述語 「ALL」
- CASE式

<!--  
実例編に入ります。
unknown絡みの直感に反したクエリの例として、3つそれぞれ取り上げていきたいと思います。
-->

---
<style scoped>
.container {
  display: flex;
  justify-content: space-around;
}

</style>

# NOT IN

##### Ex. 学校のクラステーブル

<br>

<div class="container">

  <div class="table-1">

Class_A
  | name | age | city |
  | --- | --- | --- |
  | ブラウン | 22 | 東京 |
  | ラリー | 19 | 埼玉 |
  | ボギー | 21 | 千葉 |
  
  </div>

  <div class="table-2">

Class_B
| name | age | city |
| --- | --- | --- |
| 齊藤 | 22 | 東京 |
| 田尻 | 23 | 東京 |
| 山田 | NULL | 東京 |
| 和泉 | 18 | 千葉 |
| 石川 | 19 | 神奈川 |

 </div>
</div>

Bクラスの東京在住の生徒と、年齢が一致しないAクラスの生徒を選択する


<!--  
NOT INの例として、学校のクラステーブルを使用します。名前と年齢、住まいを列として持ちます。
山田くんだけageがNULLです。
こちらでBクラスの東京在住の生徒と、年齢が一致しないAクラスの生徒を選択してみます。
答えをここで確認しておくと、Bクラスの東京在住のクラスメイトは、齊藤、田尻、山田の3人で、22と23と年齢不詳です。欲しい結果はAクラスのラリーとボギーの2人が正解になります。
-->

---
<style scoped>
.container {
 display: flex;
 justify-content: space-around;
}
.sql {
 flex-basis: 50%;
 margin-top: 10px;
}
</style>

# NOT IN
Bクラスの東京在住の生徒と、年齢が一致しないAクラスの生徒を選択する

<br>

<div class="container">
  <div class="sql">

```sql
SELECT name
FROM Class_A
WHERE age NOT IN
            (SELECT age 
               FROM Class_B
               WHERE city = '東京'
            );
```

  </div>

  <div class="table-2">

Class_B
| name | age | city |
| --- | --- | --- |
| 齊藤 | 22 | 東京 |
| 田尻 | 23 | 東京 |
| 山田 | NULL | 東京 |
| 和泉 | 18 | 千葉 |
| 石川 | 19 | 神奈川 |

  </div>
</div>

→ 結果は一つも返ってこない


<!--  
サブクエリとNOT INの組み合わせのクエリで取得できそうですが、結果は空で一つも返ってこないです。山田くんの年齢がNULLじゃなければ正常に取れるクエリで、NULLがあることによって直感に反した結果になっています。
-->

---
<style scoped>
p {
  font-size: 28px;
}
</style>
# NOT IN
処理の流れ(抜粋)


```sql
 ...
 WHERE age NOT IN
            (SELECT age FROM Class_B WHERE city = '東京');

```

```sql

WHERE age NOT IN (22, 23, NULL);

```

```sql
WHERE NOT ( (age = 22) OR (age = 23) OR (age = NULL) );
```

```sql
WHERE (age <> 22) AND (age <> 23) AND unknown;
```

<br>

AND句においてunknownは優先されるため、unknownかfalseが返ってくる。

<!--
なぜ結果が空になるのか、こちらがクエリの処理の流れになります。時間の都合上一部抜粋したものになりますが、最終的にこの形になります。22, 23に一致せずにtrueだったとしても、unknownがあることによって、結果はunknownが返されて、一つも取得できないことになります。

-->

---

<style scoped>
  ul {
    flex-basis: 70%;
  }

</style>

# NOT IN

- NOT INのサブクエリで使用されるテーブルの選択列にNULLがあると、SQLの結果は常に空になる
- NOT EXISTSにすると正常に動作する

  ```sql
    SELECT *
      FROM Class_A A
     WHERE NOT EXISTS
            ( SELECT *
                FROM Class_B B
               WHERE A.age = B.age
                 AND B.city = '東京'
            );
  ```

<!--  
整理すると、NOT INのサブクエリで使用されるテーブルの選択列にNULLがあると、SQLの結果は常に空にな
ります。これは個人的にだいぶ怖い現象だなと思いました。
一応対策として、NOT EXISTSを使用すると正常に取得することはできます
-->



--- 
# 限定述語「ALL」

「~全てと等しい」や「全て~よりも大きい」という意味

##### Bクラスの東京在住の誰よリも若いAクラスの生徒を選択する

```sql
SELECT *
  FROM Class_A
WHERE age < ALL(SELECT age　FROM Class_B　WHERE city = '東京');

-- 同値変換
-- WHERE (age < 22) AND (age < 23) AND (age < NULL);
```
→ 結果は一つも返ってこない

<!--
次に限定述語のALLです。比較述語の併用して「~全てと等しい」「全て~よりも大きい」という文脈で使用することができます。

例えば、「Bクラスの東京在住の誰よリも若いAクラスの生徒を選択する」という時に、一般的にはスライドにあるクエリで結果を取得することはできますが、これもNULLがあると結果は常に空になります。ALL述語自体、ANDで連結した式の省略形として定義されているので、実行時はコメントアウトのようなクエリになり、返ってこないということになります。
-->

---
<style scoped>
.container {
 display: flex;
 justify-content: space-around;
}
.sql {
 flex-basis: 50%;
 margin-top: 10px
}
.table-1 {
 margin-bottom: 10px;
}
</style>
# CASE式

Class_Bから22歳であれば「◯」、NULLであれば「-」、どちらでもない時は「×」を表示する

<div class="container">
  <div class="sql">

```sql
-- 正しく動作しないクエリ
SELECT name
    CASE age
      WHEN 22 THEN '⚪︎'
      WHEN NULL THEN '-'
      -- WHEN age = NULLと同義
      ELSE '×'
    END AS age
  FROM Class_B;
```

```sql
-- 正しく動作するクエリ
    ...
    CASE WHEN age = 22 THEN '⚪︎'
         WHEN age IS NULL THEN '-'
    ...
```

  </div>

  <div class="table-1">

Class_B
| name | age | city |
| --- | --- | --- |
| 齊藤 | 22 | 東京 |
| 田尻 | 23 | 東京 |
| 山田 | NULL | 東京 |
| 和泉 | 18 | 千葉 |
| 石川 | 19 | 神奈川 |

  </div>
</div>


<!--  
最後にCASE式の例です。クラスBから22歳であれば「○」、NULLであれば「-」、どちらでもない時は「×」を表示するとします。一つ目のクエリの場合、このWHENは、「age = NULL」の式の省略形になるので、unknownが返され、何もヒットしないので、結果は○か×のみ表示されるクエリになります。

ここまでで実例編は以上になります。列にNULLがあることで直感に反した結果になるということが分かったのではないかと思います。
-->

---
<style scoped>
ul {
  flex-basis: 70%;
}
</style>
# 1-3. 他に考慮すべき点
- 四則演算またはSQLの関数の引数にNULLがあると結果が全てNULLになる(NULLの伝播)
- RDBの種類によってはインデックスを使用しない
- NULLは行に余分なビットを持つ(これもRDBの種類による)
  - MySQLではドキュメントを見る限り、どの行形式もNULLビットマップを使用していて、そんなことはなさそう？
- ORDER BYのソートのルールを意識する
    - RDBの種類によって異なる

<!-- 
NULLを使用するにあたって、これまで見てきたとおり、3値論理であるということは特に意識しなくてはならないと思います。他に考慮すべき点として、4つ挙げています。
一つ目は冒頭に挙げた通り、NULLが計算式にあることで結果が全てNULLになることに注意しなくてはならないですと。



-->

---

# 2. NULLとどう向き合うのか

---
<style scoped>
ul {
  flex-basis: 70%;
}
</style>
# NULLとどう向き合うのか

- NOT NULL制約を設けて「極力」NULLを排除する
- NULLではなく、デフォルト値を検討する
  - ケースとしては、「コード」 「名前」 「数値」 「日付」

---
# デフォルト値を検討する 「コード」

- 性別コード
    - ISOの性別コードでは「1: 男性」、「2: 女性」の他に「０: 未知」「9: 適用不能」という2つの未コード化用コードが使われている
- 顧客コード
    - 「XXXXX」等を使用することを検討する
    - 99999などは避けた方が良い
        - コードには多くの場合数値が使われるため、あり得ないと思って数字を使用すると、そのコードを持つ顧客が現実に出現することがある

---
<style scoped>
ul {
  flex-basis: 70%;
}

</style>
# デフォルト値を検討する 「名前」

- コードと同様、 「不明」を表す値を与える
- 値はなんでも良い。開発チーム内で共通了承の得られた適当な名前を割り振る

---
<style scoped>
ul {
  flex-basis: 70%;
}

</style>
# デフォルト値を検討する 「数値」
- 最初からNULLを0で代替する
- とはいえ値があるのと、未知なのは異なる
    - 現実的には0を使用するようにして、どうしても0とNULLを区別したい場合だけ、NULLを許可する


---
<style scoped>
p {
  flex-basis: 70%;
}

</style>
# デフォルト値を検討する 「日付」
開始日や終了日など「期限」を意味する場合は「0001-01-01」や「9999-12-31」のように可能な最大値・最小値を使うことで対応できる

---
# 3. まとめ


---
<style scoped>
ul {
  flex-basis: 70%;
}

</style>
# まとめ

- NULLに比較述語を使用するとunknownになる
- unknownが紛れ込むと、直感に反した動作になる
- NULLは極力NULLを排除するように努める
    - NOT NULL制約
    - デフォルト値を検討
