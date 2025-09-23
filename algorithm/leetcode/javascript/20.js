/**
 * @param {string} s
 * @return {boolean}
 */
var isValid = function(s) {
  const pair = { ')':'(', ']':'[', '}':'{' };
  const stack = [];

  for (let i = 0; i < s.length; i++) {
    const ch = s[i]
    if (ch in pair) {
      if (stack.length === 0 || stack.pop() !== pair[ch] ) return false
    } else {
      stack.push(ch)
    }
  }

  return stack.length === 0
};