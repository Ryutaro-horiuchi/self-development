/**
 * @param {string} s
 * @return {number}
 */
var lengthOfLongestSubstring = function(s) {
  const lastIndex = new Map();
  let left = 0;
  let maxLen = 0;


  for (let i = 0; i < s.length; i++) {
    if (lastIndex.has(s[i]) && lastIndex.get(s[i]) >= left) {
      left = lastIndex.get(s[i]) + 1;
    }
    lastIndex.set(s[i], i)
    maxLen = Math.max(maxLen, i - left + 1);
  }

  return maxLen
};

console.log(lengthOfLongestSubstring("pwwkew"))

// leftで部分文字列の開始位置。lastIndexで、最後に文字が現れた位置。 
// for文で回していって文字が既出しているか、かつleftよりもlastIndexの位置が大きければ重複扱い。
// leftの位置を最後に文字が現れた位置の次に動かす maxlenとi-left+1を比較して大きい方をmaxlenに代入みたいな流れ
// mapを使うことでO(1)で最後の位置をとってこれる