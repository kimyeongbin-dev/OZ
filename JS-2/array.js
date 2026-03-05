// 배열(array)
let numbers = [10, "two", 30];

for (let i = 0; i < numbers.length; i++) {
    console.log(numbers[i]);
}

for (const num of numbers) {
    console.log(num);
}

for (const [i, num] of numbers.entries()) {
    console.log(i + "번 index 값: " + num);
}