"""research 보조 스크립트 — 야후 파이낸스 시세·손익 조회.

강연 연사의 회사가 비상장일 때, 그 회사와 맞닿은 상장사의 시세를 사실 그대로 가져온다.
해석·전망·투자의견은 이 스크립트도, 이걸 쓰는 AI도 붙이지 않는다. 숫자와 날짜만.

사용:
    python quotes.py 329180.KS 009240.KS 030200.KS
    python quotes.py --json 329180.KS
    python quotes.py --fin 058970.KQ 108860.KQ      # 연간·분기 매출과 영업손익

티커 규칙: 코스피 `.KS`, 코스닥 `.KQ`, 미국은 접미사 없음.

재무 수치를 읽는 자리는 손익계산서(`income_stmt`) 하나다. `info`의 `operatingMargins`,
`totalRevenue`, `ebitda`는 읽지 않는다. 2026-07-31 확인 결과 그 필드로 계산한 영업손익이
연간으로도 최근 12개월로도 재현되지 않았다. 산출 기준은 unknown이다.
같은 날 손익계산서 쪽은 두 회사 2022~2025년 8개 값이 공시와 전부 일치했다.
"""

import sys
import json
import warnings

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance가 없다. `python -m pip install yfinance` 먼저.")


PERIODS = [("1개월", 21), ("3개월", 63), ("6개월", 126), ("1년", 252)]


def fetch(ticker):
    t = yf.Ticker(ticker)
    # 1년 변화까지 계산하려면 거래일이 252일 넘게 필요하다 → 2년치를 받는다
    hist = t.history(period="2y", auto_adjust=False)
    if hist.empty:
        return {"ticker": ticker, "error": "데이터 없음 — 티커 확인 필요"}

    close = hist["Close"].dropna()
    last = float(close.iloc[-1])
    asof = close.index[-1].strftime("%Y-%m-%d")
    window52 = close.iloc[-252:]  # 52주 고저는 최근 1년 구간에서만

    try:
        info = t.get_info()
    except Exception:
        info = {}

    row = {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName") or "unknown",
        "currency": info.get("currency") or "unknown",
        "last_close": round(last, 2),
        "as_of": asof,
        "52w_high": round(float(window52.max()), 2),
        "52w_low": round(float(window52.min()), 2),
        "changes": {},
    }

    for label, days in PERIODS:
        if len(close) > days:
            past = float(close.iloc[-1 - days])
            row["changes"][label] = round((last / past - 1) * 100, 1)
        else:
            row["changes"][label] = None  # 상장 기간이 짧아 계산 불가

    mcap = info.get("marketCap")
    row["market_cap"] = mcap if mcap else "unknown"
    return row


FIN_ROWS = [("매출", "Total Revenue"), ("영업손익", "Operating Income")]


def _scale(ticker):
    """원화 종목은 억 단위로 줄인다. 그 외는 원 숫자 그대로 둔다."""
    if ticker.upper().endswith((".KS", ".KQ")):
        return 1e8, "억"
    return 1.0, ""


def fetch_fin(ticker):
    """연간·분기 매출과 영업손익을 손익계산서에서 받는다.

    돌려주는 값은 회계기간 종료일 기준이다. 분기 값은 그 분기 한 개 몫이지
    누적이 아니다. 공시와 대조할 때 기간을 먼저 맞춘다.
    """
    t = yf.Ticker(ticker)
    div, unit = _scale(ticker)
    out = {"ticker": ticker, "unit": unit or "원", "annual": {}, "quarterly": {}}

    for bucket, attr in (("annual", "income_stmt"), ("quarterly", "quarterly_income_stmt")):
        try:
            stmt = getattr(t, attr)
        except Exception as e:
            out[bucket] = {"error": f"{attr} 조회 실패: {e}"}
            continue
        if stmt is None or stmt.empty:
            out[bucket] = {"error": "데이터 없음"}
            continue
        for label, row in FIN_ROWS:
            if row not in stmt.index:
                out[bucket][label] = {"error": f"'{row}' 항목 없음"}
                continue
            vals = {}
            for col, v in stmt.loc[row].items():
                # 야후는 값이 없는 기간을 NaN으로 채워 보낸다
                vals[col.strftime("%Y-%m-%d")] = None if v != v else round(float(v) / div, 1)
            out[bucket][label] = vals
    return out


def print_fin(r):
    print(f"[{r['ticker']}] 단위 {r['unit']}  (야후 손익계산서, 공시와 대조 필요)")
    for bucket, title in (("annual", "연간"), ("quarterly", "분기")):
        block = r[bucket]
        if "error" in block:
            print(f"  {title}: {block['error']}")
            continue
        print(f"  {title}")
        for label, vals in block.items():
            if isinstance(vals, dict) and "error" in vals:
                print(f"    {label}: {vals['error']}")
                continue
            cells = " / ".join(
                f"{k[:7]} {v:,.1f}" if v is not None else f"{k[:7]} unknown"
                for k, v in vals.items()
            )
            print(f"    {label:6} {cells}")
    print()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args:
        sys.exit(__doc__)

    if "--fin" in sys.argv:
        rows = [fetch_fin(t) for t in args]
        if as_json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
            return
        for r in rows:
            print_fin(r)
        return

    rows = [fetch(t) for t in args]

    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return

    for r in rows:
        if "error" in r:
            print(f"{r['ticker']}: {r['error']}")
            continue
        ch = " / ".join(
            f"{k} {v:+.1f}%" if v is not None else f"{k} unknown"
            for k, v in r["changes"].items()
        )
        print(f"[{r['ticker']}] {r['name']}")
        print(f"  종가 {r['last_close']:,} {r['currency']} ({r['as_of']} 기준)")
        print(f"  변화 {ch}")
        print(f"  52주 {r['52w_low']:,} ~ {r['52w_high']:,}")
        print()


if __name__ == "__main__":
    main()
