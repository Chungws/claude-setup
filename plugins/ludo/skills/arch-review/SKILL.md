---
name: arch-review
description: >
  빌드 완료 후 전체 변경에 대해 아키텍처 리뷰를 실행한다.
  글로벌 /arch-review의 5개 페르소나 에이전트를 활용.
  3+ phase 완료 시 ludo:go에서 자동 호출, 수동으로도 실행 가능.
  "/ludo:arch-review" 요청 시 활성화.
user-invocable: true
argument-hint: "[review-scope]"
---

# Arch Review — Post-Build Architecture Verification

## 원칙
- 빌드 완료 후 전체 변경의 구조적 무결성 검증.
- 글로벌 `/arch-review` 스킬의 5개 페르소나 에이전트를 재사용.
- 컨텍스트 없이 실행 — GOAL.md + PLAN.md + 코드만 읽는다.

## 언제 실행하는가
- **ludo:go 자동**: 3개 이상 phase 완료 후 Stage 4에서
- **수동**: `/ludo:arch-review` 로 언제든

## Input
- $ARGUMENTS: 리뷰 범위. 없으면 이 빌드에서 변경된 영역 전체.

## 절차

1. GOAL.md, PLAN.md 읽기 — 빌드 목표와 아키텍처 결정 파악
2. `git diff main...HEAD --name-only` — 변경 범위 파악
3. 글로벌 `/arch-review` 실행 — 5개 페르소나 병렬:

| # | 페르소나 | 지시 파일 |
|---|----------|----------|
| 1 | Structure | ~/.claude/skills/arch-review/structure.md |
| 2 | Abstraction | ~/.claude/skills/arch-review/abstraction.md |
| 3 | SSOT | ~/.claude/skills/arch-review/ssot.md |
| 4 | Data Flow | ~/.claude/skills/arch-review/data-flow.md |
| 5 | Boundary | ~/.claude/skills/arch-review/boundary.md |

4. 결과 종합 시 **GOAL.md 아키텍처 결정과 대조**:
   - PLAN.md에서 결정한 아키텍처가 실제로 잘 구현됐는가?
   - 빌드 과정에서 아키텍처가 drift하지 않았는가?

## 출력

글로벌 `/arch-review`와 동일한 포맷 + GOAL/PLAN 대조 섹션:

```
# {프로젝트명} 아키텍처 리뷰 (Post-Build)

## GOAL.md 아키텍처 결정 대조
| 결정 | 구현 상태 | 근거 |
|------|----------|------|
| {결정} | OK/DIVERGED | {file:line} |

## 잘 되어있는 점
...

## High — 즉시 수정 필요
...

## Medium — 구조적 개선
...

## Low
...

## 우선순위 제안
...
```

## 규칙
- 읽기 전용 — 코드 수정 안 함
- High 이슈가 있으면 최종 보고에 포함 (ludo:go가 사용자에게 보고)
- 소규모 변경(1-2 phase)에서는 비용 대비 효과 부족 → 스킵 권장
