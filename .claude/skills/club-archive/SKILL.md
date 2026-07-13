---
name: club-archive
description: 클럽이 올린 강의 자료·주차 원본을 필요할 때 불러온다. 결석/복습용 레퍼런스. "강의 자료", "지난 강의", "강의록", "club-archive", "이번 주 자료" 요청에 사용.
---

# Club Archive — 클럽 자료 불러오기 (레퍼런스)

클럽은 강의 원본·주차 자료를 별도 창고(`club-materials` 브랜치)에 올린다. 이 스킬은 그것을 **필요할 때만** 불러온다.

## 원칙 (반드시 지킨다)

- 이건 **레퍼런스**다 — 복습·결석 보충용. 학생은 강의를 듣고 **자기 언어로** 요지를 자기 `weeks/week-0N/`에 직접 정리해야 하며, 이 원본을 그대로 복사해 넣지 않는다.
- 불러온 원본은 참가자의 판단 자산(`CLAUDE.md`/`context.md`/`journey.md`)과 섞지 않는다. 임시로 볼 때는 `_club-archive/`(gitignore 대상)에 받는다.

## 자료 위치

기본 URL:
```
https://raw.githubusercontent.com/dp-investor-club/my-investor-club-workspace/club-materials/
```

목록·구조 확인:
```
https://github.com/dp-investor-club/my-investor-club-workspace/tree/club-materials/lectures
```

## 절차

1. 참가자가 원하는 주차를 확인한다 (없으면 "몇 주차 자료가 필요하세요?"). 모르면 위 tree URL을 WebFetch로 읽어 있는 목록을 보여준다.
2. 해당 파일을 받는다 — 예: Week 1 강의 원본
   ```
   curl -fsSL -o _club-archive/week-01/ic_week1_full_v1.html \
     https://raw.githubusercontent.com/dp-investor-club/my-investor-club-workspace/club-materials/lectures/week-01/ic_week1_full_v1.html
   ```
   (먼저 `mkdir -p _club-archive/week-01`)
3. 참가자가 원하면 그 자료의 **요지를 뽑아** 설명하되, "자기 언어로 `weeks/week-0N/`에 정리해보세요 — 그게 복습입니다"라고 안내한다.
4. `.gitignore`에 `_club-archive/`가 없으면 추가를 제안한다 (레퍼런스는 내 레포에 커밋하지 않는다).

## 막힐 때

브라우저에서 직접 보기: `https://github.com/dp-investor-club/my-investor-club-workspace/tree/club-materials/lectures`
