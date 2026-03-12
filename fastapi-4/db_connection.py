# SQLAlchemy 사용에 필요한 기본 설정

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 접속 정보(DB 종류, 주소, 포트번호, 사용자, 비밀번호, DB이름)
# sqlite:// -> sqlite를 사용하겠다.
# /./test.db -> 현재 프로젝트 경로에 test.db라는 이름의 파일을 만들어라
# => 데이터베이스를 따로 실행하거나 따로 만들지 않아도, sqlalchemy를 이용해서 엔진을 연결하는 순간에, 현재 폴더에 test.db라는 파일이 자동으로 생성된다.
DATABASE_URL = "sqlite:///./test.db"

# Engine: DB와 연결을 제공하는 객체
engine = create_engine(DATABASE_URL)

# Session: DB 작업단위

# sessionmaker: 클래스를 만들어주는 함수
# sessionmaker()의 역할 -> class SessionFactory(...): 같이 클래스 만들어 줌

# SessionFactory: 세션을 생성하는 클래스
SessionFactory = sessionmaker(
    bind=engine,    # 엔진을 연결

    # 기본 옵션
    autocommit=False,       # 자동으로 commit()
    autoflush=False,        # 자동으로 flush() 실행
    expire_on_commit=False, # commit() 후에 자동으로 데이터 만료(expire)
)

# 세션 인스턴스 생성
# session = SessionFactory()


# return -> 호출부로 값 반환 & 실행한 함수 종료
# yield -> 호출부로 값 반환 & 실행한 함수 일시정지
def get_session():
    with SessionFactory() as session:
        yield session
    
    # 아래와 완전히 동일하게 동작
    # session = SessionFactory()

    # try:
    #     yield session
    # finally:
    #     session.close()