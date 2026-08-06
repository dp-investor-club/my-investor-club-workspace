# .claude/skills/peer-skill/daily-market-report/scripts/kis_client.ps1
# 한국투자증권(KIS) Open API 클라이언트 — 코스피/코스닥 지수, 거래량 순위 조회.
# 실행: powershell -File .claude/skills/peer-skill/daily-market-report/scripts/kis_client.ps1 (저장소 어디서든 실행 가능 — 아래 Find-RepoRoot가 .git 위치로 루트를 찾는다)
# 저장소 루트의 .env에서 KIS_APP_KEY/KIS_APP_SECRET/KIS_ENV를 읽어 사용한다. 키 발급 방법은 SKILL.md의 "필요한 API 키" 참고.
# 값은 어떤 경우에도 stdout/로그에 echo하지 않는다 — 결과는 구조화 JSON 한 줄로만 출력한다.
#
# 주의: 토큰 발급 경로, tr_id 코드는 KIS 공식 문서 기준 통상값이며,
# 실제 사용 전 https://apiportal.koreainvestment.com 최신 문서로 재확인이 필요하다.

$ErrorActionPreference = 'Stop'

function Find-RepoRoot {
    param([string]$StartPath)
    $current = $StartPath
    while ($current) {
        if (Test-Path (Join-Path $current '.git')) { return $current }
        $parent = Split-Path -Parent $current
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }
    return $StartPath
}

# 이 스크립트가 저장소 안 어느 깊이(.claude/skills/... 등)에 있든 .git이 있는 폴더를 저장소 루트로 찾는다 —
# 폴더 구조가 옮겨져도(예: peer가 다른 위치에 설치) 깨지지 않게 하기 위함.
$repoRoot = Find-RepoRoot -StartPath $PSScriptRoot
$envPath = Join-Path $repoRoot '.env'
$cacheDir = Join-Path $PSScriptRoot '.cache'
$tokenCachePath = Join-Path $cacheDir 'kis_token.json'

function Read-DotEnv {
    param([string]$Path)
    $result = @{}
    if (-not (Test-Path $Path)) { return $result }
    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq '' -or $line.StartsWith('#')) { return }
        $idx = $line.IndexOf('=')
        if ($idx -lt 0) { return }
        $key = $line.Substring(0, $idx).Trim()
        $value = $line.Substring($idx + 1).Trim()
        $result[$key] = $value
    }
    return $result
}

function Write-JsonResult {
    param($Object)
    $Object | ConvertTo-Json -Depth 10 -Compress
}

$envVars = Read-DotEnv -Path $envPath
$appKey = $envVars['KIS_APP_KEY']
$appSecret = $envVars['KIS_APP_SECRET']
$kisEnv = if ($envVars['KIS_ENV']) { $envVars['KIS_ENV'] } else { 'real' }

if (-not $appKey -or -not $appSecret) {
    Write-JsonResult @{ status = 'error'; stage = 'config'; message = 'KIS_APP_KEY/KIS_APP_SECRET missing in .env' }
    exit 0
}

# real: 실전투자 도메인 / mock: 모의투자 도메인 — 정확한 도메인은 구현 시점에 재확인할 것
$baseUrl = if ($kisEnv -eq 'mock') { 'https://openapivts.koreainvestment.com:29443' } else { 'https://openapi.koreainvestment.com:9443' }

function Get-KisToken {
    if (-not (Test-Path $cacheDir)) {
        New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
    }
    if (Test-Path $tokenCachePath) {
        try {
            $cached = Get-Content $tokenCachePath -Raw | ConvertFrom-Json
            $expiresAt = [datetime]$cached.expires_at
            if ($expiresAt -gt (Get-Date).AddMinutes(10)) {
                return $cached.access_token
            }
        } catch {
            # 캐시 손상/파싱 실패 시 무시하고 재발급으로 진행
        }
    }

    $body = @{
        grant_type = 'client_credentials'
        appkey     = $appKey
        appsecret  = $appSecret
    } | ConvertTo-Json

    # 토큰 발급 엔드포인트 — POST /oauth2/tokenP 로 알려져 있음, 구현 시점에 재확인할 것
    $resp = Invoke-RestMethod -Uri "$baseUrl/oauth2/tokenP" -Method Post -ContentType 'application/json' -Body $body

    $expiresIn = if ($resp.expires_in) { [int]$resp.expires_in } else { 86400 }
    $expiresAt = (Get-Date).AddSeconds($expiresIn)
    @{
        access_token = $resp.access_token
        issued_at    = (Get-Date).ToString('o')
        expires_at   = $expiresAt.ToString('o')
    } | ConvertTo-Json | Set-Content -Path $tokenCachePath -Encoding utf8

    return $resp.access_token
}

