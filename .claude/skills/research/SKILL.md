---
name: research
description: >
  주어진 토픽에 대해 논문, GitHub 프로젝트, 기술 아티클을 병렬 수집·분석하고
  Obsidian vault에 구조화된 리서치 노트를 생성한다.
  "리서치해줘", "조사해줘", "찾아봐" 등의 요청 시 자동 활성화.
user-invocable: true
---

# Research Orchestrator

## Preamble (먼저 실행)

```bash
TOPIC_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]/ /g' | tr -s ' ' '\n' | grep -vxE 'for|the|a|an|of|in|on|with|and|or|to|is|are|by|at' | head -4 | tr '\n' '-' | sed 's/-$//')
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_TIME=$(date +%H%M%S)
LOG_DIR=~/dapi-ssot/SOT/session-logs
LOG_FILE="$LOG_DIR/${SESSION_DATE}-research-${TOPIC_SLUG}.md"
mkdir -p "$LOG_DIR"
cat > "$LOG_FILE" << LOGEOF
---
created: ${SESSION_DATE}
skill: research
topic: ${ARGUMENTS}
status: in-progress
---

# Research Session: ${ARGUMENTS}

## 메타
- 시작: ${SESSION_DATE} ${SESSION_TIME}
- 키워드: (Phase 1에서 채울 것)
- 종료: (완료 시 채울 것)

## 수집 결과
- 논문: 0편
- 레포: 0개
- 아티클: 0편

## 생성된 파일
(목록)

## 오류/메모
(있으면 기록)
LOGEOF
echo "SESSION_LOG=$LOG_FILE"
echo "TOPIC_SLUG=$TOPIC_SLUG"
```

위 bash 출력의 `SESSION_LOG` 경로를 기억하고, 각 Phase 완료 시 해당 파일을 업데이트한다.

## Trigger
사용자가 `/research {토픽}` 또는 자연어로 리서치를 요청할 때 활성화.

## Input
- topic: 리서치 주제 (필수, `$ARGUMENTS`에서 추출)
- scope: 범위 (optional — papers, repos, articles, all. default: all)
- depth: shallow | deep (optional — default: deep)

## Vault 경로
모든 결과물은 `~/dapi-ssot/`에 저장한다.

## Vault 규칙 (서브에이전트에도 반드시 전달)
- 한국어로 작성
- 본문에서 다른 노트를 언급할 때 반드시 `[[위키링크]]` 사용 (frontmatter만이 아니라 본문에도)
- 노트 마지막에 `## 연결` 섹션 추가: 관련 노트 `[[위키링크]]`와 한줄 설명
- 프론트매터에 tags, related, status 필수

## Phase 1: Scoping
1. `$ARGUMENTS`에서 토픽, 범위 추출
2. `~/dapi-ssot/research/topics/`에서 기존 관련 리서치 확인 (Grep)
3. 검색 키워드 3~5개 도출
4. 기존 vault 노트와의 연결점 파악
5. 리서치 계획을 사용자에게 보여주고 확인 받기
6. **SESSION_LOG 업데이트**: 키워드 필드를 채운다

## Phase 2: Parallel Collection
확인 후 3개 서브에이전트를 Agent tool로 병렬 스폰한다.
각 서브에이전트의 프롬프트에 **반드시** 다음을 모두 포함:

```
너는 리서치 서브에이전트다.
1. Read ~/.claude/skills/research/{agent-file}.md 를 읽고 지시를 따르라.
2. 키워드: {keywords}
3. 토픽: {topic}
4. 토픽 슬러그: {topic-slug}

## 필수 규칙 (모든 노트에 적용):
- 한국어로 작성
- 본문에서 다른 노트를 언급할 때 반드시 [[위키링크]] 사용
- 노트 마지막에 "## 연결" 섹션 추가: [[topics/{topic-slug}]] 허브 노트 링크 + 관련 노트 링크
- 프론트매터에 tags, related, status 필수
- 작업 완료 후 생성한 파일 경로 목록을 반환하라
```

3개를 동시에 스폰하고 결과를 기다린다.

## Phase 3: Synthesis
서브에이전트 결과 수합 후:

### 3-1. 결과 확인
1. `~/dapi-ssot/research/papers/`, `repos/`, `articles/`에서 이번 세션에서 생성된 파일들을 Glob으로 찾기
2. 각 파일을 읽고 내용 확인
3. 중복 및 관련도 낮은 항목 제거 (파일 삭제)

### 3-2. 허브 노트 생성
`~/dapi-ssot/research/topics/{topic-slug}.md` 생성:
- 수집된 모든 노트의 **실제 파일명**으로 `[[위키링크]]` 작성 (플레이스홀더 금지)
- 핵심 인사이트 3~5개 도출
- `~/dapi-ssot/projects/` 내 진행중인 프로젝트와 연관성 분석

