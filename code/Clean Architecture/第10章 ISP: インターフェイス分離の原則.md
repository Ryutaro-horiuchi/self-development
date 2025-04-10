## インターフェイス分離の原則(ISP)

### Bad

![IMG_3654.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/c9eba254-4e0c-42c5-bd54-d4f09d6aeb81/IMG_3654.jpeg)

- 複数のユーザーがOPSクラスを使用している
    - User1は、OPSのop1。User2はOPSのop2…
- User1クラスは、実際には使っていないop2, op3にも依存している
    - 仮にop2のコードを変更したときに、User1の再コンパイルと再デプロイが必要になる

### Good

![IMG_3655.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/42b16988-a5a8-437d-af8b-c8412ee1342b/e82366a0-9404-435d-ab50-7e432c2d8cd2/IMG_3655.jpeg)

- Badの問題を解決するには、各インターフェイスを分離すれば良い
- User1クラスは、U1Opsとop1には依存しているが、OPSには依存しておらず、OPSに変更があったとしても、User1に関係ない部分(op2, op3の変更)であれば、User1の再コンパイルと再デプロイは不要になる

## インターフェイス分離の原則とアーキテクチャの関係

```mermaid
flowchart LR
  node_1["システムS"]
  node_2["フレームワークF"]
  node_3["データベースD"]
  node_1 --> node_2
  node_2 --> node_3
```

- システムSを担当するアーキテクトが、フレームワークFを導入したいとする
    - フレームワークFは特定のデータベースDのためだけに作っている(依存している)
        - SはFに依存しており、FはDに依存している
- この時、Dが変更されると、Fも再デプロイすることになる。そして、システムSも再デプロイすることになる
    - また、Dの一部の機能に障害が発生すると、それがFやSの障害の原因となってしまう可能性がある

## まとめ

必要としないお荷物を抱えたものに依存していると、予期せぬトラブルの元につながる