function Invoke-KisApi {
    param(
        [string]$Token,
        [string]$Path,
        [string]$TrId,
        [hashtable]$Query
    )
    $headers = @{
        'authorization' = "Bearer $Token"
        'appkey'        = $appKey
        'appsecret'     = $appSecret
        'tr_id'         = $TrId
    }
    $qs = ($Query.GetEnumerator() | ForEach-Object { "$($_.Key)=$([uri]::EscapeDataString([string]$_.Value))" }) -join '&'
    $uri = "$baseUrl$Path`?$qs"

    # Invoke-RestMethod가 KIS 응답의 Content-Type에 charset이 없을 때 Latin-1로 잘못 디코딩해
    # 한글 종목명이 깨지는 문제(PS 5.1/.NET Framework 알려진 동작)가 있어, UTF-8로 강제 디코딩한다.
    $request = [System.Net.HttpWebRequest]::Create($uri)
    $request.Method = 'GET'
    foreach ($h in $headers.Keys) { $request.Headers.Add($h, $headers[$h]) }
    $response = $request.GetResponse()
    try {
        $stream = $response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
        $json = $reader.ReadToEnd()
    } finally {
        $response.Close()
    }
    return $json | ConvertFrom-Json
}

$result = [ordered]@{
    status     = 'ok'
    queried_at = (Get-Date).ToString('o')
    index      = [ordered]@{}
    volume     = [ordered]@{}
    sector     = [ordered]@{}
    errors     = @()
}

try {
    $token = Get-KisToken
} catch {
    Write-JsonResult @{ status = 'error'; stage = 'token'; message = $_.Exception.Message }
    exit 0
}

# 국내업종 현재지수 조회 (코스피=0001, 코스닥=1001)
# tr_id FHPUP02100000, FID_COND_MRKT_DIV_CODE=U 로 알려져 있음 — 구현 시점에 재확인할 것
foreach ($pair in @(
    @{ code = '0001'; name = 'KOSPI' },
    @{ code = '1001'; name = 'KOSDAQ' }
)) {
    try {
        $resp = Invoke-KisApi -Token $token -Path '/uapi/domestic-stock/v1/quotations/inquire-index-price' `
            -TrId 'FHPUP02100000' `
            -Query @{ FID_COND_MRKT_DIV_CODE = 'U'; FID_INPUT_ISCD = $pair.code }
        $result.index[$pair.name] = [ordered]@{
            close_price = $resp.output.bstp_nmix_prpr
            change_rate = $resp.output.bstp_nmix_prdy_ctrt
            volume      = $resp.output.acml_vol
            trade_value = $resp.output.acml_tr_pbmn
        }
    } catch {
        $result.errors += "index/$($pair.name): $($_.Exception.Message)"
    }
}

# 거래량 순위 (코스피+코스닥 전체 시장 기준 상위 종목)
# tr_id FHPST01710000 로 알려져 있음 — 파라미터/필드명 포함 구현 시점에 재확인할 것
try {
    $resp = Invoke-KisApi -Token $token -Path '/uapi/domestic-stock/v1/quotations/volume-rank' `
        -TrId 'FHPST01710000' `
        -Query @{
            FID_COND_MRKT_DIV_CODE = 'J'
            FID_COND_SCR_DIV_CODE  = '20171'
            FID_INPUT_ISCD         = '0000'
            FID_DIV_CLS_CODE       = '0'
            FID_BLNG_CLS_CODE      = '0'
            FID_TRGT_CLS_CODE      = '111111111'
            FID_TRGT_EXLS_CLS_CODE = '000000'
            FID_INPUT_PRICE_1      = ''
            FID_INPUT_PRICE_2      = ''
            FID_VOL_CNT            = ''
            FID_INPUT_DATE_1       = ''
        }
    $result.volume.top_by_volume = @($resp.output | Select-Object -First 20 | ForEach-Object {
        [ordered]@{ name = $_.hts_kor_isnm; code = $_.mksc_shrn_iscd; volume = $_.acml_vol }
    })
} catch {
    $result.errors += "volume: $($_.Exception.Message)"
}

# 업종별(섹터) 거래 동향 — 정확한 엔드포인트를 아직 확인하지 못해 구현하지 않았다.
# 구현 시점에 KIS 문서에서 확인 후 이 자리에 추가할 것.
$result.sector.status = 'unknown'
$result.sector.note = 'KIS 업종별 거래 동향 엔드포인트 미확인 — 다음 확인 시 연결'

if ($result.errors.Count -gt 0 -and $result.index.Count -eq 0) {
    $result.status = 'partial_error'
}

Write-JsonResult $result
