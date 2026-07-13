# Block 0: Setup (혼자 진행자용 — 수업 참석자는 스킵)

## EXPLAIN

안심하고 시작하세요: **최난관은 이 설치이고, 이후엔 명령어를 직접 칠 일이 거의 없습니다** — 이전 기수 실측으로 환경 문제는 첫날 집중되고 이후 급감했습니다. 막히는 건 통과의례입니다.

| OS | 설치 한 줄 |
|---|---|
| Mac | 터미널(⌘+Space→"터미널")에서 `curl -fsSL https://claude.ai/install.sh | bash` |
| Windows | PowerShell에서 `irm https://claude.ai/install.ps1 | iex` |

설치 후 **터미널을 완전히 껐다가 다시 열고** `claude` 입력 → 테마는 Enter → `Claude account with subscription` 선택 → 브라우저에서 Authorize.

| 문제 | 해결 |
|---|---|
| `command not found: claude` | 터미널 재시작을 건너뛴 경우 99% |
| Windows 실행 정책 에러 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 후 재시도 |
| 브라우저가 안 열림 | 터미널의 링크를 복사해 브라우저에 붙여넣기 |

## EXECUTE

1. 설치 → 터미널 재시작 → `claude` 실행 → 로그인
2. 이 레포 폴더로 이동(`cd my-investor-club-workspace`) 후 다시 `claude`, "Trust this folder?"는 Yes
3. 첫 인사: `안녕, 나는 {이름}이야. 이 레포가 뭔지 한 문단으로 설명해줘`

## CHECK

퀴즈 없음. "설치와 첫 인사까지 완료했습니까?" (완료 / 진행 중 / 문제 발생)만 확인한다.
