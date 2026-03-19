---
name: lessons
description: >
  세션에서 사용자 피드백(교정, 선호, 규칙)을 감지하여 memory/rules에 반영한다.
  "/lessons", "교훈 정리", "피드백 정리" 등의 요청 시 활성화.
user-invocable: true
---

# Lessons

세션에서 사용자 피드백을 감지하고 저장할 가치가 있는 것만 추출한다.

## 동작 모드

- **인자 없음**: 현재 세션의 대화를 회고하여 피드백 감지
- **세션ID 또는 "all"**: 과거 세션 JSONL을 grep으로 피드백 패턴만 추출

## Process

### Step 1: 피드백 감지

#### 현재 세션 (인자 없음)
대화를 돌아보며 아래 시그널을 찾는다:
- **교정**: "하지마", "그거 아니고", "아닌데", "don't", "stop", "no not"
- **긍정 확인**: "그렇지", "맞아", "perfect", "exactly" (비자명한 접근을 확인한 경우만)
- **규칙 지시**: "다음부터", "앞으로", "항상", "절대", "from now on"

#### 과거 세션 ("all" 또는 세션ID)
1. `python scripts/tracker.py pending` 실행 → 미분석 세션 목록 확인
   - 스크립트 경로: `{SKILL_DIR}/scripts/tracker.py`
2. 각 세션 JSONL에 Grep으로 피드백 패턴 매칭 (전체 파일을 읽지 않는다):
   - `하지마|그거 아니고|아닌데|그렇지|맞아|다음부터|앞으로|항상|절대`
   - `don't|stop doing|no not|perfect|exactly|from now on|always|never`
3. 매칭된 줄의 전후 맥락(±2줄)만 읽어 피드백 내용을 파악한다
4. 분석 완료 후 `python scripts/tracker.py done <session_id>` 로 완료 마킹

피드백이 없으면 "피드백 없음." 출력 후 종료.

### Step 2: 분류 및 적용처 매핑

| 적용처 | 언제 |
|--------|------|
| `memory/feedback_*.md` | 사용자 선호, 행동 교정 |
| `.claude/rules/` | 매 대화 자동 적용할 행동 규칙 |
| `CLAUDE.md` | 프로젝트 전체 적용 규칙 |

### Step 3: 사용자 출력

```
## Feedback detected

### 1. {피드백 제목}
{맥락 1~2문장} → {감지된 사용자 발화 인용}
→ 적용처: `{파일}` — {구체적으로 뭘 할지}

적용할 항목을 알려주세요 (예: "1,3 적용해", "전부 적용", "패스")
```

### Step 4: 적용
사용자가 선택한 항목만 반영한다. rules/CLAUDE.md 변경은 diff를 먼저 보여주고 확인 후 적용.
