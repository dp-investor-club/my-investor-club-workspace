#!/usr/bin/env bash
# macro-brief 세션 시작 감지
# 오늘/어제가 FOMC 결정일이고 아직 브리핑을 안 했으면, 세션 열 때 알림을 stdout으로 낸다.
# 감지·알림만 한다 — 실제 브리핑은 macro-brief 스킬이 수행한다. API 호출 없음(경량).
set -euo pipefail

# 이 스크립트: .claude/skills/macro-brief/hooks/session-start.sh → repo 루트는 4단계 위
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
BRIEF_DIR="$ROOT/macro/brief"

TODAY="$(date +%Y-%m-%d)"
# 어제(발표 다음날 아침에 열어도 잡히게). macOS(date -v) 우선, Linux(date -d) 폴백.
YDAY="$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d 2>/dev/null || echo '')"

# 2026 FOMC 결정일 = Fed 공식 캘린더 [1차], 이틀째. config.md 표와 일치시킬 것.
FOMC_DATES="2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28 2026-12-09"

hit=""
for d in $FOMC_DATES; do
  if [ "$d" = "$TODAY" ] || { [ -n "$YDAY" ] && [ "$d" = "$YDAY" ]; }; then
    hit="$d"
  fi
done

# FOMC 창이 아니면 조용히 종료
[ -z "$hit" ] && exit 0

# 이미 그 날짜 브리핑 파일이 있으면 조용히 종료 (중복 알림 방지)
if ls "$BRIEF_DIR/${hit}-FOMC"* >/dev/null 2>&1; then
  exit 0
fi

cat <<EOF
[macro-brief] ${hit} FOMC 금리 결정 발표가 있었습니다 — 아직 브리핑이 남아 있습니다.
"브리핑 열자" 또는 /macro-brief 라고 하시면, 시장 컨센서스를 먼저 보여드리지 않고
의견부터 여쭙는 blind 순서로 진행합니다.
(참고: 지금 "시장 브리핑 해줘"로 시황을 먼저 보시면 blind가 깨집니다.)
EOF
exit 0
