# market-map 소개 사이트 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** market-map 스킬을 클럽 동료에게 소개하고 실제 데모를 보여주는 정적 1페이지 사이트를 만들어 Vercel에 배포한다.

**Architecture:** 빌드 도구 없는 순수 정적 `index.html` 한 장(인라인 CSS 포함)을 새 별도 public 저장소에 두고, GitHub push 후 Vercel이 그대로 정적 서빙한다. 데모 콘텐츠는 실제 `outputs/market-notes/overview.md`의 이슈 로그 2건을 하드코딩한 스냅샷이다.

**Tech Stack:** 순수 HTML + CSS (프레임워크/빌드 도구 없음), git, GitHub CLI(`gh`), Vercel(MCP 도구 `mcp__plugin_vercel_vercel__deploy_to_vercel`로 배포).

## Global Constraints

- 사이트 코드는 `my-investor-club-workspace`와 **별도의 새 public 저장소**에 둔다 (workspace에는 `context.md`/`journey.md`/`club/` 등 개인 판단 기록이 섞여 있어 공개 불가).
- `index.html` 한 장, 빌드 도구 없음, 라이트/다크 모드(`prefers-color-scheme`) + 모바일 반응형 지원.
- 데모 섹션은 자산군 개요 표를 넣지 않는다 — 실제 이슈 로그 2건(사이드카 급락 + 급락 배경)만 하드코딩한다.
- "26종목 중 2종목 코드 불일치를 스스로 잡아냈다" 같은 내용은 어떤 섹션에도 넣지 않는다 (미해결 내부 이슈, [[project_ticker_code_mismatch]]).
- **GitHub repo 생성, GitHub push, Vercel 배포는 실행 직전 사용자에게 명시적으로 확인받는다** — 되돌리기 까다롭거나 외부에 노출되는 행동이므로 자동으로 진행하지 않는다.
- **설계 결정(spec 이후 확정)**: 데모 섹션의 "전체 결과물 링크"는 넣지 않는다. 실제 `overview.html` 전체를 공개하면 방금 제외하기로 한 코드 불일치 내용(원본 표에 포함되어 있음)이 그대로 노출되기 때문이다. 대신 데모 하단은 스냅샷 고지 + "설치법" 섹션으로 이어지는 CTA로 마무리한다.

---

### Task 1: 새 저장소 스캐폴딩

**Files:**
- Create: `C:\Users\eunt6\dev\market-map-showcase\README.md`
- Create: `C:\Users\eunt6\dev\market-map-showcase\.gitignore`

**Interfaces:**
- Produces: 이후 모든 태스크가 작업할 로컬 git 저장소 `C:\Users\eunt6\dev\market-map-showcase`

- [ ] **Step 1: 디렉터리 생성 및 git 초기화**

```bash
mkdir -p "/c/Users/eunt6/dev/market-map-showcase"
cd "/c/Users/eunt6/dev/market-map-showcase"
git init
```

- [ ] **Step 2: README 작성**

`C:\Users\eunt6\dev\market-map-showcase\README.md`:

```markdown
# market-map

모의투자 고정 유니버스(26개 ETF, 5개 자산군)를 대상으로 한 이슈 정리 스킬 — 소개 페이지.

이 저장소는 소개 페이지(`index.html`)와 스킬 파일(`market-map-SKILL.md`)만 담는다.
```

- [ ] **Step 3: .gitignore 작성**

`C:\Users\eunt6\dev\market-map-showcase\.gitignore`:

```
.DS_Store
```

- [ ] **Step 4: 확인 — git 상태**

Run: `git -C "/c/Users/eunt6/dev/market-map-showcase" status`
Expected: `README.md`, `.gitignore`가 untracked로 표시됨

