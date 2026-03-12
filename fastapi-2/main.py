from fastapi import FastAPI, Path, Query

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


# 회원가입 API
# HTTP Method: GET, POST, PUT, PATCH, DELETE
@app.post("/users/sign-up")
def signup_user_handler():
    return {"msg": "hello"}

# 1번 댓글(comment) 조회
# GET /comments/1

# 10번 댓글 삭제
# DELETE /comments/10

# 새로운 댓글 생성
# POST /comments

# 요청 = HTTP Method(동작, verb) + URL(대상, object)


# 회원 검색 API
# Query Parameter
# ?key=value 형태로 Path 뒤에 붙는 값
# 데이터 조회시 부가 조건을 명시(필터링, 정렬, 검색, 페이지네이션 등)
@app.get("/users/search")
def search_user_handler(
    # name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다.
    name: str = Query(default=..., min_length=2), # ... -> 필수값(required) <> 선택적(optional)
    age: int = Query(None, ge=1), # default 값 지정 -> 선택적(optional)
):
    return {"name": name, "age": age}

# Path Parameter 과 Query Parameter의 차이
# 둘 다 매개변수를 받지만, 경로 상에 변수가 있을 경우 Path, 없을경우 Query로 받도록 구현되어 있음.


# 단일 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는지 검사 & 보장
# ... = Ellipsis -> (= 생략), 하나의 값
# Path에 Ellipsis를 넣으면, 결로에 필수로 있는 값이라고 인식한다.
# ge=1 -> 1 이상(Getter than or Equal)

# GET /users/1?field=id     -> id 반환
# GET /users/1?field=name   -> name 반환
# GET /users/1              -> id, name 반환
@app.get("/users/{user_id}")
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
):
    
    user = users[user_id - 1]

    if field in ["id", "field"]:
        return {field: user[field]}
    return user


##### 실습 ######

# GET /items/{item_name}
# item_name: str & 최대 글자수(max_length) 6
# 응답 형식: {"item_name": ...}
items = [
    {"id": 1, "name": "apple"},
    {"id": 2, "name": "banana"},
    {"id": 3, "name": "cherry"},
]

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6)
):
    return {"item_name": item_name}