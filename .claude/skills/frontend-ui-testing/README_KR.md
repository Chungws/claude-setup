# Frontend UI Testing Skill

## 개요

Chrome DevTools MCP를 사용한 Frontend UI 검증 규칙을 정의한 스킬입니다. **모든 UI 변경은 Chrome DevTools MCP 검증이 필수**입니다.

## 언제 사용하나요?

- UI 컴포넌트를 생성/수정한 후
- 레이아웃이나 스타일을 변경한 후
- Frontend MR을 생성하기 전
- 새 페이지나 라우트를 추가한 후

## 핵심 규칙

**UI 변경 시 Chrome DevTools MCP 검증은 필수입니다.**

커밋 전에 시각적으로 확인하지 않으면 안 됩니다.

## 검증 프로세스

### 1단계: 개발 서버 시작

```bash
cd frontend
npm run dev  # http://localhost:3000
```

### 2단계: Chrome DevTools MCP로 페이지 열기

```typescript
mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/your-page"
})
```

### 3단계: UI 스냅샷

```typescript
mcp__chrome-devtools__take_snapshot()
```

현재 페이지 구조, 표시되는 요소, 텍스트 내용을 확인합니다.

### 4단계: 콘솔 에러 확인

```typescript
mcp__chrome-devtools__list_console_messages()
```

JavaScript 에러가 없는지 확인합니다.

## 검증 체크리스트

```
[ ] 개발 서버 실행 중
[ ] 페이지 로드 정상
[ ] 새 컴포넌트 렌더링 정상
[ ] 레이아웃 깨지지 않음
[ ] 반응형 디자인 작동
[ ] 인터랙션 요소 클릭 가능
[ ] 콘솔 에러 없음
```

## Chrome DevTools MCP 도구

```typescript
// 페이지 열기
mcp__chrome-devtools__navigate_page({ url: "..." })

// 페이지 구조 확인
mcp__chrome-devtools__take_snapshot()

// 스크린샷 저장
mcp__chrome-devtools__take_screenshot({ path: "..." })

// 콘솔 확인
mcp__chrome-devtools__list_console_messages()

// 요소 클릭
mcp__chrome-devtools__click({ selector: "..." })

// 텍스트 입력
mcp__chrome-devtools__fill({ selector: "...", text: "..." })
```

## 팁

이 스킬은 Frontend UI를 변경할 때 자동으로 로드됩니다. Chrome DevTools MCP 검증은 **필수**입니다.
