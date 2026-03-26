---
name: go
description: >
  GOAL.md 또는 issue URL/번호를 읽어 plan → build → gate → review 파이프라인을 완전 자율 실행한다.
  모든 에이전트는 컨텍스트 없이 파일만 읽고 작업. Writer/Reviewer 구조적 분리.
  기존 도구(pr-review-toolkit, simplify, analyze-plan) 통합.
  "/ludo:go", "빌드해줘", "만들어줘" 등의 요청 시 활성화.
user-invocable: true
argument-hint: "[goal-file-path | issue-url | #issue-number]"
---

# Go — Autonomous Build Pipeline

## 원칙

1. **Goal이 진실의 원천** — GOAL.md 또는 issue 내용이 모든 에이전트의 입력
2. **컨텍스트 없이 실행** — 파일만 읽는다. 대화 히스토리 zero.
3. **Writer/Reviewer 분리** — 쓴 에이전트가 검증하지 않는다.
4. **Gate → Review 순서** — clean 코드 위에서만 리뷰.

## Input

$ARGUMENTS는 다음 중 하나:

| 입력 형태 | 예시 | 동작 |
|-----------|------|------|
| Issue URL | `https://github.com/owner/repo/issues/42` | git-platform 스킬로 issue 내용 fetch → goal로 사용 |
| Issue 번호 | `#42`, `42` | 현재 repo의 issue를 fetch → goal로 사용 |
| GOAL.md 경로 | `./GOAL.md`, `docs/GOAL.md` | 해당 파일을 goal로 사용 |
| 없음 | (빈 인자) | 프로젝트 루트의 `GOAL.md` 사용 |

### Input 해석 절차

1. $ARGUMENTS가 URL 패턴(`https://github.com/.../issues/` 또는 `https://gitlab.../issues/`)이면 → **Issue 모드**
2. $ARGUMENTS가 `#숫자` 또는 순수 숫자이면 → **Issue 모드** (현재 repo)
3. 그 외 → **GOAL.md 모드** (기존 동작)

### Issue 모드

1. git-platform 스킬 절차에 따라 플랫폼 판별 (`git remote get-url origin`)
2. issue 내용 fetch:
   ```bash
   # GitHub
   gh issue view {number} --repo {owner}/{repo}
   # GitLab
   glab issue view {number} --repo {owner}/{repo}
   ```
3. fetch한 issue 내용을 goal로 사용 (GOAL.md 파일 생성 불필요)
4. issue 내용이 모호하거나 정보 부족 시:
   ```
   issue 내용이 불충분합니다. issue #{number}에 목표, 요구사항, 제약이 명확하지 않습니다.
   issue를 보강한 후 다시 실행해주세요.
   ```
   → 종료. PR 미생성.
5. `ISSUE_NUMBER`와 `ISSUE_URL`을 파이프라인 전체에서 참조할 수 있도록 기억한다.

### GOAL.md 모드 (기존 동작)

- $ARGUMENTS가 파일 경로면 해당 파일, 없으면 프로젝트 루트의 `GOAL.md`.
- GOAL.md 없으면 → "GOAL.md가 없습니다. 목표 문서를 먼저 작성해주세요." → 종료.

### GOAL.md 형식

```markdown
# Goal: {제목}

## 목표
{무엇을 달성해야 하는지}

## 요구사항
- {구체적 동작 1}
- {구체적 동작 2}

## 제약
- {기존 코드 호환, 성능, 설정 가능 여부 등}

## 경계 조건
- {에러 시 동작, 엣지 케이스}
```

---

## Pipeline

```
Input (GOAL.md 또는 Issue)
  → Plan → Plan Gate (analyze-plan + 정합성)
  → Phase Loop:
      Build → Gate (기계적) → Review (멀티에이전트) → Fix
  → 최종 검증 (arch-review, 3+ phase일 때)
  → 완료: PR/MR 생성 (issue 모드) 또는 보고 (GOAL.md 모드)
```

**완전 자율. 사용자 개입 zero.** 재시도 한도 초과 시만 보고.

---

## Stage 1: Plan

