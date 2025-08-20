#!/usr/bin/env python3
# ⚡ .trae 性能深度监控工具
# 实时监控系统性能并给出优化建议

import time
import psutil
import platform
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.system = platform.system()
        self.metrics = {}
        
    def collect_system_metrics(self):
        """收集系统性能指标"""
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
        
        self.metrics = {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'status': 'optimal' if cpu_percent < 70 else 'warning' if cpu_percent < 90 else 'critical'
            },
            'memory': {
                'percent': memory_percent,
                'used_gb': round(memory_used_gb, 2),
                'total_gb': round(memory_total_gb, 2),
                'status': 'optimal' if memory_percent < 70 else 'warning' if memory_percent < 90 else 'critical'
            },
            'disk': {
                'percent': disk_percent,
                'used_gb': round(disk_used_gb, 2),
                'total_gb': round(disk_total_gb, 2),
                'status': 'optimal' if disk_percent < 80 else 'warning' if disk_percent < 95 else 'critical'
            },
            'boot_time': boot_time
        }
        
        return self.metrics
    
    def analyze_performance(self):
        """分析性能并给出优化建议"""
        metrics = self.collect_system_metrics()
        
        recommendations = []
        
        # CPU优化建议
        if metrics['cpu']['status'] == 'warning':
            recommendations.append("🔔 CPU使用率较高，建议关闭不必要的程序")
        elif metrics['cpu']['status'] == 'critical':
            recommendations.append("⚠️ CPU使用率过高，建议重启系统或检查进程")
        
        # 内存优化建议
        if metrics['memory']['status'] == 'warning':
            recommendations.append("📊 内存使用较高，建议清理缓存")
        elif metrics['memory']['status'] == 'critical':
            recommendations.append("🚨 内存严重不足，建议重启或增加内存")
        
        # 磁盘优化建议
        if metrics['disk']['status'] == 'warning':
            recommendations.append("💾 磁盘空间紧张，建议清理大文件")
        elif metrics['disk']['status'] == 'critical':
            recommendations.append("🗄️ 磁盘空间严重不足，建议立即清理")
        
        return {
            'metrics': metrics,
            'recommendations': recommendations,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_optimization_tips(self):
        """获取Windows特定优化建议"""
        tips = {
            'Windows': [
                "🎯 使用Windows Defender清理工具",
                "🚀 禁用开机启动项：任务管理器 > 启动",
                "💾 运行磁盘清理：cleanmgr",
                "🔍 检查大文件：使用TreeSize工具"
            ],
            'Linux': [
                "🐧 清理APT缓存：sudo apt clean",
                "🗄️ 清理日志：sudo journalctl --vacuum-time=1weeks",
                "🔍 查找大文件：du -h / | sort -hr",
                "🚀 清理旧内核：sudo apt autoremove"
            ],
            'Darwin': [
                "🍎 清理缓存：sudo rm -rf ~/Library/Caches/*",
                "🗑️ 清空废纸篓：sudo rm -rf ~/.Trash/*",
                "🔍 使用DaisyDisk分析磁盘",
                "⚡ 清理启动项：系统偏好设置 > 用户与群组"
            ]
        }
        
        return tips.get(self.system, tips['Windows'])
    
    def generate_report(self):
        """生成性能报告"""
        analysis = self.analyze_performance()
        optimization_tips = self.get_optimization_tips()
        
        report = f"""
🎯 .trae 性能深度监控报告
{'='*50}
📊 监控时间: {analysis['timestamp']}
🖥️  操作系统: {platform.system()} {platform.release()}

💡 系统状态:
🔥 CPU: {analysis['metrics']['cpu']['percent']}% ({analysis['metrics']['cpu']['status']})
🧠 内存: {analysis['metrics']['memory']['used_gb']}GB / {analysis['metrics']['memory']['total_gb']}GB ({analysis['metrics']['memory']['status']})
💾 磁盘: {analysis['metrics']['disk']['used_gb']}GB / {analysis['metrics']['disk']['total_gb']}GB ({analysis['metrics']['disk']['status']})
🕐 启动时间: {analysis['boot_time']}

🚀 优化建议:
"""
        
        for rec in analysis['recommendations']:
            report += f"  {rec}\n"
        
        report += f"\n🎯 {self.system}特定优化技巧:\n"
        for tip in optimization_tips:
            report += f"  {tip}\n"
        
        return report

# 使用示例
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    print(monitor.generate_report())