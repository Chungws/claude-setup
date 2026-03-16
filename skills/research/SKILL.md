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
TOPIC_SLUG=$(echo "$ARGUMENTS" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
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

## Phase 1: Scoping
1. `$ARGUMENTS`에서 토픽, 범위 추출
2. `~/dapi-ssot/research/topics/`에서 기존 관련 리서치 확인 (Grep)
3. 검색 키워드 3~5개 도출
4. 기존 vault 노트와의 연결점 파악
5. 리서치 계획을 사용자에게 보여주고 확인 받기

## Phase 2: Parallel Collection
확인 후 3개 서브에이전트를 Agent tool로 병렬 스폰한다.
각 서브에이전트의 프롬프트에 다음을 포함:

- **paper-scout**: "Read ~/.claude/skills/research/paper-scout.md를 읽고 지시를 따르라. 키워드: {keywords}, 토픽: {topic}"
- **repo-analyst**: "Read ~/.claude/skills/research/repo-analyst.md를 읽고 지시를 따르라. 키워드: {keywords}, 토픽: {topic}"
- **article-crawler**: "Read ~/.claude/skills/research/article-crawler.md를 읽고 지시를 따르라. 키워드: {keywords}, 토픽: {topic}"

3개를 동시에 스폰하고 결과를 기다린다.

## Phase 3: Synthesis
서브에이전트 결과 수합 후:
1. 생성된 파일들을 전부 읽기
2. 중복 및 관련도 낮은 항목 제거
3. 핵심 인사이트 3~5개 도출
4. `~/dapi-ssot/projects/` 내 진행중인 프로젝트와 연관성 분석
5. 허브 노트 생성: `~/dapi-ssot/research/topics/{topic-slug}.md`

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

## 논문
- [[paper-1]] - 한줄 요약
- [[paper-2]] - 한줄 요약

## GitHub 프로젝트
- [[repo-1]] - 한줄 설명

## 아티클
- [[article-1]] - 한줄 요약

## 관련 프로젝트
- [[projects/my-project]] - 연관성 설명

## 추가 탐색 방향
- ...
```

## Phase 4: Logging
세션 로그를 `~/dapi-ssot/SOT/session-logs/YYYY-MM-DD-research-{topic-slug}.md`에 기록:
- 검색 키워드, 수집 결과 수, 소요 시간
- 생성/수정한 파일 목록

## 실패 처리
- 검색 결과 0건 → 키워드를 동의어/상위 개념으로 확장하여 재시도
- 서브에이전트 실패 → 나머지 결과로 종합 진행, 실패한 영역은 로그에 기록
- 기존 토픽과 중복 → 기존 허브 노트에 새로운 결과를 append
