---
name: experiment
description: >
  리서치 인사이트를 기반으로 실험을 설계하고, autoresearch 스타일의 자율 루프
  (가설 → 코드 수정 → 실행 → 측정 → 판정)를 반복하여 최적 결과를 도출한다.
  "/experiment", "실험해줘", "실험 돌려줘" 등의 요청 시 활성화.
user-invocable: true
---

# Experiment Orchestrator

## Preamble (먼저 실행)

```bash
EXP_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]/ /g' | tr -s ' ' '\n' | grep -vxE 'for|the|a|an|of|in|on|with|and|or|to|is|are|by|at' | head -4 | tr '\n' '-' | sed 's/-$//')
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H:%M)
NOTE_DIR=~/dapi-ssot/projects/${EXP_SLUG}
CODE_DIR=~/experiments/${EXP_SLUG}
LOG_FILE=~/dapi-ssot/SOT/session-logs/${SESSION_DATE}-experiment-${EXP_SLUG}.md

mkdir -p "$NOTE_DIR/runs"
mkdir -p "$CODE_DIR"

cat > "$LOG_FILE" << LOGEOF
---
created: ${SESSION_DATE}
skill: experiment
topic: ${ARGUMENTS}
status: in-progress
---

# Experiment: ${ARGUMENTS}

## 메타
- 시작: ${SESSION_DATE} ${SESSION_TIME}
- 종료: (완료 시 채울 것)

## 실험 결과
- 총 실행 횟수: 0
- 최고 메트릭: (측정 후 채울 것)
- 최종 판정: (완료 시 채울 것)

## 생성된 파일
(목록)

## 오류/메모
(있으면 기록)
LOGEOF

echo "SESSION_LOG=$LOG_FILE"
echo "EXP_SLUG=$EXP_SLUG"
echo "NOTE_DIR=$NOTE_DIR"
echo "CODE_DIR=$CODE_DIR"
```

위 bash 출력의 경로들을 기억하고 이후 Phase에서 사용한다.

## Trigger
사용자가 `/experiment {주제/가설}` 또는 자연어로 실험을 요청할 때 활성화.

## Input
- $ARGUMENTS: 실험 주제, 가설, 또는 검증하고 싶은 아이디어 (필수)

## 경로
- 노트 (vault): `~/dapi-ssot/projects/{exp-slug}/` — 설계서, 결과, run 기록
- 코드: `~/experiments/{exp-slug}/` — 실험 코드, 실행 산출물
- 세션 로그: `~/dapi-ssot/SOT/session-logs/`

## Vault 규칙
- 한국어로 작성
- `[[위키링크]]`로 관련 리서치 노트 연결
- 프론트매터에 tags, related, status 필수

---

## Phase 1: Scoping — 리서치 인사이트 수집

1. `~/dapi-ssot/research/` 에서 관련 인사이트, 허브 노트, 논문/레포/아티클을 Grep으로 검색
2. 관련 자료가 있으면 읽고 핵심 내용 파악
3. 관련 자료가 부족하면 사용자에게 알림: "관련 리서치가 없습니다. 먼저 `/research {토픽}`을 실행하시겠습니까?"
4. 실험 가능성 판단 — 이 아이디어를 코드로 검증할 수 있는가?

## Phase 2: Experiment Design — program.md 생성

리서치 인사이트를 바탕으로 실험 설계서를 작성한다.
이 파일은 autoresearch의 `program.md`에 해당하며, 실험 루프의 방향을 결정한다.

`{NOTE_DIR}/program.md` 생성:

```
---
created: {date}
tags: [experiment, {topic-tags}]
related: [[topics/{관련-허브}]], [[{관련-인사이트}]]
status: in-progress
---

# {실험 제목}

## 연구 질문
{이 실험이 답하려는 질문 — 1문장}

## 가설
{예상하는 결과 — 검증 가능한 형태로}

## 메트릭
- **주 메트릭**: {자동 측정 가능한 단일 숫자} (높을수록/낮을수록 좋음)
- **보조 메트릭** (optional): {추가 관찰 지표}

## 성공 기준
{주 메트릭이 어떤 값이면 성공으로 판단하는가}

## 고정 예산
- 실행당 시간: {N분} 또는 {조건}
- 최대 반복 횟수: {N회}

## 실험 전략
{어떤 방향으로 변형을 시도할 것인가 — 탐색 범위 정의}

## 참고 자료
- [[{리서치 인사이트}]] — 핵심 아이디어
- [[{논문/레포}]] — 구현 참고
```

**사용자에게 program.md 내용을 보여주고 확인을 받는다.**
사용자가 수정을 원하면 반영 후 다시 확인.

## Phase 3: Environment Setup — 초기 코드 생성

사용자 확인 후 실험 환경을 구성한다.

### 3-1. 실험 코드 생성
`{CODE_DIR}/` 에 실험에 필요한 코드를 작성한다.
- 이 코드가 autoresearch의 `train.py`에 해당 — 루프에서 AI가 수정하는 대상
- 실행 가능해야 한다 (syntax error 없이 첫 실행이 통과)
- 필요한 의존성이 있으면 `requirements.txt` 또는 설치 명령 포함

### 3-2. 평가 코드 생성
메트릭을 자동 측정하는 코드를 작성한다.
- 실험 코드 실행 후 메트릭을 stdout으로 출력하는 형태
- 이 코드는 루프 중 수정하지 않는다 (autoresearch의 `prepare.py`에 해당)

