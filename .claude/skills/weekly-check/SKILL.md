---
name: weekly-check
description: 매주 크립토(RWA·STO) 투자자로서 챙겨야 할 거시·금리 환경(한국은행 ECOS, FRED)과 발행기관 공시·재무정보(DART, 해외 유사 제도)를 확인해 outputs/weekly-check-YYYY-MM-DD.md로 남긴다. 투자 조언 없이 근거 기록·출처 라벨링만 한다. "체크해줘", "이번 주 체크", "weekly-check", "주간 점검" 요청에 사용.
---

# Weekly Check — 주간 정보 체크 루틴

크립토(RWA·STO) 투자자로서 매주 챙기기로 한 두 가지 정보 — 거시·금리 환경, 발행기관 공시·재무정보 — 를 확인하고 근거를 남기는 스킬이다. /clarify로 선명화한 스펙(2026-07-20)을 기반으로 만들었다.

## 사전 준비 (최초 1회, API 사용 시)

- **FRED API 키**: https://fred.stlouisfed.org/docs/api/api_key.html 에서 무료 가입 후 발급받아 워크스페이스 루트 `.env`에 `FRED_API_KEY=발급받은키` 형태로 저장한다. `.env`는 `.gitignore`에 이미 등록되어 커밋되지 않는다. 키가 없으면 이 단계는 건너뛰고 기존 WebFetch/WebSearch 방식으로 대체한다.
- **CoinGecko**: 공개 엔드포인트(`api.coingecko.com/api/v3`)는 키 없이 쓴다. 단, 전주 대비 비교(아래 2번)까지 하면 호출이 7~8회로 늘어 무료 키 없이는 429(레이트리밋)에 잘 걸린다 — 걸리면 호출 사이 10~15초씩 쉬었다 재시도하거나, 무료 Demo 키(https://www.coingecko.com/en/developers/dashboard)를 받아 `.env`의 `COINGECKO_API_KEY`로 저장해 안정화한다.

## 절차

### 1. 이번 주 확인 대상 확정
- `context.md`의 "지금 보고 있는 것" 표에 특정 발행사·대상이 있으면 그것을 공시 확인 대상으로 삼는다.
- 없으면 참가자에게 이번 주 주시할 발행사가 있는지 묻는다 (없다고 답하면 거시·유동성만 확인하고 넘어간다 — 대상을 지어내지 않는다).

### 2. 거시·유동성 환경 확인
- 한국은행 기준금리는 크립토 판단과 직접 관련이 없다고 보고 이 체크에서 제외한다 (`context.md` 결정 규칙, 2026-07-23).
- **FRED API**로 아래 시리즈를 조회한다 (`.env`의 `FRED_API_KEY` 사용). 웹페이지(fred.stlouisfed.org)는 봇 차단(403)에 자주 걸리므로 API를 우선한다.
  - `DFEDTARU`/`DFEDTARL` — 연방기금금리 목표범위 (또는 `EFFR` 실효금리)
  - `WALCL` — 연준 대차대조표 총자산
  - `RRPONTSYD` — 익일역레포(ON RRP) 잔고
  - `DTWEXBGS` — 광범위 명목 달러지수 (ICE의 DXY와는 다른 시리즈이므로 그렇게 명시한다)
  - 예: `curl -s "https://api.stlouisfed.org/fred/series/observations?series_id=WALCL&api_key=$FRED_API_KEY&file_type=json&sort_order=desc&limit=1"`
- **CoinGecko 공개 API**로 BTC·ETH·SOL·USDT·USDC의 가격·24h 거래량·시총을 조회한다.
  - 예: `curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,tether,usd-coin&vs_currencies=usd&include_24hr_vol=true&include_market_cap=true"`
  - 거래소별 스테이블코인 페어 비중이 필요하면 `/exchanges/binance/tickers`도 조회한다.
- **전주 대비 변동 (참가자에게 결과를 줄 때 항상 포함)**: 각 코인(BTC·ETH·SOL·USDT·USDC)마다 `/coins/{id}/market_chart?vs_currency=usd&days=8` 로 최근 8일 시계열을 받아, 지금 시점과 정확히 7일 전에 가장 가까운 지점을 비교한다.
  - 가격 변동률(%) = (현재가 - 7일 전 가격) / 7일 전 가격 × 100 — 소수점 둘째 자리까지
  - 거래량 변동률(%) = (현재 24h거래량 - 7일 전 24h거래량) / 7일 전 24h거래량 × 100
  - 스테이블코인은 가격 변동률이 항상 0에 가까우므로 참고용으로만 표기하고 거래량 변동에 더 무게를 둔다.
- API 응답으로 확인한 수치에는 `[1차]` 라벨을 붙인다. API 키가 없거나 호출이 실패하면 WebFetch/WebSearch로 대체하고, 그마저 안 되면 `unknown` + 확인 방법을 남긴다.

### 3. 발행기관 공시·재무정보 확인
- 1번에서 정한 대상이 있으면 DART(dart.fss.or.kr) 또는 해외 유사 공시 제도에서 최신 공시·재무정보를 찾는다.
- 1차 공시가 없으면 신뢰할 만한 뉴스·리서치로 보완하고 `[2차]` 라벨을 붙인다. 라벨을 붙일 수 없는 주장은 쓰지 않는다.

### 4. `outputs/weekly-check-YYYY-MM-DD.md` 작성
파일이 이미 있으면 덮어쓰기 전에 참가자에게 보여주고 확인받는다. 없으면 아래 틀로 새로 만든다:

```markdown
# Weekly Check — {날짜}

## 거시·유동성 환경
- 주장: ... (연준 정책금리, Fed 대차대조표·RRP, 달러지수 등)
- 근거: ... [1차]/[2차]/[추정]
- unknown: 확인 안 된 것과 확인 방법

## 거래량 — BTC·ETH·SOL + 스테이블코인
- 주장: ... (가격·24h거래량 + 전주 대비 가격 변동률%·거래량 변동률%)
- 근거: ... [1차]/[2차]/[추정]
- unknown: 확인 안 된 것과 확인 방법

## 발행기관 공시·재무정보 ({대상명} / 대상 없음)
- 주장: ...
- 근거: ... [1차]/[2차]/[추정]
- unknown: 확인 안 된 것과 확인 방법
```

### 5. 완료 후
`context.md`의 "소스 이력" 표에 이번에 확인한 소스를 한 줄씩 추가할지 참가자에게 물어본다 (강제하지 않는다). 원하면 `journey.md`의 "내가 지은 방들"에도 남긴다.

## 원칙

- **투자 조언 금지.** 확인한 수치·공시 내용을 그대로 기록할 뿐, 매수·매도·목표가·기대수익률을 생성하지 않는다.
- **라벨 없이는 쓰지 않는다.** 모든 수치·핵심 주장에 `[1차]`/`[2차]`/`[추정]` 라벨을 붙이고, 불가하면 `unknown` + 확인 방법.
- **크레덴셜 커밋 금지.** API key, 계좌 정보는 어떤 파일에도 남기지 않는다.
- **참가자 소유.** `outputs/`와 `context.md`는 참가자의 판단 자산이다 — 요약 문구는 참가자 확인을 거쳐 확정한다.
- **수동 호출.** 이 스킬은 자동 실행되지 않는다. 매주 자동 알림·실행이 필요해지면 `/schedule` 연계를 별도로 검토한다 (이번 스킬 범위 아님).
