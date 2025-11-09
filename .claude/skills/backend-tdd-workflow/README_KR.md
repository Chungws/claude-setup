# Backend TDD Workflow Skill

## 개요

Dudaji Dashboard의 Test-Driven Development(TDD) 워크플로우를 정의한 스킬입니다. **Test-First는 필수**입니다.

## 언제 사용하나요?

- Backend 기능을 새로 개발할 때
- 버그를 수정할 때 (재현 테스트 먼저)
- 리팩토링할 때 (테스트로 안전망 확보)
- 테스트 코드를 작성/검토할 때

## 핵심 규칙

1. **Red-Green-Refactor 사이클 준수**
   - 🔴 Red: 실패하는 테스트 먼저 작성
   - 🟢 Green: 최소한의 코드로 테스트 통과
   - 🔵 Refactor: 코드 개선 (테스트는 계속 통과)

2. **Test-First 필수** - 구현 전에 테스트를 반드시 작성
3. **AAA 패턴** - Arrange, Act, Assert 구조
4. **pytest 사용** - 비동기 테스트는 `@pytest.mark.asyncio`

## 워크플로우

```bash
# 1. 🔴 RED: 실패하는 테스트 작성
# tests/test_translation.py
def test_create_translation_result():
    response = client.post("/api/v1/translations", json={...})
    assert response.status_code == 200

# 실행 → 실패 확인
uv run pytest tests/test_translation.py -v
# FAILED (구현 안됨)

# 2. 🟢 GREEN: 최소 구현
# app/translation/router.py
@router.post("/")
def create_result(data: dict):
    return {"status": "ok"}

# 실행 → 통과 확인
uv run pytest tests/test_translation.py -v
# PASSED

# 3. 🔵 REFACTOR: 코드 개선
# 실제 로직 구현, 타입 추가, 리팩토링
# 테스트는 계속 통과해야 함
```

## 예시

```python
# ✅ CORRECT: TDD 순서
# 1. 테스트 먼저
def test_get_translation_by_id():
    response = client.get("/api/v1/translations/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# 2. 구현
@router.get("/{id}")
def get_translation(id: int):
    return {"id": id}

# ❌ WRONG: 구현 먼저, 테스트 나중
# Don't do this!
```

## 팁

이 스킬은 Claude가 Backend 기능을 개발하거나 테스트를 작성할 때 자동으로 로드됩니다.
