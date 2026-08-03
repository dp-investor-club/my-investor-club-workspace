"""research 보조 스크립트 — 야후 파이낸스 시세 조회.

강연 연사의 회사가 비상장일 때, 그 회사와 맞닿은 상장사의 시세를 사실 그대로 가져온다.
해석·전망·투자의견은 이 스크립트도, 이걸 쓰는 AI도 붙이지 않는다. 숫자와 날짜만.

사용:
    python quotes.py 329180.KS 009240.KS 030200.KS
    python quotes.py --json 329180.KS

티커 규칙: 코스피 `.KS`, 코스닥 `.KQ`, 미국은 접미사 없음.
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


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args:
        sys.exit(__doc__)

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
