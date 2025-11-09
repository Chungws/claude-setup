# Managing Python Dependencies Skill

## 개요

this project의 Python 의존성 관리 규칙을 정의한 스킬입니다. 이 프로젝트는 **uv만 사용**하며 pip은 절대 사용하지 않습니다.

## 언제 사용하나요?

- Python 패키지를 설치/제거할 때
- pyproject.toml이나 uv.lock 파일을 수정해야 할 때
- 의존성 관련 에러를 해결해야 할 때
- 새 프로젝트 환경을 설정할 때

## 핵심 규칙

1. **uv만 사용** - `pip install` 절대 금지
2. **직접 편집 금지** - pyproject.toml을 손으로 수정하지 않음
3. **uv.lock 커밋** - pyproject.toml과 uv.lock을 항상 함께 커밋
4. **uvx 활용** - 일회성 도구는 `uvx` 사용

## 주요 명령어

```bash
# 패키지 추가
uv add fastapi
uv add pytest --dev

# 패키지 제거
uv remove fastapi

# 프로젝트 실행
uv run uvicorn app.main:app
uv run pytest

# 일회성 도구
uvx ruff check
uvx isort .
```

## 예시

```bash
# ✅ CORRECT
uv add httpx
git add pyproject.toml uv.lock
git commit -m "deps: add httpx"

# ❌ WRONG
pip install httpx  # NEVER!
echo "httpx" >> pyproject.toml  # NEVER!
```

## 팁

이 스킬은 Claude가 패키지 설치나 의존성 관리 작업을 할 때 자동으로 로드됩니다.
