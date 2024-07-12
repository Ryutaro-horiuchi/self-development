---
marp: true
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

#### 堀内 龍太朗

---

# NULLについてどのような印象？

ややこしい...
  - WHERE col_1 = NULLと書けない
    - WHERE col_1 IS NULLと書く必要がある
  - 四則演算にNULLが混じると、NULLになる


**NULLの挙動を理解しないと、思いもよらないバグにつながる**


---
<style scoped>
ol {
  flex-basis: 70%;
}

</style>
# アジェンダ

1. NULLを知る ~NULLと3値論理~
  1-1. 理論編
  1-2. 実例編
  1-3. 他に考慮すべき点
2. NULLとどう向き合うのか
3. まとめ

---
# 参考

- 達人に学ぶSQL徹底指南書 第2版
(画像を貼っつける)

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>

# 1. NULLを知る ~NULLと3値論理~

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

---

# SQLの真理値

- 真「true」、偽「false」 の他に **不明「unknown」** がある


→ これを**3値論理**と呼ぶ

3値論理を持ち込んだことよって、直感に反する振る舞いを見せる(バグを生みやすい)


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
- WHERE句は条件の評価がtrueのみ選択される
- name = NULL はunknownが返ってくる

---

# [補足]AND ORを使用した時の優先順位
- 優先順位
    - AND
        - false > unknown > true
    - OR
        - true > unknown > false

- 2値論理
    - AND
        - false > true
    - OR
        - true  > false


---
<style scoped>
ul {
  flex-basis: 60%;
}
</style>
# 1-2. 実践編

<br>

意図しない結果の例
  - NOT IN
  - 限定述語 「ALL」
  - CASE式

---
<style scoped>
ul {
  display: flex;
  justify-content: space-around;
}

</style>
# NOT IN

##### Ex. 学校のクラステーブル

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

→ Bクラスの東京在住の生徒と、年齢が一致しないAクラスの生徒を選択する

---
# NOT IN
##### Bクラスの東京在住の生徒と、年齢が一致しないAクラスの生徒を選択する

```sql
SELECT name
  FROM Class_A
 WHERE age NOT IN
            (SELECT age FROM Class_B WHERE city = '東京');

```

齊藤の22、田尻の23、山田のNULL以外の年齢の人が結果？

→ 結果は一つも返ってこない


---
<style scoped>
p {
  font-size: 28px;
}
</style>
# NOT IN
##### 処理の流れ(抜粋)


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

---
# 限定述語「ALL」

「~全てと等しい」や「全て~よりも大きい」という意味

##### Bクラスの東京在住の誰よリも若いAクラスの生徒を選択する

```sql
SELECT *
  FROM Class_A
WHERE age < ALL(SELECT age　FROM Class_B　WHERE city = '東京');
```
→ 結果は一つも返ってこない

ALL述語も実行時にAND変換されるため、NULLが入ってくると成立しなくなる

---
# CASE式

### Class_Aから22歳であれば「◯」、違ければ「×」、NULLであれば「-」を表示する

```sql
SELECT name
    CASE age
      WHEN 22 THEN '⚪︎'
      WHEN NULL THEN '-'
    ELSE '×' END AS age
  FROM Class_A;
```
→ 絶対に「-」は出力されない

2つ目のWHENは、「age = NULL」の式になる

---
<style scoped>
ul {
  flex-basis: 70%;
}
</style>
# 1-3. 他に考慮すべき点
- 四則演算またはSQLの関数の引数にNULLがあると結果が全てNULLになる(NULLの伝播)
- NULLは行に余分なビットを持つ
  - MySQLではドキュメントを見る限り、どの行形式もNULLビットマップを使用していて、そんなことはなさそう？
- ORDER BYのソートのルールを意識する
    - RDBの種類によって異なる
- RDBの種類によってはインデックスを使用しない

---
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>

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
<style scoped>
  section {
    align-items: center;
    justify-content: center;
  }
</style>
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