```
Agent(prompt: "goal을 읽고 빌드 계획을 수립하라.

입력: {goal_source}, CLAUDE.md, 프로젝트 코드 구조, ~/dapi-ssot/research/ (관련 인사이트)

{goal_source}는 다음 중 하나:
- Issue 모드: fetch한 issue 내용 (issue #{number})
- GOAL.md 모드: GOAL.md 파일

PLAN.md를 프로젝트 루트에 생성:
- 각 phase: 범위, 변경 파일, 수용 기준(체크박스), 예상 LOC, 상태(pending)
- phase당 max 300줄, 3-4 커밋
- 각 phase 독립적으로 green
- 아키텍처 결정과 이유 명시
- goal 매핑 테이블 포함 (요구사항 → phase)

Issue 모드이고 ISSUE_NUMBER가 있으면:
- git-platform 스킬로 issue에 PLAN.md 내용을 댓글로 게시
- 댓글 앞에 '## Build Plan' 헤더 추가

대화 히스토리 참조 금지.")
```

**Plan 에이전트 반환 후 바로 Stage 2.**

## Stage 2: Plan Gate

Plan 에이전트와 **다른 에이전트**가 검증. 2개를 병렬 스폰:

### 2a. analyze-plan (기존 스킬)
PLAN.md를 understanding 라이브러리로 객관적 품질 측정:
```
Agent(prompt: "/analyze-plan 실행하라. PLAN.md 내용을 /tmp/plan_to_analyze.md에 저장하고
uvx --from 'git+https://github.com/Testimonial/understanding' understanding /tmp/plan_to_analyze.md --json
결과를 반환하라.")
```

### 2b. 정합성 검증
```
Agent(prompt: "goal과 PLAN.md의 정합성을 검증하라.

goal 소스: {goal_source} (Issue 모드면 issue 내용, GOAL.md 모드면 GOAL.md 파일)

- goal의 모든 요구사항이 PLAN.md에 매핑되는가?
- 제약이 아키텍처 결정에 반영됐는가?
- 경계 조건이 수용 기준에 포함됐는가?
- phase 분할이 합리적인가?

PLAN_GATE: PASS/FAIL, MISSING: [누락], SUGGESTIONS: [제안]")
```

**FAIL:** fix 에이전트가 PLAN.md 수정 → re-gate. 최대 3회.

## Stage 3: Phase Loop

PLAN.md에서 pending phase를 순서대로:

### 3a. Build

```
Agent(prompt: "PLAN.md의 Phase {N}을 TDD로 구현하라.

입력: PLAN.md Phase {N}, CLAUDE.md

1. 수용 기준마다 실패하는 테스트 → 모두 RED
2. 테스트를 하나씩 green → green마다 커밋
3. 리팩토링 → 별도 커밋
4. ruff check --fix && ruff format && mypy . && pytest
5. PLAN.md 상태: pending → complete, 체크박스 [x]

대화 히스토리 참조 금지.")
```

### 3b. Gate (기계적, blocking)

Build와 **다른 에이전트**. review 전 필수 통과:

```
Agent(prompt: "Phase {N} 품질 게이트를 실행하라.

전체 코드베이스 대상:
1. ruff check . → PASS/FAIL
2. ruff format --check . → PASS/FAIL
3. mypy . → PASS/FAIL
4. pytest --tb=short --cov --cov-fail-under=100 → PASS/FAIL
5. 새 # noqa / # type: ignore 감사 → 이유 + 합리성 판단
6. PLAN.md 수용 기준 체크박스 [x] 확인

GATE_RESULT: PASS/FAIL, FAIL_ITEMS: [목록]")
```

**FAIL:** fix 에이전트 → re-gate. 최대 3회.

### 3c. Review (멀티에이전트, gate PASS 후)

**한 메시지에서 5개를 동시에 스폰:**

#### Group A: 코드 품질 (기존 도구)

```
Agent(subagent_type: "pr-review-toolkit:review-pr",
  prompt: "Phase {N} 변경사항을 리뷰하라. 범위: {range}")
```

```
Agent(subagent_type: "feature-dev:code-reviewer",
  prompt: "Phase {N} 변경사항의 버그, 보안, 코드 품질을 리뷰하라. 범위: {range}")
```

#### Group B: 정합성 (커스텀, worktree 격리)

3개 서브에이전트를 각각 `isolation: worktree`로 스폰.
각 에이전트에게 `~/.claude/skills/ludo/review/{agent-file}.md` 지시 파일과 컨텍스트 전달:

| # | 파일 | 역할 |
|---|------|------|
| 1 | goal-align.md | GOAL.md 요구사항/제약 정합성 |
| 2 | plan-align.md | PLAN.md 범위/수용기준/아키텍처 결정 |
| 3 | drift.md | 새 작업 발견 → PLAN.md 추가 제안 |

### 3d. Review 결과 처리

