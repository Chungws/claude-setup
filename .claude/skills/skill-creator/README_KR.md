# Skill Creator - 한국어 가이드

> 이 문서는 팀원을 위한 한국어 요약입니다. Claude는 영어 원본 SKILL.md를 참조합니다.

## Skill이란?

**Skill**은 Claude의 능력을 확장하는 모듈형 패키지입니다. 특정 도메인이나 작업을 위한 "온보딩 가이드"라고 생각하면 됩니다.

### Skill이 제공하는 것

1. **전문 워크플로우** - 특정 도메인을 위한 다단계 절차
2. **도구 통합** - 특정 파일 형식이나 API 작업 지침
3. **도메인 전문 지식** - 회사별 지식, 스키마, 비즈니스 로직
4. **번들 리소스** - 복잡하고 반복적인 작업을 위한 스크립트, 참고자료, 자산

## Skill 구조

```
skill-name/
├── SKILL.md (필수)        # Claude가 읽는 instruction
│   ├── YAML frontmatter   # name, description
│   └── Markdown 본문      # 사용 방법, 워크플로우
└── Bundled Resources (선택)
    ├── scripts/           # 실행 가능한 스크립트 (Python/Bash 등)
    ├── references/        # 참고 문서 (스키마, API 명세 등)
    └── assets/            # 출력에 사용되는 파일 (템플릿, 아이콘 등)
```

### 각 리소스의 용도

| 리소스 | 용도 | 예시 |
|--------|------|------|
| **scripts/** | 반복 작성되는 코드를 재사용 | `rotate_pdf.py` |
| **references/** | Claude가 필요 시 참조할 문서 | `schema.md`, `api_docs.md` |
| **assets/** | 출력에 포함할 파일 (context에 안 올림) | `logo.png`, `template.pptx` |

## Skill 생성 프로세스

### 1️⃣ 구체적인 예시로 이해하기
- "어떤 기능을 지원해야 하나?"
- "사용 예시를 들어줄 수 있나?"
- "어떤 요청이 이 skill을 트리거해야 하나?"

### 2️⃣ 재사용 가능한 컨텐츠 계획
- 각 예시를 분석하여 필요한 `scripts/`, `references/`, `assets/` 식별

### 3️⃣ Skill 초기화
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```
- 템플릿 생성 및 디렉토리 구조 자동 생성

### 4️⃣ Skill 편집
- **작성 스타일:** 명령형/부정사형 (예: "To do X, run Y")
- **SKILL.md 질문:**
  1. 이 skill의 목적은?
  2. 언제 사용해야 하나?
  3. Claude가 어떻게 사용해야 하나?

### 5️⃣ 패키징
```bash
scripts/package_skill.py <path/to/skill-folder>
```
- 자동으로 validation 후 zip 파일 생성

### 6️⃣ 반복 개선
- 실제 사용 → 문제점 발견 → 개선 → 재테스트

## Progressive Disclosure 원칙

Skill은 3단계 로딩 시스템으로 context를 효율적으로 관리합니다:

1. **Metadata** (name + description) - 항상 context에 (~100 단어)
2. **SKILL.md 본문** - Skill 트리거 시 (<5k 단어)
3. **Bundled resources** - Claude가 필요 시 (무제한*)

*스크립트는 context에 안 올리고 실행 가능하므로 무제한

## 작성 팁

- **SKILL.md는 간결하게** - 상세 정보는 `references/`로 분리
- **Grep 패턴 제공** - 큰 파일(>10k words)인 경우
- **중복 방지** - 같은 정보를 SKILL.md와 references에 모두 넣지 말 것

## 라이센스

Apache License 2.0 - 자유롭게 사용, 수정, 배포 가능

---

**원본:** `SKILL.md` (English)
**상세 라이센스:** `LICENSE.txt`
