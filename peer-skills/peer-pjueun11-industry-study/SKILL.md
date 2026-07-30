---
name: industry-study
description: 산업명 하나를 받아서 처음이면 개요(정의·밸류체인·플레이어·시장구조 등 10항목 + 메커니즘 질문)를 정리하고, 이미 있으면 최근 이슈만 outputs/industry-notes/에 누적 기록한다. "드론 산업 정리해줘", "이 산업 공부하고 싶어", "오늘 왜 오르는지 봐줘", "이슈 업데이트해줘" 요청에 사용. (참가자 소유 스킬 — /clarify 2026-07-23로 확정)
---

## 이 스킬은
- 어떤 병목: 새로운 산업이 궁금할 때, 빠르게 스캔할 수 있는 스킬이 필요했다
- 입력 → 남는 것: 스킬명과 산업명을 넣으면 산업의 밸류체인, 체인별 주요 플레이어와 기업, 최신 이슈, 글로벌 대비 국내 위상 등을 알 수 있다
- 설치 후 첫 실행: `/industry-study {산업명}` (예: `/industry-study 드론`)
- 아직 안 되는 것: 아직 모름

# Industry Study

산업명 하나로 시작해서, 처음이면 그 산업을 이해하는 데 필요한 것들을 정리하고, 이후엔 새로 생긴 이슈만 계속 쌓는 스킬이다. `routine-check`(ARKX 유지보수 전용)와는 완전히 별개다 — 이건 새 산업을 발견했을 때 폭넓게 훑는 용도.

**첫 실행**: `/industry-study {산업명}` (예: `/industry-study 드론`)

## 실행 방식

### 1. 입력 확인
산업명을 받는다. `outputs/industry-notes/<산업명 슬러그>.md`가 이미 있으면 **갱신 모드**(이슈만 추가, 개요는 요청 시에만 갱신), 없으면 **신규 모드**(개요부터 작성)로 들어간다.

### 2. 시장 기준 확인
국내/미국/글로벌 중 어느 시장 기준으로 볼지 먼저 확인한다. 국내로 임의로 고정하지 않는다 — 미국 시장 산업(예: 미국 상장 드론 관련주)을 물어볼 수도 있다.

### 3. 개요 작성 (신규 모드, 또는 갱신 요청 시)

아래 10개 항목을 체크리스트로 채운다. 확인 불가한 항목은 `[1차]`/`[2차]`/`[추정]` 라벨과 함께, 정 안 되면 `unknown`으로 남긴다 — 지어내지 않는다.

1. **정의/범위** — 이 산업이 뭘 포함하고 뭘 제외하는가
2. **밸류체인** — 단계별 흐름 (원재료 → 제조 → 유통 → 최종 수요 등)을 한 줄로 요약한 뒤, 아래 6열 표로 단계별 세부 내용을 채운다:

   | 단계 | 국내 대장주 | 국내 기타 관련주 | 해외 기업 (선도사 순) | 국산화·경쟁력 | 원가 비중 | 성장성·주목도 |
   |---|---|---|---|---|---|---|
   | ... | ... | ... | ... | ... | ... | ... |

   - **국내 대장주**: 이 단계를 이끄는 국내 기업 1개 (예: 반도체의 하이닉스처럼 — 영향력이 가장 큰 곳)
   - **국내 기타 관련주**: 같은 단계에 있는 다른 국내 종목들 (확인되는 만큼, 없으면 `unknown`)
   - **해외 기업 (선도사 순)**: 같은 단계에서 세계적으로 앞서는 기업을 순서대로
   - **국산화·경쟁력**: 이 단계를 국내가 자체 조달하는지, 수입에 의존하는지, 세계 대비 어디쯤인지
   - **원가 비중**: 드론(또는 해당 산업) 전체 원가에서 이 단계가 차지하는 비중 (확인 안 되면 `unknown`)
   - **성장성·주목도**: 이 단계가 지금 산업 안에서 얼마나 빠르게 크고 있는지, 기술적으로 얼마나 고도화되는 중인지, 최근 특히 주목받는 단계인지
   - 각 셀의 수치·주장에도 `[1차]`/`[2차]`/`[추정]` 라벨을 붙인다. 표라고 라벨을 생략하지 않는다
