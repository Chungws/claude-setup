---
name: fix
description: >
  작은 버그 수정, 후속 수정, 개선 등을 처리한다. issue URL/번호도 지원.
  plan 없이 바로 구현 → gate → simplify.
  "/ludo:fix", "고쳐줘", "수정해줘" 등의 요청 시 활성화.
user-invocable: true
argument-hint: "<what-to-fix | issue-url | #issue-number>"
---

# Fix — Lightweight Build (No Plan, No Multi-Review)

## 언제 쓰는가
- 버그 수정, 오타, 작은 개선
- 사용 후 발견된 후속 수정
- ludo:go로 돌리기엔 과잉인 작업
- issue에 기술된 간단한 버그/개선

## Input

$ARGUMENTS는 다음 중 하나:

| 입력 형태 | 예시 | 동작 |
|-----------|------|------|
| Issue URL | `https://github.com/owner/repo/issues/42` | issue 내용 fetch → 수정 지시로 사용 |
| Issue 번호 | `#42`, `42` | 현재 repo의 issue를 fetch → 수정 지시로 사용 |
| 자연어 | `config 파서에서 NPE 수정` | 기존 동작 그대로 |
| 없음 | (빈 인자) | 물어본다 |

### Input 해석 절차

1. $ARGUMENTS가 URL 패턴(`https://github.com/.../issues/` 또는 `https://gitlab.../issues/`)이면 → **Issue 모드**
2. $ARGUMENTS가 `#숫자` 또는 순수 숫자이면 → **Issue 모드** (현재 repo)
3. 그 외 → **자연어 모드** (기존 동작)

### Issue 모드

1. issue 내용을 fetch한다 (MCP 도구 또는 CLI 중 사용 가능한 것 사용)
2. fetch한 issue 내용을 수정 지시로 사용
3. issue 내용이 모호하거나 정보 부족 시:
   ```
   issue 내용이 불충분합니다. issue #{number}에 수정 대상과 기대 동작이 명확하지 않습니다.
   issue를 보강한 후 다시 실행해주세요.
   ```
   → 종료. PR 미생성.
4. `ISSUE_NUMBER`와 `ISSUE_URL`을 파이프라인 전체에서 참조할 수 있도록 기억한다.

---

## Pipeline

```
Input (자연어 또는 Issue)
  → Build → Gate (전체 코드베이스) → Simplify
  → 완료: PR/MR 생성 (issue 모드) 또는 보고 (자연어 모드)
```

plan/drift/멀티에이전트 리뷰 없음. gate + simplify만.

---

## Stage 1: Build

```
Agent(
  subagent_type: "ludo:build-fix",
  prompt: "다음을 수정하라: {fix_instruction}

{fix_instruction}는 다음 중 하나:
- Issue 모드: fetch한 issue 내용 (issue #{number})
- 자연어 모드: $ARGUMENTS 그대로

입력: CLAUDE.md, 관련 코드

절차:
1. 문제가 되는 코드를 찾아 읽어라
2. 수정하라
3. 관련 테스트가 있으면 수정, 없으면 추가하라
4. ruff check --fix && ruff format && mypy . && pytest
5. 커밋하라 (fix: {요약})

대화 히스토리 참조 금지. 코드만 읽어라.")
```

## Stage 2: Gate

Build와 **다른 에이전트**:

```
Agent(
  subagent_type: "ludo:gate",
  prompt: "방금 수정된 코드의 품질 게이트를 실행하라.

전체 코드베이스 대상:
1. ruff check . → PASS/FAIL
2. ruff format --check . → PASS/FAIL
3. mypy . → PASS/FAIL
4. pytest --tb=short --cov --cov-fail-under=100 → PASS/FAIL
5. 새 # noqa / # type: ignore → 이유 + 합리성 판단

GATE_RESULT: PASS/FAIL, FAIL_ITEMS: [목록]")
```

**FAIL:** Agent(ludo:fix)로 수정 → re-gate. 최대 3회.

## Stage 3: Simplify

Gate PASS 후:

```
Agent(prompt: "방금 수정된 코드를 리뷰하고,
단순화할 수 있는 부분을 찾아 수정하라.
수정 후 테스트가 여전히 green인지 확인하라.
변경이 있으면 커밋하라 (refactor: simplify {영역}).")
```

Simplify가 코드를 수정하면 → gate 한 번 더.

## Stage 4: 완료 처리

### 4a. PR/MR 생성 (Issue 모드일 때)

Gate PASS 후 ISSUE_NUMBER가 있으면:

1. 작업 브랜치를 push:
   ```bash
   git push -u origin $(git branch --show-current)
   ```
2. PR/MR 생성 (제목 `fix: {수정 요약}`, `closes #{ISSUE_NUMBER}` 포함)

**실패 시** (gate 3회 실패 등 파이프라인 중단): PR/MR을 생성하지 않는다. 실패 보고만 한다.

### 4b. 완료 보고

```
## Fix Complete: {수정 내용 요약}

### 변경
- {파일}: {뭘 바꿨는지}

### 커밋
- {hash} {message}

### Gate
- ruff: PASS | mypy: PASS | pytest: PASS (coverage {N}%)

### Simplify
- {변경 여부 + 내용}

### PR/MR (issue 모드일 때)
- {PR/MR URL} — closes #{ISSUE_NUMBER}
```

## 제약
- plan 없음, drift 없음, 멀티에이전트 리뷰 없음
- gate는 항상 전체 코드베이스 대상 (치트 방지)
- 수정 범위가 커지면 멈추고 "ludo:go 사용을 권장합니다" 보고
- Issue 모드에서 파이프라인 실패 시 PR/MR을 생성하지 않고 실패 내용만 보고한다.
- Issue URL이 아닌 기존 입력(자연어)은 기존 동작 그대로 유지.
