---
name: save
description: >
  URL을 받아 Obsidian vault(~/dapi-ssot)에 구조화된 노트로 저장한다.
  타입(논문/레포/아티클)을 자동 판별하고 기존 리서치와 연결한다.
  "저장해줘", "북마크", "vault에 넣어줘" 등의 요청 시 활성화.
user-invocable: true
---

# Save to Vault

URL을 받아 Obsidian vault에 구조화된 노트로 저장한다.

## Input
- url: 저장할 URL (필수, `$ARGUMENTS`에서 추출)
- tags: 추가 태그 (optional)

## Process

### 1. URL 분석
WebFetch로 내용을 가져온 뒤 타입을 판별:
- `arxiv.org`, `semanticscholar.org`, `aclanthology.org` → **paper**
- `github.com` → **repo**
- 그 외 (블로그, 뉴스, 문서 등) → **article**

### 2. 기존 vault 연결점 찾기
`~/dapi-ssot/research/topics/`의 허브 노트들을 Glob으로 찾고, 각 허브 노트의 tags를 확인하여 이 URL의 내용과 관련된 토픽을 찾는다. 관련 토픽이 있으면 해당 허브 노트에 위키링크로 연결한다.

### 3. 노트 생성
타입별 저장 경로와 템플릿:

**Paper** → `~/dapi-ssot/research/papers/{YYYY}-{first-author}-{short-title}.md`
```
---
created: {date}
title: "{제목}"
authors: [저자1, 저자2]
year: YYYY
venue: 학회/저널
url: {url}
tags: [paper, {관련 태그들}]
related: [[topics/{관련-토픽}]]
status: done
---

# {제목}

## Problem
(2~3문장)

## Method
(3~5문장)

## Results
(2~3문장)

## Limitations
(2~3문장)

## Key Takeaway
(1~2문장)

## 연결
- [[topics/{관련-토픽}]] — 연관성 설명
- [[{기존 vault 관련 노트}]] — 연관성 설명
```

**Repo** → `~/dapi-ssot/research/repos/{owner}-{repo-name}.md`
```
---
created: {date}
repo: "{owner}/{repo}"
url: {url}
stars: N
language: {primary_language}
tags: [repo, {관련 태그들}]
related: [[topics/{관련-토픽}]]
status: done
---

# {owner}/{repo}

## 개요
(2~3문장)

## 아키텍처
- 주요 구조

## 기술 스택
- 언어/프레임워크/의존성

## 우리 프로젝트에 적용 가능한 점
- ...

## 연결
- [[topics/{관련-토픽}]] — 연관성 설명
- [[{기존 vault 관련 노트}]] — 연관성 설명
```

**Article** → `~/dapi-ssot/research/articles/{YYYY-MM-DD}-{short-title}.md`
```
---
created: {date}
title: "{제목}"
author: 저자
source: 출처
url: {url}
tags: [article, {관련 태그들}]
related: [[topics/{관련-토픽}]]
status: done
---

# {제목}

## 핵심 요약
(3~5문장)

## 주요 내용
- 포인트 1
- 포인트 2
- 포인트 3

## 우리 프로젝트에 적용 가능한 점
- ...

## 연결
- [[topics/{관련-토픽}]] — 연관성 설명
- [[{기존 vault 관련 노트}]] — 연관성 설명
```

### 4. 기존 허브 노트 업데이트
관련 토픽 허브 노트가 있으면, 해당 노트의 적절한 섹션에 새 노트 위키링크를 append한다.

### 5. Ripple Update — 교차 연결 강화

허브 노트뿐 아니라 관련 기존 노트들에도 양방향 연결을 추가한다.

**5a. 관련 기존 노트 탐색**
새 노트의 핵심 키워드(tags + 제목 핵심어)로 vault를 Grep 검색:
- `research/articles/`, `research/papers/`, `research/repos/`에서 유사 주제 노트 탐색
- 최대 5개까지 가장 관련도 높은 기존 노트 선별

**5b. 새 노트 → 기존 노트 연결**
새 노트의 `## 연결` 섹션에 찾은 기존 노트들의 위키링크 추가.
연관성 한줄 설명 포함.

**5c. 기존 노트 → 새 노트 연결**
찾은 기존 노트의 `## 연결` 섹션에 새 노트 위키링크를 추가.
- `## 연결` 섹션이 있으면 마지막 항목 뒤에 append
- `## 연결` 섹션이 없으면 파일 끝에 섹션 생성 후 추가

**5d. 관련 insight 연결**
`research/insights/`에서 새 노트와 관련된 인사이트가 있으면:
- 새 노트의 연결 섹션에 인사이트 링크 추가
- 인사이트 노트에도 새 노트 backlink 추가 (source_notes에)

### 6. index.md 갱신
`research/index.md`의 "최근 추가 노트" 섹션에 새 노트를 추가한다.
- 최대 10개 유지, 오래된 항목은 제거
- 형식: `- [[{파일명}]] — {한줄 설명}`

## 필수 규칙
- 한국어로 작성
- 본문에 `[[위키링크]]` 사용
- `## 연결` 섹션 필수
- 관련 토픽이 없으면 연결 없이 저장하되, 태그는 내용 기반으로 추가
