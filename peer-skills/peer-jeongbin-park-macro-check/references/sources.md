# 지표별 소스 매핑

## 발표 일정 확인 — saveticker.com 캘린더 (2026-07-23 확인)

**용도: "언제 물어봐야 하는지"(일정)와 "컨센서스가 얼마인지"를 한 번에 빠르게 훑는 것.** 실제값의 최종 확정 라벨은 여전히 1차 소스(FRED/ECOS/EIA 등) 기준이다.

- URL: `https://www.saveticker.com/calendar`
- 우측 패널 중요도 필터에서 **★★★(3개)**를 누르면 시장에 영향 큰 지표만 남는다 — 확인해보니 macro-check 기본 지표 세트(CPI·근원CPI·PPI·근원PPI·PCE·근원PCE·GDP·실업률·비농업고용·신규실업수당청구·ISM 제조업/서비스업 PMI·기존/신규주택판매·EIA 원유재고·FOMC 의사록/기자회견/기준금리 결정)와 거의 그대로 겹친다.
- 한 줄에 **날짜/시간 + 예상치(컨센서스) + 실제값 + 이전값**이 같이 나온다 — 아직 발표 전인 지표는 예상치만, 발표 후엔 실제값까지 채워진다.
- JS 렌더링 페이지라 WebFetch로는 내용이 안 보인다(2026-07-23 확인) — **claude-in-chrome으로 열어서 확인**해야 한다.
- 이 사이트 값은 스크래핑 집계라 `[2차]`. 판단 로그에 쓰는 "실제값"은 여기서 먼저 스캔하되, 라벨을 붙일 땐 가능하면 FRED/BLS/BEA/ECOS 1차로 교차 확인한다. 컨센서스(예상치)는 investing.com/TradingEconomics와 마찬가지로 `[2차]`+스크래핑 신뢰도 캐비어트를 유지한다.

### 사용법 (macro-check 0번 단계에서)
1. `https://www.saveticker.com/calendar` 열고 ★★★ 필터 적용
2. **오늘 이전 ~ 지난 macro-check 이후** 구간에서 새로 실제값이 채워진 지표 = 오늘 판단 로그 대상 (SKILL.md 6번)
3. **앞으로 예정된 날짜** = 그 지표의 "다음 소스 액션" 사후 대조 예정일로 그대로 쓴다 (예: 다음 CPI는 캘린더에서 확인되는 다음 CPI 날짜)
4. 예상치(컨센서스) 칸은 SKILL.md 2번의 "구해지면 컨센서스" 부분을 여기서 바로 채울 수 있다 — investing.com 별도 조회가 필수가 아니게 된다.

각 지표를 가져올 때 이 표를 참고한다. **series ID는 반드시 FRED series 페이지 제목과 대조해 확인한 뒤 쓴다** — 이름만 보고 짐작해서 숫자를 붙이면 CLAUDE.md의 "근거 없는 수치 생성 금지"를 어기는 것이다. 확신이 없으면 값 대신 `unknown`으로 쓰고 확인 방법을 남긴다.

## FRED API로 확인 가능 (환경변수 FRED_API_KEY 필요)

| 지표 | series ID (확인 필요) | 비고 |
|---|---|---|
| 미 기준금리 (실효) | `FEDFUNDS` | 목표 상단/하단은 `DFEDTARU`/`DFEDTARL` |
| 미 CPI (전체) | `CPIAUCSL` | 전월비/전년비는 계산 필요 |
| 미 실업률 | `UNRATE` | |
| 미 실질GDP | `GDPC1` | 분기 데이터, 전기비 성장률은 계산 필요 |
| 신규 실업수당 청구건수 | `ICSA` | 주간 데이터 |
| PCE 물가지수 | `PCEPI` (헤드라인) / `PCEPILFE` (근원) | 연준이 가장 중시하는 물가지표 |
| PPI | `PPIACO` | 세부 품목별 ID는 다름 — 필요시 FRED 사이트에서 재검색 |
| 주택판매 | `EXHOSLUSM495S`(기존주택) / `HSN1F`(신규주택) | |

호출 예시 (PowerShell, 키는 세션 환경변수에서만):
```
curl "https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key=$env:FRED_API_KEY&file_type=json&sort_order=desc&limit=1"
```

## FRED에 없음 — 별도 소스 필요

| 지표 | 소스 | 상태 |
|---|---|---|
| ISM 제조업 PMI | ismworld.org 보도자료 (유료 라이선스 데이터라 FRED 미제공) | WebFetch로 헤드라인 수치만 확인, [2차]로 취급 |
| 원유재고 (EIA) | EIA Petroleum Status Report, `eia.gov` — 자체 API는 무료지만 별도 키 등록 필요 (`opendata.eia.gov`) | 키 미등록 상태 — 등록 전까지 WebFetch로 eia.gov 주간 보고서 페이지 직접 확인 |

## 한국 지표 — ECOS API (2026-07-23 키 발급, 코드 실제 호출로 검증 완료)

`https://www.bok.or.kr/...` 메인 페이지는 JS 렌더링이라 WebFetch로 안 통했지만(2026-07-17 확인, 2017년 캐시 데이터 반환), **ECOS는 별도 API 시스템이라 문제없이 통한다.**

| 지표 | 통계표코드 | 항목코드 | 주기 | 비고 |
|---|---|---|---|---|
| 기준금리 | `722Y001` | `0101000` | `M`(월) | 2026-07-23 실제 호출로 확인: "1.3.1. 한국은행 기준금리 및 여수신금리" 반환 |
| 소비자물가지수 (총지수) | `901Y009` | `0` | `M`(월) | 2026-07-23 실제 호출로 확인: 2020=100 기준 지수. YoY는 계산 필요 |

