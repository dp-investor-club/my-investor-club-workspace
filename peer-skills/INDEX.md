# 동료 스킬 카탈로그 — Week 4 (28개)

Week 4에서 여러분이 만든 스킬이 전부 여기 모여 있습니다. **PR이 merge됐든 아직 열려 있든 상관없이, 여기 있으면 지금 바로 받아 쓸 수 있습니다.**

## 받는 법

Claude Code에서 딱 두 줄입니다.

```
/update
```
```
동료 스킬 중에 <폴더이름> 받아줘
```

받으면 `.claude/skills/<폴더이름>/`에 들어가고, `peer-` 접두어가 붙은 채로 유지돼서 **내 스킬과 섞이지 않습니다.**

## 고르는 법

내 스킬과 비슷한 걸 찾지 마세요. **내가 지금 막혀 있는 것**과 같은 병목을 푸는 것을 찾으세요. 아래 표는 각자가 SKILL.md에 직접 쓴 "어떤 병목" 문장 그대로입니다.

"준비 필요" 칸이 비어 있으면 받아서 바로 첫 실행이 됩니다. 뭔가 적혀 있으면 그것부터 있어야 켜집니다.

---

## 1. 처음 보는 산업·기업을 어디부터 볼지

| 폴더 | 만든 사람 | 이 스킬이 푸는 병목 | 첫 실행 | 준비 필요 |
|---|---|---|---|---|
| `peer-nicekimms1025-industry-map` | nicekimms1025 | 리서치를 봐도 다음에 무엇을 볼지가 안 정해지는 막막함 | `화장품 산업 정리해줘` | — |
| `peer-nicekimms1025-company-analysis` | nicekimms1025 | 위와 같은 병목을 회사 단위로 | `CJ올리브영 정리해줘` | — |
| `peer-jungjmjj0217-svg-industry-map` | jungjmjj0217-svg | 산업의 큰 그림(밸류체인)이 먼저 안 잡힌다 | `2차전지 산업 지도 그려줘` | — |
| `peer-yunnaa00-industry-sop` | yunnaa00 | 산업분석을 어떤 순서로 시작할지 확신이 안 선다 | `반도체 산업분석 어디서부터 시작해?` | — |
| `peer-pjueun11-industry-study` | pjueun11 | 새 산업이 궁금할 때 빠르게 스캔할 방법이 없다 | `/industry-study 드론` | — |
| `peer-juhok303-scope-topic` | juhok303 | 주제 범위와 질문을 정하지 않은 채 자료부터 모은다 | `scope-topic <주제>` | — |
| `peer-ChoSeongji-ic-report-builder` | ChoSeongji | 투자 심사 과정이 매번 처음부터다 | `스페이스린텍 투자 심사해줘` | — |
| `peer-Bearjsw-research` | Bearjsw | 조사해도 판단이 안 남아 다음번에 다시 시작한다 | `조사해줘, 셀바스AI 판단 모드로` | DART 키(`DART_KEY`) |
| `peer-thdqjatjr-주식리서치` | thdqjatjr | 상장사 리서치를 혼자 찾고 읽고 정리하는 데 수십시간 | `/주식리서치 <종목명>` | Obsidian vault · Windows 기준 경로 · PDF 직접 투입 |

## 2. 매일·매주 뭘 볼지 고정하기

