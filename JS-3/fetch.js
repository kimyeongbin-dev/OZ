// Fetch API = 서버에 HTTP 요청을 보내는 API

// 비동기 프로그래밍(Asyncronous Programming)
// 클라이언트는 서버에 요청을 보내는 순간, 서버가 언제 응답할지 알 수 없다.
// 응답을 기다리는 동안, 다른 작업을 처리

// // GET 요청
// fetch("https://jsonplaceholder.typicode.com/posts")
//     .then(response => response.json())
//     .then(data => console.log(data));

// POST 요청
fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({ title: "Hello", body: "World" })
})
    .then(response => response.json())
    .then(data => console.log(data));