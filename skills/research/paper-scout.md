# Paper Scout

## Input
- keywords: 검색 키워드 (필수)
- topic: 상위 토픽명 (허브 노트 연결용)

## Process
1. WebSearch로 관련 논문 검색:
   - `{keyword} site:arxiv.org`
   - `{keyword} paper 2025 2026`
   - Semantic Scholar API: `https://api.semanticscholar.org/graph/v1/paper/search?query={keyword}`
   - arxiv 카테고리별 최신 목록: `https://arxiv.org/list/{category}/recent` (cs.AI, cs.LG, cs.CL 등 토픽에 맞는 카테고리)
   - Google Scholar: `{keyword} site:scholar.google.com`
   - ACL Anthology: `{keyword} site:aclanthology.org` (NLP 관련 토픽인 경우)
2. 상위 5~10편 선정 기준:
   - 최신성 (최근 6개월 우선)
   - 인용수 (50+ 우선, 최신은 예외)
   - 관련도 (abstract에 핵심 키워드 포함)
3. 각 논문에 대해 요약 노트 생성

## Output
파일: `~/dapi-ssot/research/papers/{YYYY}-{first-author}-{short-title}.md`

```
---
created: {date}
title: "{논문 제목}"
authors: [저자1, 저자2]
year: YYYY
venue: 학회/저널
url: https://arxiv.org/abs/XXXX
citations: N
tags: [paper, {topic-tags}]
related: [[topics/{topic}]]
status: done
---

# {논문 제목}

## Problem
이 논문이 해결하려는 문제 (2~3문장)

## Method
제안하는 방법론 핵심 (3~5문장)

## Results
주요 실험 결과 및 수치 (2~3문장)

## Limitations
한계점 및 미래 연구 방향 (2~3문장)

## Key Takeaway
우리 프로젝트에 적용할 수 있는 핵심 아이디어 (1~2문장)
```

## 실패 처리
- 검색 결과 0건 → 키워드 확장 후 재시도 1회, 여전히 0건이면 빈 결과 보고
