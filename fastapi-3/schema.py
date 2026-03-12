from pydantic import BaseModel

# 회원가입 시 요청 본문(Request Body)의 데이터 형태
class UserSignUpRequest(BaseModel):
    name: str   # 필수값(required)
    age: int | None = None


# 사용자 정보 응답 본문(Response Body)의 데이터 형태
class UserResponse(BaseModel):
    id: int
    name: str
    age: int | None


# 사용자 정보 수정 요청 본문
class UserUpdateRequest(BaseModel):
    name: str | None = None # 선택적
    age: int | None = None  # 선택적

# 부분 수정(PUT)
# 1) name만 수정하는 경우
# 2) age만 수정하는 경우
# 3) name, age 모두 수정하는 경우