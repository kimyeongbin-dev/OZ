// 함수(function)
function add(num1, num2) {
    // 반환(return) = 호출부로 값을 되돌려주는 것
    return num1 + num2;
}

let myfunction = add;
console.log(myfunction);
console.log(add(1, 2));

// console.log(add(1, 2));

// let result = add(1, 2);
// console.log(result);

function wrapper(func) {
    const result = func(1, 2);
    console.log(result);
}

wrapper(add)