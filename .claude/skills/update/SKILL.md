---
name: update
description: 클럽이 새로 올린 스킬(예: week2, clarify)을 내 작업실로 받아온다. 내가 만든 스킬은 건드리지 않는다. "update", "최신 스킬 받아줘", "새 스킬 받기", "클럽 업데이트" 요청에 사용.
---

# Update — 클럽 최신 스킬 받아오기

클럽은 매주 새 스킬을 템플릿 레포에 올린다. 이 스킬은 그 **클럽 소유 스킬**만 내 `.claude/skills/`로 받아온다. **내가 만든 스킬(check-in 등)은 절대 덮어쓰지 않는다.**

## 원천

- 템플릿 레포: `github.com/dp-investor-club/my-investor-club-workspace` (브랜치 `main`)
- 클럽 소유 스킬 목록(manifest): 레포 루트의 `.claude/club-skills.txt`
- manifest에 없는 `.claude/skills/*` 는 **참가자 소유** → 절대 건드리지 않는다.
- 클럽 소유 **문서**: `curriculum.md` 1개. 클럽이 갱신하는 공통 지도이므로 스킬과 함께 받아온다.

## 절차

1. 템플릿의 manifest를 읽는다:
   ```
   curl -fsSL https://raw.githubusercontent.com/dp-investor-club/my-investor-club-workspace/main/.claude/club-skills.txt
   ```
   각 줄이 클럽 스킬 이름이다 (`#` 주석·빈 줄 무시).

2. 각 스킬에 대해, 템플릿의 해당 폴더 파일 전체를 GitHub API로 나열하고 받아온다.
   예 (skill 이름을 `$S`로):
   ```
   # 폴더 안 모든 파일 경로 나열
   curl -fsSL "https://api.github.com/repos/dp-investor-club/my-investor-club-workspace/git/trees/main?recursive=1" \
     | (파이썬/grep으로 ".claude/skills/$S/" 로 시작하는 blob 경로 추출)
   # 각 경로를 raw로 받아 같은 상대경로에 저장
   #   https://raw.githubusercontent.com/.../main/<경로>  →  로컬 <경로>
   ```
   폴더가 없으면 새로 만들고, 있으면 덮어쓴다(클럽 스킬이므로).

3. **`curriculum.md` 갱신** (클럽 소유 문서):
   ```
   # 기존 파일이 있으면 먼저 사본을 남긴다
   cp curriculum.md curriculum.md.bak   # 있을 때만
   curl -fsSL https://raw.githubusercontent.com/dp-investor-club/my-investor-club-workspace/main/curriculum.md -o curriculum.md
   ```
   - 받은 뒤 **무엇이 바뀌었는지 요약해서 알려준다**(`diff curriculum.md.bak curriculum.md` 참고).
     특히 "지금 내 작업실에 있어야 하는 것" 체크리스트에 새로 생긴 항목을 짚어준다.
   - 참가자가 `curriculum.md` 에 개인 메모를 써 놨을 수 있다. 사본(`curriculum.md.bak`)이
     남아 있으니 그 사실을 알려주고, 개인 메모는 `journey.md` 로 옮기라고 안내한다.

4. **안전 규칙**:
   - manifest에 **없는** `.claude/skills/` 폴더는 절대 삭제·수정하지 않는다 (참가자 소유).
   - `journey.md` `CLAUDE.md` `context.md` `outputs/` `weeks/` 등 참가자 파일은 건드리지 않는다.
     (`curriculum.md` 는 예외 — 위 3번대로 클럽이 갱신한다.)
   - 크레덴셜·토큰 파일은 받지도 만들지도 않는다.

5. 끝나면 보고한다: **받은 스킬 목록 / 새로 생긴 것 / 갱신된 것 / `curriculum.md` 변경 요약**. 그리고 새 스킬을 어떻게 쓰는지 한 줄씩 안내한다 (예: "`/week2` 로 이번 주 실습 시작").

## 동료 스킬 받기 (Week 4부터, 선택)

동료가 PR로 올린 스킬은 템플릿의 `peer-skills/` 아래에 `peer-{ID}-{스킬이름}/` 형태로 들어온다. **manifest(`club-skills.txt`)에는 없다** — 클럽 스킬이 아니므로 자동으로 받지 않는다.

참가자가 "누구 스킬 받아줘" / "동료 스킬 보여줘"라고 하면:

1. 템플릿의 `peer-skills/` 목록을 보여준다(`git/trees/main?recursive=1` 에서 `peer-skills/` 로 시작하는 경로).
2. 참가자가 고른 것만 받아 **`.claude/skills/peer-{ID}-{스킬이름}/`** 에 저장한다 — 이름에 `peer-` 접두어를 유지해 **내 스킬과 절대 섞이지 않게** 한다.
3. 받은 뒤 그 SKILL.md 맨 위 "이 스킬은" 4줄을 읽어주고, 거기 적힌 "설치 후 첫 실행" 한 줄을 그대로 실행해본다.
4. 안 되면 그게 데이터다 — 어디서 막혔는지 한 줄로 정리해 원저자에게 전달할 수 있게 남긴다. 남의 스킬을 대신 고치지 않는다.

## 막힐 때

브라우저에서 최신 스킬 확인: `https://github.com/dp-investor-club/my-investor-club-workspace/tree/main/.claude/skills`