3. **주요 플레이어** — 국내·해외, 상장 여부와 티커 구분 (밸류체인 표의 기업들을 상장사 전체 관점에서 다시 한 번 정리 — 표는 단계별 관점, 이 항목은 기업별 관점)
4. **시장 구조·규모** — 시장 규모·성장률 (숫자엔 라벨 필수)
5. **경쟁구도·진입장벽** — 과점 정도, 특허·기술력 같은 진입장벽 유무
6. **정책·규제 환경** — 정부 지원·규제에 얼마나 민감한가
7. **기술 동향·사이클** — 초기/성장/성숙 중 어디인가
8. **수요 동인** — 최종 수요자가 누구고 왜 사는가 (B2B/B2C/B2G 구분)
9. **핵심 추적 지표** — 이 산업만의 KPI (예: 드론 산업이면 출하대수·인허가 건수)
10. **글로벌 vs 국내 비교** — 선도국·선도기업 대비 위치 (산업 자체가 미국 시장 기준이면 "미국 내 경쟁 구도"로 대체)

**메커니즘 질문 2~3개**: `mechanism-question-builder`의 6축(수익/비용/자본/위험/시장기대/회수) + 반증조건 형식을 그대로 가져와 산업 수준 질문으로 만든다. "유망한가" 같은 방향성 질문은 실격 — 반증 조건을 쓸 수 없는 질문도 실격.

### 4. 이슈 업데이트

이슈는 시간대별로 네 겹으로 나눠서 다룬다. 갱신 모드에서는 매번 네 겹을 다 훑는다 — 한 겹만 보고 끝내지 않는다.

**당일성 이슈** (오늘, 예: "오늘 왜 오르는지"):
- 당일 뉴스·속보 `[2차]`
- 당일 공시 (상한가·하한가 사유 공시 등) `[1차]`
- 동종업계 동반 등락 여부 — 업종 전체가 같이 움직였는지, 개별 종목만의 이슈인지 반드시 구분한다
- 당일 수급 동향 (외국인·기관 매매동향)

**단기 이슈** (이번 주, 최근 7일 — 당일성만큼 즉각적이진 않지만 주간 단위로 쌓인 흐름):
- 이번 주 누적 뉴스·속보 `[2차]`
- 이번 주 공시 중 당일 건 외에 누적으로 봐야 할 것 `[1차]`
- 이번 주 수급 동향 누적 (외국인·기관 매매동향)

**중단기 이슈** (이번 달, 최근 4주 — 누적되기 전 단계의 흐름):
- 이번 달 갱신된 통계·지표 (예: 시가총액·자산총계 월간 변동, 업종 지수 등락률)
- 이번 달 나온 증권사 리서치·산업 동향 기사 `[2차]`
- 이번 달 공시·정책 예고 중 아직 구조적 변화로 확정되진 않았지만 주시할 것

**중장기 이슈** (누적·연간 트렌드, 산업의 개요 자체를 흔드는 구조적 변화):
- 1차: 공시·IR, 정부 통계, 법령 개정·시행
- 2차: 국내외 경제·산업지 뉴스, **증권사 리서치·산업 백서**

CLAUDE.md 절대 규칙을 그대로 따른다: 모든 수치·핵심 주장에 라벨을 붙이고, 확인 불가한 수치는 `unknown`으로 남기며, 매수·매도 추천이나 목표가는 생성하지 않는다.

새로 확인된 이슈만 이슈 로그에 날짜순으로 추가한다. 기존 로그는 건드리지 않는다. 로그 항목마다 `[당일성]`/`[단기]`/`[중단기]`/`[중장기]` 중 하나를 태그로 붙인다.

### 5. 저장 템플릿

`outputs/industry-notes/<산업명 슬러그>.md`:

```markdown
# <산업명> 산업 노트

- 시장 기준: 국내/미국/글로벌
- 마지막 갱신: YYYY-MM-DD

## 개요
- 정의/범위: ...
- 밸류체인: ... (단계별 흐름 한 줄 요약)

  | 단계 | 국내 대장주 | 국내 기타 관련주 | 해외 기업 (선도사 순) | 국산화·경쟁력 | 원가 비중 | 성장성·주목도 |
  |---|---|---|---|---|---|---|
  | ... | ... | ... | ... | ... | ... | ... |

- 주요 플레이어: ... (국내·해외, 상장 여부·티커)
- 시장 구조·규모: ... (라벨 또는 unknown)
- 경쟁구도·진입장벽: ...
- 정책·규제 환경: ...
- 기술 동향·사이클: ...
- 수요 동인: ...
- 핵심 추적 지표: ...
- 글로벌 vs 국내 비교: ...

## 메커니즘 질문
Q1. ... [축1][축2]
  - 반증 조건: ...

## 이슈 로그 (최신순)

### YYYY-MM-DD — <이슈 한 줄 요약> [당일성 / 단기 / 중단기 / 중장기]
- 소스: <출처> `[1차]`/`[2차]`/`[추정]`
- (당일성·단기면) 업종 전체 등락인가 개별 이슈인가: ...
- 핵심 내용: ...
- 개요/메커니즘 질문에 영향 있는지: ...
```

### 6. HTML 변환

`.md`를 저장할 때마다 (신규 모드든 갱신 모드든) 같은 폴더에 같은 이름의 `.html`을 함께 만들거나 갱신한다: `outputs/industry-notes/<산업명 슬러그>.html`. `.md`가 원본이고 `.html`은 그 내용을 그대로 옮긴 읽기용 사본이다 — `.html`에만 있고 `.md`엔 없는 내용을 만들지 않는다.

아래 스켈레톤을 그대로 재사용한다 (라이트/다크 테마 자동 대응, `[1차]`/`[2차]`/`[추정]`/`unknown` 라벨을 색이 있는 뱃지로, 밸류체인은 가로 스크롤 표, 메커니즘 질문·이슈 로그는 카드로 표시):

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title><산업명> 산업 노트</title>
<style>
  :root {
    --bg: #ffffff; --fg: #1a1a1a; --muted: #6b6b6b; --border: #e2e2e2; --card: #f7f7f8; --accent: #2563eb;
    --tag1: #2563eb; --tag2: #7c3aed; --tage: #b45309; --tagu: #b91c1c;
    --tagbg1: #eaf0fe; --tagbg2: #f2eafe; --tagbge: #fdf1e2; --tagbgu: #fdeaea;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14161a; --fg: #e8e8ea; --muted: #9a9ba3; --border: #2c2f36; --card: #1b1e24; --accent: #7fa6ff;
      --tag1: #8fb2ff; --tag2: #c6a7ff; --tage: #f0b862; --tagu: #ff9b9b;
      --tagbg1: #1d2740; --tagbg2: #2a2140; --tagbge: #332714; --tagbgu: #3a1e1e;
    }
  }
  :root[data-theme="dark"] {
    --bg: #14161a; --fg: #e8e8ea; --muted: #9a9ba3; --border: #2c2f36; --card: #1b1e24; --accent: #7fa6ff;
    --tag1: #8fb2ff; --tag2: #c6a7ff; --tage: #f0b862; --tagu: #ff9b9b;
    --tagbg1: #1d2740; --tagbg2: #2a2140; --tagbge: #332714; --tagbgu: #3a1e1e;
  }
  :root[data-theme="light"] {
    --bg: #ffffff; --fg: #1a1a1a; --muted: #6b6b6b; --border: #e2e2e2; --card: #f7f7f8; --accent: #2563eb;
    --tag1: #2563eb; --tag2: #7c3aed; --tage: #b45309; --tagu: #b91c1c;
    --tagbg1: #eaf0fe; --tagbg2: #f2eafe; --tagbge: #fdf1e2; --tagbgu: #fdeaea;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg); color: var(--fg);
    font-family: -apple-system, "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
    line-height: 1.65; max-width: 980px; margin: 0 auto; padding: 2.5rem 1.5rem 5rem;
  }
  h1 { font-size: 1.7rem; margin-bottom: 0.3rem; }
  h2 { font-size: 1.15rem; margin-top: 2.4rem; padding-bottom: 0.4rem; border-bottom: 2px solid var(--border); }
  .meta { color: var(--muted); font-size: 0.9rem; margin-bottom: 0.2rem; }
  ul.overview { list-style: none; padding: 0; margin: 0; }
  ul.overview > li { padding: 0.7rem 0; border-bottom: 1px dashed var(--border); }
  ul.overview > li:last-child { border-bottom: none; }
  ul.overview > li > b { display: block; margin-bottom: 0.25rem; color: var(--accent); }
  .sub { margin: 0.3rem 0 0 0; padding-left: 1.1rem; color: var(--muted); font-size: 0.92rem; }
  .tag { display: inline-block; font-size: 0.75rem; font-weight: 600; padding: 0.05rem 0.45rem; border-radius: 999px; margin-left: 0.15rem; white-space: nowrap; }
  .tag-1 { color: var(--tag1); background: var(--tagbg1); }
  .tag-2 { color: var(--tag2); background: var(--tagbg2); }
  .tag-e { color: var(--tage); background: var(--tagbge); }
  .tag-u { color: var(--tagu); background: var(--tagbgu); }
  .table-scroll { overflow-x: auto; margin: 0.8rem 0; border: 1px solid var(--border); border-radius: 10px; }
  table { border-collapse: collapse; width: 100%; font-size: 0.88rem; min-width: 900px; }
  th, td { border-bottom: 1px solid var(--border); padding: 0.6rem 0.7rem; text-align: left; vertical-align: top; }
  th { background: var(--card); color: var(--muted); font-weight: 700; position: sticky; top: 0; }
  tr:last-child td { border-bottom: none; }
  .q { background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; }
  .q .qhead { font-weight: 700; margin-bottom: 0.35rem; }
  .q .falsify { color: var(--muted); font-size: 0.9rem; }
  .sources { columns: 1; font-size: 0.88rem; color: var(--muted); }
  .sources li { margin-bottom: 0.4rem; }
  .sources a { color: var(--accent); text-decoration: none; }
  .sources a:hover { text-decoration: underline; }
  .empty { color: var(--muted); font-style: italic; }