5개 에이전트 결과를 종합:
- 중복 제거, severity 결정 (Critical/Suggestion/Info)
- **Critical > 0:** fix 에이전트 → **Stage 3b gate부터 다시**. 최대 2회.
- **DISCOVERED_WORK:** drift 에이전트 결과를 PLAN.md에 새 phase로 추가.
- **Suggestion:** 보고만, 자동 수정 안 함.

### 3e. Simplify (기존 스킬)

review 통과 후, 코드 단순화 에이전트 실행:
```
Agent(prompt: "이 phase에서 변경된 코드를 리뷰하고,
재사용성, 품질, 효율성 관점에서 단순화할 수 있는 부분을 찾아 수정하라.
수정 후 테스트가 여전히 green인지 확인하라.")
```

simplify가 코드를 수정하면 → gate 한 번 더 돌린다.

### Phase 전환

Phase {N} 사이클 완료 후:
1. **PLAN.md를 다시 읽는다** — drift로 새 phase가 추가됐을 수 있음
2. 다음 pending phase로 진행
3. 모든 phase가 complete가 될 때까지 반복

## Stage 4: 최종 검증 (선택적)

**3개 이상 phase를 완료한 경우**, 전체 변경에 대해 아키텍처 리뷰:

```
Agent(prompt: "/arch-review 실행하라. 이 빌드에서 변경된 영역을 대상으로 구조적 무결성을 검증하라.")
```

1-2 phase 소규모 변경에는 스킵 (비용 대비 효과 부족).

## Stage 5: 완료 처리

### 5a. PR/MR 생성 (Issue 모드일 때)

모든 phase가 complete이고 ISSUE_NUMBER가 있으면:

1. 작업 브랜치를 push:
   ```bash
   git push -u origin $(git branch --show-current)
   ```
2. git-platform 스킬로 PR/MR 생성:
   ```bash
   # GitHub
   gh pr create \
     --title "{적절한 제목}" \
     --body "## Summary
   {변경 요약}

   ## Issue
   closes #{ISSUE_NUMBER}

   ## Changes
   {phase별 주요 변경 목록}" \
     --head $(git branch --show-current)

   # GitLab
   glab mr create \
     --title "{적절한 제목}" \
     --description "## Summary
   {변경 요약}

   closes #{ISSUE_NUMBER}" \
     --source-branch $(git branch --show-current)
   ```

**실패 시** (gate 3회 실패 등 파이프라인 중단): PR/MR을 생성하지 않는다. 실패 보고만 한다.

### 5b. 완료 보고

```
## Build Complete: {goal 제목}

### Phase 결과
| # | Phase | 커밋 | LOC | Gate | Review | Simplify |
|---|-------|------|-----|------|--------|----------|
| 1 | {명}  | {N}  | {N} | PASS | {N}c/{N}s | {변경 여부} |

### Goal 요구사항 충족
- [x] {요구사항 1}
- [x] {요구사항 2}

### PR/MR (issue 모드일 때)
- {PR/MR URL} — closes #{ISSUE_NUMBER}

### Review Suggestions (미반영)
- {suggestion 목록}

### Arch Review (3+ phase일 때)
- {High/Medium 이슈 요약}

### 사용 가이드

goal의 요구사항, 제약, 경계 조건에서 자동 도출한다.

#### 기본 사용
{goal 요구사항 기반 — 이 기능을 실제로 쓰는 방법}
- {명령어, API 호출, 설정 변경 등 구체적 사용 예시}
- {주요 유스케이스별 실행 방법}

#### 설정
{goal 제약에서 도출 — 설정이 필요한 경우}
- {설정 파일 경로, 환경변수, config 값}
- {기본값과 커스터마이즈 방법}

#### 주의사항
{goal 경계 조건에서 도출}
- {에러 시 어떻게 되는지}
- {엣지 케이스와 대처 방법}

### 다음
- `/ship` — MR 생성 (GOAL.md 모드일 때)
- `/ludo:review` — 수동 추가 리뷰
```

## 제약

- **사용자 개입 zero** — goal 작성(GOAL.md 또는 issue)만 사람. 나머지 완전 자율.
- 재시도 한도: plan-gate 3회, gate 3회, review-fix 2회.
- 중단 후 `/ludo:go` 재실행하면 PLAN.md pending phase부터 이어감.
- 모든 에이전트 입력: 파일뿐. 대화 히스토리 참조 금지.
- Issue 모드에서 파이프라인 실패 시 PR/MR을 생성하지 않고 실패 내용만 보고한다.
- Issue URL이 아닌 기존 입력(GOAL.md 경로, 자연어)은 기존 동작 그대로 유지.