- [ ] **Step 5: 커밋**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
git add README.md .gitignore
git commit -m "chore: init market-map-showcase repo"
```

---

### Task 2: index.html 본문 작성 (전체 섹션 + CSS)

**Files:**
- Create: `C:\Users\eunt6\dev\market-map-showcase\index.html`

**Interfaces:**
- Consumes: 없음 (신규 파일)
- Produces: 완결된 정적 페이지 `index.html` — Task 3의 SKILL.md 링크(`./market-map-SKILL.md`)가 이 파일 안에서 참조된다.

- [ ] **Step 1: index.html 작성**

`C:\Users\eunt6\dev\market-map-showcase\index.html`:

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>market-map — 모의투자 26종목 한눈에</title>
<style>
  :root {
    --bg: #ffffff;
    --fg: #1a1a1a;
    --muted: #6b6b6b;
    --border: #e2e2e2;
    --card: #f7f7f8;
    --accent: #2563eb;
    --tagbg: #f2eafe;
    --tagfg: #7c3aed;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14161a;
      --fg: #e8e8ea;
      --muted: #9a9ba3;
      --border: #2c2f36;
      --card: #1b1e24;
      --accent: #7fa6ff;
      --tagbg: #2a2140;
      --tagfg: #c6a7ff;
    }
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
    line-height: 1.7;
    max-width: 760px;
    margin: 0 auto;
    padding: 3rem 1.25rem 5rem;
  }
  h1 { font-size: 1.9rem; margin-bottom: .4rem; }
  h2 {
    font-size: 1.05rem;
    margin-top: 3rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .04em;
    font-weight: 600;
  }
  .sub { color: var(--muted); font-size: 1.05rem; margin-top: 0; }
  .hook {
    border-left: 3px solid var(--accent);
    padding-left: 1rem;
    margin: 2rem 0;
    font-size: 1.15rem;
  }
  ul.features { list-style: none; padding: 0; }
  ul.features li {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: .75rem;
  }
  .demo-grid {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr 1fr;
  }
  @media (max-width: 640px) {
    .demo-grid { grid-template-columns: 1fr; }
  }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
  }
  .card h3 { margin-top: 0; font-size: 1rem; }
  .tag {
    display: inline-block;
    font-size: .72rem;
    font-weight: 600;
    padding: .1rem .5rem;
    border-radius: 999px;
    background: var(--tagbg);
    color: var(--tagfg);
    margin-left: .4rem;
  }
  .card .meta { color: var(--muted); font-size: .85rem; margin: .4rem 0; }
  .note { color: var(--muted); font-size: .85rem; margin-top: 1rem; }
  a.btn {
    display: inline-block;
    margin-top: .5rem;
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
  }
  code { background: var(--card); padding: .15rem .4rem; border-radius: 4px; }
  ul.principles { color: var(--muted); font-size: .95rem; }
</style>
</head>
<body>

  <h1>market-map</h1>
  <p class="sub">국내주식·해외주식·채권·원자재·리츠 — 5개 자산군, 26개 ETF를 한 장으로.</p>

  <p class="hook">모의투자를 하고 있는데, 26개 종목을 한 번에 보고 싶다면?</p>

  <p>26종목을 ticker-review로 하나하나 공부했는데, 정작 어느 시장을 골라야 할지는 보이지 않았다. 흩어진 걸 한 번에 모아볼 데가 없었다.</p>

  <h2>이 스킬이 하는 일</h2>
  <ul class="features">
    <li>이번주 시장에서 있었던 주요 이슈를 자산군별로 정리해준다 (기사·뉴스 기반, 출처 라벨 포함)</li>
    <li>26종목이 각각 뭘 추종하는지, 패시브/액티브·환헤지 여부까지 표로 한눈에</li>
    <li>자산군 전체가 움직인 건지 개별 종목만의 이슈인지, 다른 자산군과 반대로 움직였는지까지 구분</li>
  </ul>

  <h2>실제 데모</h2>
  <div class="demo-grid">
    <div class="card">
      <h3>무슨 일이 있었나<span class="tag">2차</span></h3>
      <div class="meta">2026-07-29 · 국내 주식 자산군 전체</div>
      <p><strong>코스피·코스닥 동반 급락, 양대 시장 매도 사이드카 발동.</strong>
      코스피 -5.98%(5663.24), 코스닥 -6.12%(662.68)로 마감.
      7월 한 달간 코스피 -28.9%(1990년 이후 최대 월간 낙폭).</p>
      <p class="meta">다른 자산군과 반대로 움직였는지: 같은 날 일본 니케이225(+0.52%), 중국 CSI300(+0.67%)는 상승 — 국내 증시만 반대 방향.</p>
    </div>
    <div class="card">
      <h3>왜 그랬나<span class="tag">2차</span></h3>
      <div class="meta">2026-07-29 · 반도체 비중 종목 (삼성전자, SK하이닉스)</div>
      <p><strong>급락 배경: 반도체 피크아웃 우려 + 레버리지 반대매매 악순환.</strong>
      삼성전자·SK하이닉스 레버리지 ETF 반대매매 규모가 직전 41거래일 대비 약 77% 증가.</p>
      <p class="meta">담보가치 하락 → 강제매도 → 추가 하락의 악순환으로 지목됨.</p>
    </div>
  </div>
  <p class="note">위 두 항목은 2026-07-29 시점 실제 이슈 로그의 스냅샷이다. 실시간으로 갱신되지 않는다 — 직접 실행하면 내 계정 기준 최신 이슈가 쌓인다.</p>

  <h2>쓰는 법 / 설치</h2>
  <p><code>/market-map</code> 한 줄이면 된다. 처음 실행하면 26종목 개요부터, 이후엔 "오늘 왜 움직였는지" 이슈만 계속 쌓인다.</p>
  <p><a class="btn" href="./market-map-SKILL.md" target="_blank" rel="noopener">SKILL.md 받기 →</a></p>

  <h2>원칙</h2>
  <ul class="principles">
    <li>모든 수치·핵심 주장에 <code>[1차]</code>/<code>[2차]</code>/<code>[추정]</code> 라벨을 붙이고, 확인 안 되면 <code>unknown</code>으로 남긴다.</li>
    <li>매수·매도 추천, 목표가, 기대수익률, 배분 비율을 생성하지 않는다.</li>
  </ul>

</body>
</html>
```

