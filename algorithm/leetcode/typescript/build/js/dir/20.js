"use strict";
function isValid(s) {
    const pairs = {
        '(': ')',
        '{': '}',
        '[': ']'
    };
    const strs = [];
    for (let i = 0; i < s.length; i++) {
        if (Object.values(pairs).some((pair) => pair == s[i])) {
            const pre = strs.pop();
            if (!pre)
                return false;
            if (pairs[pre] != s[i])
                return false;
        }
        else {
            strs.push(s[i]);
        }
    }
    return !strs.length;
}
;
console.log(isValid("([)]"));
//# sourceMappingURL=20.js.map