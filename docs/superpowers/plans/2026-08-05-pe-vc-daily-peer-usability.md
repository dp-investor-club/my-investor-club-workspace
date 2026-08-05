# pe-vc-daily 동료 사용성 (더벨 링크 복구 + 첫 실행 안내) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 더벨(모바일) 원문 링크 추출 실패를 실제로 고치고(curl 기반 3단계 fallback), "이 스킬은" 4줄에 첫 실행 기대치·남은 한계를 정직하게 적어서, `/update`로 이 스킬을 받아가는 동료가 나(junha) 없이도 신뢰하고 쓸 수 있게 한다.

**Architecture:** 애플리케이션 코드가 아니라 AI가 따르는 자연어 절차 문서(SKILL.md) 두 사본을 수정하는 작업이다. Git으로 추적되는 원본은 `peer-skills/peer-junha-pe-vc-daily/SKILL.md`(과거 커밋 이력이 여기 있음)이고, `.claude/skills/pe-vc-daily/SKILL.md`는 내 컴퓨터에서 실제로 실행되는 로컬 사본(추적 이력 없음, 지금은 두 파일이 바이트 단위로 동일)이다. **먼저 tracked 원본(peer-skills)을 고치고, 마지막에 그대로 로컬 사본에 복사**해 두 파일을 다시 동일하게 맞춘다. 코드 테스트 대신, 더벨 링크 복구는 실제 오늘자 데이터로 curl→URL 재구성→WebFetch까지 한 번 실행해 검증한다.

**Tech Stack:** Markdown(SKILL.md) — 코드 없음. 검증에 Bash(curl)·WebFetch 도구 사용.

## Global Constraints

- 투자 조언(매수·매도 추천, 목표가, 기대수익률)을 생성하지 않는다 — 기존 SKILL.md "하지 않는 것" 원칙, 이번 수정도 위반하지 않는다.
- 근거 없는 수치를 만들지 않는다. 확인 불가하면 `unknown`으로 남긴다 — 이번 수정과 직접 관련은 없지만 절차 문구에 남아있는 기존 원칙이므로 건드리지 않는다.
- club 컨벤션(`peer-skills/README.md`): "각 SKILL.md 맨 위 '이 스킬은' 4줄이 설치 안내다" — 새 섹션을 만들지 않고 이 4줄만 고친다.
- 실패는 조용히 넘어가지 않는다 — 더벨 복구가 실패하면 어느 단계에서 왜 실패했는지 브리핑에 구체적으로 남긴다(스펙 결정 사항).
- `peer-skills/peer-junha-pe-vc-daily/SKILL.md`가 git 추적 원본이다. `.claude/skills/pe-vc-daily/SKILL.md`는 이번에도 git에 추가하지 않는다(기존 관례 유지 — 로컬 실행 사본).

---

## File Structure

- Modify: `peer-skills/peer-junha-pe-vc-daily/SKILL.md` — 매체 테이블의 더벨 행, 절차 1단계(더벨 링크 복구 로직 추가), `## 이 스킬은` 4줄 중 "설치 후 첫 실행"·"아직 안 되는 것" 두 줄.
- Modify: `.claude/skills/pe-vc-daily/SKILL.md` — 위 파일과 동일한 내용으로 덮어써서 동기화(마지막 태스크).

## Task 1: 더벨 미디어 테이블 행 + 절차 1단계에 링크 복구 로직 추가

**Files:**
- Modify: `peer-skills/peer-junha-pe-vc-daily/SKILL.md` (매체 테이블 "핵심 — 매번 확인" 섹션의 더벨 행, `## 절차` 1번 항목)

**Interfaces:**
- Consumes: 없음 (파일 전체가 이미 존재)
- Produces: 더벨 링크 복구 절차(curl→newskey 추출→URL 재구성→실패 시 폴백). Task 2·3은 이 로직의 존재를 전제로 "아직 안 되는 것" 문구를 쓴다.

- [ ] **Step 1: 더벨 매체 테이블 행 교체**

`peer-skills/peer-junha-pe-vc-daily/SKILL.md`에서 다음 줄을 찾는다:

