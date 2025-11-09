# FastAPI Patterns Skill

## 개요

this project의 FastAPI 아키텍처 패턴을 정의한 스킬입니다. 4-Layer 구조를 따르며 비즈니스 로직은 Service Layer에 집중합니다.

## 언제 사용하나요?

- Backend API 엔드포인트를 만들 때
- FastAPI 프로젝트 구조를 설계할 때
- Service/Router 계층을 나누는 방법이 궁금할 때

## 핵심 규칙

1. **4-Layer 구조**: models → schemas → service → router
2. **비즈니스 로직은 Service Layer에**
3. **Router는 얇게** (요청/응답 처리만)
4. **모든 DB 호출은 async/await**

## 파일 구조

```
app/feature/
├── models.py      # SQLModel 테이블
├── schemas.py     # Pydantic 스키마
├── service.py     # 비즈니스 로직
└── router.py      # API 엔드포인트
```

## 예시

```python
# 1. Model (테이블)
class Feature(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

# 2. Schemas (API 입출력)
class FeatureCreate(BaseModel): ...
class FeatureResponse(BaseModel): ...

# 3. Service (비즈니스 로직)
class FeatureService:
    @staticmethod
    async def create(db: AsyncSession, data: FeatureCreate):
        ...

# 4. Router (엔드포인트)
@router.post("/", response_model=FeatureResponse)
async def create_feature(
    data: FeatureCreate,
    db: AsyncSession = Depends(get_db)
):
    return await FeatureService.create(db, data)
```

## Schema 네이밍

- `*Create` - POST 요청 body
- `*Update` - PUT/PATCH 요청 body
- `*Response` - API 응답
- `*Filter` - Query parameters

## 팁

이 스킬은 Backend 기능을 개발할 때 자동으로 로드됩니다.
