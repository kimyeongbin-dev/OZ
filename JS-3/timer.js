// Timer API = 시간을 다루는 기능
// setTimeOut(함수, 시간(ms)) -> 일정 시간이 지난 다음에 함수를 실행
// setTimeout(() => console.log("5초 경과."), 5000);

// setInterval(함수, 시간(ms)) -> 일정 시간마다 함수를 반복 실행
const timerId = setInterval(() => console.log("1초마다 실행"), 1000);

setTimeout(() => clearInterval(timerId), 5000);