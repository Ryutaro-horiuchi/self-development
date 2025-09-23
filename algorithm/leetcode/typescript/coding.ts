function func(s: string): boolean {
  if (s.length <= 1) return false;

  const map = new Map<string, string>()
  map.set(")", "(")
  map.set("]", "[")
  map.set("}", "{")

  const stack: string[] = []
  for(let i = 0; i < s.length; i++) {
    if(map.has(s[i])) {
      const bracket = stack.pop()
      if (map.get(s[i]) !== bracket) return false
    } else {
      stack.push(s[i])
    }
  }

  return stack.length === 0
}

console.log(func("(())"))
