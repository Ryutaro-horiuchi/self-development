N = int(input())
keys = set()
rokkotsu = []
for _ in range(N):
    a,b = map(int, input().split())
    keys.add(a)
    rokkotsu.append([a,b])

M = int(input())
lens_moji = { k: [] for k in keys }

moji = []
for i in range(M):
    s = input()
    moji.append(s)
    if len(s) in keys:
        lens_moji[len(s)].append(s)

def func(m):
    """
    Args:
        m せきづいに記入する文字
    """
    ans = True
    if len(m) != N:
        ans = False
    else:
        for i, st in enumerate(m): # せきづいの頭からi文字目 # 実際に記入する文字 st
            a, b = rokkotsu[i] # a 肋骨の文字列の長さ b 肋骨の何文字目を参照するか
            for le in lens_moji[a]: # aの文字列の長さとイコールの文字列群
                if st == le[b-1]:
                    break
            else:
                ans = False
                break

    print("Yes" if ans  else "No")

for mo in moji:
    func(mo)
