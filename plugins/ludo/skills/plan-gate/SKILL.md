---
name: plan-gate
description: >
  PLAN.md의 품질과 GOAL.md 정합성을 검증한다.
  analyze-plan(understanding 라이브러리) + 정합성 검증을 병렬 실행.
  "/ludo:plan-gate" 또는 ludo:go에서 자동 호출.
user-invocable: true
---

# Plan Gate — Plan Quality + Goal Alignment

## 원칙
- Plan 에이전트와 **다른 에이전트**가 실행 (writer/reviewer 분리).
- 2가지를 병렬 검증: 객관적 품질 측정 + GOAL 정합성.

## Input
- PLAN.md, GOAL.md (프로젝트 루트)

---

## 검증 1: Plan 품질 (analyze-plan)

PLAN.md를 understanding 라이브러리(IEEE 830, ISO 29148 기반 31개 메트릭)로 객관 측정:

```bash
# PLAN.md 내용을 임시 파일에 영어로 변환 후 저장
uvx --from "git+https://github.com/Testimonial/understanding" understanding /tmp/plan_to_analyze.md --json
```

카테고리별 점수:
- structure (30%) — 원자성, 완전성, 모호성
- testability (20%) — 정량적 제약, 경계값
- readability (15%) — 가독성
- cognitive (15%) — 복잡도
- semantic (10%) — Actor/Action/Object
- behavioral (10%) — 시나리오 분해

**Overall 70% 미만이면 WARNING** (FAIL은 아님 — 참고 지표).

## 검증 2: GOAL 정합성

| # | 항목 | 판정 |
|---|------|------|
| 1 | GOAL.md 모든 요구사항이 PLAN.md에 매핑되는가? | PASS/FAIL |
| 2 | 제약이 아키텍처 결정에 반영됐는가? | PASS/FAIL |
| 3 | 경계 조건이 수용 기준에 포함됐는가? | PASS/FAIL |
| 4 | phase 분할이 합리적인가? (독립 green, ~300줄) | PASS/FAIL |
| 5 | GOAL.md 매핑 테이블이 완전한가? | PASS/FAIL |

## 출력

```
## Plan Gate

### 품질 점수 (analyze-plan)
Overall: {N}% {바 차트}
{카테고리별 점수}

### GOAL 정합성
| 항목 | 결과 |
|------|------|
| 요구사항 매핑 | PASS/FAIL: {누락} |
| 제약 반영 | PASS/FAIL |
| 경계 조건 | PASS/FAIL: {누락} |
| phase 분할 | PASS/FAIL |
| 매핑 테이블 | PASS/FAIL |

### Verdict: PASS / FAIL
PLAN_GATE: PASS/FAIL
MISSING: [누락 항목]
QUALITY_SCORE: {N}%
```
