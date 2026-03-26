---
name: git-platform
description: >
  Git 플랫폼(GitHub/GitLab) CLI 래퍼 유틸.
  원격 저장소 URL로 플랫폼을 자동 판별하여 gh/glab CLI를 선택한다.
  다른 ludo 스킬(ludo:go, ludo:fix)이 issue fetch, 댓글, PR/MR 생성 시 사용.
  직접 호출하지 않는 유틸 스킬.
user-invocable: false
---

# Git Platform -- GitHub/GitLab CLI Abstraction

## 목적

gh(GitHub) / glab(GitLab) CLI 명령을 플랫폼에 따라 자동 선택한다.
다른 ludo 스킬이 이 스킬의 절차를 참조하여 issue, PR/MR 작업을 수행한다.

## 플랫폼 판별

원격 저장소 URL 패턴으로 판별한다:

```bash
REMOTE_URL=$(git remote get-url origin)
```

| 패턴 | 플랫폼 | CLI |
|------|--------|-----|
| `github.com` 포함 | GitHub | `gh` |
| `gitlab.` 포함 | GitLab | `glab` |
| 그 외 | **에러** | -- |

판별 실패 시:
```
ERROR: 원격 저장소 URL '{url}'에서 Git 플랫폼을 판별할 수 없습니다.
지원 플랫폼: GitHub (github.com), GitLab (gitlab.*)
```

## Issue 내용 fetch

```bash
# GitHub
gh issue view {number} --repo {owner}/{repo}

# GitLab
glab issue view {number} --repo {owner}/{repo}
```

- `{number}`: issue 번호 (URL에서 추출 또는 직접 전달)
- `--repo`: 현재 디렉토리가 해당 repo가 아닐 때 명시

## Issue에 댓글 게시

```bash
# GitHub
gh issue comment {number} --body "{comment}"

# GitLab
glab issue note {number} --message "{comment}"
```

## PR/MR 생성

```bash
# GitHub
gh pr create \
  --title "{title}" \
  --body "{body}

closes #{issue_number}" \
  --head {branch}

# GitLab
glab mr create \
  --title "{title}" \
  --description "{body}

closes #{issue_number}" \
  --source-branch {branch}
```

- `closes #{issue_number}`: PR/MR이 merge되면 issue 자동 종료
- `{branch}`: 현재 작업 브랜치 (`git branch --show-current`)

## 에러 처리

| 상황 | 대응 |
|------|------|
| `gh`/`glab` CLI 미설치 | `ERROR: {cli} CLI가 설치되어 있지 않습니다. 컨테이너 이미지에 {cli}를 포함해주세요.` |
| 인증 실패 | CLI 에러 메시지를 그대로 전달 (인증 설정은 이 스킬 범위 밖) |
| 플랫폼 판별 실패 | 위 판별 실패 메시지 출력 후 종료 |
| issue 번호 누락 | `ERROR: issue 번호가 필요합니다.` |

## 사용 예시 (다른 스킬에서)

```
1. git remote get-url origin으로 REMOTE_URL 확인
2. REMOTE_URL에 github.com이 포함되면 gh, gitlab.이 포함되면 glab 사용
3. gh issue view 42로 issue 내용 fetch
4. 작업 완료 후 gh pr create --title "feat: ..." --body "closes #42"
```
