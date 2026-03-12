from fastapi import FastAPI, Path, Query, status, HTTPException, Body, Depends
from sqlalchemy import select

from db_connection import SessionFactory, get_session
from models import User
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

app = FastAPI()

# 서버에 GET /hello 요청이 들어오면, root_handler를 실행한다.
@app.get("/hello")
def hello_handler():
    return {"ping": "pong"}

# 전체 사용자 조회 API
@app.get(
    "/users",   
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
def get_users_handlers(
    # 요청 시작 -> session 생성
    # 응답 반환 -> session.close()
    session = Depends(get_session),
):
    # statement = 구분 -> SELECT * FROM user
    stat = select(User)
    result = session.execute(stat)

    # [user1, user2, ...]
    users = result.scalars().all()   # scalars() -> 모든 데이터를 가져올 때
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
    response_model=UserResponse,
)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"),
    session = Depends(get_session),
):
   
    stat = select(User).where(User.id == user_id)
    result = session.execute(stat)
    user = result.scalar()  # 1개의 데이터를 가져올 때

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자ID입니다.",
        )
    
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
def sign_up_handler(
    body: UserSignUpRequest,
    session = Depends(get_session),
):
    # Pydantic
    # 함수에 선언한 매개변수의 타입힌트가 BaseModel을 상속 받은 경우, 요청 본문에서 가져옴
    # 데이터 가져오면서, 타입힌트에 선언한 데이터 구조와 맞는지 검사
    
    # body = UserSignUpRequest(name=..., age=...)
    # body 데이터가 문제 없으면 -> 핸들러 함수로 전달
    # body 데이터가 문제 있으면 -> 즉시 실행이 멈추고, 422 에러
    
    # SQLAlchemy ORM을 통해 새로운 user 인스턴스 생성
    # id -> 데이터베이스가 관리하도록 위임
    new_user = User(name=body.name, age=body.age)

    # DB 작업 단위 & 임시 저장소
    # session = SessionFactory()

    # try:
    #     session.add(new_user)
    #     session.commit()    # DB에 저장
    # finally:
    #     # 항상 close()가 호출 -> 연결 종료
    #     session.close()
    
    # DB 작업 단위 & 임시 저장소
    # with 문 벗어나는 순간 close()가 자동 호출
    session.add(new_user)
    session.commit()    # DB에 저장
    
    return new_user

    # name, age만 응답 -> response_model이랑 안 맞음 => FastAPI ResponseValidationError
    # return {"name": body.name, "age": body.age}


# 사용자 정보 수정 API
@app.patch(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
    session = Depends(get_session),
):
   
    # 1) body 데이터 검증
    if body.name is None and body.age is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 데이터가 없습니다.",
        )

    # 2) 사용자 조회 
    stat = select(User).where(User.id == user_id)
    result = session.execute(stat)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자 ID입니다.",
        )
    
    if body.name is not None:
        user.name = body.name

    if body.age is not None:
        user.age = body.age

    session.commit()

    # 3) 응답 반환
    return user

# 사용자 삭제(회원탈퇴) API
@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT, # 응답 본문 X
)
def delete_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    stat = select(User).where(User.id == user_id)
    result = session.execute(stat)
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자 ID입니다.",
        )
    
    session.delete(user)
    session.commit()




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