- [ ] **Step 2: 필수 카피 존재 확인 (자동 검사)**

Run:
```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
for s in \
  "모의투자를 하고 있는데, 26개 종목을 한 번에 보고 싶다면?" \
  "26종목을 ticker-review로 하나하나 공부했는데" \
  "이번주 시장에서 있었던 주요 이슈를 자산군별로 정리해준다" \
  "패시브/액티브·환헤지 여부까지 표로 한눈에" \
  "다른 자산군과 반대로 움직였는지까지 구분" \
  "사이드카 발동" \
  "-5.98%" \
  "약 77% 증가" \
  "레버리지 반대매매" \
  "/market-map" \
  "배분 비율을 생성하지 않는다" \
  ; do
  grep -qF "$s" index.html && echo "OK: $s" || echo "MISSING: $s"
done
```
Expected: 모든 줄이 `OK:`로 출력됨. 하나라도 `MISSING:`이면 Step 1의 해당 텍스트를 다시 확인한다.

- [ ] **Step 3: 금지 문구 미포함 확인 (네거티브 검사)**

Run:
```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
grep -qF "코드 불일치" index.html && echo "FAIL: 코드 불일치 언급 발견" || echo "OK: 코드 불일치 미포함"
grep -qF "443250" index.html && echo "FAIL: 443250 발견" || echo "OK: 443250 미포함"
```
Expected: 둘 다 `OK:`

