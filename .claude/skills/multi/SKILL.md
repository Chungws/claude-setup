---
name: multi
description: >
  This skill should be used when the user asks to "multi", "멀티", "여러 모델한테 물어봐",
  "다중 모델", "codex gemini한테도", "여러 모델로 리뷰", "멀티 리뷰", "multi-review",
  or wants to run the same prompt across multiple AI CLI models in parallel.
user-invocable: true
---

# Multi-Model CLI

동일한 프롬프트를 여러 AI CLI(Claude Code, Codex CLI, Gemini CLI)에 병렬로 보내고,
현재 세션의 Claude가 결과를 종합하여 합의/분기점을 보여준다.
각 CLI는 git worktree 격리 환경에서 전체 코드베이스에 접근하며 독립적으로 실행된다.

## Trigger
`/multi "프롬프트"` 또는 자연어로 멀티모델 요청 시 활성화.

## Input
`$ARGUMENTS`에서 프롬프트와 에이전트를 추출한다.
- 첫 번째 인자 또는 따옴표로 감싼 문자열 → 프롬프트
- 나머지 → 에이전트 목록 (optional, default: claude codex gemini)

사용 예시:
- `/multi 이 브랜치의 변경사항 리뷰해줘`
- `/multi "보안 취약점 찾아줘" claude gemini`
- `/multi "테스트 전략 제안해줘"`
- `/multi "이 함수를 리팩토링하는 방법 3가지"`

## Process

### Phase 1: 에이전트 병렬 실행
`scripts/run.sh`를 실행하여 모든 에이전트의 응답을 수집한다.

```bash
RESULTS_DIR=$(bash ~/.claude/skills/multi/scripts/run.sh "$PROMPT" [agents...])
```

스크립트가 반환한 `$RESULTS_DIR` 경로의 파일들을 Read tool로 읽는다:
- `$RESULTS_DIR/claude.json` — Claude Code 응답
- `$RESULTS_DIR/codex.json` — Codex CLI 응답
- `$RESULTS_DIR/gemini.json` — Gemini CLI 응답

에이전트 실행 실패 시 `"error": "execution failed"` 이 포함된다. 해당 에이전트는 건너뛴다.

### Phase 2: 종합 분석
현재 세션의 Claude는 **종합자** 역할만 하며, 응답 자체는 별도 인스턴스들이 수행한다.
각 모델의 응답을 비교하여 아래 형식으로 출력한다.

```
## 멀티모델 응답 종합

### 🔴 합의 — 모든 모델이 동의
모든 모델이 동일하게 지적/제안한 내용. 신뢰도 최고.

### 🟡 다수 동의 — 대부분 동의
대부분의 모델이 언급한 내용.

### 🔵 고유 의견 — 한 모델만 제시
한 모델만 제시한 내용. 다른 모델이 놓친 것일 수 있다.

#### Claude
- ...

#### Codex
- ...

#### Gemini
- ...

### 📊 요약
- 참여 모델: N개
- 합의율: N%
```

프롬프트가 코드 리뷰인 경우 severity(critical/warning/info)와 file:line을 포함한다.

## 주의사항
- 최소 2개 에이전트가 필요하다.
- 각 에이전트는 별도 worktree에서 전체 코드베이스에 접근한다.
- worktree 브랜치는 실행 후 자동 정리된다.

## Prerequisites
- Claude Code: 이미 설치됨 (`claude -p` 사용)
- Codex CLI: `npm install -g @openai/codex` + `OPENAI_API_KEY` 환경변수
- Gemini CLI: `npx -y @google/gemini-cli` (설치 없이 실행) + Google 인증
