"""research 보조 스크립트 — DART 전자공시 원문 조회.

투자 메모의 1차 자료를 공시에서 직접 받는다. 해석·전망·투자의견은 이 스크립트도,
이걸 쓰는 AI도 붙이지 않는다. 공시에 적힌 수치와 날짜, 문구만 옮긴다.

인증키는 환경변수 DART_KEY로만 받는다. 코드나 레포 안 어느 파일에도 적지 않는다.
(작업실 절대 규칙: 크레덴셜 커밋 금지)

사용:
    set DART_KEY=...            # PowerShell은 $env:DART_KEY="..."
    python dart.py find 엠로                     # 회사명으로 corp_code 찾기
    python dart.py find --stock 058970           # 종목코드로 찾기
    python dart.py acnt 00396925 2025 11011      # 주요계정 (매출/영업이익/자산)
    python dart.py owner 00396925 2025           # 최대주주 현황
    python dart.py list 00396925 20260101 20261231   # 공시 목록
    python dart.py doc 20260515001878            # 공시 원문 텍스트
    python dart.py doc 20260515001878 --save q1.txt  # 파일로 저장 (큰 보고서용)

reprt_code: 11011 사업보고서 / 11012 반기 / 11013 1분기 / 11014 3분기

알아둘 것:
- 재무 API(fnlttSinglAcnt, fnlttSinglAcntAll)가 분기 데이터를 "013 데이타 없음"으로
  돌려줄 때가 있다. 그때도 분기보고서 원문(doc)에는 손익과 재무상태표가 들어 있다.
- 특수관계자 거래 주석에는 전분기 수치가 같이 실려 있어, 한 문서만으로 전년 동기
  비교가 된다.
- 사업보고서는 40만 자를 넘는다. --save로 떨군 뒤 필요한 절만 잘라 읽는다.
"""

import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

BASE = "https://opendart.fss.or.kr/api/"


def key():
    k = os.environ.get("DART_KEY")
    if not k:
        sys.exit("DART_KEY 환경변수가 없다. 인증키를 코드에 적지 말고 환경변수로 넘긴다.")
    return k


def raw(ep, **kw):
    kw["crtfc_key"] = key()
    url = BASE + ep + "?" + urllib.parse.urlencode(kw)
    with urllib.request.urlopen(url, timeout=90) as r:
        return r.read()


def get(ep, **kw):
    d = json.loads(raw(ep, **kw).decode("utf-8"))
    if d.get("status") not in ("000", None):
        print("[DART %s] %s" % (d.get("status"), d.get("message")), file=sys.stderr)
    return d


def eok(v):
    """원 단위 문자열을 억원으로."""
    try:
        return "%.1f억" % (int(str(v).replace(",", "")) / 1e8)
    except Exception:
        return str(v) if v else "-"


def cmd_find(args):
    """회사명 또는 종목코드로 corp_code를 찾는다."""
    by_stock = False
    if args and args[0] == "--stock":
        by_stock = True
        args = args[1:]
    if not args:
        sys.exit("찾을 회사명이나 종목코드를 달라.")
    q = args[0]

    z = zipfile.ZipFile(io.BytesIO(raw("corpCode.xml")))
    root = ET.fromstring(z.read(z.namelist()[0]).decode("utf-8"))
    hits = []
    for c in root.iter("list"):
        name = (c.findtext("corp_name") or "").strip()
        stock = (c.findtext("stock_code") or "").strip()
        if by_stock:
            if stock == q:
                hits.append((name, c.findtext("corp_code"), stock, c.findtext("modify_date")))
        elif q in name:
            hits.append((name, c.findtext("corp_code"), stock, c.findtext("modify_date")))

    # 상장사를 위로
    hits.sort(key=lambda h: (h[2] == "", h[0]))
    for n, cc, st, md in hits[:20]:
        print("%-28s corp_code=%s  종목=%s  갱신=%s" % (n[:28], cc, st or "비상장", md))
    if not hits:
        print("못 찾았다. 회사명 일부만 넣어보거나 --stock 로 종목코드를 쓴다.")


def cmd_acnt(args):
    """주요계정: 매출액, 영업이익, 당기순이익, 자산·부채·자본."""
    corp, year, rpt = args[0], args[1], (args[2] if len(args) > 2 else "11011")
    for div in ("CFS", "OFS"):
        d = get("fnlttSinglAcnt.json", corp_code=corp, bsns_year=year, reprt_code=rpt, fs_div=div)
        rows = [i for i in d.get("list", []) if i.get("fs_div") == div]
        if not rows:
            continue
        print("=== %s %s (%s)" % (year, rpt, "연결" if div == "CFS" else "별도"))
        want = ("매출액", "영업이익", "당기순이익", "자산총계", "부채총계", "자본총계")
        for it in rows:
            if it["account_nm"] in want:
                print("  %-8s 당기 %-10s 전기 %-10s 전전기 %s" % (
                    it["account_nm"], eok(it.get("thstrm_amount")),
                    eok(it.get("frmtrm_amount")), eok(it.get("bfefrmtrm_amount"))))
        return
    print("주요계정이 안 나온다. `doc`으로 보고서 원문에서 뽑는다.")


def cmd_owner(args):
    corp, year = args[0], (args[1] if len(args) > 1 else "2025")
    rpt = args[2] if len(args) > 2 else "11011"
    d = get("hyslrSttus.json", corp_code=corp, bsns_year=year, reprt_code=rpt)
    for it in d.get("list", []):
        print("  %-16s %-10s %14s주 (%s%%)" % (
            it.get("nm"), it.get("relate") or "", it.get("trmend_posesn_stock_co"),
            it.get("trmend_posesn_stock_qota_rt")))


def cmd_list(args):
    corp = args[0]
    bgn = args[1] if len(args) > 1 else "20240101"
    end = args[2] if len(args) > 2 else "20261231"
    d = get("list.json", corp_code=corp, bgn_de=bgn, end_de=end, page_count="100")
    print("총 %s건" % d.get("total_count"))
    for it in d.get("list", []):
        print("  %s  %-14s  %s" % (it["rcept_dt"], it["rcept_no"], it["report_nm"].strip()[:60]))


def cmd_doc(args):
    rcept = args[0]
    save = None
    if "--save" in args:
        save = args[args.index("--save") + 1]

    z = zipfile.ZipFile(io.BytesIO(raw("document.xml", rcept_no=rcept)))
    txt = ""
    for n in z.namelist():
        b = z.read(n)
        for enc in ("utf-8", "cp949", "euc-kr"):
            try:
                txt += b.decode(enc)
                break
            except Exception:
                continue
    t = re.sub(r"<[^>]+>", " ", txt)
    t = re.sub(r"&[a-zA-Z]+;", " ", t)
    t = re.sub(r"[ \t]+", " ", t)

    if save:
        with open(save, "w", encoding="utf-8") as f:
            f.write(t)
        print("%s자 저장: %s" % (len(t), save))
        print("찾을 만한 절 위치:")
        for kw in ("특수관계자", "주요 제품 및 서비스", "주식매수선택권", "재무상태표",
                   "요약재무정보", "직원 등의 현황", "배당에 관한 사항"):
            idx = [m.start() for m in re.finditer(kw, t)][:3]
            if idx:
                print("  %-16s %s" % (kw, idx))
    else:
        print(t[:4000])


CMDS = {"find": cmd_find, "acnt": cmd_acnt, "owner": cmd_owner, "list": cmd_list, "doc": cmd_doc}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
