## TypeScriptの関数宣言

```tsx
function range(min: number, max: number): number[] {
	...
}
```

### 返り値がない関数を作る

`void型`を使用する

- Ex.
    
    ```tsx
    function helloWorldTimes(n: number): void {
    	for(let i=0; i < n; i++) {
    		console.log("Hello World")
    	}
    }
    ```
    
- 早期リターンで戻り値がないときもvoid側を使用