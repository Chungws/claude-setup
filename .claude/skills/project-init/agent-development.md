# Agent Development Setup Guide

AI Agent를 개발할 때 어떤 환경을 셋팅해야 하고, 어떤 것을 명심하면서 개발해야 하는지를 정리한 문서.

**핵심 원칙: 가설 → 실험 → 평가 → 채택/폐기 루프를 최대한 빠르게 돌린다.**
이 피드백 루프의 속도가 곧 에이전트 프로젝트의 성패를 결정한다.

---

## 1. 프로젝트 구조

```
my-agent/
├── CLAUDE.md                  # 에이전트별 Claude 지침 (아래 템플릿 참고)
├── pyproject.toml
├── src/
│   └── my_agent/
│       ├── types.py           # ★ 데이터 타입/스키마 (의존 없음, 최하위 레이어)
│       ├── config.py          # ★ 설정 중앙 관리 (types만 의존)
│       ├── core/              # 코어 — 인터페이스 의존 없음
│       │   ├── loop.py        # 에이전트 루프 (순수 로직)
│       │   ├── events.py      # 이벤트 타입 정의
│       │   └── event_log.py   # 이벤트 기록
│       ├── prompts/           # 프롬프트 템플릿 (버전 관리)
│       │   └── v1.txt
│       ├── tools/             # 에이전트가 사용하는 도구
│       ├── guardrails/        # 안전장치 (입력 검증, 출력 검증, 위험도 게이트)
│       ├── cli.py             # CLI 인터페이스 (core 호출)
│       └── api.py             # Web API 인터페이스 (core 호출)
├── dashboard/                 # 프론트엔드 (api.py 소비)
├── bench/
│   ├── tasks/                 # 벤치마크 태스크 정의
│   │   ├── canary-easy/
│   │   │   ├── instruction.md
│   │   │   └── test.sh        # 자동 채점
│   │   └── canary-hard/
│   ├── variants/              # ablation variant configs
│   │   ├── baseline.json
│   │   └── with-notepad.json
│   ├── results/               # git hash별 결과 캐시
│   │   └── {git_hash}/
│   │       └── {variant}/{task}/run-{n}.json
│   ├── run.py                 # variant × task × N회 실행
│   ├── compare.py             # baseline vs variant 비교 리포트
│   └── analyze.py             # AI 인과 분석 (diff + results → why)
├── docs/                      # 에이전트가 탐색할 수 있는 심층 문서
│   ├── architecture.md
│   └── domain-context.md
└── tests/                     # 일반 단위 테스트
```

### 의존성 방향

**초기부터 강제 (절대 규칙):**
```
types.py   ← 모든 모듈이 의존. types는 아무것도 import하지 않음.
config.py  ← types만 의존. 환경변수, 모델 설정, 실행 파라미터를 여기서만 로딩.

        types, config (기반 레이어)
              ↑
      ┌───────┼───────┐
   tools/  guardrails/  events    ← 서로 독립. types/config만 의존.
      └───────┼───────┘
              ↓
           loop.py                ← 위 모듈들을 조합하는 오케스트레이터

cli.py ──→ core/    ← bench/run.py도 여기를 직접 호출
api.py ──→ core/
dashboard → api.py
```

types와 config를 초기부터 분리하지 않으면 나중에 모든 모듈이 서로를 import하는 괴물이 된다. rloop에서 38개 파일이 flat하게 놓이면서 subprocess 관리 + CPU 할당 + 설정 로딩이 뒤섞인 것이 교훈.

