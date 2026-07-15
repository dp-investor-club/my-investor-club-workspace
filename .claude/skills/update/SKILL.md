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

3. **안전 규칙**:
   - manifest에 **없는** `.claude/skills/` 폴더는 절대 삭제·수정하지 않는다 (참가자 소유).
   - `journey.md` `CLAUDE.md` `context.md` `curriculum.md` `outputs/` `weeks/` 등 참가자 파일도 건드리지 않는다.
   - 크레덴셜·토큰 파일은 받지도 만들지도 않는다.

4. 끝나면 보고한다: **받은 스킬 목록 / 새로 생긴 것 / 갱신된 것**. 그리고 새 스킬을 어떻게 쓰는지 한 줄씩 안내한다 (예: "`/week2` 로 이번 주 실습 시작").

## 막힐 때

브라우저에서 최신 스킬 확인: `https://github.com/dp-investor-club/my-investor-club-workspace/tree/main/.claude/skills`
