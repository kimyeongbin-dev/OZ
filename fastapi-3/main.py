from fastapi import FastAPI, Path, Query, status, HTTPException, Body

from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

app = FastAPI()

# 서버에 GET /hello 요청이 들어오면, root_handler를 실행한다.
@app.get("/hello")
def hello_handler():
    return {"ping": "pong"}

users: list[dict[str, int | str]] = [
    {"id": 1, "name": "alex", "age": 20},
    {"id": 2, "name": "bob", "age": 30},
    {"id": 3, "name": "chris", "age": 40},
]

# 전체 사용자 조회 API
@app.get(
    "/users",   
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
def get_users_handlers(
):
    return users


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
@app.get(
    "/users/search",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def search_user_handler(
    # name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다.
    name: str = Query(default=..., min_length=2), # ... -> 필수값(required) <> 선택적(optional)
    age: int = Query(None, ge=1), # default 값 지정 -> 선택적(optional)
):
    return {"id": 0, "name": name, "age": age}

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
@app.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    # response_model=UserResponse,
)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"),
    field: str = Query(None, description="출력할 필드 선택(id 또는 name)"),
):
    if user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자의 ID입니다.",
        )
    
    user = users[user_id - 1]

    if field in ["id", "field"]:
        return {field: user[field]}
    return user



# 회원가입 API
@app.post(
    "/users/sign-up",
    status_code=status.HTTP_201_CREATED,

    # 응답은 UserResponse 데이터 구조를 따라야한다.
    # UserResponse(id: int, name: str, age: int | None)

    # 1) 서버에서 원하는 데이터 형식으로 응답이 반환되는 지 검증
    # 2) 노출되면 안 되는 값을 자동으로 제거
    # 3) API 문서에 예상되는 응답 출력
    response_model=UserResponse,
)
def sign_up_handler(body: UserSignUpRequest):
    # Pydantic
    # 함수에 선언한 매개변수의 타입힌트가 BaseModel을 상속 받은 경우, 요청 본문에서 가져옴
    # 데이터 가져오면서, 타입힌트에 선언한 데이터 구조와 맞는지 검사
    
    # body = UserSignUpRequest(name=..., age=...)
    # body 데이터가 문제 없으면 -> 핸들러 함수로 전달
    # body 데이터가 문제 있으면 -> 즉시 실행이 멈추고, 422 에러
    
    new_user = {
        "id": len(users) + 1, "name": body.name, "age": body.age,
        # "grade": "special" # 특별 유저 -> 실수로 응답에 노출
    }

    users.append(new_user)
    return new_user

    # name, age만 응답 -> response_model이랑 안 맞음 => FastAPI ResponseValidationError
    # return {"name": body.name, "age": body.age}

# 사용자 정보 수정 API
@app.patch(
    "users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
):
    # Pseudo Code
    # 1-a) user_id 검증
    if user_id > len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자의 ID입니다.",
        )
    
    # 1-b) body 데이터 검증
    if body.name is None and body.age is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 데이터가 없습니다.",
        )

    # 2) 사용자 조회 & 수정
    user = users[user_id - 1]

    # 1) name만 수정하는 경우               -> L#135
    # 2) age만 수정하는 경우                -> L#138
    # 3) name, age 모두 수정하는 경우       -> L#135 & L#138
    # 4) name, age 모두 수정하지 않는 경우  -> 1-b 처리

    if body.name is not None:
        user["name"] = body.name

    if body.age is not None:
        user["age"] = body.age

    # 3) 응답 반환
    return user


#################### 실습 ########################
items = [
    {"id": 1, "name": "apple"},
    {"id": 2, "name": "banana"},
    {"id": 3, "name": "cherry"},
]

# GET /items/{item_name}
# item_name: str & 최대 글자수(max_length) 6
# 응답 형식: {"item_name": ...}

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6)
):
    return {"item_name": item_name}