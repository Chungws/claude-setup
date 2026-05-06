---
name: lint-vault
description: >
  Obsidian vault(~/dapi-ssot)의 전체 헬스체크를 수행한다.
  고아 노트, 깨진 위키링크, 허브 미등록, 태그 불일치, 연결 부족을 탐지하고 자동 수정한다.
  "/lint-vault", "vault 점검", "헬스체크" 등의 요청 시 활성화.
user-invocable: true
---

# Lint Vault

vault 전체의 구조적 건강 상태를 점검하고 자동 수정한다.

## Input
- scope: all | orphans | links | tags | connections (optional, default: all)
- fix: true | false (optional, default: true — 자동 수정 여부)

## Step 1: 전체 노트 수집

Glob으로 `~/dapi-ssot/research/**/*.md` 전체 파일 목록 수집.
타입별 분류:
- `topics/*.md` → hub
- `papers/*.md` → paper
- `articles/*.md` → article
- `repos/*.md` → repo
- `insights/*.md` → insight
- `threads/*.md` → thread
- `artifacts/*.md` → artifact

## Step 2: 깨진 위키링크 탐지

모든 노트에서 `[[...]]` 패턴을 grep으로 추출.
각 위키링크가 가리키는 파일이 vault에 실제 존재하는지 확인.

**판정 기준:**
- `[[파일명]]` → `research/**/파일명.md` 존재 여부
- `[[topics/파일명]]` → 경로 포함 링크는 그대로 확인

**자동 수정:**
- 파일명이 변경된 경우 (유사도 높은 파일 존재) → 링크 업데이트
- 파일이 삭제된 경우 → 리포트만 (수동 판단 필요)

## Step 3: 고아 노트 탐지

**정의:** 다른 어떤 노트에서도 `[[파일명]]`으로 링크되지 않는 노트.

**면제:**
- `topics/*.md` (허브 노트) — 최상위 진입점이므로 면제
- `index.md` — 카탈로그이므로 면제

**자동 수정:**
- 고아 노트의 tags와 내용을 분석하여 관련 허브 노트 식별
- 허브 노트의 적절한 키워드맵 섹션에 위키링크 추가
- 고아 노트의 `related:` 프론트매터에 허브 링크 추가

## Step 4: 허브 미등록 탐지

각 비허브 노트(paper, article, repo, thread)가 최소 1개의 허브 노트에서 링크되는지 확인.

**자동 수정:**
- 노트의 tags/related를 기반으로 가장 관련 높은 허브 식별
- 허브의 키워드맵에 등록

## Step 5: 연결 부족 탐지

**insight 노트 전용:** Zettelkasten 규칙상 최소 2개 다른 노트와 연결 필요.

본문의 `[[위키링크]]` 개수를 카운트.
- 2개 미만 → 연결 부족 경고
- 0개 → critical (고립된 인사이트)

**자동 수정 안 함** — 의미 있는 연결은 내용을 이해해야 하므로 리포트만.

## Step 6: 태그 일관성 점검

프론트매터의 `tags:` 필드를 전수 조사.
- 동일 개념의 다른 표기 탐지 (예: `multi-agent` vs `multiagent` vs `multi_agent`)
- 허브 노트 태그와 하위 노트 태그 정합성
- 타입 태그 누락 (paper/article/repo/insight 중 하나 필수)

**자동 수정:**
- 타입 태그 누락 → 경로 기반으로 추가
- 표기 불일치 → 가장 빈도 높은 형태로 통일 (사용자 확인 후)

## Step 7: 프론트매터 필수 필드 점검

모든 노트에 아래 필드가 있는지 확인:
- `created:` — 필수
- `tags:` — 필수
- `status:` — 필수
- `related:` — hub/insight 필수, 나머지 권장
- `url:` — paper/article/repo 필수

**자동 수정:**
- `status:` 누락 → `status: done` 추가
- `tags:` 누락 → 경로 기반 타입 태그만 추가

## Step 8: 리포트 생성

`~/dapi-ssot/SOT/learnings/{date}-lint.md`에 기록:

```
---
created: {date}
type: vault-lint
total_notes: N
issues_found: N
auto_fixes: N
---

# Vault Lint — {date}

## 요약
| 검사 항목 | 전체 | 이슈 | 자동 수정 |
|-----------|------|------|-----------|
| 깨진 위키링크 | N | N | N |
| 고아 노트 | N | N | N |
| 허브 미등록 | N | N | N |
| 연결 부족 (insight) | N | N | - |
| 태그 불일치 | N | N | N |
| 프론트매터 누락 | N | N | N |

## 상세 이슈
### 깨진 위키링크
- {파일}: [[{링크}]] → 대상 없음

### 고아 노트
- {파일}: 어디서도 링크 안 됨 → {허브}에 등록

### 허브 미등록
- {파일}: 허브 연결 없음 → {허브}에 등록

### 연결 부족 (insight)
- {파일}: 위키링크 {N}개 (최소 2개 필요)

### 태그 불일치
- {태그A} vs {태그B}: {N}개 노트 영향

### 프론트매터 누락
- {파일}: {필드} 누락 → 자동 추가

## 자동 수정 내역
1. {파일}: {무엇을 수정}
```

## Step 9: 사용자 출력

```
## Vault Lint: {date}

전체 {N}개 노트 검사

| 항목 | 이슈 | 수정 |
|------|------|------|
| 깨진 링크 | N | N |
| 고아 노트 | N | N |
| 허브 미등록 | N | N |
| 연결 부족 | N | - |
| 태그 불일치 | N | N |
| 프론트매터 | N | N |

자동 수정: {N}건 완료
수동 확인 필요: {N}건
리포트: {경로}
```

## 자동 수정 원칙
- **수정하는 것:** 프론트매터 필드 추가, 타입 태그 추가, 고아 노트 허브 등록, 깨진 링크 중 명백한 rename
- **수정 안 하는 것:** 내용 변경, 노트 삭제, 의미적 연결 추가, 태그 통일 (리포트 후 사용자 확인)
- **절대 안 하는 것:** CLAUDE.md/SKILL.md 수정, 노트 내용 재작성
