# .claude/skills/peer-skill/daily-market-report/scripts/dart_client.ps1
# DART(전자공시) Open API 클라이언트 — 오늘 날짜로 필터한 공시 목록 조회.
# 실행: powershell -File .claude/skills/peer-skill/daily-market-report/scripts/dart_client.ps1 (저장소 어디서든 실행 가능 — 아래 Find-RepoRoot가 .git 위치로 루트를 찾는다)
# 저장소 루트의 .env에서 DART_API_KEY를 읽어 사용한다. 키 발급 방법은 SKILL.md의 "필요한 API 키" 참고.
# 값은 어떤 경우에도 stdout/로그에 echo하지 않는다 — 결과는 구조화 JSON 한 줄로만 출력한다.
#
# 주의: 공시검색(list.json) 엔드포인트의 파라미터명/응답 필드명은 opendart.fss.or.kr
# 공식 문서 기준 통상값이며, 실제 사용 전 최신 문서로 재확인이 필요하다.

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

$repoRoot = Find-RepoRoot -StartPath $PSScriptRoot
$envPath = Join-Path $repoRoot '.env'

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
$apiKey = $envVars['DART_API_KEY']

if (-not $apiKey) {
    Write-JsonResult @{ status = 'error'; stage = 'config'; message = 'DART_API_KEY missing in .env' }
    exit 0
}

$today = Get-Date -Format 'yyyyMMdd'
$baseUrl = 'https://opendart.fss.or.kr/api/list.json'

$allFilings = New-Object System.Collections.Generic.List[object]
$pageNo = 1
$pageCount = 100
$totalPage = 1
$errorMessage = $null

try {
    do {
        $uri = "$baseUrl`?crtfc_key=$apiKey&bgn_de=$today&end_de=$today&page_no=$pageNo&page_count=$pageCount"
        $resp = Invoke-RestMethod -Uri $uri -Method Get

        if ($resp.status -ne '000') {
            if ($resp.status -eq '013') {
                # 013: 조회된 데이터가 없습니다 — 오늘 신규 공시가 없는 정상 상태
                break
            }
            throw "DART API status $($resp.status): $($resp.message)"
        }

        if ($resp.list) {
            foreach ($item in @($resp.list)) { $allFilings.Add($item) }
        }
        $totalPage = if ($resp.total_page) { [int]$resp.total_page } else { 1 }
        $pageNo++
    } while ($pageNo -le $totalPage)
} catch {
    $errorMessage = $_.Exception.Message
}

if ($errorMessage) {
    Write-JsonResult @{
        status          = 'error'
        stage           = 'fetch'
        message         = $errorMessage
        partial_filings = $allFilings.Count
    }
    exit 0
}

$filings = @($allFilings | ForEach-Object {
    [ordered]@{
        corp_name = $_.corp_name
        report_nm = $_.report_nm
        rcept_no  = $_.rcept_no
        rcept_dt  = $_.rcept_dt
        flr_nm    = $_.flr_nm
        dart_url  = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=$($_.rcept_no)"
    }
})

Write-JsonResult @{
    status      = 'ok'
    queried_at  = (Get-Date).ToString('o')
    date        = $today
    total_count = $filings.Count
    filings     = $filings
}
