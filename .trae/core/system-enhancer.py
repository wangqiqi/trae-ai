#!/usr/bin/env python3
# 🎯 系统增强器 - 合并版
# 统一的系统优化和性能监控工具
# 替代: performance-monitor.py + universal-system-enhancer.py

import os
import sys
import platform
import subprocess
import json
import psutil
from pathlib import Path
from datetime import datetime

class SystemEnhancer:
    """
    系统增强器
    职责：系统级优化、性能监控、环境管理
    边界：不涉及项目业务逻辑
    """
    
    def __init__(self):
        self.system = platform.system()
        self.python_version = platform.python_version()
        self.is_admin = self._check_admin()
        
    def _check_admin(self):
        """检查是否具有管理员/超级用户权限"""
        try:
            if self.system == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def get_system_info(self):
        """获取跨平台系统信息"""
        info = {
            "system": self.system,
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": self.python_version,
            "is_admin": self.is_admin,
            "hostname": platform.node()
        }
        
        # 平台特定信息
        if self.system == "Windows":
            try:
                import winreg
                info.update({
                    "platform": "Windows",
                    "win_version": sys.getwindowsversion().major
                })
            except:
                pass
        elif self.system == "Linux":
            try:
                with open("/etc/os-release") as f:
                    os_info = {}
                    for line in f:
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            os_info[key] = value.strip('"')
                    info.update({
                        "distro": os_info.get("NAME", "Unknown"),
                        "distro_version": os_info.get("VERSION_ID", "Unknown")
                    })
            except:
                pass
        elif self.system == "Darwin":
            info.update({
                "platform": "macOS",
                "mac_version": platform.mac_ver()[0]
            })
        
        return info
    
    def collect_performance_metrics(self):
        """收集详细性能指标"""
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # 内存使用
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        
        # 磁盘使用
        disk = psutil.disk_usage('.')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        
        # 系统启动时间
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        
        # 网络接口
        network_stats = psutil.net_io_counters()
        
        return {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'frequency': psutil.cpu_freq()._asdict() if hasattr(psutil.cpu_freq(), '_asdict') else None,
                'status': 'optimal' if cpu_percent < 70 else 'warning' if cpu_percent < 90 else 'critical'
            },
            'memory': {
                'percent': memory_percent,
                'used_gb': round(memory_used_gb, 2),
                'total_gb': round(memory_total_gb, 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'status': 'optimal' if memory_percent < 70 else 'warning' if memory_percent < 90 else 'critical'
            },
            'disk': {
                'percent': disk_percent,
                'used_gb': round(disk_used_gb, 2),
                'total_gb': round(disk_total_gb, 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'status': 'optimal' if disk_percent < 80 else 'warning' if disk_percent < 95 else 'critical'
            },
            'network': {
                'bytes_sent': network_stats.bytes_sent,
                'bytes_recv': network_stats.bytes_recv,
                'packets_sent': network_stats.packets_sent,
                'packets_recv': network_stats.packets_recv
            },
            'boot_time': boot_time,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def optimize_path_environment(self):
        """优化PATH环境变量"""
        print("🛠️ 优化PATH环境变量...")
        
        current_path = os.environ.get("PATH", "")
        path_dirs = current_path.split(os.pathsep)
        
        # 清理重复和无效路径
        unique_paths = []
        seen = set()
        
        for path_dir in path_dirs:
            path_dir = path_dir.strip()
            if path_dir and path_dir not in seen:
                if os.path.exists(path_dir):
                    unique_paths.append(path_dir)
                    seen.add(path_dir)
        
        # 建议添加的常用路径
        suggested_additions = {
            "Windows": [
                "%USERPROFILE%\\AppData\\Local\\Programs\\Python\\Python39\\Scripts",
                "%USERPROFILE%\\.local\\bin",
                "%USERPROFILE%\\AppData\\Roaming\\npm"
            ],
            "Linux": [
                "~/.local/bin",
                "/usr/local/bin",
                "~/.cargo/bin"
            ],
            "Darwin": [
                "~/Library/Python/3.9/bin",
                "/usr/local/bin",
                "~/.cargo/bin"
            ]
        }
        
        new_paths = unique_paths.copy()
        for tool_path in suggested_additions.get(self.system, []):
            expanded_path = os.path.expandvars(os.path.expanduser(tool_path))
            if expanded_path not in seen and os.path.exists(expanded_path):
                new_paths.append(expanded_path)
                seen.add(expanded_path)
        
        return {
            "original_count": len(path_dirs),
            "optimized_count": len(unique_paths),
            "final_count": len(new_paths),
            "removed_duplicates": len(path_dirs) - len(unique_paths),
            "suggested_paths": new_paths
        }
    
    def get_platform_optimization_tips(self):
        """获取平台特定优化建议"""
        tips = {
            "Windows": [
                "🎯 使用Windows Defender清理工具: Get-WindowsDefenderSystemScan",
                "🚀 禁用开机启动项: 任务管理器 > 启动",
                "💾 运行磁盘清理: cleanmgr",
                "🔍 检查大文件: TreeSize Free",
                "⚡ 优化电源设置: 控制面板 > 电源选项"
            ],
            "Linux": [
                "🐧 清理APT缓存: sudo apt clean && sudo apt autoremove",
                "🗄️ 清理日志: sudo journalctl --vacuum-time=1weeks",
                "🔍 查找大文件: du -h / | sort -hr | head -20",
                "🚀 清理旧内核: sudo apt autoremove",
                "💾 检查磁盘使用: df -h"
            ],
            "Darwin": [
                "🍎 清理缓存: sudo rm -rf ~/Library/Caches/*",
                "🗑️ 清空废纸篓: sudo rm -rf ~/.Trash/*",
                "🔍 使用DaisyDisk分析磁盘空间",
                "⚡ 清理启动项: 系统偏好设置 > 用户与群组 > 登录项",
                "🧹 使用CleanMyMac清理系统"
            ]
        }
        
        return tips.get(self.system, tips["Windows"])
    
    def analyze_system_health(self):
        """分析系统健康状况"""
        metrics = self.collect_performance_metrics()
        
        issues = []
        recommendations = []
        
        # CPU分析
        if metrics['cpu']['status'] == 'warning':
            issues.append("🔔 CPU使用率较高")
            recommendations.append("关闭不必要的程序或浏览器标签")
        elif metrics['cpu']['status'] == 'critical':
            issues.append("⚠️ CPU使用率过高")
            recommendations.append("重启系统或检查高CPU进程")
        
        # 内存分析
        if metrics['memory']['status'] == 'warning':
            issues.append("📊 内存使用较高")
            recommendations.append("清理缓存或关闭内存占用大的应用")
        elif metrics['memory']['status'] == 'critical':
            issues.append("🚨 内存严重不足")
            recommendations.append("重启系统或考虑增加内存")
        
        # 磁盘分析
        if metrics['disk']['status'] == 'warning':
            issues.append("💾 磁盘空间紧张")
            recommendations.append("清理大文件或移动数据到外部存储")
        elif metrics['disk']['status'] == 'critical':
            issues.append("🗄️ 磁盘空间严重不足")
            recommendations.append("立即清理磁盘或扩容")
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'severity': 'critical' if any('critical' in str(issue) for issue in issues) else 
                       'warning' if issues else 'optimal',
            'metrics': metrics
        }
    
    def generate_comprehensive_report(self):
        """生成综合系统报告"""
        print("📊 正在生成系统增强报告...")
        
        system_info = self.get_system_info()
        performance_metrics = self.collect_performance_metrics()
        path_optimization = self.optimize_path_environment()
        health_analysis = self.analyze_system_health()
        optimization_tips = self.get_platform_optimization_tips()
        
        report = f"""
🎯 .trae 系统增强综合报告
{'='*60}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🖥️  操作系统: {system_info['system']} {system_info['release']}
🐍 Python版本: {system_info['python_version']}
🔐 管理员权限: {'是' if system_info['is_admin'] else '否'}

💡 系统健康状况:
"""
        
        # 健康状况
        if health_analysis['severity'] == 'optimal':
            report += "✅ 系统状态良好\n"
        else:
            report += f"⚠️ 发现问题: {len(health_analysis['issues'])}个\n"
            for issue in health_analysis['issues']:
                report += f"   {issue}\n"
        
        report += f"""

📊 性能指标:
🔥 CPU: {performance_metrics['cpu']['percent']}% ({performance_metrics['cpu']['status']})
🧠 内存: {performance_metrics['memory']['used_gb']}GB / {performance_metrics['memory']['total_gb']}GB ({performance_metrics['memory']['status']})
💾 磁盘: {performance_metrics['disk']['used_gb']}GB / {performance_metrics['disk']['total_gb']}GB ({performance_metrics['disk']['status']})
🕐 启动时间: {performance_metrics['boot_time']}

🔧 PATH优化结果:
📁 原始路径数: {path_optimization['original_count']}
🎯 优化后路径数: {path_optimization['optimized_count']}
➕ 建议添加路径: {path_optimization['final_count'] - path_optimization['optimized_count']}个

🚀 优化建议:
"""
        
        for rec in health_analysis['recommendations']:
            report += f"  {rec}\n"
        
        report += f"\n🎯 {system_info['system']}特定优化技巧:\n"
        for tip in optimization_tips:
            report += f"  {tip}\n"
        
        return report
    
    def run_optimization_suite(self):
        """运行完整优化套件"""
        print("🚀 启动系统增强套件...")
        
        # 1. 系统信息收集
        system_info = self.get_system_info()
        print(f"✅ 系统信息收集完成: {system_info['system']}")
        
        # 2. 性能监控
        performance_metrics = self.collect_performance_metrics()
        print(f"✅ 性能监控完成: CPU {performance_metrics['cpu']['percent']}%")
        
        # 3. PATH优化
        path_optimization = self.optimize_path_environment()
        print(f"✅ PATH优化完成: 清理了 {path_optimization['removed_duplicates']} 个重复路径")
        
        # 4. 健康分析
        health_analysis = self.analyze_system_health()
        print(f"✅ 健康分析完成: {health_analysis['severity']} 状态")
        
        return {
            'system_info': system_info,
            'performance': performance_metrics,
            'path_optimization': path_optimization,
            'health': health_analysis,
            'timestamp': datetime.now().isoformat()
        }

# 使用示例
if __name__ == "__main__":
    enhancer = SystemEnhancer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        # 完整模式
        print(enhancer.generate_comprehensive_report())
    else:
        # 快速模式
        result = enhancer.run_optimization_suite()
        print(f"\n🎉 系统增强完成！")
        print(f"📊 系统状态: {result['health']['severity']}")
        print(f"🔥 CPU使用率: {result['performance']['cpu']['percent']}%")
        print(f"💾 内存使用: {result['performance']['memory']['used_gb']}GB")