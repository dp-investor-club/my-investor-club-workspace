# macro-brief/config.md — 발표 일정 & API 상태

> 이 파일은 **소유자가 유지**한다. 스킬은 여기 적힌 것만 쓰고, 없으면 `unknown`으로 처리한다.
> **일정을 지어내지 않는다** — 틀린 날짜는 브리핑을 통째로 놓치게 만든다.

## 2026 FOMC 결정일 (Fed 공식 캘린더 `[1차]`)

출처: [Federal Reserve FOMC Calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) — 확인일 2026-07-23.
브리핑 트리거 = **결정일(이틀째)**. hook은 이 날짜와 오늘/어제를 비교한다.

| 회의 | 결정일 | SEP(점도표) | 상태 |
|---|---|---|---|
| 1월 | 2026-01-28 | | 지남 |
| 3월 | 2026-03-18 | ✅ | 지남 |
| 4월 | 2026-04-29 | | 지남 |
| 6월 | 2026-06-17 | ✅ | 지남 |
| 7월 | 2026-07-29 | | **브리핑 완료** → `macro/brief/2026-07-29-FOMC.md` |
| **9월** | **2026-09-16** | ✅ | 다음 |
| 10월 | 2026-10-28 | | |
| 12월 | 2026-12-09 | ✅ | |

> hook 스크립트(`hooks/session-start.sh`)의 `FOMC_DATES`와 이 표를 **일치**시킬 것.
> 2027 일정이 나오면 Fed 캘린더에서 확인해 `[1차]`로 갱신.

## 그 외 지표 발표일

| 날짜 | 지표 | 라벨 | 비고 |
|---|---|---|---|
| 2026-08-12 08:30 ET | CPI (7월분) | `[2차]` | 언론·계산기 사이트 인용. BLS 페이지에서 재확인 필요 |
| unknown | CPI (8월분 이후) | — | 아래 방법으로 채울 것 |
| unknown | 고용 (Employment Situation) | — | 아래 방법으로 채울 것 |
| unknown | PCE · GDP | — | 아래 방법으로 채울 것 |

### 채우는 방법 (1차 출처)

| 지표 | 출처 | 자동 조회 |
|---|---|---|
| FOMC | [Fed FOMC Calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | ✅ 가능 |
| CPI | [BLS CPI Schedule](https://www.bls.gov/schedule/news_release/cpi.htm) | ❌ **403 차단** |
| 고용 | [BLS Employment Situation Schedule](https://www.bls.gov/schedule/news_release/empsit.htm) | ❌ **403 차단** |
| PCE · GDP | [BEA Release Schedule](https://www.bea.gov/news/schedule) | 미확인 |
| 다수 일괄 | [FRED release dates API](https://fred.stlouisfed.org/docs/api/fred/release_dates.html) | ✅ 키 있으면 가능 |

> ⚠️ **BLS는 자동 조회를 차단한다** (`WebFetch` → HTTP 403, 확인일 2026-07-30).
> ISM PMI가 로그인벽 뒤라 `[1차]`가 불가능한 것과 같은 상황이다.
> BLS 일정은 (a) 소유자가 브라우저로 직접 열어 `[1차]`로 적거나, (b) FRED API로 받거나,
> (c) 언론 인용본을 `[2차]`로 적되 **반드시 라벨을 붙인다.** 셋 중 하나이지 추측이 아니다.

## API 상태

> 아래 "이 워크스페이스" 칸은 **이 레포 소유자의 상태**다. 스킬을 복사해 간 사람은 자기 상태로 다시 적을 것.

| 키 | 용도 | 발급(무료) | 이 워크스페이스 |
|---|---|---|---|
| `FRED_API_KEY` | 지표 자동 수집 (`scripts/fred_fetch.py`), 발표일 조회 | https://fredaccount.stlouisfed.org/ | 발급·검증 완료 (2026-07-23) |
| `FINNHUB_API_KEY` | (계획) 컨센서스 estimate | https://finnhub.io/ | 발급했으나 **economic calendar가 프리미엄 전용** → 무료로 불가 |

- 키는 `.env`에만 둔다 (이미 `.gitignore`). **절대 커밋 금지.**
- **키가 없어도 스킬은 동작한다** — 컨센서스는 WebSearch 폴백(`[추정]`), 일정은 이 파일의 표. 자동성과 정확도만 낮아진다.

## 자동화 로드맵

| 단계 | 발표 감지 | 컨센서스 |
|---|---|---|
| **지금 (MVP)** | hook의 정적 일정(위 표) | WebSearch → `[추정]`/`[2차]` |
| **Full (키 발급 후)** | FRED release dates API로 FOMC 외 지표까지 자동 | Finnhub 경제 캘린더 `estimate` — **단 현재 무료 플랜에선 막힘** |

> ⚠️ 진짜 애널리스트 서베이 컨센서스는 무료 API로 구할 수 없다. 질적 의견은 계속 WebSearch(`[2차]`)다.
> hook은 **API를 호출하지 않는다**(세션 시작을 느리게 만들지 않기 위해). 캘린더 조회는 브리핑이 돌 때 그 자리에서 한다.

## 확장

FOMC로 검증되면 CPI·고용으로 확장한다. 그때 이 config에 해당 지표의 발표일을 `[1차]`로 추가하고,
hook에서 `FOMC_DATES` 외에 그 지표 일정도 비교하도록 넓힌다.
