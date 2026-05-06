---
name: arch-review
description: >
  멀티 페르소나 에이전트 5개를 병렬 스폰하여 프로젝트 아키텍처를 20개 관심사로 심층 리뷰한다.
  "아키텍처 리뷰", "구조 리뷰", "arch review", "큰 그림 봐줘", "architecture review" 등의 요청 시 활성화.
user-invocable: true
---

# Architecture Review — Multi-Persona

5개 전문 페르소나 에이전트를 병렬 스폰하여 프로젝트 아키텍처를 20개 관심사로 리뷰한다.

## Trigger
`/arch-review` 또는 자연어로 아키텍처 리뷰 요청 시 활성화.

## Input
- `$ARGUMENTS`: 리뷰 범위 (optional)
  - 없으면 프로젝트 전체 리뷰
  - 있으면 해당 영역에 집중 (예: `/arch-review services/`, `/arch-review error handling`)

## Phase 1: Context Discovery

리뷰 전에 프로젝트 컨텍스트를 수집한다. 이 정보가 에이전트 프롬프트의 `{context}`가 된다.

### 수집 항목
1. **CLAUDE.md** — 프로젝트 루트의 CLAUDE.md 읽기
2. **아키텍처 규칙** — `.claude/rules/*.md` 중 architecture, dependency, layer 관련 파일 읽기
3. **소스 트리** — 메인 소스 디렉토리 구조 스캔 (Glob으로 `src/**/*.py`, `src/**/*.ts` 등)
4. **기술 스택** — `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod` 등에서 언어/프레임워크 파악
5. **테스트 구조** — `tests/` 또는 `__tests__/` 디렉토리 구조 파악

### context 블록 구성
수집한 정보를 아래 형식으로 조합:

```
## Project: {프로젝트명}
## Tech Stack: {언어, 프레임워크}
## Source Root: {src 경로}
## Review Scope: {$ARGUMENTS 또는 "전체"}

## Architecture Rules (from CLAUDE.md / .claude/rules/):
{수집한 규칙 내용 — 레이어 정의, 의존 방향, 금지 사항 등}

## Source Tree:
{디렉토리 구조}
```

규칙이 없는 프로젝트는 "프로젝트에 명시된 아키텍처 규칙 없음. 일반적인 레이어드 아키텍처 원칙으로 리뷰." 로 대체.

**수집 완료 후, 에이전트 스폰 전에 사용자에게 context 요약을 보여주고 바로 Phase 2로 진행한다. 확인을 기다리지 않는다.**

## Phase 2: Parallel Agent Spawn

5개 에이전트를 Agent tool로 **한 메시지에서 동시에** 스폰한다.
모두 `subagent_type: "feature-dev:code-explorer"`를 사용한다.

### 에이전트 프롬프트 템플릿

각 에이전트에게 아래 프롬프트를 전달한다. `{agent-file}`만 에이전트별로 다르다.

```
너는 아키텍처 리뷰 서브에이전트다.

## Step 1: 지시 파일 읽기
Read ~/.claude/skills/arch-review/{agent-file}.md 를 읽고 Persona, Checklist, Process, Output Format을 따르라.

## Step 2: 프로젝트 컨텍스트
프로젝트 루트: {project_root}
리뷰 범위: {scope}

{context}

## Step 3: 실행
지시 파일의 Process에 따라 소스 파일을 읽고 체크리스트를 검증하라.

## 필수 규칙:
- 모든 소스 파일을 직접 Read tool로 읽어라 (추측 금지)
- 발견 사항마다 절대 경로 file:line 레퍼런스 필수
- severity 표기: High / Medium / Low / Info
- 최종 출력은 지시 파일의 Output Format을 따르라
- 긍정 발견("잘 되어있는 점")도 반드시 포함
```

### 에이전트 목록

| # | 파일 | 역할 | 관심사 수 |
|---|------|------|-----------|
| 1 | structure.md | 구조적 무결성 | 7 |
| 2 | abstraction.md | 추상화 품질 | 4 |
| 3 | ssot.md | SSOT & 중복 | 3 |
| 4 | data-flow.md | 데이터 흐름 | 3 |
| 5 | boundary.md | 경계 & 통합 | 3 |

## Phase 3: Synthesis

5개 에이전트 결과를 종합하여 **대화에 직접** 출력한다. 파일에 저장하지 않는다.

### 종합 규칙

1. **중복 제거**: 같은 이슈를 N개 에이전트가 발견하면 하나로 합치고 `[N/5 agents]` 표기
2. **severity 결정**:
   - High = 런타임 버그 가능성, 명시된 규칙 위반
   - Medium = 중복, 우회 패턴, 책임 과다
   - Low = 문서화 부족, 마이너 비대칭
   - Info = 설계 관찰, 개선 기회
3. **구체성**: 모든 이슈에 file:line 레퍼런스. 추상적 제안 금지
4. **actionable**: Medium 이상 이슈에 Fix 방향 제시

### 출력 형식

```
# {프로젝트명} 아키텍처 리뷰

## 잘 되어있는 점
- {에이전트들이 공통 긍정 평가한 항목}
- ...

## High — 즉시 수정 필요
### 1. {제목}
**{위치}** [N/5 agents]
{설명}
> **Fix**: {해결 방향}

## Medium — 구조적 개선
### N. {제목}
**{위치}**
{설명}
> **Fix**: {해결 방향}

## Low — 알고 있으면 좋은 것
| # | 이슈 | 위치 |
|---|------|------|
| N | 한줄 설명 | `file:line` |

## 우선순위 제안
1. {가장 먼저 할 것 + 이유}
2. {다음 + 이유}
3. ...
```

## 주의사항
- Phase 1에서 아키텍처 규칙을 못 찾아도 진행 — 일반 원칙으로 리뷰
- 에이전트가 파일을 직접 읽었으므로 file:line은 신뢰
- 5개 에이전트가 동시에 파일을 읽으므로 대형 프로젝트에서는 시간이 걸릴 수 있음
- 리뷰 범위가 지정되면 해당 영역 + 그 영역과 직접 상호작용하는 코드까지만 리뷰