</style>
</head>
<body>

<h1><산업명> 산업 노트</h1>
<div class="meta">시장 기준: 국내/미국/글로벌 · 마지막 갱신: YYYY-MM-DD</div>

<h2>개요</h2>
<ul class="overview">
  <!-- 10항목을 <li><b>항목명</b> 내용 <span class="tag tag-1|tag-2|tag-e|tag-u">1차|2차|추정|unknown</span></li> 로. 밸류체인 항목엔 표를 .table-scroll > table 로 삽입 -->
</ul>

<h2>메커니즘 질문</h2>
<!-- 각 질문을 <div class="q"><div class="qhead">Q1. ... 축 뱃지</div><div class="falsify">반증 조건: ...</div></div> 로 -->

<h2>이슈 로그 (최신순)</h2>
<!-- 각 이슈를 <div class="q" style="border-left-color: var(--tag2)"><div class="qhead">YYYY-MM-DD — 요약 <span class="tag tag-2">당일성|단기|중단기|중장기</span></div><p>소스: <a href="...">...</a> 라벨</p><p>핵심 내용: ...</p><p class="falsify">개요/메커니즘 질문에 영향: ...</p></div> 로 -->

<h2>참고 출처</h2>
<ul class="sources">
  <!-- <li><a href="URL" target="_blank" rel="noopener">제목</a></li> 를 이슈 로그·개요에서 인용한 링크 전부 나열 -->
</ul>

</body>
</html>
```

갱신 모드에서는 `.html`을 처음부터 다시 쓰지 않고, `.md`에 반영한 변경분(새 이슈, 갱신된 개요 항목)만큼만 대응하는 `.html` 블록을 추가·수정한다.

### 7. 보고
신규 모드면 개요 10항목 + 메커니즘 질문을 요약해서 보여준다. 갱신 모드면 새로 추가된 이슈만 요약한다. `.html` 경로도 함께 알려준다. 특정 종목에 관심이 생기면 `/context-layer-builder`로 그 종목을 `context.md`에 등록하라고 안내한다 (다음 단계로 연결).

## 금지

- 라벨 없는 수치를 산출물에 쓰지 않는다.
- 매수·매도 추천, 목표가, 기대수익률을 생성하지 않는다.
- SNS·커뮤니티 등 라벨을 붙일 수 없는 소스는 쓰지 않는다.
- 확인 안 된 걸 지어내서 10항목을 억지로 다 채우지 않는다 — 안 되면 `unknown`.
