# .trae 快速检查清单
# 使用方法: 在PowerShell中运行 .\.trae\tools\quick-checklist-fixed.ps1

Write-Host ".trae 开发状态快速检查" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 当前项目检查
$projectRoot = Get-Location
Write-Host "项目路径: $projectRoot" -ForegroundColor Cyan

# 检查清单
$checks = @(
    @{Name="需求文档"; Path="docs/requirements.md"; Icon="[+]"},
    @{Name="技术选型"; Path="docs/tech-choice.md"; Icon="[*]"},
    @{Name="系统设计"; Path="docs/architecture.md"; Icon="[@]"},
    @{Name="开发环境"; Path="package.json"; Icon="[#]"},
    @{Name="版本控制"; Path=".git"; Icon="[~]"}
)

$passed = 0
$total = $checks.Count

foreach ($check in $checks) {
    $path = Join-Path $projectRoot $check.Path
    $exists = Test-Path $path
    
    $status = if ($exists) { "[OK] 已就绪" } else { "[X] 待创建" }
    $color = if ($exists) { "Green" } else { "Red" }
    
    Write-Host "$($check.Icon) $($check.Name): $status" -ForegroundColor $color
    
    if ($exists) { $passed++ }
}

Write-Host "`n完成度: $passed/$total" -ForegroundColor Yellow

# 建议下一步
if ($passed -eq $total) {
    Write-Host "所有检查通过！可以开始开发" -ForegroundColor Green
} else {
    Write-Host "建议优先完成缺失项" -ForegroundColor Yellow
}