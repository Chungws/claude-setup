# Repo Analyst

## Input
- keywords: 검색 키워드 (필수)
- topic: 상위 토픽명 (허브 노트 연결용)

## Process
1. WebSearch로 GitHub 레포 검색:
   - `{keyword} github stars:>100`
   - `{keyword} language:{lang} site:github.com`
2. 상위 5~10개 레포 선정 기준:
   - Star 수 100+ 또는 최근 30일 내 활발한 커밋
   - README 품질
   - 이슈/PR 활성도
3. 각 레포에 대해 WebFetch로 README + 주요 파일 구조 확인

## Output
파일: `~/dapi-ssot/research/repos/{owner}-{repo-name}.md`

```
---
created: {date}
repo: "{owner}/{repo}"
url: https://github.com/{owner}/{repo}
stars: N
language: {primary_language}
last_commit: YYYY-MM-DD
tags: [repo, {topic-tags}]
related: [[topics/{topic}]]
status: done
---

# {owner}/{repo}

## 개요
이 프로젝트가 하는 일 (2~3문장)

## 아키텍처
- 전체 구조 설명
- 주요 디렉토리/모듈 역할

## 기술 스택
- 언어:
- 프레임워크:
- 주요 의존성:

## 활성도
- 최근 커밋 빈도
- 오픈 이슈/PR 수
- 기여자 수

## 우리 프로젝트에 적용 가능한 점
- ...
```

## 실패 처리
- 검색 결과 0건 → 키워드 확장 후 재시도 1회, 여전히 0건이면 빈 결과 보고
