---
description: Plan mode 명세를 understanding 라이브러리(IEEE 830, ISO 29148 기반 31개 메트릭)로 분석하여 품질 점수를 보여준다.
user-invocable: true
---

현재 대화에서 가장 최근 plan mode 출력(Claude가 작성한 명세)을 찾아 품질을 분석한다.

## 분석 대상

대화 컨텍스트에서 plan mode로 작성된 명세를 찾는다. plan이 없으면 "분석할 plan이 없습니다. plan mode에서 먼저 명세를 작성해주세요."라고 안내하고 종료한다.

plan이 영어가 아니면, 분석 전에 먼저 영어 버전의 plan을 작성하여 사용자에게 보여준 뒤 그것을 분석 대상으로 사용한다. understanding 라이브러리가 영어 spaCy 모델 기반이므로 영어가 아니면 정확한 분석이 불가능하다.

## 분석 실행

plan 텍스트를 임시 파일(`/tmp/plan_to_analyze.md`)에 저장한 뒤, `uvx`로 실행한다:

```bash
uvx --from "git+https://github.com/Testimonial/understanding" understanding /tmp/plan_to_analyze.md --json
```

실패하면 사용자에게 `uv` 설치 여부를 확인하라고 안내한다.

## 출력 형식

분석 결과를 다음 형식으로 **사용자에게** 출력한다. 한국어로 작성한다.

```
📋 Plan 명세 품질 분석

Overall: {점수}%
{바 차트 — █ 20칸 기준}

카테고리별:
  structure      {바 차트} {점수}%
  testability    {바 차트} {점수}%
  readability    {바 차트} {점수}%
  cognitive      {바 차트} {점수}%
  semantic       {바 차트} {점수}%
  behavioral     {바 차트} {점수}%

💡 {가장 낮은 1~2개 카테고리}가 낮습니다 — {어떤 개별 메트릭이 점수를 끌어내렸는지 1~2문장}.
   "왜 낮은지 자세히 알려줘" 또는 "개선 방법 알려줘"라고 물어보세요.
```

바 차트: `█`(채움)과 `░`(빈칸) 20칸. 점수 비율만큼 채운다.

## 중요: 사용자에게 보여주지 않는 것

- understanding이 반환하는 개별 메트릭 상세 수치(31개)는 사용자에게 직접 출력하지 않는다.
- 이 수치는 Bash tool result로 Claude 컨텍스트에 자동으로 남아 있으므로, 후속 질문 시 참조하여 답한다.

## 후속 대화 지원

사용자가 후속 질문을 하면 컨텍스트에 있는 상세 메트릭과 원본 plan 텍스트를 참조하여 한국어로 답한다:

- "readability 왜 낮아?" → 개별 메트릭(Flesch, Gunning Fog 등) 수치 중 낮은 항목과 원인 문장 설명
- "testability 올리려면?" → plan 원문에서 모호한 부분 지목 + 구체적 수정안
- "이 plan 수정해줘" → 분석 결과 반영하여 개선된 명세 작성

## 메트릭 참고 (후속 답변용)

| 카테고리 | 비중 | 측정 대상 |
|---|---|---|
| Structure | 30% | 원자성, 완전성, 수동태 비율, 모호한 대명사, 조동사 강도 |
| Testability | 20% | 정량적 제약조건 비율, 제약 밀도, 경계값 커버리지 |
| Readability | 15% | Flesch, Kincaid, Gunning Fog, SMOG, Coleman-Liau, ARI |
| Cognitive | 15% | 문장 길이, 복잡도, 개념 밀도, 부정문, 조건문 부하 |
| Semantic | 10% | Actor/Action/Object 존재, 결과, 트리거 |
| Behavioral | 10% | 시나리오 분해, 전이 완전성, 분기 커버리지, 관찰 가능성 |
