# Self Code Review Skill

## 개요

MR 생성 전 자체 코드 리뷰 체크리스트를 제공하는 스킬입니다. Backend/Frontend 변경사항에 대한 종합 검증을 수행합니다.

## 언제 사용하나요?

- MR 생성 전 (/review-phase 실행 시)
- 코드 리뷰 체크리스트를 확인해야 할 때
- 모든 컨벤션을 준수했는지 검증할 때

## 핵심 규칙

**자체 리뷰는 MR 생성 전 필수입니다.**

### 공통 체크리스트

```
[ ] feature/* 브랜치 사용 (develop/main 아님)
[ ] Conventional Commits (<type>: <subject>)
[ ] MR 크기 300줄 이하
[ ] Target branch: develop
[ ] MR 언어: 한국어
```

### Backend 체크리스트

```
[ ] TDD: 테스트 먼저 작성
[ ] Foreign Keys 미사용 (index만)
[ ] uv add로 의존성 추가
[ ] alembic --autogenerate 사용
[ ] 코드 스타일: Import 위치, 영어 주석, Type hints
[ ] uvx ruff check 통과 ✅
[ ] uvx ruff format --check 통과 ✅
[ ] uv run pytest -s 통과 ✅
```

### Frontend 체크리스트

```
[ ] RSC 패턴 준수
[ ] shadcn/ui 사용
[ ] npm run lint 통과 ✅
[ ] Chrome DevTools MCP 검증 완료 ✅ (UI 변경 시 필수!)
```

## 사용법

```bash
# 자동 리뷰 (권장)
/review-phase

# 수동 체크
cd backend && uvx ruff check && uvx ruff format --check && uv run pytest -s
cd frontend && npm run lint
git diff develop --shortstat  # 라인 수 확인
```

## Backend 코드 스타일 필수 규칙

1. **Import 위치** - 파일 맨 위에만 (함수 안 금지)
2. **주석 영어 only** - 한글 주석 절대 금지
3. **Type Hints 필수** - 모든 함수 파라미터/리턴값에 타입 명시

## 팁

이 스킬은 `/review-phase` 명령어 실행 시 자동으로 로드됩니다.
