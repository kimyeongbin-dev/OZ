// 변수 선언
let num1 = 15;
let num2 = 10;

// 연산자 정의
let operator = '*';

// 연산자별 결과 출력
let result;

if (operator === '+') {
    result = num1 + num2;
} else if (operator === '-') {
    result = num1 - num2;
} else if (operator === '*') {
    result = num1 * num2;
} else if (operator === '/') {
    result = num1 / num2;
} else {
    result = '올바르지 않은 연산자입니다.';
}

console.log(`결과: ${result}`);
