# SQLModel No Foreign Keys Skill

## 개요

Dudaji Dashboard의 데이터베이스 모델링 규칙을 정의한 스킬입니다. 이 프로젝트는 **Foreign Key를 절대 사용하지 않는** 정책(ADR-001)을 따릅니다.

## 언제 사용하나요?

- SQLModel 모델을 작성할 때
- 데이터베이스 테이블 관계를 설계할 때
- Foreign Key 사용 여부를 판단해야 할 때
- 서비스 레이어에서 데이터 무결성을 관리해야 할 때

## 핵심 규칙

1. **Foreign Key 절대 금지** - `foreign_key` 파라미터 사용 불가
2. **Index만 사용** - 관계는 `Field(index=True)`로만 표현
3. **서비스 레이어에서 무결성 관리** - 트랜잭션으로 데이터 일관성 보장

## 예시

```python
# ✅ CORRECT
class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sample_id: int = Field(index=True)  # Index only, NO FK

# ❌ WRONG
class TranslationResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sample_id: int = Field(foreign_key="sample.id")  # NEVER!
```

## 관련 문서

- [ADR-001 발췌](./references/adr-001-excerpt.md) - FK 금지 정책의 상세 근거

## 팁

이 스킬은 Claude가 "sample_id를 Foreign Key로 만들어도 돼?"와 같은 질문을 받으면 자동으로 로드됩니다.
