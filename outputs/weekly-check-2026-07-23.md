# Weekly Check — 2026-07-23

## 거시·유동성 환경
(한국 기준금리는 크립토 판단에 직접 영향 없다고 판단해 이번 체크부터 제외 — context.md 결정 규칙 참고. 이번 체크부터 FRED API로 직접 조회 — 지난 체크 때 겪은 fred.stlouisfed.org 웹페이지 403 차단을 API 호출로 우회함)
- 주장: 연방기금금리 목표범위는 3.50%~3.75%(2026-07-22 기준, 6/17 FOMC 결정 유지), 실효금리(EFFR)는 3.63%(2026-07-21). 연준 대차대조표 총자산은 6.743조 달러(2026-07-15 주간치)로 양적긴축(QT) 기조 지속 중. 익일역레포(ON RRP) 잔고는 3.76억 달러(2026-07-22)로 사실상 바닥 수준 — RRP 시설이 더 이상 유동성 흡수 역할을 하지 않는다는 뜻. 광범위 명목 달러지수(DTWEXBGS)는 120.53(2026-07-17).
- 근거 (전부 FRED API, api.stlouisfed.org/fred/series/observations, 2026-07-23 조회):
  - 연방기금금리 목표범위 상단 3.75%/하단 3.50% (2026-07-22) [1차] — series DFEDTARU/DFEDTARL
  - 실효연방기금금리(EFFR) 3.63% (2026-07-21) [1차] — series EFFR
  - 연준 총자산(WALCL) 6,743,028백만 달러 = 약 6.743조 달러 (2026-07-15) [1차] — series WALCL
  - ON RRP 잔고(RRPONTSYD) 3.76억 달러 (2026-07-22) [1차] — series RRPONTSYD
  - 광범위 명목 달러지수(DTWEXBGS) 120.53 (2026-07-17) [1차] — series DTWEXBGS
- unknown:
  - 2026-07-28~29 FOMC 결과 — 확인 방법: 회의 이후 FRED series DFEDTARU/DFEDTARL 재조회
  - DTWEXBGS는 FRED 고유 지수(2006=100 기준, 현재 120대)로, 지난 체크에서 썼던 ICE DXY(1973=100 기준, 현재 100대)와 산출 방식·기준연도가 달라 서로 직접 비교 불가 — 두 지수를 같은 것으로 착각하지 않도록 주의
  - WALCL·RRPONTSYD의 전주 대비 변화량(추세) — 이번 체크는 최신 관측치 1건만 조회함. 확인 방법: FRED API에 `limit=4~8`로 여러 주 데이터 요청

## 거래량 — BTC·ETH·SOL + 스테이블코인

### BTC·ETH·SOL 24h 거래량 (CoinGecko API, 2026-07-23 조회)
- 주장: BTC 가격 65,563달러(24h -1.13%), 24h 거래대금 약 283.0억 달러, 시총 약 1.315조 달러. ETH 가격 1,918.55달러(24h -0.82%), 거래대금 약 96.6억 달러. SOL 가격 77.44달러(24h -0.68%), 거래대금 약 16.6억 달러. 크립토 전체 시총 약 2.322조 달러, 24h 전체 거래대금 약 653억 달러. 시총 기준 BTC 도미넌스 56.6%, ETH 10.0%.
- 근거: CoinGecko 공개 API(api.coingecko.com/api/v3) [1차] — `/simple/price`(BTC/ETH/SOL/USDT/USDC 가격·거래량·시총), `/global`(전체 시총·도미넌스), 2026-07-23 조회 시점 스냅샷
- unknown: 선물·파생 거래량 포함 여부(위 수치는 CoinGecko 집계 기준 spot 중심으로 추정 — 거래소별 spot/derivatives 구분은 확인 안 함). 확인 방법: CoinGecko `/derivatives` 엔드포인트 별도 조회

## 발행기관 공시·재무정보 (Circle / Tether / Binance 스테이블코인 거래량)

### Circle (NYSE: CRCL)
- 주장: Circle은 2026-05-11 발표한 2026년 1분기(2026-03-31 마감) 실적에서 총매출+준비금수익 6.94억 달러(YoY +20%), USDC 유통량 770억 달러(YoY +28%), 순이익 5,500만 달러(YoY -15%)를 보고함.
- 근거: Circle 공식 보도자료 [1차] — https://www.circle.com/pressroom/circle-reports-first-quarter-2026-results
- unknown: 2026년 2분기(6월 마감) 실적 — 아직 발표 전으로 보임. 확인 방법: circle.com/pressroom 또는 SEC EDGAR(CRCL) 10-Q 재확인

### Tether
- 주장: Tether International의 2026년 1분기(2026-03-31 기준) 준비금 증명(attestation)에서 총자산 1,917.7억 달러, 총부채 1,835.4억 달러, 초과준비금 82.3억 달러(사상 최고)로 순이익 10.4억 달러를 기록. 미 국채 익스포저 약 1,410억 달러, 금 약 200억 달러, 비트코인 약 70억 달러 보유.
- 근거: Tether 공식 발표 및 BDO(회계법인) 증명 보고서 [1차] — https://tether.io/news/tether-posts-1-04b-q1-2026-profit-despite-highly-volatile-global-markets-reaches-all-time-highs-8-23b-reserve-buffer-and-maintains-u-s-treasury-heavy-backing/ (2026-05-01 게시)
- unknown: 2026년 2분기 증명 보고서 — tether.io 뉴스 페이지에서 아직 확인 안 됨. 확인 방법: tether.io/news 또는 transparency 페이지 재확인. Tether는 SEC/DART 등 정식 감사가 아닌 분기 증명(attestation)만 발행한다는 점 — 완전한 감사(audit)와는 신뢰 수준이 다름.

### 스테이블코인 거래량 (Binance 중심, CoinGecko API 조회)
- 주장: USDT 시총 약 1,840.5억 달러(24h 거래대금 약 438.7억 달러), USDC 시총 약 731.9억 달러(24h 거래대금 약 102.2억 달러). Binance 개별 페어 기준 USDC/USDT가 24h 약 20.9억 달러로 최대 거래쌍, BTC/USDT 약 11.5억 달러, ETH/USDT 약 4.4억 달러, BTC/USDC 약 2.9억 달러, ETH/USDC 약 2.2억 달러, SOL/USDT 약 1.1억 달러 순. 업계 전반으로는 2026년 상반기 조정 스테이블코인 거래량이 8.82조 달러로 2024년 연간(5.8조 달러)을 이미 상회했고, USDC가 상반기 조정 거래량의 약 70%, USDT가 약 25%를 차지(2020년 USDT 90% vs USDC 10%였던 것과 역전).
- 근거:
  - USDT/USDC 시총·거래량, Binance 페어별 24h 거래대금 [1차] — CoinGecko 공개 API `/simple/price`, `/exchanges/binance/tickers` (api.coingecko.com/api/v3), 2026-07-23 조회
  - 스테이블코인 업계 전체 조정 거래량 및 USDC/USDT 점유율 역전 [2차] — CoinDesk, "Stablecoin trading volume is on track to smash records in 2026" (https://www.coindesk.com/business/2026/07/06/circle-s-usdc-is-leaving-tether-behind-in-the-stablecoin-volume-race), 지난 체크(7/20)에서 확인한 내용 유지
- unknown: Binance 거래소 자체가 공식 공시하는 스테이블코인별 거래량 통계(1차, 정기 발행물)가 있는지 — CoinGecko가 집계한 값으로 대체함. 확인 방법: Binance 공식 API(data-api.binance.vision) 직접 비교
