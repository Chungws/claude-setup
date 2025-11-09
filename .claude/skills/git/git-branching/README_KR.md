# Git Branching Strategy Skill

## 개요

this project의 Git Flow 브랜치 전략을 정의한 스킬입니다. **작업 전 브랜치 확인은 필수**이며, develop/main에서 직접 작업하면 안 됩니다.

## 언제 사용하나요?

- 새 기능 작업을 시작할 때
- 브랜치를 생성/관리할 때
- 실수로 develop에서 작업했을 때 복구 방법이 필요할 때
- MR을 생성하기 전 브랜치 상태를 확인할 때

## 핵심 규칙

1. **작업 전 브랜치 확인 필수** - `git branch --show-current`
2. **develop/main에서 직접 작업 금지**
3. **Main branch는 `develop`** (NOT main)
4. **모든 MR은 `develop`으로**

## 브랜치 확인 (필수)

**모든 작업 전에:**

```bash
# 항상 먼저 실행!
git branch --show-current

# "develop" 또는 "main"이 나오면:
# ❌ 멈추고 feature 브랜치 생성!

# "feature/something"이 나오면:
# ✅ 작업 가능
```

## 브랜치 종류

| 브랜치 | 용도 | 생성 출처 | 병합 대상 |
|--------|------|-----------|-----------|
| `main` | Production | - | - |
| `develop` | 개발 (Main) | `main` | `main` |
| `feature/*` | 기능 개발 | `develop` | `develop` |

## Feature 브랜치 워크플로우

```bash
# 1. 브랜치 확인
git branch --show-current

# 2. develop 최신화 후 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 3. 작업 및 커밋
git add .
git commit -m "feat: add feature"

# 4. Push
git push -u origin feature/your-feature-name

# 5. MR 생성 (target: develop)
/create-mr

# 6. 병합 후 정리
git checkout develop
git pull origin develop
git branch -d feature/your-feature-name
```

## 브랜치 네이밍

### ✅ 올바른 예시

```bash
feature/translation-eval-phase-1
feature/fix-login-bug
feature/add-user-profile
```

### ❌ 잘못된 예시

```bash
bugfix/issue-123          # feature/ 사용
refactor/cleanup          # feature/ 사용
translation-eval          # feature/ 접두사 없음
feature/TRANSLATION-EVAL  # 소문자 사용
```

**패턴:** `feature/<설명-하이픈-구분>`

## 실수 복구

### develop에서 작업한 경우 (커밋 전)

```bash
git stash
git checkout -b feature/my-new-feature
git stash pop
```

### develop에서 작업한 경우 (커밋 후)

```bash
git checkout -b feature/my-new-feature
git checkout develop
git reset --hard origin/develop
git checkout feature/my-new-feature
```

## 팁

이 스킬은 브랜치를 생성하거나 관리할 때 자동으로 로드됩니다. 작업 전 **반드시** 브랜치를 확인하세요!
