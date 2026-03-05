// 정수 배열을 입력 받아서, 평균을 반환하는 함수

function getAverages(scores) {
    if (scores.length === 0) {
        return
    }

    let sum = 0;
    for(const score of scores) {
        sum += score;
    }
    return sum / scores.length;
}

console.log(getAverages([80, 90, 75, 83]));
console.log(getAverages([]));