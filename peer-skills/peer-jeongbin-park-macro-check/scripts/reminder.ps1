# macro-check 발표일 리마인더
# - 매주 고정 일정(신규실업수당청구=목요일, EIA 원유재고=수요일)
# - context.md "다음 소스 액션"의 `- [ ] YYYY-MM-DD: ...` 항목 중 예정일이 도래한 것
# 을 확인해 있으면 알림 창을 띄운다. 판단(6번)은 여전히 소유자가 macro-check를 직접 실행해서 남긴다 —
# 이 스크립트는 "오늘이 그 날"이라는 것만 알려준다.

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")
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
