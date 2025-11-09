# Committing Changes Skill

## 개요

this project의 Git 커밋 가이드라인을 정의한 스킬입니다. `<type>: <subject>` 형식의 커밋 메시지 규칙을 따릅니다.

## 언제 사용하나요?

- Git 커밋을 작성할 때
- 커밋 메시지 형식을 확인해야 할 때
- Granular commit 전략을 적용해야 할 때
- 코드 리뷰에서 커밋 히스토리를 평가할 때

## 핵심 규칙

1. **형식:** `<type>: <subject>` (예: `feat: add user authentication`)
2. **작은 커밋:** 10-50 lines per commit (이상적), 최대 100-200 lines
3. **Granular commits:** 논리적 단위로 커밋 분리 (models → schemas → service → router → tests)
4. **커밋 전 ruff 체크:** Backend 변경 시 `uvx ruff check` 필수 통과
5. **현재형 동사:** "add" (O), "added" (X)
6. **Claude 기여 표시:** Co-Authored-By: Claude 추가

## 왜 작은 커밋인가?

1. **리뷰 용이** - 리뷰어가 각 변경사항을 명확히 이해
2. **버그 추적** - 어느 커밋에서 버그가 발생했는지 찾기 쉬움
3. **안전한 롤백** - 특정 변경사항만 되돌릴 수 있음
4. **명확한 히스토리** - Git log가 기능 구현 스토리를 명확히 보여줌
5. **원자적 변경** - 각 커밋이 완전하고 독립적인 단위

## 커밋 타입

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새 기능 추가 | `feat: add translation API` |
| `fix` | 버그 수정 | `fix: resolve null pointer error` |
| `refactor` | 리팩토링 | `refactor: simplify auth logic` |
| `test` | 테스트 추가 | `test: add user service tests` |
| `docs` | 문서 수정 | `docs: update API documentation` |

## 커밋 전 체크리스트

### Backend 변경 시

```bash
cd backend

# 1. Ruff 체크 (필수!)
uvx ruff check              # 코드 품질
uvx ruff format --check     # 포매팅
# 둘 다 ✅ 통과해야 커밋 가능

# 개발 중 자동 수정
uvx ruff check --fix        # 린트 자동 수정
uvx ruff format             # 포매팅 적용

# 2. 커밋 크기 확인
git diff --stat
# 10-50 lines: 이상적 ✅
# 100-200 lines: 괜찮음 ⚠️
# 300+ lines: 분할 필요 ❌

# 3. 커밋
git add file.py
git commit -m "feat: add model"
```

### Backend 코드 스타일 필수 규칙

**1. Import 위치**
- ✅ 파일 맨 위에만
- ❌ 함수/클래스 중간에 import 금지

**2. 주석 영어 only**
- ✅ 영어로만 작성
- ❌ 한글 주석 절대 금지

**3. Type Hints 필수**
- ✅ 모든 함수에 타입 명시
```python
def get_user(user_id: int, db: Session) -> User | None:
    ...
```

### Frontend 변경 시

```bash
cd frontend

# 1. Lint 체크
npm run lint

# 2. 커밋
git add file.tsx
git commit -m "feat: add component"
```

## 예시

### ✅ GOOD: 작은 커밋들

```bash
git commit -m "feat: add TranslationResult model"           # 15 lines
git commit -m "feat: add TranslationResult schemas"         # 25 lines
git commit -m "feat: implement translation service"         # 45 lines
git commit -m "feat: add translation API endpoints"         # 35 lines
git commit -m "test: add translation tests"                 # 50 lines

# 총 5개 커밋, 각각 10-50 lines
# 리뷰 용이, 롤백 용이, 히스토리 명확
```

### ❌ BAD: 거대한 커밋

```bash
git commit -m "feat: add translation feature"  # 500 lines

# 문제점:
# - 리뷰 어려움 (한 번에 500줄)
# - 버그 발생 시 어디서 생겼는지 불명확
# - 일부만 롤백 불가능
```

## 팁

- 이 스킬은 Claude가 커밋을 생성하거나 검증할 때 자동으로 로드됩니다
- Backend 커밋 전에는 **항상** `uvx ruff check` 실행 필수
- 커밋이 100줄 넘으면 분할 고려: `git add -p`로 일부만 스테이징 가능