```
| 더벨(모바일) | `https://m.thebell.co.kr/m/news.asp?svccode=01` | deal 섹션. 모바일판이 무료 기사만 보여줘서 데스크톱판보다 읽기 편함(2026-08-04 확인) |
```

아래로 교체한다:

```
| 더벨(모바일) | `https://m.thebell.co.kr/m/news.asp?svccode=01` | deal 섹션. 모바일판이 무료 기사만 보여줘서 데스크톱판보다 읽기 편함(2026-08-04 확인). 목록의 기사 링크는 `<a href>`가 아니라 JS `onclick=readNews('newskey')`라서 WebFetch만으로는 원문 URL을 못 얻는다 — curl로 원본 HTML을 가져와 링크를 재구성한다(2026-08-05 확인, 아래 절차 1단계 참고) |
```

- [ ] **Step 2: 절차 1단계에 더벨 링크 복구 문단 삽입**

같은 파일에서 다음 텍스트를 찾는다 (`## 절차` 섹션의 1번과 2번 항목 사이):

```
목록에 오늘 날짜 기사가 없으면(딜사이트처럼 매일 갱신 안 되는 경우) 그 사실을 밝히고 넘어간다 — 억지로 지난 기사를 오늘 것처럼 쓰지 않는다.
2. 그중 딜 관련성이 높은 순으로 최대 10건을 고르고,
```

아래로 교체한다(1번 항목에 이어지는 문단을 추가하고, 2번 항목은 그대로 둔다):

```
목록에 오늘 날짜 기사가 없으면(딜사이트처럼 매일 갱신 안 되는 경우) 그 사실을 밝히고 넘어간다 — 억지로 지난 기사를 오늘 것처럼 쓰지 않는다.

   **더벨 링크 복구**: 더벨(모바일) 목록 페이지는 기사 링크를 `<a href>`가 아니라 JS `onclick=readNews('newskey')`로 그려서 WebFetch로는 원문 링크를 못 얻는다. 다음 순서로 시도한다 — (1) curl로 목록 URL의 원본 HTML을 가져와 `attr={"newskey":"...","subject":"...","freedtm":"...",...}` 형태의 인라인 JS 데이터에서 newskey·제목·게시일을 추출하고, `https://m.thebell.co.kr/m/newsview.asp?svccode=01&newskey=<값>`으로 원문 URL을 재구성한다. (2) curl을 못 쓰거나(Bash 도구 없음 등) 이 방식이 실패하면 기존처럼 WebFetch로 목록만 읽어 제목·날짜만 확보한다. (3) 그래도 링크를 못 구하면 더벨을 제외하되, 어느 단계에서 왜 실패했는지(예: "curl 명령을 찾을 수 없음", "newskey 패턴 없음 — 사이트 구조 변경 추정") 브리핑 앞에 구체적으로 남긴다.