- [ ] **Step 4: 커밋**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
git add index.html
git commit -m "feat: add market-map showcase landing page"
```

---

### Task 3: SKILL.md 사본 추가 + 설치 링크 연결

**Files:**
- Create: `C:\Users\eunt6\dev\market-map-showcase\market-map-SKILL.md` (원본: `C:\Users\eunt6\dev\my-investor-club-workspace\.claude\skills\market-map\SKILL.md`)

**Interfaces:**
- Consumes: Task 2의 `index.html`에 있는 `href="./market-map-SKILL.md"` 링크
- Produces: 실제로 존재하는 `market-map-SKILL.md` 파일 — Task 4의 링크 유효성 검사가 이 파일을 확인한다.

- [ ] **Step 1: 원본 SKILL.md 그대로 복사**

```bash
cp "/c/Users/eunt6/dev/my-investor-club-workspace/.claude/skills/market-map/SKILL.md" \
   "/c/Users/eunt6/dev/market-map-showcase/market-map-SKILL.md"
```

- [ ] **Step 2: 복사 결과 확인**

Run:
```bash
diff "/c/Users/eunt6/dev/my-investor-club-workspace/.claude/skills/market-map/SKILL.md" \
     "/c/Users/eunt6/dev/market-map-showcase/market-map-SKILL.md"
```
Expected: 출력 없음 (완전히 동일)

- [ ] **Step 3: index.html의 링크가 실제 파일을 가리키는지 확인**

Run:
```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
href=$(grep -oE 'href="\./[^"]+"' index.html | grep SKILL | sed -E 's/href="\.\///; s/"$//')
test -f "$href" && echo "OK: $href 존재" || echo "FAIL: $href 없음"
```
Expected: `OK: market-map-SKILL.md 존재`

- [ ] **Step 4: 커밋**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
git add market-map-SKILL.md
git commit -m "docs: add market-map SKILL.md copy for install link"
```

---

### Task 4: 로컬 QA (라이트/다크/모바일/링크)

**Files:**
- 없음 (검증만 수행, 코드 변경 시 `index.html` 수정)

**Interfaces:**
- Consumes: Task 2의 `index.html`, Task 3의 `market-map-SKILL.md`
- Produces: 배포 전 통과된 로컬 페이지 (Task 5의 push 대상)

- [ ] **Step 1: 로컬 서버 기동**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
python -m http.server 8934 &
sleep 1
curl -sf -o /dev/null -w "%{http_code}\n" http://localhost:8934/index.html
```
Expected: `200`

- [ ] **Step 2: HTML 구조 기본 검증 (닫히지 않은 태그 등 gross error 검사)**

```bash
python3 - <<'EOF'
from html.parser import HTMLParser

class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag not in ("meta", "link", "br", "img", "input"):
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            raise SystemExit(f"MISMATCH at </{tag}>, stack={self.stack}")
        self.stack.pop()

with open("index.html", encoding="utf-8") as f:
    html = f.read()

c = Checker()
c.feed(html)
if c.stack:
    raise SystemExit(f"UNCLOSED TAGS: {c.stack}")
print("OK: 태그 균형 정상")
EOF
```
Expected: `OK: 태그 균형 정상`

- [ ] **Step 3: 브라우저로 수동 확인**

로컬에서 `http://localhost:8934/index.html`을 브라우저로 열어 다음을 확인한다 (claude-in-chrome 스킬을 쓰거나 사용자가 직접 확인):
- 라이트 모드 / 다크 모드(OS 설정 전환) 둘 다 텍스트 대비가 충분한가
- 브라우저 폭을 375px(모바일)로 줄였을 때 데모 카드 2개가 세로로 쌓이는가 (`.demo-grid`의 `@media (max-width: 640px)` 규칙 확인)
- "SKILL.md 받기" 링크 클릭 시 실제 파일이 열리는가

- [ ] **Step 4: 로컬 서버 종료**

```bash
kill %1 2>/dev/null || true
```

