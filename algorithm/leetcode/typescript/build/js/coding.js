"use strict";
function func(s) {
    if (s.length <= 1)
        return false;
    const map = new Map();
    map.set(")", "(");
    map.set("]", "[");
    map.set("}", "{");
    const stack = [];
    for (let i = 0; i < s.length; i++) {
        // 開きかっこであれば、stackに追加する
        // 閉じかっこであれば、stackなので直前に入れた値を取得する
        // 閉じかっこに対応する開きかっこかどうか
        if (map.has(s[i])) {
            const bracket = stack.pop();
            if (map.get(s[i]) !== bracket)
                return false;
        }
        else {
            stack.push(s[i]);
        }
        return stack.length === 0;
    }
}
console.log(func("()"));
//# sourceMappingURL=coding.js.map