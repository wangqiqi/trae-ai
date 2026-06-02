#!/usr/bin/env python3
# 🎯 性能监控工程师
# 实时性能分析和优化建议

import os
import sys
import time
import psutil
import json
import subprocess
import gc
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class PerformanceMonitor:
    """
    性能监控工程师
    职责：实时性能分析，提供优化建议
    功能：CPU监控、内存分析、响应时间测量、性能瓶颈检测
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.trae_path = self.project_root / ".trae"
        self.report_path = self.trae_path / "reports"
        self.report_path.mkdir(exist_ok=True)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统性能指标"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        return {
            "cpu": {
                "percent": cpu_percent,
                "cores": psutil.cpu_count(),
                "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            },
            "memory": {
                "total": round(memory.total / (1024**3), 2),
                "used": round(memory.used / (1024**3), 2),
                "free": round(memory.free / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total": round(disk.total / (1024**3), 2),
                "used": round(disk.used / (1024**3), 2),
                "free": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            },
            "network": {
                "bytes_sent": round(network.bytes_sent / (1024**2), 2),
                "bytes_recv": round(network.bytes_recv / (1024**2), 2)
            }
        }
    
    def analyze_python_performance(self) -> Dict[str, Any]:
        """分析Python代码性能"""
        import linecache
        import tracemalloc
        
        tracemalloc.start()
        snapshot1 = tracemalloc.take_snapshot()
        
        time.sleep(0.5)
        
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        memory_usage = []
        for stat in top_stats[:10]:
            frame = stat.traceback[0]
            line = linecache.getline(frame.filename, frame.lineno).strip()
            memory_usage.append({
                "file": os.path.basename(frame.filename),
                "line": frame.lineno,
                "size": stat.size_diff,
                "line_content": line
            })
        
        tracemalloc.stop()
        
        return {
            "memory_snapshot": memory_usage,
            "objects_count": len(gc.get_objects())
        }
    
    def measure_code_execution(self, code: str, iterations: int = 100) -> Dict:
        """测量代码执行性能"""
        results = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            try:
                exec(code)
            except:
                pass
            end = time.perf_counter()
            results.append(end - start)
        
        avg_time = sum(results) / len(results)
        min_time = min(results)
        max_time = max(results)
        
        return {
            "iterations": iterations,
            "avg_ms": avg_time * 1000,
            "min_ms": min_time * 1000,
            "max_ms": max_time * 1000,
            "std_dev": (sum((x - avg_time) ** 2 for x in results) / len(results)) ** 0.5 * 1000
        }
    
    def check_project_performance(self) -> Dict:
        """检查项目性能状态"""
        issues = []
        recommendations = []
        
        metrics = self.get_system_metrics()
        
        # CPU检查
        if metrics["cpu"]["percent"] > 80:
            issues.append(f"CPU使用率过高: {metrics['cpu']['percent']}%")
            recommendations.append("考虑优化CPU密集型任务，使用异步处理或多线程")
        
        # 内存检查
        if metrics["memory"]["percent"] > 85:
            issues.append(f"内存使用率过高: {metrics['memory']['percent']}%")
            recommendations.append("检查内存泄漏，优化数据结构，考虑使用生成器")
        
        # 磁盘检查
        if metrics["disk"]["percent"] > 90:
            issues.append(f"磁盘空间不足: {metrics['disk']['percent']}%")
            recommendations.append("清理日志文件，删除临时文件，扩展磁盘空间")
        
        # 检查Python文件数量和大小
        py_files = list(self.project_root.rglob("*.py"))
        large_files = [f for f in py_files if f.stat().st_size > 100 * 1024]
        
        if large_files:
            issues.append(f"发现{len(large_files)}个大型Python文件")
            recommendations.append("考虑将大型文件拆分为多个模块")
        
        return {
            "issues": issues,
            "recommendations": recommendations,
            "py_files_count": len(py_files),
            "large_files_count": len(large_files)
        }
    
    def generate_performance_report(self) -> str:
        """生成性能报告"""
        print("📊 正在执行性能分析...")
        
        metrics = self.get_system_metrics()
        project_check = self.check_project_performance()
        
        report = f"""
🎯 性能监控报告
{'='*60}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
📁 项目路径: {self.project_root}

🖥️ 系统性能指标
---------------
CPU:
  ├── 使用率: {metrics['cpu']['percent']}%
  ├── 核心数: {metrics['cpu']['cores']}
  └── 频率: {metrics['cpu']['freq']} MHz

内存:
  ├── 总量: {metrics['memory']['total']} GB
  ├── 已用: {metrics['memory']['used']} GB
  ├── 可用: {metrics['memory']['free']} GB
  └── 使用率: {metrics['memory']['percent']}%

磁盘:
  ├── 总量: {metrics['disk']['total']} GB
  ├── 已用: {metrics['disk']['used']} GB
  ├── 可用: {metrics['disk']['free']} GB
  └── 使用率: {metrics['disk']['percent']}%

📈 项目性能分析
--------------
- Python文件数量: {project_check['py_files_count']}
- 大型文件(>100KB): {project_check['large_files_count']}
"""
        
        if project_check["issues"]:
            report += "\n⚠️  检测到的问题:\n"
            for i, issue in enumerate(project_check["issues"], 1):
                report += f"   {i}. {issue}\n"
        
        if project_check["recommendations"]:
            report += "\n💡 优化建议:\n"
            for i, rec in enumerate(project_check["recommendations"], 1):
                report += f"   {i}. {rec}\n"
        
        # 性能评分
        score = 100
        if metrics["cpu"]["percent"] > 80:
            score -= 20
        if metrics["memory"]["percent"] > 85:
            score -= 20
        if metrics["disk"]["percent"] > 90:
            score -= 20
        if project_check["large_files_count"] > 5:
            score -= 10
        
        report += f"\n🎯 综合性能评分: {score}/100\n"
        
        if score >= 80:
            report += "✅ 系统性能良好"
        elif score >= 60:
            report += "⚠️  系统性能一般，建议优化"
        else:
            report += "❌ 系统性能较差，需要立即优化"
        
        # 保存报告
        report_file = self.report_path / f"performance-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 性能报告已保存: {report_file}")
        
        return report
    
    def run(self):
        """运行性能监控"""
        report = self.generate_performance_report()
        print(report)

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.run()