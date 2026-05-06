# Dependency Analysis Before Planning

## 공개 API 변경/제거 전 필수

구현 plan을 짜기 전에 반드시:

1. 변경/제거할 함수, 타입, 상수를 grep으로 사용처 전수조사
2. import chain을 끝까지 따라가서 영향 범위 파악
3. 영향받는 파일이 있으면 같은 커밋에 포함

## 예시

```bash
# parse_claude_result 제거 전
grep -r "parse_claude_result" src/ tests/
# → node_repo.py, ssh_node_repo.py에서 import → 같은 커밋에서 교체
```

## 금지

- grep 없이 "이 함수는 여기서만 쓰일 것이다" 추측 금지
- 영향받는 consumer가 있는데 커밋 분리 금지 (독립적으로 green이 아니면 합친다)