### 3-3. Best 파일 초기화
실험 코드의 초기 버전을 best로 복사해둔다:
```bash
cp {CODE_DIR}/search.py {CODE_DIR}/search.py.best  # 파일명은 실험마다 다름
```
이후 루프에서 개선 시 best를 갱신하고, 퇴보 시 best에서 복원한다.

### 3-4. 첫 실행 테스트
1. 실험 코드를 실행하여 에러 없이 돌아가는지 확인
2. 평가 코드로 메트릭을 측정하여 **베이스라인** 기록
3. `{NOTE_DIR}/runs/run-000-baseline.md` 에 기록:

```
---
run: 0
type: baseline
metric: {측정값}
created: {date}
---

# Run 000: Baseline

## 변경 사항
초기 버전 (변경 없음)

## 결과
- 주 메트릭: {값}

## 메모
{첫 실행 관찰}
```

## Phase 4: Experiment Loop — 자율 반복

program.md의 고정 예산 내에서 아래 루프를 반복한다.
**매 반복은 하나의 가설 — 하나의 수정 — 하나의 측정이다.**

### 루프 1회 (Run N):

1. **분석**: 이전 run들의 결과를 읽고, program.md의 전략을 참고하여 다음 가설 수립
2. **수정**: `{CODE_DIR}/`의 실험 코드를 수정 (한 번에 하나의 변경만)
3. **실행**: 코드 실행 (고정 예산 내)
4. **측정**: 평가 코드로 메트릭 측정
5. **판정 + 롤백**:
   - **개선** → `cp 실험코드 실험코드.best` (best 갱신)
   - **퇴보** → `cp 실험코드.best 실험코드` (best로 복원)
   - **동등** → best 유지, 다른 방향 시도
6. **기록**: `{NOTE_DIR}/runs/run-{NNN}.md` 생성:

```
---
run: {N}
hypothesis: "{가설 한줄}"
change: "{변경 한줄}"
metric: {측정값}
best_metric: {최고값}
verdict: improved | regressed | neutral
created: {date}
---

# Run {NNN}: {가설 한줄}

- **변경**: {뭘 바꿨는가}
- **결과**: {메트릭값} (이전: {이전}, 최고: {최고}) → {verdict}
- **교훈**: {다음 가설에 참고할 것}
```

run 기록은 간결하게. 상세 분석은 results.md에서 종합한다.

### 종료 조건 (하나라도 충족 시 루프 종료):
- 최대 반복 횟수 도달
- 성공 기준 달성
- 연속 3회 이상 개선 없음 (수렴)
- 사용자가 중단 요청

## Phase 5: Results — 결과 정리

### 5-1. 결과 보고서 생성
`{NOTE_DIR}/results.md` 작성:

```
---
created: {date}
tags: [experiment, {topic-tags}]
related: [[topics/{관련-허브}]]
status: done
total_runs: {N}
best_metric: {값}
baseline_metric: {값}
improvement: {%}
---

# {실험 제목} — 결과

## 요약
{실험 목적, 핵심 결과 — 3문장 이내}

## 메트릭 추이
| Run | 가설 | 메트릭 | 판정 |
|-----|------|--------|------|
| 000 | baseline | {값} | - |
| 001 | {가설} | {값} | improved |
| ... | ... | ... | ... |

## 핵심 발견
1. {가장 큰 개선을 가져온 변경}
2. {예상과 다른 결과}
3. {향후 시도할 방향}

## 최종 코드
`{CODE_DIR}/` 의 현재 상태가 최적 버전

## 연결
- [[topics/{허브}]] — 관련 리서치
- [[{인사이트}]] — 실험 근거
```

### 5-2. 인사이트 생성
실험에서 새로운 발견이 있으면 `~/dapi-ssot/research/insights/`에 atomic note 작성.
기존 insight 규칙과 동일한 포맷.

### 5-3. 세션 로그 마감
SESSION_LOG의 status를 `done`으로 변경, 종료 시간/실행 횟수/최고 메트릭/파일 목록 업데이트.

## Phase 6: 사용자 출력

**모든 파일 작업이 끝난 후 가장 마지막에** 대화에 직접 출력:

```
## 실험 완료: {제목}

### 결과
- 베이스라인: {값} → 최종: {값} ({개선%})
- 총 {N}회 반복, {M}회 개선

### 핵심 발견
1. {발견 1}
2. {발견 2}
3. {발견 3}

### 파일
- 노트: {NOTE_DIR}/
- 결과 보고서: {NOTE_DIR}/results.md
- 실험 코드: {CODE_DIR}/

### 다음 단계
- "{후속 실험 제안}" → `/experiment {주제}`
- "{관련 리서치}" → `/research {토픽}`
```

## 실패 처리
- 코드 실행 에러 → 에러 수정 후 재실행 (수정 횟수가 3회 초과 시 롤백하고 다른 가설 시도)
- 메트릭 측정 불가 → 평가 코드 점검, 불가능하면 해당 run 스킵
- 관련 리서치 없음 → Phase 1에서 사용자에게 `/research` 먼저 권장
- 환경 문제 (패키지 미설치 등) → 자동 설치 시도, 실패 시 사용자에게 안내
