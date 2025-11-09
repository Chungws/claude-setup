# Creating Pull Requests Skill

## 개요

이 프로젝트의 GitHub Pull Request 생성 규칙을 정의한 스킬입니다. **한국어 PR, main 브랜치**를 사용합니다.

## 언제 사용하나요?

- 기능 구현이 완료되어 PR을 생성할 때
- PR 설명을 작성해야 할 때
- GitHub MCP 도구로 PR을 생성할 때
- PR 크기나 커밋 구조를 검토할 때

## 핵심 규칙 - 프로젝트 정책

| 항목 | 설정 |
|------|------|
| **Target Branch** | `main` |
| **PR 언어** | **한국어** (제목, 설명) |
| **PR 크기** | **<300 lines** (권장) |

## PR 생성 워크플로우

```bash
# 1. Pre-PR 체크리스트
cd backend && uvx ruff check && uv run pytest -s
cd frontend && npm run lint

# 2. 변경 크기 확인
git diff main --shortstat
# 300 라인 이하 권장, 초과 시 분할

# 3. Granular commits
git add app/models.py
git commit -m "feat: add TranslationResult model"
git add app/schemas.py
git commit -m "feat: add TranslationResult schema"
# ... (models → schemas → service → router → tests)

# 4. Push
git push -u origin feature/translation-result

# 5. PR 생성 (GitHub MCP)
# 한국어로 작성
```

## PR 설명 구조

```markdown
## 요약
[1-3문장으로 변경사항 설명]

## 변경사항
### Backend/Frontend
- 주요 파일 및 내용

## 테스트 계획
- [x] Backend/Frontend 테스트 통과
- [ ] 수동 테스트 필요 사항

## 영향
- Breaking Changes: 없음/있음
- 데이터베이스 변경: 마이그레이션 필요 여부
- 의존성 추가: 새 패키지

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## GitHub MCP 사용

```typescript
mcp__github__create_pull_request({
  owner: "owner-name",
  repo: "repo-name",
  title: "feat: Translation Result 저장 기능 추가",
  head: "feature/translation-result",
  base: "main",
  body: "...",  // 위 구조 따름
  draft: false
})
```

## 예시

```markdown
## 요약
Translation Result 모델 및 API 엔드포인트를 추가하여 번역 결과를 저장하고 조회할 수 있습니다.

## 변경사항
### Backend
- `app/translation/models.py`: TranslationResult 모델 추가
- `app/translation/router.py`: API 엔드포인트 추가

## 테스트 계획
- [x] pytest 통과
- [x] ruff, isort 통과

## 영향
- Breaking Changes: 없음
- 데이터베이스 변경: 마이그레이션 필요
- 의존성 추가: 없음

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 주의사항

- ❌ Target branch를 `main`이 아닌 다른 브랜치로 하지 말 것
- ❌ 영어로 PR 작성하지 말 것 → 한국어 사용
- ❌ 300 라인 초과하지 말 것 → 분할
- ❌ 단일 커밋으로 몰아넣지 말 것 → Granular commits

## 팁

이 스킬은 Claude가 PR을 생성하거나 PR 설명을 작성할 때 자동으로 로드됩니다. `/create-mr` 커맨드와 함께 사용됩니다.
