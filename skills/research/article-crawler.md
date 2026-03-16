# Article Crawler

## Input
- keywords: 검색 키워드 (필수)
- topic: 상위 토픽명 (허브 노트 연결용)

## Process
1. WebSearch로 관련 아티클 검색:
   - `{keyword} blog tutorial guide 2025 2026`
   - `{keyword} site:medium.com OR site:dev.to`
2. 상위 5~10개 선정 기준:
   - 최신성
   - 저자 신뢰도 (기업 블로그, 유명 개발자 우선)
   - 실용성 (코드 예제, 벤치마크 포함)
3. WebFetch로 본문 확인 후 요약

## Output
파일: `~/dapi-ssot/research/articles/{YYYY-MM-DD}-{short-title}.md`

```
---
created: {date}
title: "{아티클 제목}"
author: 저자
source: 출처 (블로그명, 매체명)
url: URL
tags: [article, {topic-tags}]
related: [[topics/{topic}]]
status: done
---

# {아티클 제목}

## 핵심 요약
3~5문장으로 요약

## 주요 내용
- 포인트 1
- 포인트 2
- 포인트 3

## 코드/예시 (있는 경우)
핵심 코드 스니펫이나 아키텍처 설명

## 우리 프로젝트에 적용 가능한 점
- ...
```

## 실패 처리
- 검색 결과 0건 → 키워드 확장 후 재시도 1회, 여전히 0건이면 빈 결과 보고
