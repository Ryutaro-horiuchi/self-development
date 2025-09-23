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
            start = s;
            end = e;
        }
    }
    result.push([start, end]);
    return result;
}
;
console.log(merge([[1, 3], [2, 6], [8, 10], [15, 18]]));
//# sourceMappingURL=56.js.map