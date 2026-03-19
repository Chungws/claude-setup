# Skill Improvement Plan

Based on: [Lessons from Building Claude Code: How We Use Skills](https://x.com/i/status/2033949937936085378) by Thariq (@trq212)

## Current State

- 12 skills (+ 2 incomplete: orchestrate, insight-queue)
- Gotchas sections: 0/12
- Progressive disclosure: 3/12 (research, project-init, tdd-principles)
- Scripts/assets: 3/12 (multi, research, project-init)
- On-demand protection hooks: 0

## P0 — Immediate Impact

### 1. Gotchas sections for all skills
- [ ] 각 스킬 사용 시 Claude가 실패한 패턴을 `## Gotchas`에 축적
- [ ] 시작: 자주 쓰는 스킬부터 (research, save, experiment)
- Why: "가장 높은 가치의 콘텐츠는 Gotchas 섹션" — 아티클 핵심 메시지

### 2. Description field as trigger condition
- [ ] quality-setup — "무엇을 하는지" → "언제 트리거할지"로 변경
- [ ] project-init — 트리거 조건 명시 필요
- [ ] tdd-principles — 트리거 조건 보강
- Good examples: find-skills, save, daily-review (이미 트리거 패턴 포함)

## P1 — High Impact

### 3. `/careful` on-demand hook skill
- [ ] rm -rf, force-push, DROP TABLE, kubectl delete 차단
- [ ] PreToolUse matcher on Bash
- [ ] 세션 단위로만 활성화

### 4. `/freeze` on-demand hook skill
- [ ] 특정 디렉토리 외 Edit/Write 차단
- [ ] 디버깅 시 실수로 다른 코드 수정 방지

### 5. Progressive disclosure expansion
- [ ] experiment — 실험 루프 상세 지침을 references/로 분리
- [ ] daily-review — 분석 기준/템플릿을 별도 파일로
- [ ] lessons — 교훈 포맷/예시를 templates/로

## P2 — Structural

### 6. Product verification skill
- [ ] Playwright 기반 UI 검증 워크플로우
- [ ] pytest assertion 자동 검증
- [ ] 검증 영상 녹화 패턴 고려

### 7. Cleanup
- [ ] orchestrate/ — 삭제 또는 완성
- [ ] insight-queue — SKILL.md 추가 여부 결정

## P2.5 — Obsidian Skills (kepano/obsidian-skills)

Installed: obsidian-markdown (~/dapi-ssot/.claude/skills/)

### Candidates
- [ ] obsidian-bases — vault 노트를 DB처럼 쿼리하는 .base 파일 생성. 노트 많아지면 도입
- [ ] defuddle — 웹페이지 클린 추출. /save 스킬의 WebFetch 대체 후보
- [ ] obsidian-cli — Obsidian API 경유 vault 조작. 현재 파일시스템 직접 접근으로 충분
- [ ] json-canvas — .canvas 파일 생성. 캔버스 사용 시 도입

## P3 — Future

### 8. Skill usage logging
- [ ] PreToolUse hook으로 스킬 트리거 로깅
- [ ] undertrigger 스킬 파악

### 9. Railroading audit
- [ ] 각 스킬의 과도한 순서 지정 검토
- [ ] 판단 기준 + 정보 제공 → Claude가 상황 맞게 적응하도록