호출 URL 패턴:
```
https://ecos.bok.or.kr/api/StatisticSearch/{ECOS_API_KEY}/json/kr/{시작행}/{종료행}/{통계표코드}/{주기}/{시작YYYYMM}/{종료YYYYMM}/{항목코드}
```
예시: `.../json/kr/1/13/722Y001/M/202601/202607/0101000`

**주의 (2026-07-23 확인)**: 응답은 날짜 오름차순이다 — `시작행/종료행`을 작게 주면(예: `1/5`) **가장 과거 데이터**가 반환되고 최신값이 아니다. 최신값을 보려면 시작~종료 범위를 충분히 넓히고 응답 배열의 마지막 항목을 최신으로 읽거나, `list_total_count`를 먼저 확인해 종료행을 그 값 근처로 맞춘다. FRED처럼 `sort_order=desc` 파라미터가 따로 없으니 계속 조심할 것.

키는 세션 환경변수 `ECOS_API_KEY`로만 참조하고 이 레포 어떤 파일에도 값 자체를 적지 않는다 (FRED_API_KEY와 동일 규칙).

**대안(2차, ECOS 자체가 막힐 때만)**: WebSearch로 "한국은행 기준금리 {연월} 금융통화위원회"를 검색해 뉴스([2차])로 값·날짜를 확인하고, 가능하면 "통화정책방향 결정문"(한국은행 보도자료, [1차])을 찾아 교차 확인한다. 뉴스만으로 확정할 경우 반드시 `[2차]`로 라벨하고 "믿기 어려운 점"에 "공식 1차 문서 미대조"라고 남긴다.

## FOMC 성명문·의사록

**중요**: `federalreserve.gov/newsevents/pressreleases/monetary{날짜}a.htm` 링크는 안내문(landing page)만 있고 전문이 없다 (2026-07-17 실전 확인). 실제 전문은 별도 URL 패턴에 있다:
- 의사록 전문: `https://www.federalreserve.gov/monetarypolicy/fomcminutes{회의종료일 YYYYMMDD}.htm` (예: 2026년 6월 17일 종료 회의 → `fomcminutes20260617.htm`)
- PDF도 동일 패턴: `.../monetarypolicy/files/fomcminutes{YYYYMMDD}.pdf`
- 성명문(statement): `https://www.federalreserve.gov/newsevents/pressreleases/monetary{성명발표일 YYYYMMDD}a.htm` (이건 성명문 자체가 실려 있어 landing page 문제가 없음 — 의사록만 별도 페이지로 빠진다)
- 최신 목록: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

의사록 원문 소제목은 대체로 다음 순서다: Developments in Financial Markets and Open Market Operations → Staff Review of the Economic Situation → Staff Review of the Financial Situation → Staff Economic Outlook → Participants' Views → Committee Policy Actions → Voting.

WebFetch는 긴 문서를 자동 요약할 수 있다(툴 자체 한계). "전문 번역"을 원하면 한 번에 전체를 요청하지 말고 섹션별로 나눠 WebFetch를 여러 번 호출한다. 그래도 남는 결과가 요약 수준이라면 그 사실을 숨기지 말고 "WebFetch 요약 결과, 원문 대조 권장"이라고 표시한다 — 원문 그 자체를 옮기는 것이므로 [1차]로 라벨하되, 참가자의 해석이 섞이는 순간부터는 그 부분만 구분한다.

## 컨센서스(예상치) 대비 서프라이즈

FRED·ECOS는 실제 발표치만 준다. 컨센서스는 Investing.com·TradingEconomics 등 2차 소스에만 있고 스크래핑 신뢰도가 낮을 수 있다. 구해지면 `[2차]`로 라벨하고 "믿기 어려운 점"에 출처 한계를 적는다. 못 구하면 서프라이즈 칸은 `unknown`으로 두고 다음 확인에 "발표 당일 언론 속보로 컨센서스 확인" 같은 구체적 방법을 남긴다.

### 사전 컨센서스 종합 — 다중 소스 (SKILL.md 3번, 선택 사항)

판단 전에 컨센서스를 더 보고 싶을 때만, 한 소스가 아니라 최소 2개 이상 시도한다:
- Investing.com(경제캘린더), TradingEconomics — 위와 동일하게 스크래핑 신뢰도 낮음, 매번 `[2차]`
- 한국 증권사 리서치 자체 API·데이터 접근: **unknown** — 2026-07-23 세션 기준 검증된 접근 경로 없음(신한투자증권 API 조사 결과 확인 안 됨). 접근 가능한 경로가 확인되면 이 표에 추가한다.
- **CME FedWatch Tool** (`cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html`) — 연방기금선물 가격에서 역산한 FOMC 회의별 금리 확률. 시장가격에서 직접 산출되므로 `[1차]`로 취급. 이 지표가 CPI 등 새 지표 발표로 얼마나 바뀌었는지 보려면 "Historical" 패널에서 발표 직전 스냅샷(1일/1주/1개월 전)을 조회한다 — **발표 30분 전에 실시간으로 미리 캡처해둘 필요 없이, 판단 시점(사후)에 언제든 되돌아 조회 가능**하다는 뜻. 판단(SKILL.md 6번) 때 "그 발표 직전 확률이 뭐였는지"를 이 Historical 뷰로 같이 가져와 보여준다.

여러 소스가 다르면 평균과 범위만 계산해 보여준다 — "어느 쪽이 맞다"는 AI가 판단하지 않는다. FedWatch 확률은 평균 대상이 아니라 그 자체로 하나의 참고 수치로 나란히 보여준다. 표 형식은 macro-check SKILL.md 7번(Obsidian 템플릿) "컨센서스 종합" 표 참고. 이 단계는 어디까지나 선택 사항이며, 켜지 않아도 판단(6번)은 정상 진행한다.
