---
description: Korean help guide for all slash commands
---

# Slash Commands 한국어 가이드

이 문서는 모든 slash commands의 사용법을 한국어로 설명합니다.

## 📋 전체 워크플로우

```
/new-feature → /clarify → /start-phase → /verify-phase → /review-phase → /create-pr → /end-phase
```

---

## 🚀 Phase 워크플로우 Commands

### `/new-feature` - 새 기능 명세 작성

**용도:** WORKSPACE/FEATURES/에 새로운 기능 명세 문서를 생성합니다.

**사용 시점:** 새 기능 개발을 시작하기 전

**주요 작업:**
- 기능 정보 수집 (기능명, 목표, 요구사항)
- Phase 분할 계획 (각 Phase = 1-2개 PR)
- 기술 스택 분석
- FEATURES 문서 생성
- ROADMAP 업데이트

**다음 단계:**
- 복잡한 기능 → `/clarify` (권장)
- 간단한 기능 → `/start-phase`

---

### `/clarify` - 요구사항 명확화 및 아키텍처 설계

**용도:** 구현 전에 불분명한 요구사항을 명확히 하고 아키텍처를 설계합니다.

**사용 시점:** `/new-feature` 이후, `/start-phase` 이전

**주요 작업:**

**Part 1: 명확화 질문**
- Edge cases, 에러 처리, 통합 지점 등 검토
- 불분명한 부분 질문 리스트 생성
- 사용자 답변 대기 (중요!)
- FEATURES 문서에 Q&A 추가

**Part 2: 아키텍처 설계**
- 3가지 설계 옵션 제시:
  - Option A: Minimal Changes (빠른 구현)
  - Option B: Clean Architecture (우아한 설계)
  - Option C: Pragmatic Balance (실용적 균형)
- 추천안 제시 및 사용자 선택 대기
- FEATURES 문서에 설계 추가

**다음 단계:** `/start-phase`

---

### `/start-phase` - Phase 개발 시작

**용도:** 새로운 Phase 개발을 시작합니다.

**사용 시점:** 새 Phase 작업을 시작할 때

**주요 작업:**
- 브랜치 안전성 확인 (develop에 있는지)
- 기능명 및 Phase 번호 수집
- Feature 브랜치 생성 (`feature/{기능명}-{phase-번호}`)
- 프로젝트 정책 확인 (WORKSPACE/00_PROJECT.md)
- Feature 문서 확인
- TodoWrite로 작업 계획 수립

**중요:** 절대 develop에서 직접 작업하지 마세요!

**다음 단계:** 작업 완료 후 → `/verify-phase`

---

### `/verify-phase` - Phase 코드 검증

**용도:** Phase 작업의 모든 코드 품질 검사를 실행합니다.

**사용 시점:** Phase 작업 완료 후

**주요 작업:**

**Backend 검증** (변경 시):
- Ruff 린트 검사
- Import 정렬 검사 (isort)
- 테스트 실행 (pytest)

**Frontend 검증** (변경 시):
- ESLint 검사
- **UI 변경 시: Chrome DevTools MCP 검증 필수!**

**중요:** 모든 검사가 통과해야 합니다.

**다음 단계:** 검사 통과 후 → `/review-phase`

---

### `/review-phase` - Phase 리뷰 및 문서 업데이트

**용도:** PR 생성 전 자체 코드 리뷰 및 문서 업데이트를 수행합니다.

**사용 시점:** `/verify-phase` 통과 후

**주요 작업:**
1. **develop 브랜치 최신화 (중요!)**
2. 변경사항 분석 (파일, 라인 수)
3. PR 크기 평가 (300줄 이하 권장)
4. 프로젝트 정책 확인 (FK 금지, PR 정책 등)
5. 컨벤션 준수 체크 (TDD, RSC, Playwright 등)
6. 문서 업데이트 (FEATURES 체크리스트, ROADMAP)
7. 리뷰 결과 보고

**중요:**
- 체크리스트 절대 생략 금지
- 300줄 초과 시 PR 분할 권장

**다음 단계:** 리뷰 통과 후 → `/create-pr`

---

### `/create-pr` - GitHub PR 생성

**용도:** 커밋, 푸시, PR 생성을 수행합니다.

**사용 시점:** `/review-phase` 완료 후

**전제 조건:**
- `/review-phase` 완료 필수
- Feature 브랜치에 있어야 함
- 모든 테스트 통과

