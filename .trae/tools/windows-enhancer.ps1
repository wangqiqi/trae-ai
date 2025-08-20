# 🎯 Windows 深度优化工具
# 专为Windows系统优化的实用功能

# Windows注册表优化
function Optimize-WindowsRegistry {
    Write-Host "🔧 优化Windows注册表..." -ForegroundColor Green
    
    # PowerShell执行策略优化
    $currentPolicy = Get-ExecutionPolicy
    if ($currentPolicy -eq "Restricted") {
        Write-Host "⚡ 优化PowerShell执行策略..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✅ 执行策略已优化" -ForegroundColor Green
    }
}

# Windows终端美化
function Set-WindowsTerminalProfile {
    Write-Host "🎨 配置Windows终端美化..." -ForegroundColor Green
    
    # 设置PowerShell提示符
    $profilePath = $PROFILE
    if (!(Test-Path $profilePath)) {
        New-Item -ItemType File -Path $profilePath -Force
    }
    
    $terminalConfig = @'
# 🎯 .trae PowerShell优化配置
function prompt {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal] $identity
    $adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator
    
    $isAdmin = if ($principal.IsInRole($adminRole)) { "🔴" } else { "🟢" }
    $path = Get-Location
    $time = Get-Date -Format "HH:mm:ss"
    
    Write-Host "`n$isAdmin" -NoNewline -ForegroundColor Green
    Write-Host " [$time]" -NoNewline -ForegroundColor Cyan
    Write-Host " $path" -ForegroundColor Yellow
    Write-Host "❯ " -NoNewline -ForegroundColor Green
    return " "
}

# 🚀 .trae 快捷命令
function traecheck { . .\.trae\tools\quick-checklist-fixed.ps1 }
function traehelp { Get-Content .\.trae\tools\principles-cheat-sheet.md }
function traecleanup { python .\.trae\tools\smart-cleanup.py }
'@
    
    Add-Content -Path $profilePath -Value $terminalConfig
    Write-Host "✅ 终端配置已优化" -ForegroundColor Green
}

# Windows路径优化
function Optimize-WindowsPath {
    Write-Host "📁 优化Windows路径处理..." -ForegroundColor Green
    
    # 创建trae快捷路径
    $traePath = Join-Path $PWD.Path ".trae"
    $env:PATH = "$env:PATH;$traePath\tools"
    
    Write-Host "✅ 路径环境已优化" -ForegroundColor Green
}

# Windows性能监控
function Show-SystemPerformance {
    Write-Host "📊 系统性能监控..." -ForegroundColor Green
    
    $cpu = Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty LoadPercentage
    $memory = Get-CimInstance -ClassName Win32_OperatingSystem
    $totalMemory = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
    $freeMemory = [math]::Round($memory.FreePhysicalMemory / 1MB, 2)
    $usedMemory = $totalMemory - $freeMemory
    
    Write-Host "CPU使用率: $cpu%" -ForegroundColor $(if ($cpu -gt 80) { "Red" } else { "Green" })
    Write-Host "内存使用: $usedMemory GB / $totalMemory GB" -ForegroundColor Cyan
}

# Windows特定命令优化
function Get-WindowsSpecificCommands {
    Write-Host "🔍 Windows特定优化命令:" -ForegroundColor Green
    
    $commands = @{
        "traecheck" = "运行项目状态检查"
        "traehelp" = "查看原则速查表"
        "traecleanup" = "运行智能清理"
        "Show-SystemPerformance" = "显示系统性能"
    }
    
    foreach ($cmd in $commands.GetEnumerator()) {
        Write-Host "  $($cmd.Key): $($cmd.Value)" -ForegroundColor Yellow
    }
}

# 🚀 主优化流程
function Start-WindowsOptimization {
    Write-Host "🎯 .trae Windows深度优化启动!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    
    Optimize-WindowsRegistry
    Set-WindowsTerminalProfile
    Optimize-WindowsPath
    Show-SystemPerformance
    Get-WindowsSpecificCommands
    
    Write-Host "`n✅ Windows深度优化完成!" -ForegroundColor Green
    Write-Host "💡 重启PowerShell后生效" -ForegroundColor Yellow
}

# 执行优化
Start-WindowsOptimization