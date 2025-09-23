"use strict";
function merge(intervals) {
    intervals.sort((a, b) => a[0] - b[0]);
    const result = [];
    let [start, end] = intervals[0];
    for (let i = 1; i < intervals.length; i++) {
        let [s, e] = intervals[i];
        if (s <= end) {
            end = Math.max(end, e);
        }
        else {
            result.push([start, end]);
        }
    }
    return result;
}
;
// 1 ~ 1000 のフラグ配列を用意。デフォルトは0。出てきた値を1にする
// フラグ配列をfor文で回して、1の区間を配列として出力するようにする
// 計算量はO(N)
console.log(merge([[1, 4], [4, 5]]));
//# sourceMappingURL=56.js.map