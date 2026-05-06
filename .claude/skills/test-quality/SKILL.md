---
name: test-quality
description: >
  mutation testing + CRAP score로 테스트 품질을 심층 분석한다.
  survived mutant와 CRAP 위반 함수를 우선순위별로 정리하고, Claude가 테스트 추가/리팩토링으로 수정한다.
  MR/PR 직전 advisory 게이트. "/test-quality", "뮤테이션 테스트", "테스트 품질 확인" 등의 요청 시 활성화.
user-invocable: true
argument-hint: "[--src SRC] [--changed-only] [--base-branch BRANCH] [--fix]"
---

# Test Quality

mutation testing(mutmut) + CRAP score(radon + coverage)로 테스트가 실제로 의미 있는지 검증한다.

Uncle Bob의 전략: "AI가 mutation tester를 돌리고, CRAP을 5 이하로 낮춰라."

## 전제 조건

- `quality-setup`이 완료된 프로젝트 (mutmut, radon이 dev dependency에 있어야 함)
- pytest + coverage 설정이 완료되어 있어야 함
- 테스트가 모두 green인 상태에서 실행 (red 상태에서는 의미 없음)

## Input

`$ARGUMENTS`:
- 없음: `src/` 전체를 대상으로 실행
- `--src <path>`: 분석 대상 소스 디렉토리 지정
- `--changed-only`: git diff 기반으로 변경된 파일만 대상 (빠름, PR 워크플로우 권장)
- `--base-branch <branch>`: `--changed-only` 기준 브랜치 (기본: main)
- `--fix`: 리포트 생성 후 자동 수정 루프 실행 (기본: advisory만)

## Step 1: 전제 조건 확인

```bash
uv run pytest -q --tb=no 2>&1 | tail -3
```

테스트가 failing 상태면 멈추고 사용자에게 알린다:
```
테스트가 failing 상태입니다. test-quality은 green 상태에서만 실행하세요.
먼저 실패 테스트를 수정한 뒤 다시 실행해주세요.
```

## Step 2: 리포트 생성

```bash
uv run ~/.claude/skills/test-quality/report.py $ARGUMENTS
```

`quality-report.md`가 생성된다.

## Step 3: 리포트 요약 출력

```
## Test Quality 결과

| 항목 | 값 |
|------|----|
| Mutation Score | {N}% |
| Survived Mutants | {N}개 |
| CRAP 위반 함수 | {N}개 |

{CRAP 위반 + survived mutant 있는 함수 목록}
```

`--fix` 없이 실행했으면 여기서 종료. 리포트만 보여준다.

## Step 4: 수정 루프 (`--fix` 모드)

`--fix`가 지정된 경우에만 실행.

### 우선순위 선택

CRAP이 높고 survived mutant가 많은 함수부터 처리.
한 번에 한 함수씩.

### 수정 전략

**survived mutant가 있는 경우:**

mutant diff를 읽고 어떤 경계값/조건이 테스트되지 않았는지 파악한다.

예시:
```diff
-    if score >= 90:
+    if score > 90:
```
→ `score=90`이 경계값인데 테스트가 없음

어느 레이어에 추가할지 판단:
- **Layer 2** (기본): 구체적 예시 → `assert classify_score(90) == "A"`
- **Layer 1**: 불변 조건이라면 property test → `score >= 90`이면 항상 `"A"`여야 한다

**CRAP > 5인 경우:**

함수를 더 작은 단위로 분리하거나, 커버되지 않는 분기에 테스트를 추가한다.
CRAP = CC² × (1 - cov)³ + CC 이므로 커버리지를 올리거나 CC를 낮춰야 한다.

### 수정 후 검증

```bash
uv run pytest -q && uv run ~/.claude/skills/test-quality/report.py $ARGUMENTS
```

새 리포트와 이전 리포트를 비교하여 개선됐는지 확인.
개선이 없으면 다른 접근법 시도.

### 종료 조건

다음 중 하나:
- 모든 함수 CRAP ≤ 5, survived mutant 0개
- 사용자가 "충분하다"고 판단
- 3회 시도 후에도 개선 없는 함수는 스킵하고 리포트에 기록

## Step 5: 최종 요약

```
## Test Quality 완료

### 변경 전 → 후
| 항목 | 전 | 후 |
|------|----|----|
| Mutation Score | {N}% | {N}% |
| Survived | {N}개 | {N}개 |
| CRAP 위반 | {N}개 | {N}개 |

### 수정한 함수
- `{함수명}`: {무엇을 고쳤는지}

### 잔여 이슈 (해결 불가/스킵)
- `{함수명}`: {이유}
```

## 주의사항

- **advisory 모드 (기본)**: 리포트만 생성, 코드 수정 안 함
- **fix 모드**: 수정 전 사용자에게 각 함수 수정 계획을 보여주고 확인받는다
- mutmut은 느림. 전체 프로젝트 대상이면 수 분 소요될 수 있음
- CRAP 기준(5)은 `--crap-threshold` 옵션으로 조정 가능
