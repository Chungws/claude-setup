# Alembic Migrations Skill

## 개요

this project의 데이터베이스 마이그레이션 관리 규칙을 정의한 스킬입니다. Alembic을 사용하며 **--autogenerate는 필수**입니다.

## 언제 사용하나요?

- SQLModel 모델을 수정한 후
- 데이터베이스 스키마를 변경해야 할 때
- 마이그레이션 파일을 생성/적용할 때
- 마이그레이션 충돌을 해결해야 할 때

## 핵심 규칙

1. **--autogenerate 필수** - 수동으로 마이그레이션 파일 생성 금지
2. **직접 편집 금지** - 자동 생성된 파일을 손으로 수정하지 않음 (데이터 마이그레이션 제외)
3. **모델 + 마이그레이션 함께 커밋** - 항상 같이 커밋
4. **PostgreSQL 실행 필수** - `docker compose up -d` 먼저

## 워크플로우

```bash
# 1. 모델 수정
# app/translation/models.py
class TranslationResult(SQLModel, table=True):
    score: float | None = Field(default=None)  # 새 필드 추가

# 2. PostgreSQL 실행 확인
docker compose up -d

# 3. 마이그레이션 자동 생성
uv run alembic revision --autogenerate -m "add score field"

# 4. 마이그레이션 적용
uv run alembic upgrade head

# 5. 함께 커밋
git add app/translation/models.py migrations/versions/*.py
git commit -m "feat: add score field to TranslationResult"
```

## 예시

```bash
# ✅ CORRECT
uv run alembic revision --autogenerate -m "add user email field"
uv run alembic upgrade head

# ❌ WRONG
touch migrations/versions/001_add_email.py  # NEVER!
alembic revision -m "..."  # Missing --autogenerate!
```

## 충돌 해결

```bash
# Multiple head error 발생 시
rm migrations/versions/충돌파일.py  # 충돌 파일 삭제
git pull origin develop  # 최신 마이그레이션 받기
uv run alembic upgrade head  # 다른 사람 마이그레이션 적용
uv run alembic revision --autogenerate -m "your changes"  # 재생성
```

## 팁

이 스킬은 Claude가 데이터베이스 모델을 수정하거나 마이그레이션을 생성할 때 자동으로 로드됩니다.
