---
name: daily-market-report
description: 한국투자증권(KIS) Open API와 DART Open API를 실제로 호출해 오늘의 코스피/코스닥 지수·거래량·주요종목, 그리고 오늘 신규 접수된 기업공시 목록을 daily-market-report-log.md에 누적 기록한다. 참가자가 "일일 시장 리포트", "오늘 공시 확인", "daily-market-report" 라고 요청하거나, 매일 자동 실행되는 스케줄 트리거가 호출할 때 사용한다.
---

# daily-market-report — KIS·DART 실 API 기반 일일 리포트

이 스킬은 `market-watch-log.md`(WebSearch 기반, `[2차]`)와는 별개로, **실제 API 호출 결과([1차])**만 다룬다. 참가자가 수동으로 부르든 스케줄 트리거가 매일 자동으로 부르든 똑같이 아래 절차를 그대로 실행하는 단일 진입점이다.

이 워크스페이스의 `CLAUDE.md` 절대 규칙을 예외 없이 따른다:
1. 매수·매도·목표가·기대수익률을 생성하지 않는다.
2. 확인 불가한 수치는 `unknown`으로 남기고 확인 방법을 제안한다.
3. 모든 수치·핵심 주장에 `[1차]`/`[2차]`/`[추정]` 라벨을 붙인다. 라벨 불가면 쓰지 않는다.
4. `.env`, API 키, 계좌 정보를 절대 읽어서 출력하거나 커밋하지 않는다.

## 필요한 API 키

이 스킬은 두 개의 실 API를 부른다. 둘 다 무료로 발급되지만, 키가 없으면 해당 부분만 `unknown`으로 남고 나머지는 정상 동작한다 — 하나도 없어도 스킬 자체는 에러 없이 끝까지 실행되고 실패 사실만 로그에 남는다.

