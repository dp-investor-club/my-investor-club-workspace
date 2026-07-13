---
name: github-helper
description: git/GitHub 초보자의 일상 언어 질문을 git 작업으로 번역하고 에러를 해결하는 안전망. "깃허브에 올리고 싶어", "에러 났어", "예전 걸로 되돌리고 싶어" 같은 요청에 사용.
---

# GitHub Helper — 초보자 안전망

참가자는 비개발자다. 이 skill의 역할은 **일상 언어 → git 작업 번역**과 **패닉 진정**이다. 모든 작업은 main 브랜치에서 직접 한다 (feature branch, PR 없음).

## 질문 번역표

| 참가자의 말 | 실제 의도 | 실행 |
|---|---|---|
| "올리고 싶어 / 저장하고 싶어" | commit + push | `/submit` 권장, 급하면 add → commit → push |
| "최신 걸로 받고 싶어" | pull | `git pull --rebase origin main` |
| "뭐가 바뀌었는지 보고 싶어" | status / diff | `git status`, `git diff` |
| "아까 걸로 되돌리고 싶어" | 미커밋: restore / 커밋됨: revert | 상태 확인 후 분기 |
| "누가 언제 뭘 했는지" | log | `git log --oneline -10` |
| "내 게 안 올라가" | push 거부 | 아래 에러 해결표 |

번역 후에는 실행 전에 한 줄로 설명한다: "지금부터 {비유}에 해당하는 작업을 합니다." (commit=세이브, push=업로드, pull=최신본 내려받기)

## 진행 원칙

1. **항상 `git status`부터.** 현재 상태를 모르고 명령을 실행하지 않는다
2. 참가자가 명령을 외우게 하지 않는다. "다음에도 말로 시키면 됩니다"를 반복한다
3. 파괴적 작업(`reset --hard`, `push --force`, 파일 삭제) 전에는 반드시 결과를 설명하고 확인을 받는다. force push는 이 레포에서 금지다
4. 작업이 `club/` 아래를 수정하려 하면 멈춘다 — `club/`은 클럽 교재라 읽기 전용으로 다룬다

## 자주 나오는 에러 해결

| 에러 | 의미 (일상 언어) | 해결 |
|---|---|---|
| `rejected ... fetch first` | 다른 사람이 먼저 올렸음 | `git pull --rebase origin main` 후 다시 push |
| rebase 충돌 | 같은 파일을 두 사람이 고침 | 본인 파일이면 충돌 부분을 함께 열어 선택, 타인 파일이면 `git rebase --abort` 후 강사 호출 |
| `Permission denied` / 인증 실패 | GitHub이 나를 못 알아봄 | `git remote -v` 확인, HTTPS + Personal Access Token 재설정 안내 |
| `not a git repository` | 레포 폴더 밖에 있음 | `cd`로 레포 루트 이동 |
| 한글 파일명이 깨져 보임 | 표시 문제일 뿐 | `git config core.quotepath false` |

## 패닉 시나리오

"다 날아간 것 같아요" 요청 시 순서:

1. 안심시킨다 — commit된 것은 거의 항상 복구 가능하다
2. `git status` + `git log --oneline -5` + 필요시 `git reflog`로 상태 파악
3. 복구 실행 전, 안전망으로 현재 상태를 백업한다: `git branch backup-{날짜}`
4. 복구 후 무슨 일이 있었는지 1문단으로 설명한다

## 이 skill이 하지 않는 것

- 브랜치 전략, PR, fork 설명 — 이 프로그램에서는 쓰지 않는다. 물어보면 "main 직접 커밋으로 충분하다"고 답하고 이유(참가자 27명, 개인 폴더 격리)를 설명한다
- 크레덴셜이 이미 push된 경우의 은폐 — 즉시 강사에게 보고하게 한다. 토큰/키는 회수(rotate)가 유일한 해법이다