**주요 작업:**
1. 리뷰 결과 확인
2. 브랜치 확인 (feature/* 브랜치인지)
3. 브랜치 이름 평가 (선택)
4. **커밋 생성 (분할 커밋 필수!)**
   - 논리적 단위로 분할 (10-50줄 권장)
   - Backend: models → schemas → service → router → tests
   - Frontend: types → service → component → page
5. 푸시 및 PR 생성 (영어, Target: develop)
6. PR 정보 보고

**PR 규칙:**
- 언어: 영어
- 제목: `<type>: <description>`
- Target: develop

**다음 단계:** PR 머지 후 → `/end-phase`

---

### `/end-phase` - Phase 종료

**용도:** 현재 Phase를 완료하고 다음 Phase를 준비합니다.

**사용 시점:** GitHub PR 머지 완료 후

**전제 조건:**
- GitHub PR 머지 완료
- Checks 통과 완료

**주요 작업:**
1. develop 최신화
2. 로컬 feature 브랜치 삭제 (원격은 자동 삭제될 수 있음)
3. 다음 Phase 확인 (FEATURES 문서)
4. 완료 보고

**다음 단계:**
- 다음 Phase 있음 → `/start-phase`
- 새 기능 시작 → `/new-feature`

---

## 🔍 문서 관리 Commands

### `/check-outdated` - 문서 최신성 검증

**용도:** WORKSPACE 문서들이 최신 상태인지 확인하고 오래된 정보를 찾습니다.

**사용 시점:** 정기적으로 또는 문서 업데이트 전

**검증 항목:**

1. **00_ROADMAP.md 검증**
   - "현재 집중 기능" vs 실제 작업
   - Phase 완료 상태 vs FEATURES 체크리스트
   - "다음 개발 기능" vs 실제 우선순위

2. **CLAUDE.md 검증**
   - "Current Status" vs ROADMAP
   - "Latest Branch" vs 실제 브랜치
   - "Recent Achievements" 누락 항목

3. **FEATURES 문서 검증**
   - ROADMAP ↔ FEATURES 양방향 검증
   - Status vs 체크리스트 일치 여부

4. **날짜 정보 검증**
   - "Last Updated" vs 실제 수정 날짜
   - "Created" 날짜 정확성

5. **정책 테이블 검증**
   - CLAUDE.md vs 00_PROJECT.md 정책 일치

**결과 형식:**
- ✅ 최신 상태 (Up-to-date)
- ❌ Outdated 문서 발견 (Critical)
- ⚠️ 주의 필요 (Warning)
- 💡 개선 제안 (Suggestions)

**수정 우선순위:**
- 🔴 High: 즉시 수정 (ROADMAP 현재 집중 기능 등)
- 🟡 Medium: 시간 날 때 (Last Updated 날짜 등)
- 🟢 Low: 선택 사항 (Created 날짜 등)

---

### `/sync-docs` - 문서-코드 동기화 검사

**용도:** WORKSPACE 문서들이 실제 코드와 동기화되어 있는지 확인합니다.

**사용 시점:** 코드 구현 후, PR 전

**검증 항목:**

1. **코드 패턴 검증**
   - Frontend 참조 구조 (announcements/ 모듈 패턴)
   - Backend 패턴 (models, schemas, service, router)

2. **FEATURES 체크리스트 검증**
   - 체크리스트 항목 vs 실제 구현
   - ✅로 체크된 항목의 코드 존재 여부
   - 코드 있는데 ❌로 체크된 경우

3. **코드 예제 검증**
   - Skills 패턴 준수 검증
   - 금지된 패턴 사용 여부 (FK, raw HTML 등)
   - 문서에 언급된 파일 경로 존재 여부

4. **WORKSPACE 폴더 구조 검증**
   - 00_PROJECT.md 구조 vs 실제 구조
   - README 인덱스 vs 실제 파일

**결과 형식:**
- ✅ 일치하는 항목
- ❌ 불일치 항목 (문서에는 있으나 코드 없음 등)
- ⚠️ 주의 항목 (금지된 패턴 사용 등)

**중요:**
- 자동 수정하지 않음 (보고만 함)
- False positive 고려
- 의미 기반 검증 (단순 문자열 매칭 X)

---

## 💡 사용 팁

### 일반적인 워크플로우

**새 기능 개발:**
```
1. /new-feature        # 명세 작성
2. /clarify            # 요구사항 명확화 (복잡한 기능)
3. /start-phase        # Phase 1 시작
4. [코드 작성]
5. /verify-phase       # 코드 검증
6. /review-phase       # 리뷰 및 문서 업데이트
7. /create-pr          # PR 생성 (영어)
8. [PR 머지 대기]
9. /end-phase          # Phase 1 종료
10. 다음 Phase 반복 (3-9)
```

**문서 정리:**
```
1. /check-outdated     # 오래된 문서 찾기
2. [문서 수정]
3. /sync-docs          # 코드와 동기화 확인
4. /verify-phase       # 커밋
```

### Command 생략 가능한 경우

- `/clarify`: 매우 간단한 기능, 명세가 이미 구체적
- `/start-phase`: 긴급 버그 수정 (develop에서 직접 작업 금지는 유지!)
- `/verify-phase`: UI 변경 없는 문서 수정
- `/review-phase`: 문서만 수정 (코드 변경 없음)

### 주의사항

1. **브랜치 안전성**
   - 항상 feature 브랜치에서 작업
   - 절대 develop에서 직접 작업 금지

2. **분할 커밋**
   - `/create-pr`은 자동으로 granular commits 생성
   - 10-50줄 단위로 논리적 분할

3. **문서 업데이트**
   - Phase 작업 시 FEATURES 체크리스트 업데이트 필수
   - ROADMAP 진행 상황 반영

4. **UI 변경**
   - Chrome DevTools MCP 검증 절대 생략 금지
   - `/verify-phase`에서 자동 체크

5. **PR 언어**
   - PR 제목과 설명은 영어로 작성
   - 코드 커밋 메시지도 영어

---

## 🔗 관련 문서

- **CLAUDE.md**: 프로젝트 개요, Critical Rules
- **WORKSPACE/00_PROJECT.md**: 프로젝트 정책
- **WORKSPACE/00_ROADMAP.md**: 로드맵, 완료/진행/계획 기능
- **WORKSPACE/FEATURES/**: 기능 명세 및 Phase 체크리스트
- **.claude/skills/**: 개발 컨벤션 (자동 로드됨)

---

## ❓ 질문이 있나요?

이 가이드에 없는 내용이나 추가 도움이 필요하면 언제든지 물어보세요!

**Last Updated:** 2025-10-31