| API | 가입 | 키 발급 | 키 없으면 |
|---|---|---|---|
| 한국투자증권(KIS) Open API | [apiportal.koreainvestment.com](https://apiportal.koreainvestment.com) — KIS 증권 계좌(모의투자 계좌도 가능) 필요 | 로그인 후 "OpenAPI 신청" 메뉴에서 앱키(App Key)·앱시크릿(App Secret) 발급 | 코스피/코스닥 지수·거래량 상위 종목 파트가 `unknown`으로 남고, DART 공시 파트는 정상 동작 |
| DART(전자공시) Open API | [opendart.fss.or.kr](https://opendart.fss.or.kr) — 이메일만 있으면 가입 가능, 계좌 불필요 | 가입 후 "인증키 신청/관리" 메뉴에서 즉시 발급 | 신규 공시 파트가 `unknown`으로 남고, KIS 지수·거래량 파트는 정상 동작 |

발급받은 키는 저장소 루트(이 skill 폴더가 아니라 최상위)에 `.env` 파일을 만들어 아래처럼 채운다 (`.env`는 `.gitignore`에 포함돼 있어 커밋되지 않는다 — 절대 이 값 자체를 SKILL.md나 다른 파일에 옮겨 적지 않는다):

```
KIS_APP_KEY=
KIS_APP_SECRET=
KIS_ENV=real
DART_API_KEY=
```

## 절차

1. 오늘 날짜(Asia/Seoul 기준)를 확인한다. 주말·공휴일이라 데이터가 비어도 로그 자체는 남긴다 — 건너뛰지 않는다.
2. `scripts/kis_client.ps1`을 실행해 stdout의 JSON을 캡처한다 (`powershell -File .claude/skills/peer-skill/daily-market-report/scripts/kis_client.ps1`, 저장소 어디서든 실행 가능 — 스크립트가 `.git` 위치로 저장소 루트의 `.env`를 스스로 찾는다).
3. `scripts/dart_client.ps1`을 실행해 stdout의 JSON을 캡처한다 (`powershell -File .claude/skills/peer-skill/daily-market-report/scripts/dart_client.ps1`).
4. 두 JSON을 파싱한다. 어느 한쪽이 `status: "error"`거나 `status: "partial_error"`면 중단하지 않고, 어느 항목이 실패했는지를 5단계 로그의 "Unknowns"에 그대로 옮긴다. 스크립트가 원래 결과값에 `null`/누락으로 남긴 항목(예: KIS 업종별 섹터 데이터 — 아직 엔드포인트 미구현)도 `unknown`으로 옮긴다.
5. `daily-market-report-log.md`가 없으면 아래 헤더를 포함해 새로 만들고, 있으면 그 파일 맨 아래에 오늘 날짜 섹션을 append한다 (기존 내용 수정 금지):

   파일이 처음 만들어질 때 넣을 헤더:
   ```markdown
   # daily-market-report-log.md — KIS/DART 실 API 기반 일일 로그

   이 로그는 실제 KIS Open API·DART Open API 호출 결과([1차])를 담는다.
   WebSearch 기반의 market-watch-log.md([2차])와는 성격이 다른 파일이다 — 섞어서 보지 않는다.
   ```

   매일 append할 섹션 형식:
   ```markdown
   ## YYYY-MM-DD 조회 (daily-market-report skill)

   ### 코스피/코스닥 지수
   | 지수 | 종가 | 등락률 | 거래량 | 거래대금 | 라벨 | 출처 |
   |---|---|---|---|---|---|---|
   | KOSPI | ... | ... | ... | ... | [1차] | KIS Open API |
   | KOSDAQ | ... | ... | ... | ... | [1차] | KIS Open API |

   ### 거래량 상위 종목
   | 순위 | 종목명 | 종목코드 | 거래량 | 라벨 | 출처 |
   |---|---|---|---|---|---|

   ### 섹터별 거래 동향
   - unknown (KIS 업종별 거래 동향 엔드포인트 미구현 — scripts/kis_client.ps1의 sector 섹션 참고. 이 스킬 폴더 안 상대경로다)

   ### 신규/갱신 기업공시
   - 오늘 DART 신규 접수 공시: 총 N건 [1차] (출처: DART Open API)
   - 아래 표는 그중 `market-watch-log.md`의 관찰 대상 종목(코스피 시총 상위·watchlist 등록 종목)과 관련된 공시만 추린 것 — 전체 목록은 이 로그에 남기지 않는다(2026-07-30 참가자 결정: 건수 요약 + watchlist 대상 종목만 표로, 나머지는 필요시 DART 원본 재조회).

   | 기업명 | 공시제목 | 접수일시 | DART 링크 | 라벨 |
   |---|---|---|---|---|

   ### Unknowns
   - (예: KIS/DART 호출 실패 시 어느 항목이 실패했는지와 이유)

   ### 다음 확인 시점
   - 다음 거래일
   ```

   **공시 필터링 방법(2026-07-30부터 적용)**: DART 응답의 `filings` 전체를 표로 옮기지 않는다. `market-watch-log.md`에 기록된 코스피 시총 상위/watchlist 종목명 목록(현재: 삼성전자·SK하이닉스·SK스퀘어·삼성전자우·삼성전기·현대차·LG에너지솔루션·삼성생명·삼성바이오로직스·KB금융·한화에어로스페이스·두산에너빌리티·HD현대중공업)과 `corp_name`이 정확히 일치하는 건만 표에 남기고, 전체 건수는 요약 한 줄로만 기록한다. `market-watch-log.md`의 관찰 대상 종목이 갱신되면 이 목록도 그에 맞춰 갱신할 것.

6. 공시 항목은 "무엇이 접수됐다"는 사실만 기록한다 — 그 공시가 시장에 어떤 영향을 줄지, 왜 냈는지에 대한 해석·추론은 쓰지 않는다 (이 부분은 CLAUDE.md의 투자조언 금지 규칙과 맞닿아 있어, 기존 서브에이전트들의 "메커니즘 질문" 단계를 이 항목에는 적용하지 않는다).
7. append가 끝나면 호출한 쪽에 한 줄 요약을 돌려준다 (예: "2026-07-30 리포트 기록 완료 — 공시 12건, KOSPI [1차] 확인, 섹터 데이터는 unknown").

## 추가 데이터 소스 연계 — 텔레그램 검색 (2026-08-06)

KIS·DART 두 API만으로는 증권사 리포트(투자의견·목표주가·PDF 원문 추정실적)까지는 커버가 안 된다. 이 병목은 강지현님(peer-bananawooyou-invest)의 `peer-skills/peer-bananawooyou-invest-telegram-search/` 스킬로 보완한다 — 리포트가 올라오는 텔레그램 채널 여러 곳을 동시에 검색해 최신순으로 병합하고, 첨부 PDF 본문과 수출입 그래프 이미지까지 읽어 증권사별 투자의견·목표주가 비교표 + PDF 원문 추정실적 비교표를 `[1차]`/`[2차]`/`[추정]` 라벨과 함께 정리해준다 (설치 안내: https://telegram-search-guide.vercel.app).

- **이 스킬 절차 안에서 자동 호출하지 않는다.** 관심 종목의 증권사 리포트가 필요하면 별도로 "텔레그램에서 <종목명> 리포트 찾아줘"라고 호출한다.
- **선행 조건(미설치 상태)**: 이 워크스페이스 로컬 환경엔 Python이 없어 그 스킬의 `server/server.py`·`server/login.py`를 아직 설치하지 못했다. 설치하려면 Python 런타임 + `requirements.txt` 패키지 설치 + 본인 텔레그램 계정 로그인(1회) + 관심 채널 가입이 필요하다.
- 검색 대상은 본인 텔레그램 계정이 가입한 채널로 한정된다 — 미가입 채널은 결과에서 빠지고 그 스킬이 그 사실을 알린다.

## 추가 연계 — 회사 단위 리포트 심화 (2026-08-06)

이 스킬은 오늘의 지수·거래량·신규공시를 "무엇이 접수됐다"는 사실 수준으로만 기록하고 해석은 하지 않는다(위 6번 규칙). 신규공시나 거래량 상위 종목 중 더 깊이 볼 대상이 생기면, 정성원님(Bearjsw)의 `peer-skills/peer-Bearjsw-research/` 스킬로 넘긴다 — DART 공시 원문(`dart.py`)과 야후 파이낸스 시세(`quotes.py`, 손익계산서 `--fin` 기준)를 엮어 comps 표가 포함된 md+html 리포트를 만들어주는 회사 단위 조사 스킬이다.

- **이 스킬 절차 안에서 자동 호출하지 않는다.** daily-market-report는 로그 기록까지만 하고, 특정 종목을 더 볼지는 참가자가 판단한다. 필요하면 별도로 "조사해줘, <종목명> 판단 모드로"라고 호출한다.
- 세 모드(강연/판단/스캔) 중 이 워크스페이스의 관심 종목 추적과 가장 맞는 것은 판단 모드다 — `outputs/` + `context.md` 초안으로 남는다.
- 시세와 재무를 소스별로 분리해서 쓴다(시세는 야후로 교차 확인용, 재무 산출물은 DART 공시 값 우선) — PR에서 실제로 두 소스가 어긋난 사례(엠로·셀바스AI·안랩)를 검증한 뒤 정리된 규칙이다.

## 하지 않는 것

- 종목 추천, 목표가, "지금 사야 한다/팔아야 한다" 같은 표현을 쓰지 않는다.
- 공시나 시황 변화의 원인을 AI가 단정하지 않는다.
- API 키나 토큰 값을 응답이나 로그 파일에 절대 출력하지 않는다.
- 스크립트 실행이 실패해도 로그 항목 자체를 건너뛰지 않는다 — 실패 사실을 그대로 기록한다.
