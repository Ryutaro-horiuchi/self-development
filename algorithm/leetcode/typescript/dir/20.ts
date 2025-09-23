type Bracket = '(' | '{' | '['
type CloseBracket = ')' | '}' | ']'

function isValid(s: string): boolean {
    const pairs: Record<Bracket, CloseBracket> = {
      '(': ')',
      '{': '}',
      '[': ']'
    }

    const strs: Bracket[] = []
    for(let i = 0; i < s.length; i++) {
      if(Object.values(pairs).some((pair) => pair == s[i])) {
        const pre = strs.pop()
        if (!pre) return false;
        if (pairs[pre] != s[i]) return false;

      } else {
        strs.push(s[i] as Bracket)
      }
    }

    return !strs.length
};

console.log(isValid("([)]"))