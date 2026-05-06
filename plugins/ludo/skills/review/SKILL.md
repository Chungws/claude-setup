---
name: review
description: >
  멀티에이전트 코드 리뷰. gate PASS 후 clean 코드 위에서 실행.
  기존 도구(pr-review-toolkit, simplify) + 커스텀 정합성 에이전트 병렬 스폰.
  모든 에이전트는 컨텍스트 없이 파일만 읽고 작업.
  "/ludo:review" 또는 ludo:go에서 자동 호출.
user-invocable: true
argument-hint: "[phase-number|branch|commit-range]"
---

# Review — Multi-Agent Code Review

## 원칙
- **gate PASS 후 실행** — clean 코드 위에서만 의미 있는 리뷰가 나옴.
- **컨텍스트 없이 실행** — 모든 에이전트는 파일만 읽는다.
- **Writer/Reviewer 분리** — build 에이전트와 다른 에이전트가 실행.
- **기존 도구 재사용** — 코드 리뷰는 검증된 도구, 정합성은 커스텀.

## Input
- $ARGUMENTS:
  - 숫자 → phase 번호
  - branch/range → git diff 범위
  - 없음 → `git diff main...HEAD`

---

## Phase 1: Context Discovery (silent)

arch-review 패턴으로 컨텍스트를 수집하여 서브에이전트에 전달:

```
## Project: {프로젝트명}
## Phase: {N}
## Review Scope: {git diff range}

## GOAL.md:
{목표, 요구사항, 제약, 경계 조건}

## PLAN.md Phase {N}:
{범위, 파일, 수용 기준, 아키텍처 결정}

## CLAUDE.md:
{프로젝트 규칙}

## Changes:
{git diff --stat}
{git log --oneline}
```

## Phase 2: Parallel Agent Spawn

**한 메시지에서 모두 동시에 스폰한다.**

### Group A: 코드 품질 (기존 도구)

```
Agent(
  subagent_type: "pr-review-toolkit:code-reviewer",
  prompt: "Phase {N}의 변경사항을 리뷰하라.
  버그, 로직 에러, 보안, 코드 품질, 프로젝트 컨벤션 준수를 확인하라.
  변경 범위: {range}")
```

### Group B: 정합성 (커스텀 서브에이전트)

각 에이전트에게 지시 파일 + 컨텍스트를 전달:

```
Agent(
  isolation: worktree,
  prompt: "너는 리뷰 서브에이전트다.

  ## Step 1: 지시 파일 읽기
  이 플러그인의 agents/{agent-file}.md 를 찾아 읽고 따르라.
  경로: ~/claude-setup/plugins/ludo/agents/{agent-file}.md

  ## Step 2: 컨텍스트
  {context}

  ## Step 3: 실행
  지시 파일의 Process에 따라 파일을 읽고 검증하라.

  ## 규칙:
  - 대화 히스토리 참조 금지. 파일만 읽어라.
  - 발견 사항마다 file:line 레퍼런스 필수
  - severity: Critical / Suggestion / Info
  - 최종 출력은 지시 파일의 Output Format을 따르라")
```

| # | 파일 | 역할 |
|---|------|------|
| 1 | goal-align.md | GOAL.md 요구사항/제약 정합성 |
| 2 | plan-align.md | PLAN.md 범위/수용기준/아키텍처 결정 |
| 3 | drift.md | 새 작업 발견 → PLAN.md 업데이트 |

## Phase 3: Synthesis

모든 에이전트 결과를 종합한다.

### 종합 규칙
1. **중복 제거**: 같은 이슈를 N개 에이전트가 발견하면 하나로 합치고 `[N agents]` 표기
2. **severity 결정**:
   - Critical = 확실한 버그, 보안, GOAL 위반
   - Suggestion = 개선 가능, 스타일, 설계 제안
   - Info = 관찰, drift 발견
3. **모든 이슈에 file:line 레퍼런스**

### 출력

```
## Review: Phase {N}

### Critical (반드시 수정)
- **{파일}:{줄}** — {문제}. {이유}. {수정 방향}. [{source}]

### Suggestion (개선 제안)
- **{파일}:{줄}** — {제안}. {이유}. [{source}]

### Plan Drift (새 발견 작업)
- {설명} → PLAN.md Phase {M} 추가

### Verdict
REVIEW_CRITICAL: {N}
REVIEW_ITEMS: [critical 목록]
REVIEW_SUGGESTIONS: [suggestion 목록]
DISCOVERED_WORK: [drift 목록]
```

## Phase 4: Drift 반영

DISCOVERED_WORK가 있으면 PLAN.md에 새 phase를 추가한다.
drift 에이전트의 결과를 기반으로 범위, 수용 기준을 포함하여 추가.

## 규칙
- 읽기 전용 — 코드 수정은 fix 에이전트가 담당
- Critical이 있으면 fix → gate부터 다시 (go가 처리)
- Suggestion은 보고만 — 자동 수정 안 함