### Hub Note Template
```
---
created: {date}
topic: {topic}
tags: [research, {topic-tags}]
status: done
papers_count: N
repos_count: N
articles_count: N
---

# {Topic} 리서치 요약

## 핵심 인사이트
1. ...
2. ...
3. ...

## 키워드 맵
수집한 자료들을 키워드/테마별로 분류하여 큰 그림을 보여준다.
타입(논문/레포/아티클) 구분 없이, 내용 기준으로 묶는다.

### {키워드 1}: {한줄 설명}
- [[{파일명}]] — 한줄 요약
- [[{파일명}]] — 한줄 요약

### {키워드 2}: {한줄 설명}
- [[{파일명}]] — 한줄 요약
- [[{파일명}]] — 한줄 요약

### {키워드 3}: {한줄 설명}
- ...

(하나의 자료가 여러 키워드에 속할 수 있다)

## 추천 읽기 순서
수집한 자료 중 가장 임팩트 있는 것부터 순서대로.
🔑 표시 = 반드시 읽어야 할 핵심 자료.

1. 🔑 [[{파일명}]] — 이것부터 읽어야 하는 이유
2. 🔑 [[{파일명}]] — 이유
3. [[{파일명}]] — 이유
4. [[{파일명}]] — 이유
5. ...나머지는 관심 영역에 따라

## 인사이트 노트
- [[{insight-slug}]] — 한줄 설명
- [[{insight-slug}]] — 한줄 설명
(Phase 3-3에서 생성한 인사이트 노트를 여기에 링크)

## 딥다이브 추천
이 리서치에서 더 파고 싶은 방향. 복붙해서 바로 실행 가능한 형태로.

- "{궁금할 수 있는 질문}" → `/research {구체적 서브토픽}`
- "{궁금할 수 있는 질문}" → `/research {구체적 서브토픽}`
- "{궁금할 수 있는 질문}" → `/research {구체적 서브토픽}`

## 관련 프로젝트
- [[projects/{project}]] - 연관성 설명
```

### 3-3. Insight 노트 생성 (depth: deep일 때)
핵심 인사이트 3~5개를 각각 atomic note로 작성:
- 파일: `~/dapi-ssot/research/insights/{short-slug}.md`
- 하나의 노트 = 하나의 아이디어
- 자기 말로 재해석 (원문 복붙 금지)
- 본문에 출처 `[[위키링크]]` + 다른 insight `[[위키링크]]` 포함
- `## 연결` 섹션 필수

### Insight Note Template
```
---
created: {date}
tags: [insight, {topic-tags}]
source_notes: [[{출처1}]], [[{출처2}]]
related: [[topics/{topic-slug}]]
status: done
---

# {아이디어 제목}

{자기 말로 재해석한 내용 — 3~5문장}

## 연결
- [[topics/{topic-slug}]] — 허브 노트
- [[{다른-insight}]] — 연관성 한줄 설명
- 출처: [[{논문/아티클 파일명}]], [[{논문/아티클 파일명}]]
```

## Phase 4: Logging
SESSION_LOG 파일을 **최종 업데이트**:
1. status를 `done`으로 변경
2. 종료 시간 기록
3. 수집 결과 수치 업데이트 (논문 N편, 레포 N개, 아티클 N편)
4. 생성된 파일 **전체 경로 목록** 나열 (허브 노트, insight 포함)
5. 오류/메모에 실패한 검색, 접근 불가 URL 등 기록

## Phase 5: 사용자 출력
**모든 파일 작업이 끝난 후 가장 마지막에** 사용자에게 아래 형식으로 출력한다.
파일에 쓰는 것이 아니라 **대화에 직접 출력**하는 것이다.
Phase 4까지의 파일 쓰기가 대화를 밀어올리므로, 이 출력이 반드시 마지막이어야 사용자가 바로 볼 수 있다.

```
## 리서치 완료: {토픽}

### 핵심 발견 (인사이트 요약)
1. **{제목}** — 한줄 설명
2. **{제목}** — 한줄 설명
3. ...

### 🔑 추천 읽기 순서
1. 🔑 {파일명} — 이것부터 읽어야 하는 이유
2. 🔑 {파일명} — 이유
3. {파일명} — 이유

### 딥다이브 추천
- "{궁금할 수 있는 질문}" → `/research {서브토픽}`
- "{궁금할 수 있는 질문}" → `/research {서브토픽}`
- "{궁금할 수 있는 질문}" → `/research {서브토픽}`

### 수집 통계
논문 N편 / 레포 N개 / 아티클 N편 / 인사이트 N개
허브 노트: {경로}
```

이 출력이 있어야 사용자가 바로 다음 행동을 판단할 수 있다.
"어떤 것부터 읽어볼까?" 또는 딥다이브 명령어를 복붙해서 이어갈 수 있게.

## 실패 처리
- 검색 결과 0건 → 키워드를 동의어/상위 개념으로 확장하여 재시도
- 서브에이전트 실패 → 나머지 결과로 종합 진행, 실패한 영역은 로그에 기록
- 기존 토픽과 중복 → 기존 허브 노트에 새로운 결과를 append
