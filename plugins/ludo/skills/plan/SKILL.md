---
name: plan
description: >
  GOAL.md 또는 issue 내용을 읽어 phase별 빌드 계획(PLAN.md)을 생성한다.
  issue 모드일 때 plan을 issue 댓글로도 게시한다.
  컨텍스트 없이 파일만 읽고 작업.
  "/ludo:plan" 또는 ludo:go에서 자동 호출.
user-invocable: true
argument-hint: "[goal-file-path | issue-url | #issue-number]"
---

# Plan -- Goal → PLAN.md

## 원칙
대화 히스토리 참조 금지. goal 소스(GOAL.md 또는 issue 내용)와 코드베이스만 읽는다.

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
3. fetch한 issue 내용을 goal로 사용 (GOAL.md 파일 불필요)
4. issue 내용이 모호하거나 정보 부족 시:
   ```
   issue 내용이 불충분합니다. issue #{number}에 목표, 요구사항, 제약이 명확하지 않습니다.
   issue를 보강한 후 다시 실행해주세요.
   ```
   → 종료. PLAN.md 미생성.
5. `ISSUE_NUMBER`를 기억한다 (댓글 게시에 사용)

### GOAL.md 모드 (기존 동작)

- $ARGUMENTS가 파일 경로면 해당 파일, 없으면 프로젝트 루트의 `GOAL.md`.
- GOAL.md 없으면 → "GOAL.md를 먼저 작성해주세요." 종료.

## 절차

1. **Goal 소스** 읽기 — 목표, 요구사항, 제약, 경계 조건
2. **CLAUDE.md** 읽기 — 프로젝트 규칙
3. 프로젝트 코드 구조 파악
4. `~/dapi-ssot/research/` 관련 인사이트 검색 (없으면 "SSOT 참고 없음")
5. PLAN.md 생성:

```markdown
# Plan: {goal 제목}

> 생성: {date} | 상태: in-progress | 목표: {GOAL.md 또는 issue #{number}}

## 배경
{goal의 목표 요약}

## Phase 1: {이름}
- **범위**: {scope}
- **파일**: {변경할 파일}
- **수용 기준**:
  - [ ] {goal 요구사항에서 도출}
  - [ ] {경계 조건에서 도출}
- **예상 LOC**: ~{N}
- **상태**: pending

## 아키텍처 결정
- {결정}: {선택} — {goal 제약과의 연관}

## Goal 매핑
| 요구사항 | Phase |
|----------|-------|
| {요구사항 1} | Phase {N} |
| {제약 1} | 아키텍처 결정 |
```

6. **Issue 모드일 때**: PLAN.md 생성 후 git-platform 스킬로 issue에 댓글 게시
   ```bash
   # GitHub
   gh issue comment {ISSUE_NUMBER} --body "## Build Plan

   {PLAN.md 내용}"

   # GitLab
   glab issue note {ISSUE_NUMBER} --message "## Build Plan

   {PLAN.md 내용}"
   ```

## 규칙
- phase당 max 300줄, 3-4 커밋
- 각 phase 독립적으로 green
- goal의 모든 요구사항이 최소 하나의 phase에 매핑되어야 한다
- 매핑 테이블로 추적 가능성 보장
- Issue 모드에서 댓글 게시 실패 시 경고만 출력하고 계속 진행 (PLAN.md는 이미 로컬에 생성됨)
