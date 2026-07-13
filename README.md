# club-materials — 클럽 창고 (운영 브랜치)

이 브랜치는 **학생 fork에 딸려가지 않는다.** "Use this template"은 기본 브랜치(`main`)만 복사하기 때문에, 여기 있는 강의 원본·주차 자료는 템플릿을 가볍게 유지하면서 클럽이 따로 관리한다.

## 구조

```
lectures/
  week-01/ic_week1_full_v1.html   # 강의 슬라이드 원본
  week-02/ ...                     # 매주 추가
```

## 운영 원칙

- **학생에게 미리 떠먹이지 않는다.** 학생은 강의를 듣고 **자기 언어로** 요지를 자기 레포의 `weeks/week-0N/`에 직접 정리한다(그 정리 자체가 학습).
- 이 원본은 **레퍼런스**다 — 결석/막힌 학생 안내, 운영진 차주 설계, Week 5 baseline.
- 학생은 `/club-archive` 스킬로 필요할 때만 이 브랜치의 자료를 불러본다 (raw URL fetch).

## 주차 자료 올리는 법 (운영자)

```
git checkout club-materials
mkdir -p lectures/week-0N && cp <자료> lectures/week-0N/
git add lectures/week-0N && git commit -m "week-0N 자료" && git push origin club-materials
```

올린 뒤 Slack 공지: "이번 주 강의 자료 올라왔어요 — Claude Code에서 `/club-archive` 하세요."
