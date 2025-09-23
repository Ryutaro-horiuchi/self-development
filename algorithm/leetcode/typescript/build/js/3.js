"use strict";
function lengthOfLongestSubstring(s) {
    let left = 0;
    let currentLength = 0;
    let maxLength = 0;
    const lastIndexMap = new Map();
    for (let i = 0; i < s.length; i++) {
        if (lastIndexMap.has(s[i])) {
            const lastIndex = lastIndexMap.get(s[i]);
            left = Math.max(left, lastIndex + 1);
        }
        lastIndexMap.set(s[i], i);
        currentLength = i - left + 1;
        maxLength = Math.max(currentLength, maxLength);
    }
    return maxLength;
}
;
console.log(lengthOfLongestSubstring("pwwkew"));
//# sourceMappingURL=3.js.map