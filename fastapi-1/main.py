from fastapi import FastAPI

app = FastAPI()

# 서버에 GET /hello 요청이 들어오면, root_handler를 실행한다.
@app.get("/hello")
def hello_handler():
    return {"ping": "pong"}

users = [
    {"id": 1, "name": "alex"},
    {"id": 2, "name": "bob"},
    {"id": 3, "name": "chris"},
]

# 전체 사용자 조회 API
@app.get("/users")
def get_users_handlers():
    return users

# {user_id}번 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사 & 보장
@app.get("/users/{user_id}")
def get_user_handler(user_id: int):
    return users[user_id - 1]