| 폴더 | 만든 사람 | 이 스킬이 푸는 병목 | 첫 실행 | 준비 필요 |
|---|---|---|---|---|
| `peer-dusen120-ai-macro-check` | dusen120-ai | 수치만 쌓이고 글로 정리가 안 남는다 | `오늘 지표 보여줘` | — |
| `peer-marina0898-daily-briefing` | Marina0898 | 매일 지표·실적을 여기저기 찾아다니는 게 번거롭다 | `오늘 브리핑` | 수익률까지 보려면 `holdings.md` |
| `peer-MJN035-뉴스` | MJN035 | 매일 경제뉴스를 열 시간도, 뭘 볼지도 없다 | `/뉴스` | 브리핑 사이트 repo · Vercel |
| `peer-han-yunsu-dc-briefing` | yunsuhan0107 | 만든 스킬을 켜야 한다는 걸 까먹어서 안 쓴다 | `이번 주 데이터센터 뭐 있었어` | — |
| `peer-junha-pe-vc-daily` | junhajkim | 매일 PE/VC 뉴스를 직접 찾아 읽는 게 번거롭다 | `pe-vc-daily` | Obsidian vault 경로 |
| `peer-chaeminh-etf-weekly-news` | chaeminh | 관찰 ETF의 이번 주 핵심 뉴스가 흩어져 있다 | `이번 주 뉴스 정리해줘` | `context.md`에 관찰 ETF 등록 |
| `peer-minjae-weekly-scan` | Minjae-0319 | 어디까지 깊이 봐야 하는지 기준이 없다 | `주간 스캔 해줘` | — |
| `peer-mingso-03-market-scan` | mingso-03 | 관심 산업을 좁히기 전, 매번 다른 산업을 훑어야 한다 | `마켓 스캔` | — |
| `peer-pjueun11-market-map` | pjueun11 | 모의투자 26개 ETF의 이슈가 흩어져 있다 | `/market-map` | — |
| `peer-bananawooyou-invest-consensus-tracker` | bananawooyou-invest | 지난주 대비 컨센서스 비교 기록이 안 남는다 | `에이피알의 컨센서스를 트래킹해줘` | — |

## 3. 판단의 이유를 남기기

| 폴더 | 만든 사람 | 이 스킬이 푸는 병목 | 첫 실행 | 준비 필요 |
|---|---|---|---|---|
| `peer-nuheat0526-macro-brief` | nuheat0526 | 기록이 안 남는다 — 특히 **판단의 이유**가 안 남는다 | `시장 브리핑 해줘` | FRED 키(없으면 [추정]까지만) |
| `peer-jeongbin-park-macro-check` | binnie620-droid | 내 거시 판단이 맞았는지 확인하고 교정받을 길이 없다 | `이번 주 매크로 체크해줘` | FRED/ECOS 키 · Obsidian(없으면 `outputs/`로 대체됨) |
| `peer-mingso-03-check-in` | mingso-03 | 매주 내 방향이 어디로 움직였는지 안 남는다 | `체크인` | Notion(선택 — 없으면 건너뜀) |
| `peer-eunjaekim50-career-check` | eunjaekim50 | 강연을 들어도 커리어 방향이 좁혀지는지 모르겠다 | `/career-check` | — |
| `peer-dylancho-lecture-log` | dylancho | 매주 강연 내용이 구조 없이 흩어진다 | `강연 정리해줘` | 요약본 PDF를 다운로드 폴더에 |
| `peer-mingso-03-dreamplus-lecture` | mingso-03 | 강연 원문을 내 언어로 다시 쓰는 절차가 없다 | `드림플러스 강연 정리` | Notion 연동 |

## 4. 내 산출물을 밖으로 내보내기

| 폴더 | 만든 사람 | 이 스킬이 푸는 병목 | 첫 실행 | 준비 필요 |
|---|---|---|---|---|
| `peer-nicekimms1025-web-publish` | nicekimms1025 | 산출물이 파일로만 있어 남에게 공유가 안 된다 | `배포해줘` | Vercel 계정 |
| `peer-jihunx-collab-blog-write` | jihunx-collab | 사실 확인과 글로 풀어내는 게 빨리 안 된다 | `블로그 글 써줘` | Notion 연동 |
| `peer-dylancho-code-explain` | dylancho | AI가 짠 코드를 이해 못 해 뭘 고칠지 판단이 안 선다 | `이 코드 설명해줘` | — |

---

## 안 되면 그게 데이터입니다

받아서 첫 실행이 안 되면 **대신 고치지 마세요.** 어디서 막혔는지 한 줄로 정리해 만든 사람에게 주세요. 그게 Week 4의 진짜 결과물입니다 — 내가 만든 것이 나 없이 돌아가는지는 남이 켜봐야만 알 수 있습니다.

"준비 필요" 칸이 채워진 스킬들이 지금 그 상태입니다. 개인 컴퓨터 경로·개인 계정·개인 파일을 전제하고 있어서, 만든 사람 자리에서는 되지만 옆자리에서는 안 켜집니다. 고치는 건 만든 사람 몫입니다.
