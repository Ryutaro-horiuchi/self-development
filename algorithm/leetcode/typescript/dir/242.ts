function isAnagram(s: string, t: string): boolean {
  if (s.length != t.length) return false;

  const map = new Map<string, number>();
  for (let i = 0; i < s.length; i++) {
    if (map.has(s[i])) {
      map.set(s[i], map.get(s[i]) as number + 1)
    } else {
      map.set(s[i], 1)
    }
  }

  for (let i = 0; i < t.length; i++) {
    if (map.has(t[i])) {
      let cnt = map.get(t[i]) as number
      if (cnt === 0) return false;

      map.set(t[i], cnt -1)
    } else {
      return false
    }
  }

  return true
};

console.log(isAnagram("rat", "car"))