2. 그중 딜 관련성이 높은 순으로 최대 10건을 고르고,
```

- [ ] **Step 3: 실제 데이터로 검증 — curl→URL 재구성→WebFetch**

아래 명령을 그대로 실행해 오늘자 더벨 목록에서 newskey를 하나 뽑는다:

```bash
curl -s -A "Mozilla/5.0" "https://m.thebell.co.kr/m/news.asp?svccode=01" | grep -o 'attr={"newskey":"[0-9]*"' | head -1
```

Expected: `attr={"newskey":"202608..."` 형태로 20자리 숫자 newskey가 최소 1개 출력된다 (0건이면 사이트 구조가 바뀐 것 — Step 2에서 적은 폴백 문구가 실제로 필요해진 상황이니, 그 사실을 이 태스크 완료 메모에 남기고 다음 단계로 넘어간다).

뽑은 newskey로 실제 기사 URL을 만들어 WebFetch로 읽는다:

```
https://m.thebell.co.kr/m/newsview.asp?svccode=01&newskey=<위에서 뽑은 값>
```

Expected: 에러 페이지가 아니라 실제 기사 제목·본문이 나온다. 이게 확인되면 재구성 로직이 실제로 작동하는 것이다.

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\junha\dev\my-investor-club-workspace"
git add peer-skills/peer-junha-pe-vc-daily/SKILL.md
git commit -m "pe-vc-daily: 더벨 링크 curl 복구(newskey 재구성) + 3단계 fallback 추가"
```

## Task 2: "이 스킬은" 4줄 중 첫 실행 기대치·한계 갱신

**Files:**
- Modify: `peer-skills/peer-junha-pe-vc-daily/SKILL.md` (`## 이 스킬은` 섹션)

**Interfaces:**
- Consumes: Task 1에서 확정한 더벨 복구 로직(폴백 3단계) — "아직 안 되는 것" 문구가 이를 정확히 반영해야 한다.
- Produces: 없음 (문서 최상단, club 설치 안내의 전부)

- [ ] **Step 1: "설치 후 첫 실행" 줄 교체**

다음 줄을 찾는다:

```
- 설치 후 첫 실행: "pe-vc-daily" (별도 설정 없이 바로 실행 가능)
```

아래로 교체한다:

```
- 설치 후 첫 실행: "pe-vc-daily" (별도 설정 없이 바로 실행 가능). 여러 매체를 순서대로 확인하느라 몇 분 걸릴 수 있고, 그날 나온 딜 뉴스 양에 따라 결과가 보통 4~10건으로 달라진다 — 적게 나온다고 실패한 게 아니다.
```

- [ ] **Step 2: "아직 안 되는 것" 줄 교체**

다음 줄을 찾는다:

```
- 아직 안 되는 것: 매체 간 중복 딜 병합 판단은 AI의 해석에 의존해 케이스마다 결과가 조금 다를 수 있음(기준은 최대한 구체화했지만 완전히 결정론적이진 않음). 오늘 하루치 수집 안에서의 중복만 다루고, 전날 브리핑과의 병합은 안 함. 마켓인사이트는 PE/VC 전용 카테고리가 없어 관련성 낮은 기사가 섞일 수 있음
```

아래로 교체한다:

```
- 아직 안 되는 것: 매체 간 중복 딜 병합 판단은 AI의 해석에 의존해 케이스마다 결과가 조금 다를 수 있음(기준은 최대한 구체화했지만 완전히 결정론적이진 않음). 오늘 하루치 수집 안에서의 중복만 다루고, 전날 브리핑과의 병합은 안 함. 더벨은 curl로 링크를 복구하지만 동료 환경에서 Bash/curl을 못 쓰면 여전히 빠질 수 있음(그 경우 이유가 브리핑에 남음). 딜사이트는 매일 갱신되지 않아 오늘자가 없는 날이 많음. 마켓인사이트는 PE/VC 전용 카테고리가 없어 관련성 낮은 기사가 섞일 수 있음
```

- [ ] **Step 3: 확인**

`peer-skills/peer-junha-pe-vc-daily/SKILL.md`의 `## 이 스킬은` 섹션(4줄)을 다시 읽고, 각 줄이 한 문장/한 흐름으로 자연스럽게 읽히는지, Task 1의 폴백 3단계(curl 시도 → WebFetch만 → 제외+사유 기록)와 "아직 안 되는 것" 줄의 설명이 서로 모순 없이 맞는지 확인한다.

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\junha\dev\my-investor-club-workspace"
git add peer-skills/peer-junha-pe-vc-daily/SKILL.md
git commit -m "pe-vc-daily: 첫 실행 기대치(소요시간·건수 편차)와 더벨 fallback 한계 명시"
```

## Task 3: 로컬 실행 사본 동기화 + 전체 일관성 확인

**Files:**
- Modify: `.claude/skills/pe-vc-daily/SKILL.md` (Task 1·2를 반영한 `peer-skills/peer-junha-pe-vc-daily/SKILL.md`와 동일하게 덮어쓴다)

**Interfaces:**
- Consumes: Task 1·2가 완료된 `peer-skills/peer-junha-pe-vc-daily/SKILL.md`의 최종 내용
- Produces: 없음 (동기화 태스크, 이후 다른 태스크 없음)

- [ ] **Step 1: 로컬 사본을 tracked 원본과 동일하게 덮어쓴다**

`peer-skills/peer-junha-pe-vc-daily/SKILL.md`의 전체 내용을 그대로 `.claude/skills/pe-vc-daily/SKILL.md`에 복사한다(파일 전체 교체).

- [ ] **Step 2: 두 파일이 바이트 단위로 동일한지 확인**

```bash
cd "C:\Users\junha\dev\my-investor-club-workspace"
diff "peer-skills/peer-junha-pe-vc-daily/SKILL.md" ".claude/skills/pe-vc-daily/SKILL.md" && echo IDENTICAL
```

Expected: 출력 없이 `IDENTICAL`만 찍힌다. 차이가 있으면 Step 1을 다시 한다.

- [ ] **Step 3: 최종 git 상태 확인**

```bash
git log --oneline -3
git status
```

Expected: Task 1·2의 커밋 2개가 위쪽에 보이고, `git status`에는 `.claude/skills/pe-vc-daily/SKILL.md`가 (기존 관례대로) untracked로 남아있거나 — 이 워크스페이스에서 `.claude/skills/`가 `.gitignore`에 없으므로 untracked 파일로 표시된다. 이번 계획과 무관한 변경이 섞여 있지 않은지만 확인하고, `.claude/skills/pe-vc-daily/SKILL.md`는 커밋하지 않는다(Global Constraints 참고).

이 태스크는 git commit을 만들지 않는다 — 로컬 실행 사본은 의도적으로 미추적 상태를 유지한다.
