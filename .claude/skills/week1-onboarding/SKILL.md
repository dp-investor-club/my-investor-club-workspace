---
name: week1-onboarding
description: Week 1 온보딩 = 첫 수업 복습 리플레이 × Claude Code 기능 탐험 × 작업실 짓기 × 자기 선언(과제). "온보딩", "week1", "복습", "시작", "과제" 요청에 사용.
---

# Week 1 Onboarding — 수업을 손으로 다시 살기

각 블록은 첫 수업(7/10)의 한 장면을 복습하고, 그 장면의 Claude Code 기능을 직접 탐험하며, 그 결과로 **작업실의 실제 조각이 하나씩 생긴다.** 마지막 블록이 Week 1 과제(자기 선언)다. 참가자는 비개발자 투자 지망생이다.

---

## STOP PROTOCOL — 절대 위반 금지

각 블록은 반드시 2턴에 걸쳐 진행한다.

```
┌─ Phase A (첫 번째 턴) ─────────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN을 읽고 설명한다  │
│ 2. EXECUTE를 안내한다: "지금 직접 실행해보세요"             │
│ 3. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│ ❌ 금지: Phase A에서 퀴즈 출제, AskUserQuestion, 되묻기     │
└──────────────────────────────────────────────────────────┘
   ⬇️ 참가자가 "완료", "다음" 등을 입력하면
┌─ Phase B (두 번째 턴) ─────────────────────────────────┐
│ 1. QUIZ/CHECK를 AskUserQuestion으로 진행하고 피드백한다     │
│ 2. [스캐폴드]가 있으면 만들어진 조각을 눈으로 확인시킨다      │
│ 3. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다        │
└──────────────────────────────────────────────────────────┘
```

### Phase A 종료 시 필수 문구

```
---
👆 위 내용을 직접 실행해보세요.
끝나면 "완료" 또는 "다음"이라고 입력해 주세요.
```

이 문구 뒤에는 어떤 도구 호출이나 텍스트도 출력하지 않는다.

## References 맵

| Block | 주제 | 파일 |
|---|---|---|
| 0 | Setup (혼자 진행자용) | `references/block0-setup.md` |
| 1 | Why — 왜 터미널인가 | `references/block1-why.md` |
| 2 | 위임 — 첫 방 짓기 | `references/block2-delegate.md` |
| 3 | 대화 — 읽기·질문시키기 | `references/block3-conversation.md` |
| 4 | 모드 — plan과 auto | `references/block4-modes.md` |
| 5 | Memory — 나의 CLAUDE.md 채우기 | `references/block5-memory.md` |
| 6 | 자기 선언 (Week 1 과제) | `references/block6-declaration.md` |

## 진행 규칙

- 한 번에 한 블록. "다음", "skip", 블록 번호로 이동한다.
- Claude Code 기능 질문이 오면 내장 claude-code-guide 에이전트로 정확히 답하고, 따라할 수 있게 단계별로 안내한 뒤 현재 블록으로 복귀한다.
- 에러/막힘은 그 자리에서 해결하고 복귀한다.
- 참가자의 파일(CLAUDE.md, journey.md 등)에 기록할 때는 반드시 참가자의 말을 받아 적는다 — 대필하지 않는다.

## 시작

아래 표를 보여주고 AskUserQuestion으로 시작점을 묻는다. **수업에 참석했다면 Block 1부터** (설치·로그인 완료 상태), 혼자 처음이면 Block 0부터.

| Block | 주제 | 만들어지는 것 |
|---|---|---|
| 0 | Setup | 설치 + 로그인 |
| 1 | 왜 터미널인가 | (수업 복습 퀴즈) |
| 2 | 위임 | `weeks/` 강의안 서랍 |
| 3 | 대화 | journey.md 1주차 기록 |
| 4 | 모드 | plan mode 경험 |
| 5 | 나의 CLAUDE.md 채우기 | 나에게 맞춰진 CLAUDE.md |
| 6 | **자기 선언 (과제)** | journey.md 선언 + Slack 제출 |
