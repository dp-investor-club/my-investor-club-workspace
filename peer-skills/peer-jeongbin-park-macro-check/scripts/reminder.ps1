# macro-check 발표일 리마인더
# - 매주 고정 일정(신규실업수당청구=목요일, EIA 원유재고=수요일)
# - context.md "다음 소스 액션"의 `- [ ] YYYY-MM-DD: ...` 항목 중 예정일이 도래한 것
# 을 확인해 있으면 알림 창을 띄운다. 판단(6번)은 여전히 소유자가 macro-check를 직접 실행해서 남긴다 —
# 이 스크립트는 "오늘이 그 날"이라는 것만 알려준다.

# 레포 루트를 고정 상대경로(../../../..)로 찾지 않는다 — 이 파일이 어느 폴더 깊이에
# 놓이는지는 받는 사람의 레포 구조에 따라 달라진다(예: peer-skills/<이름>/scripts/는
# .claude/skills/<이름>/scripts/보다 한 단계 얕다). git 레포 최상단을 직접 물어보고,
# git이 없으면 context.md가 나올 때까지 상위 폴더를 올라가며 찾는다.
function Find-RepoRoot {
    param([string]$StartPath)
    try {
        $gitRoot = & git -C $StartPath rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $gitRoot) { return $gitRoot.Trim() }
    } catch {}
    $dir = Get-Item $StartPath
    for ($i = 0; $i -lt 8; $i++) {
        if (Test-Path (Join-Path $dir.FullName "context.md")) { return $dir.FullName }
        if ($null -eq $dir.Parent) { break }
        $dir = $dir.Parent
    }
    return $StartPath
}

$repoRoot = Find-RepoRoot -StartPath $PSScriptRoot
$contextFile = Join-Path $repoRoot "context.md"
$today = Get-Date
$todayStr = $today.ToString("yyyy-MM-dd")
$messages = New-Object System.Collections.Generic.List[string]

switch ($today.DayOfWeek) {
    "Wednesday" { $messages.Add("오늘은 EIA 원유재고 발표일입니다 (매주 수요일).") }
    "Thursday"  { $messages.Add("오늘은 신규실업수당청구건수 발표일입니다 (매주 목요일).") }
}

if (Test-Path $contextFile) {
    $lines = Get-Content $contextFile -Encoding UTF8
    foreach ($line in $lines) {
        if ($line -match '^\s*-\s*\[\s*\]\s*(\d{4}-\d{2}-\d{2}):\s*(.+)$') {
            $dueDate = [datetime]::ParseExact($matches[1], "yyyy-MM-dd", $null)
            if ($dueDate.Date -le $today.Date) {
                $messages.Add("예정일 도래 ($($matches[1])): $($matches[2])")
            }
        }
    }
}

if ($messages.Count -gt 0) {
    Add-Type -AssemblyName System.Windows.Forms
    $body = ($messages -join "`r`n`r`n") + "`r`n`r`nClaude Code에서 `"매크로 체크`"를 실행하세요."
    [System.Windows.Forms.MessageBox]::Show($body, "macro-check 리마인더 ($todayStr)", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
}