- **types.py**: dataclass/TypedDict로 공유 데이터 구조 정의. 여기에 로직 넣지 마라. 타입명은 의미론적으로 — `str` 대신 `TaskId`, `PromptHash`, `RunId`. 에이전트(사람이든 AI든)가 데이터 흐름을 이름만 보고 추적할 수 있어야 한다.
- **config.py**: 환경변수, 모델 설정, variant 파라미터. 흩어지면 "이 값 어디서 오는 거지?" 지옥.
- **tools/, guardrails/, events**: 서로 모른다. 각자 types/config만 의존. tools가 guardrails를 import하거나 그 반대도 금지.
- **loop.py**: 유일한 오케스트레이터. tools, guardrails, events를 조합하는 유일한 장소.
- **core/**: 인터페이스(cli, api, dashboard) 의존 금지. bench/에서 직접 import할 수 있어야 함.
- **파일은 작게, 경로는 의미있게**: `utils/helpers.py` 대신 `tools/search_code.py`. 파일 경로 자체가 문서 역할을 한다. 작은 파일이 에이전트의 컨텍스트 관리 효율을 높인다.

### 개발 환경 속도

피드백 루프 속도는 개발 환경 속도에 직결된다.
- **테스트 1분 이내**: 느린 테스트는 실험 횟수를 줄인다
- **새 환경 즉시 구성**: `make new-env NAME=experiment-x` 한 줄로 격리된 환경이 떠야 함
- **동시 실행 충돌 없이**: 포트, DB, 캐시가 환경별로 격리되어 여러 variant를 동시에 돌릴 수 있어야 함

---

## 2. 에이전트 코어 설계

에이전트 = **Model + Tools + Instructions**. 이 세 가지를 분리하여 독립적으로 교체/실험 가능하게.

### core/loop.py — 에이전트 루프
```python
# 핵심 구조 (의사 코드)
def run(config: AgentConfig, task: Task) -> RunResult:
    state = initial_state(task)

    while not exit_condition(state):
        # 1. LLM 호출
        response = call_model(config.model, config.prompt, state)

        # 2. Tool 실행
        if response.has_tool_calls:
            results = execute_tools(response.tool_calls, config.tools)

        # 3. Self-verify (선택적이지만 권장)
        if config.enable_self_verify and state.is_near_completion:
            verify_result = call_model(config.model, VERIFY_PROMPT, state)
            if verify_result.found_issues:
                state.reopen()
                continue

        state.update(response, results)

    return state.to_result()
```

### Exit conditions (루프 종료 조건)
명시적으로 정의해야 함. 안 하면 에이전트가 무한 루프를 돈다.
- 태스크 완료 선언 (agent가 "done" 출력)
- 최대 턴 수 도달
- 에러 임계값 초과
- 토큰/비용 한도 초과
- 타임아웃

### prompts/ — 프롬프트 템플릿
프롬프트 변경이 곧 에이전트 변경이다. 반드시 버전 관리.

```
prompts/
├── v1.txt                     # baseline
├── v1-notepad.txt             # NOTEPAD 추가
└── v1-self-critique.txt       # SELF-CRITIQUE 추가
```

프롬프트 작성 시간이 개발 시간의 대부분을 차지한다. 팁:
- 정보를 과적하지 마라 — 맵을 주고, 필요시 탐색하게
- 변수화된 템플릿 사용 (`{{task_description}}`, `{{available_tools}}`)
- "더 열심히 하라"는 효과 없음 → 도구/환경 개선으로 해결

### tools/ — 도구 설계

```python
# 각 도구는 명확한 목적 + 읽기/쓰기 구분
tools/
├── read_file.py       # read-only — 위험도 낮음
├── search_code.py     # read-only — 위험도 낮음
├── run_command.py     # write — 위험도 중간
├── deploy.py          # write, 비가역 — 위험도 높음
└── registry.py        # 도구 등록 + 메타데이터
```

도구 설계 원칙:
- 하나의 도구 = 하나의 명확한 목적
- read/write 분리, 각 도구에 위험도(low/mid/high) 태깅
- 도구 설명(description)이 에이전트 성능에 직결 — 이름, 파라미터, 설명을 명확하게
- 15개 이상도 괜찮지만, 비슷한 도구가 겹치면 에이전트가 혼란 → 통합하거나 분리

### guardrails/ — 안전장치

에이전트가 폭주하지 않도록 다층 방어. 나중에 필요할 때 추가하되, 자리는 미리 만들어둔다.

```python
guardrails/
├── input_validator.py    # 입력 검증 (범위 이탈, 프롬프트 인젝션)
├── output_validator.py   # 출력 검증 (형식, 안전성)
├── tool_gate.py          # 위험도 높은 도구 실행 전 확인/차단
└── escalation.py         # human escalation 트리거
```

Human escalation 트리거:
- 실패 임계값 초과 (N번 연속 실패)
- 고위험 도구 실행 (비가역적 action)
- 신뢰도 낮은 판단

---

## 3. CLAUDE.md 템플릿 (에이전트 프로젝트용)

기존 글로벌 CLAUDE.md에 추가로, 프로젝트 루트에 놓는 에이전트 개발 전용 지침.

```markdown
# CLAUDE.md

## Project
{프로젝트 한 줄 설명}

## Architecture
- `src/core/` — 에이전트 루프, 이벤트, 도구. 인터페이스 의존 금지.
- `src/tools/` — 에이전트 도구. 각 도구에 위험도 태그.
- `src/guardrails/` — 입력/출력 검증, 도구 게이트, escalation.
- `bench/` — 벤치마크 + ablation 인프라
- `docs/` — 심층 문서 (프롬프트에 넣지 말고, 포인터만 줘)

## Agent Development Rules
- core/에 인터페이스(CLI, API, 대시보드) 의존 코드 넣지 마라
  - core/는 import flask/fastapi/click/argparse 금지
  - 의존 방향: cli.py → core/, api.py → core/ (역방향 절대 금지)
  - core/만 떼어서 bench/에서 직접 호출할 수 있어야 함
- 프롬프트 변경은 반드시 bench/ 결과로 검증
- 한 번에 하나만 변경 (변인통제)
- 프롬프트 파일은 prompts/ 에 버전 관리
- stdout 최소화, 파일 기반 모니터링 우선
- 도구만 제공, 전략 강제 X
- "더 열심히 하라" 식 프롬프트 금지 → 도구/환경 개선으로 해결

## Bench
- 실행: `python bench/run.py --variant baseline.json --tasks canary --seeds 3`
- 비교: `python bench/compare.py --base baseline --target with-notepad`
- 분석: `python bench/analyze.py --base baseline --target with-notepad`

## Lint & Test
- `ruff check && ruff format --check`
- `pytest tests/`
```

---

## 4. 벤치마크 셋업

### bench/run.py — 핵심 인터페이스
```
# 실행
python bench/run.py \
  --variant variants/with-notepad.json \
  --tasks canary \
  --seeds 3

# 결과 저장 위치
# bench/results/{git_hash}/{variant_name}/{task_name}/run-{seed}.json
```

### 결과 JSON 스키마 (범용)
```json
{
  "variant": "with-notepad",
  "task": "polyglot-rust-c",
  "seed": 1,
  "git_hash": "abc1234",
  "pass": true,
  "score": 1.0,
  "tokens_used": 15000,
  "duration_seconds": 120,
  "trajectory_path": "bench/results/.../trajectory.jsonl",
  "artifacts": {}
}
```

### Variant config 스키마 (범용)
```json
{
  "name": "with-notepad",
  "description": "baseline + NOTEPAD section in prompt",
  "prompt_template": "prompts/v1-notepad.txt",
  "tools": ["default", "notepad"],
  "model": "claude-opus-4-6",
  "params": {
    "max_turns": 50,
    "enable_self_verify": true
  }
}
```

### Canary task 선정 기준
- variant에 민감한 것 (변경 시 결과가 갈림)
- 실행 시간이 짧은 것 (빠른 피드백)
- 자동 채점 가능한 것

---

## 5. Ablation 비교

### bench/compare.py — 정량 비교
```
python bench/compare.py --base baseline --target with-notepad

# 출력 예시:
# Task              | baseline | with-notepad | delta
# polyglot-rust-c   | 0/3      | 3/3          | +100%
# openssl-cert      | 2/3      | 3/3          | +33%
# Total             | 2/6      | 6/6          | +67%
# Tokens (avg)      | 12,000   | 15,000       | +25%
```

### bench/analyze.py — AI 인과 분석
```
python bench/analyze.py --base baseline --target with-notepad

# Input: git diff + 양쪽 trajectory 로그
# Output:
#   critical_step: turn 12
#   failure_type: plan_non_adherence
#   summary: "baseline은 turn 12에서 cleanup 단계를 건너뜀.
#             compiled binary(main, cmain)가 남아 verifier fail.
#             variant는 NOTEPAD의 CLEANUP checklist로 추적하여 모두 제거."
```

### 실패 분류 체계 (AgentRx 기반)

analyze.py가 실패를 분류할 때 사용하는 카테고리. 자유 형식 분석보다 체계적 태깅이 패턴 파악에 유리하다.

| 분류 | 설명 | 예시 |
|------|------|------|
| `plan_non_adherence` | 필수 단계 건너뜀 또는 불필요한 추가 작업 | cleanup 단계 누락 |
| `information_fabrication` | trajectory/도구 출력에 없는 사실 발명 | 존재하지 않는 파일 참조 |
| `invalid_tool_call` | 스키마 미준수 도구 호출 | 잘못된 파라미터 전달 |
| `tool_output_misread` | 도구 출력을 잘못 해석 | 에러 메시지를 성공으로 오독 |
| `intent_plan_mismatch` | 태스크 목표 자체를 오해 | 백플립 요청에 전진 구현 |
| `insufficient_info` | 필수 정보 부족으로 진행 불가 | 환경 스펙 누락 |
| `unsupported_intent` | 사용 가능한 도구로 작업 불가능 | 알고리즘 난이도 초과 |
| `system_error` | 외부 시스템 장애 | API timeout, 컨테이너 crash |

**Critical failure step**: 단순히 "실패했다"가 아니라, **"정확히 어느 turn에서 복구 불가능한 오류가 시작됐는가"**를 짚는다. 이게 있어야 "왜 실패했는가"에서 "어디를 고쳐야 하는가"로 넘어갈 수 있다.

### Feedback → Code 인코딩
ablation에서 발견한 것을 시스템에 정착시키는 흐름:

```
발견: "NOTEPAD이 cleanup 태스크에 효과적"
  → prompts/v2.txt에 NOTEPAD을 기본 포함
  → bench/variants/baseline.json 업데이트
  → 다음 ablation의 baseline이 됨
```

발견이 문서에만 남으면 썩는다. **코드(프롬프트, config, 테스트)로 인코딩**해야 다음 실험의 기반이 된다.

---

## 6. CI/CD

3단계: **quality (자동, 매 push)** → **docs (자동, MR)** → **bench (수동, MR)**

```yaml
# .gitlab-ci.yml

stages:
  - quality
  - docs
  - bench

# ──────────────────────────────────────
# Stage 1: Quality — 매 push마다 자동
# ──────────────────────────────────────
lint:
  stage: quality
  script:
    - ruff check && ruff format --check

test:
  stage: quality
  script:
    - pytest tests/

structure:
  stage: quality
  script:
    # 의존성 방향 검증:
    #   - types.py는 아무것도 import하지 않는지
    #   - config.py는 types만 의존하는지
    #   - tools/, guardrails/, events는 서로 import하지 않는지
    #   - core/가 인터페이스(cli, api, dashboard)를 import하지 않는지
    - python scripts/check_deps.py

# ──────────────────────────────────────
# Stage 2: Docs — MR마다 자동
# ──────────────────────────────────────
docs:freshness:
  stage: docs
  rules:
    - if: $CI_MERGE_REQUEST_IID    # MR일 때만
  script:
    # 1. MR의 코드 변경 diff 추출
    # 2. AI가 판단: "이 변경에 대해 docs/ 업데이트가 필요한가?"
    # 3. 필요한데 docs/ 변경이 없으면 → MR 코멘트로 warning
    - python scripts/check_docs_freshness.py --post-comment
  allow_failure: true              # 블로킹 X, warning만

# ──────────────────────────────────────
# Stage 3: Bench — MR에서 수동 트리거
# ──────────────────────────────────────
bench:ablation:
  stage: bench
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID
  script:
    - MAIN_HASH=$(git merge-base HEAD $CI_MERGE_REQUEST_TARGET_BRANCH_NAME)
    # main 결과 캐시 확인
    - |
      if [ ! -d "bench/results/${MAIN_HASH}" ]; then
        python bench/run.py --variant variants/baseline.json --tasks canary --seeds 3
      fi
    # feature 실행
    - python bench/run.py --variant variants/baseline.json --tasks canary --seeds 3
    # 비교 리포트를 MR 코멘트로
    - python bench/compare.py --base ${MAIN_HASH} --target $(git rev-parse HEAD) --format markdown > report.md
    - python scripts/post_mr_comment.py report.md
  artifacts:
    paths:
      - bench/results/
```

### scripts/check_docs_freshness.py

```
Input:  git diff (MR의 코드 변경)
Flow:
  1. 변경된 소스 파일 목록 추출
  2. docs/ 내 마크다운에서 해당 파일/모듈을 참조하는 문서 탐색
  3. AI에게 질문: "이 코드 변경이 다음 문서의 내용을 무효화하는가?"
     - diff + 관련 문서 내용을 컨텍스트로 전달
  4. 무효화 가능성 있으면 → MR 코멘트:
     "⚠️ core/loop.py에 timeout exit condition이 추가됐는데,
      docs/architecture.md의 exit conditions 섹션이
      업데이트되지 않았습니다."
Output: MR 코멘트 (warning) 또는 조용히 통과
```

---

## 7. Observability

에이전트 루프의 모든 이벤트를 기록하고, CLI와 대시보드 두 인터페이스로 확인.

### Event Lifecycle Logging

에이전트 루프에서 발생하는 모든 이벤트를 structured log로 남긴다.

이벤트 타입:
```json
{"type": "llm_call",    "model": "...", "input_tokens": 1200, "output_tokens": 350, "duration_ms": 2100, "prompt_hash": "..."}
{"type": "llm_response","thinking": "...", "content": "...", "stop_reason": "end_turn"}
{"type": "tool_call",   "tool": "bash", "input": "ls -la", "output": "total 42\n...", "duration_ms": 50}
{"type": "tool_error",  "tool": "bash", "input": "rm /root", "error": "Permission denied"}
{"type": "state_change","key": "phase", "from": "planning", "to": "executing"}
{"type": "decision",    "description": "retry with different approach", "reason": "timeout after 3 attempts"}
{"type": "metric",      "key": "pass_rate", "value": 0.8}
{"type": "guardrail",   "name": "tool_gate", "action": "blocked", "tool": "deploy", "reason": "high-risk, no approval"}
```

저장:
```
runs/{run_id}/
├── events.jsonl                 # 전체 이벤트 스트림 (SSOT)
├── summary.json                 # 메트릭 요약 (events에서 파생)
└── artifacts/                   # 산출물 (파일, 스크린샷 등)
```

### 인터페이스 1: CLI (개발/디버깅)

실시간으로 에이전트가 뭘 하고 있는지 확인.

```bash
# 실행 + 실시간 이벤트 스트림
python -m my_agent run --task polyglot-rust-c --stream

# [14:32:01] llm_call     model=opus tokens=1200
# [14:32:03] llm_response thinking="파일 목록을 확인해야..."
# [14:32:03] tool_call    bash: ls -la
# [14:32:03] tool_call    bash: → total 42...
# [14:32:04] state_change planning → executing

# 과거 실행 재생
python -m my_agent replay --run-id abc123

# 특정 이벤트 필터링
python -m my_agent replay --run-id abc123 --filter "type=llm_call"
```

### 인터페이스 2: Web Dashboard (분석/비교)

사후에 여러 실행을 비교하고, 실패 원인을 추적.

```
dashboard/
├── app.py                       # FastAPI
├── frontend/                    # Next.js (or 경량 대안)
└── ...
```

대시보드 핵심 뷰:
- **Run Timeline**: 한 실행의 이벤트를 시간순으로 시각화
- **LLM Inspector**: 각 LLM call의 input/output/thinking 전문 확인
- **Comparison**: variant A vs B의 이벤트 흐름 나란히 비교
- **Metrics Overview**: 실행별 pass rate, 토큰, 시간 요약

### 설계 원칙

- **events.jsonl이 SSOT** — CLI도 대시보드도 같은 이벤트 파일을 읽음
- **최대한 많이 남기고, 보여줄 때 필터링** — 기록 시점에 "이건 필요 없겠지" 판단 X
- **agent loop 코어에 logging을 깊이 삽입** — 별도 wrapper가 아니라 루프 자체에

---

## 8. 설계 판단 가이드

프로젝트 초기에 내려야 하는 결정들.

### 단일 에이전트부터 시작
멀티 에이전트는 복잡성을 폭발시킨다. 단일 에이전트의 능력을 먼저 최대화하라.
멀티로 전환하는 신호:
- 프롬프트에 조건 분기(if-else)가 너무 많을 때
- 도구가 서로 겹쳐서 에이전트가 혼란할 때
- 도구 설명을 아무리 명확히 해도 잘못 고를 때

### 모델 선택 + LLM SDK 활용

**SOTA + extended thinking max로 시작하라.** 비용/속도 최적화는 나중이다.
- 처음부터 작은 모델로 시작하면, 모델 한계인지 프롬프트/도구 문제인지 구분이 안 됨
- 최강 모델 + thinking max로 성능 상한(ceiling)을 먼저 확인
- 충분하면 작은 모델로 교체 — variant config에 model 필드가 있으므로 ablation으로 비교

**SDK API를 먼저 파악하고, 적용 가능한 것은 초기부터 적용하라.**
- **Prompt caching**: 반복되는 시스템 프롬프트/도구 정의를 캐싱 → 비용/지연시간 대폭 절감. 에이전트 루프는 매 턴마다 같은 프롬프트를 보내므로 효과가 크다.
- **Streaming**: CLI 실시간 표시 + 체감 지연시간 감소
- **Structured output**: 도구 호출/응답 파싱 안정성
- **Batch API**: 벤치마크 대량 실행 시 비용 절감 (50% 할인, 비동기)
- **Token counting**: 비용 추적 + exit condition (토큰 한도)에 활용
- 각 SDK(Anthropic, OpenAI 등)의 최신 기능을 프로젝트 시작 시 한번 훑고, 에이전트 루프에 맞는 것을 초기에 적용

### Progressive autonomy
처음부터 fully autonomous로 만들지 마라.
```
Level 1: human-in-the-loop   — 매 단계 승인
Level 2: human-on-the-loop   — 결과만 검토, 고위험 시 개입
Level 3: autonomous           — 에이전트가 end-to-end 수행
```
guardrails/ + bench/ 결과에 자신이 생기면 단계를 올린다.

---

## Quick Start Checklist

새 에이전트 프로젝트 시작 시:

1. [ ] 위 디렉토리 구조 생성 (core/, tools/, guardrails/, bench/, prompts/)
2. [ ] CLAUDE.md 작성 (위 템플릿 기반)
3. [ ] core/loop.py 최소 구현 (model + tools + exit condition)
4. [ ] Canary task 3~5개 정의 (instruction.md + test.sh)
5. [ ] baseline variant config + prompt 작성
6. [ ] `bench/run.py`로 1회 실행 확인
7. [ ] `bench/compare.py`로 비교 리포트 동작 확인
8. [ ] events.jsonl 로깅 확인 (CLI에서 --stream으로)
9. [ ] 첫 번째 가설 실험 시작

---

## References

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI가 Codex로 100만 줄 코드를 에이전트만으로 개발한 사례. 환경 설계, 컨텍스트 관리, 아키텍처 제약의 기계적 강제, 피드백 루프, 엔트로피 관리 등 harness engineering 방법론.
- [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) — OpenAI의 에이전트 구축 실용 가이드. Model + Tools + Instructions 설계, orchestration 패턴 (단일/매니저/분산), guardrails, human escalation, 평가 방법론.
- [AgentRx: Systematic debugging for AI agents](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/) — Microsoft Research의 에이전트 실패 진단 프레임워크. 9가지 실패 분류 체계, 임계 실패 단계(critical failure step) 식별, 궤적 기반 체계적 디버깅. [코드](https://aka.ms/AgentRx)
- [AI is forcing us to write good code](https://bits.logic.inc/p/ai-is-forcing-us-to-write-good-code) — 100% 테스트 커버리지, 의미론적 타입명, 작은 파일+네임스페이스, 빠른 개발 환경이 AI 시대에 선택이 아니라 필수가 된 이유.
- [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns) — 170개+ 에이전트 패턴 큐레이션. 8개 카테고리 (Context & Memory, Feedback Loops, Orchestration, Reliability & Eval 등). [웹사이트](https://agentic-patterns.com) | [llms.txt](https://agentic-patterns.com/llms.txt)
