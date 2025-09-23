"use strict";
function isAnagram(s, t) {
    if (s.length != t.length)
        return false;
    const map = new Map();
    for (let i = 0; i < s.length; i++) {
        if (map.has(s[i])) {
            map.set(s[i], map.get(s[i]) + 1);
        }
        else {
            map.set(s[i], 1);
        }
    }
    for (let i = 0; i < t.length; i++) {
        if (map.has(t[i])) {
            let cnt = map.get(t[i]);
            if (cnt === 0)
                return false;
            map.set(t[i], cnt - 1);
        }
        else {
            return false;
        }
    }
    return true;
}
;
console.log(isAnagram("rat", "car"));
//# sourceMappingURL=242.js.map