---
name: quality-setup
description: 프로젝트에 ruff + mypy + pytest 품질 설정을 적용한다. "/quality-setup", "린트 설정", "ruff 적용", "품질 설정" 등의 요청 시 활성화.
---

# Quality Setup

프로젝트의 `pyproject.toml`에 ruff + mypy + pytest 설정을 적용한다.

## 템플릿

`~/.claude/skills/quality-setup/quality-config.toml` 파일을 읽어서 설정값을 가져온다.

## Step 1: 프로젝트 확인

1. 현재 디렉토리 또는 사용자가 지정한 프로젝트 경로 확인
2. `pyproject.toml` 존재 여부 확인
3. `pyproject.toml`이 없으면 `uv init --lib`로 프로젝트 생성

## Step 2: 적용 범위 확인

사용자에게 물어본다:

```
적용할 설정을 선택하세요:
1. 전체 (ruff + mypy + pytest)
2. ruff + mypy
3. ruff만
4. 선택 적용
```

## Step 3: Python 버전 확인

프로젝트의 Python 버전을 확인한다:
- `pyproject.toml`의 `requires-python` 또는 `tool.poetry.dependencies.python` 확인
- 없으면 사용자에게 물어본다
- `target-version`을 해당 버전에 맞게 조정

## Step 4: 적용

- `pyproject.toml`이 없으면: `uv init --lib`로 생성 후 진행
- `pyproject.toml`이 있고 해당 섹션이 없으면: 섹션 추가
- `pyproject.toml`이 있고 해당 섹션이 있으면: 덮어쓸지 사용자에게 확인

기존 `pyproject.toml`의 다른 섹션은 절대 건드리지 않는다.

### dev 의존성 설치

`[dependency-groups]` dev 그룹에 추가하고 `uv sync`로 설치:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=6.0",
    "pytest-asyncio>=0.24",
    "mypy>=1.13",
    "ruff>=0.8",
]
```

### pytest 설정 적용 시

- `testpaths`는 프로젝트의 실제 테스트 디렉토리에 맞게 조정
- `--cov` 대상은 프로젝트의 소스 디렉토리에 맞게 조정 (예: `--cov=src`)
- `tests/` 디렉토리가 없으면 생성

### mypy overrides

서드파티 라이브러리 중 타입 스텁이 없는 경우, 사용자에게 안내:

```
mypy에서 import 에러가 나는 라이브러리가 있으면 다음을 추가하세요:

[[tool.mypy.overrides]]
module = ["라이브러리명.*"]
ignore_missing_imports = true
```

## Step 5: 완료 요약

```
적용 완료:
- [x] ruff (N개 카테고리, M개 ignore)
- [x] mypy (strict mode)
- [x] pytest (coverage 100%, Layer 3 마커 분리)

실행 방법:
  uv run ruff check .          # 린트
  uv run ruff check --fix .    # 린트 + 자동 수정
  uv run ruff format .         # 포맷팅
  uv run mypy src/             # 타입 체크
  uv run pytest                # 테스트 (Layer 1+2, with coverage)
  uv run pytest -m integration # Integration 테스트 (Layer 3)
```

## 주의사항

- 기존 `pyproject.toml`의 ruff/mypy/pytest 외 섹션은 절대 건드리지 않는다
- 템플릿의 설정값을 그대로 사용한다 — 임의로 규칙을 추가/제거하지 않는다
- `target-version`, `testpaths`, `--cov` 대상만 프로젝트에 맞게 조정한다