- [ ] **Step 5: 수정 사항이 있었다면 커밋**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
git add -A
git commit -m "fix: QA 과정에서 발견된 수정 반영" --allow-empty
```
(수정할 게 없었다면 이 커밋은 건너뛴다.)

---

### Task 5: GitHub 저장소 생성 + push (사용자 확인 필수)

**Files:** 없음 (원격 저장소 조작)

**Interfaces:**
- Consumes: Task 1~4에서 완성된 로컬 저장소 `C:\Users\eunt6\dev\market-map-showcase`
- Produces: 공개 GitHub 저장소 URL (Task 6의 Vercel 배포가 이 저장소를 참조)

- [ ] **Step 1: 사용자에게 확인받기**

다음을 사용자에게 그대로 확인받는다 — **승인 전에는 Step 2로 진행하지 않는다**:

> "`market-map-showcase`라는 이름으로 **public** GitHub 저장소를 새로 만들고 지금까지 커밋한 내용을 push하려 합니다. 진행해도 될까요? (저장소 이름을 바꾸고 싶으시면 알려주세요.)"

- [ ] **Step 2: (승인 후) GitHub 저장소 생성 및 push**

```bash
cd "/c/Users/eunt6/dev/market-map-showcase"
gh repo create market-map-showcase --public --source=. --remote=origin --push
```

- [ ] **Step 3: 생성 결과 확인**

```bash
gh repo view market-map-showcase --json url -q .url
```
Expected: 저장소 URL이 출력됨 (예: `https://github.com/<user>/market-map-showcase`)

---

### Task 6: Vercel 배포 (사용자 확인 필수)

**Files:** 없음 (배포만 수행)

**Interfaces:**
- Consumes: Task 5의 GitHub 저장소
- Produces: 공개 Vercel URL

- [ ] **Step 1: 사용자에게 확인받기**

다음을 사용자에게 그대로 확인받는다 — **승인 전에는 Step 2로 진행하지 않는다**:

> "이제 `market-map-showcase`를 Vercel에 실제로 배포해서 공개 URL을 만들려고 합니다. 진행해도 될까요?"

- [ ] **Step 2: (승인 후) `mcp__plugin_vercel_vercel__deploy_to_vercel` 도구로 배포**

`C:\Users\eunt6\dev\market-map-showcase`를 대상 디렉터리로 지정해 `mcp__plugin_vercel_vercel__deploy_to_vercel` MCP 도구를 호출한다 (프레임워크 없음 / 정적 사이트로 배포).

- [ ] **Step 3: 배포 확인**

배포 도구가 반환한 URL에 대해:
```bash
curl -sf -o /dev/null -w "%{http_code}\n" "<배포된 URL>"
```
Expected: `200`

- [ ] **Step 4: 사용자에게 최종 URL 전달**

배포된 공개 URL을 사용자에게 보여주고 세션을 마무리한다.

---

## Self-Review

**Spec coverage:**
- 저장소 분리 (별도 public repo) → Task 1, 5
- 정적 index.html 한 장, 빌드 도구 없음 → Task 2
- Hook/병목/기능3가지/원칙 카피 → Task 2 (Step 1) + Step 2의 grep 검증
- 데모 2건(사이드카 + 급락 배경), 표 미포함 → Task 2 Step 1 (표 요소 없음), Step 3 네거티브 검사
- 코드 불일치 사례 비공개 → Task 2 Step 3 네거티브 검사
- 쓰는 법/설치(SKILL.md) → Task 3
- 라이트/다크/반응형 QA → Task 4
- GitHub push, Vercel 배포 + 실행 직전 확인 → Task 5, 6

**Placeholder scan:** 각 태스크의 코드 블록은 실제 최종 콘텐츠이며 TBD/TODO 없음. 확인 완료.

**Type/name consistency:** `index.html`의 링크(`./market-map-SKILL.md`)와 Task 3에서 생성하는 파일명이 일치함. `.demo-grid`/`.card`/`.tag` 클래스명이 CSS 정의와 마크업에서 일치함. 확인 완료.
