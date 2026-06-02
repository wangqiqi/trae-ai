#!/usr/bin/env python3
# 🎯 智能代码审查工程师
# 自动生成PR审查报告，提供代码质量评估和改进建议

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class CodeReviewEngineer:
    """
    智能代码审查工程师
    职责：自动分析代码变更，生成专业的PR审查报告
    功能：代码质量评估、安全性审查、性能优化建议、最佳实践检查
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.trae_path = self.project_root / ".trae"
        self.report_path = self.trae_path / "reports"
        self.report_path.mkdir(exist_ok=True)
    
    def run_git_diff(self, base_branch="main", compare_branch="HEAD") -> str:
        """获取两个分支之间的代码差异"""
        try:
            result = subprocess.run(
                ["git", "--no-pager", "diff", f"{base_branch}...{compare_branch}"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.stdout
        except Exception as e:
            print(f"❌ Git diff 执行失败: {e}")
            return ""
    
    def analyze_diff(self, diff_output: str) -> Dict:
        """分析diff输出，提取代码变更信息"""
        files_changed = {}
        current_file = None
        additions = 0
        deletions = 0
        
        for line in diff_output.split('\n'):
            if line.startswith('diff --git'):
                if current_file and (additions > 0 or deletions > 0):
                    files_changed[current_file] = {
                        'additions': additions,
                        'deletions': deletions,
                        'total_changes': additions + deletions
                    }
                current_file = line.split()[-1].replace('b/', '')
                additions = 0
                deletions = 0
            elif line.startswith('+') and not line.startswith('+++'):
                additions += 1
            elif line.startswith('-') and not line.startswith('---'):
                deletions += 1
        
        if current_file and (additions > 0 or deletions > 0):
            files_changed[current_file] = {
                'additions': additions,
                'deletions': deletions,
                'total_changes': additions + deletions
            }
        
        return files_changed
    
    def detect_code_smells(self, file_path: str) -> List[str]:
        """检测代码异味和潜在问题"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # 检测超长行
                if len(line) > 120:
                    issues.append(f"第{i}行: 代码行过长({len(line)}字符)")
                
                # 检测魔法数字
                if re.search(r'\b\d{4,}\b', line) and not re.search(r'(0x[0-9a-fA-F]+|#[0-9a-fA-F]{6})', line):
                    issues.append(f"第{i}行: 存在魔法数字")
                
                # 检测未使用变量模式
                if 'unused' in line.lower() or '_' * 3 in line:
                    issues.append(f"第{i}行: 可能存在未使用变量")
                
                # 检测print调试语句
                if line.strip().startswith('print(') and 'debug' in content.lower():
                    issues.append(f"第{i}行: 可能存在调试打印语句")
                
                # 检测硬编码密码/密钥模式
                if re.search(r'(password|secret|key|token)\s*[=:]\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                    issues.append(f"第{i}行: 可能存在硬编码敏感信息")
            
            # 检测函数复杂度
            func_pattern = re.compile(r'(def|function|func)\s+\w+\s*\([^)]*\)\s*:')
            matches = func_pattern.findall(content)
            if len(matches) > 20:
                issues.append(f"文件包含{len(matches)}个函数，建议拆分")
            
        except Exception as e:
            issues.append(f"分析失败: {str(e)}")
        
        return issues[:5]
    
    def check_security_issues(self, file_path: str) -> List[str]:
        """检查安全问题"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # SQL注入风险
            if re.search(r'(execute|query|cursor)\s*\(\s*["\'].*\s*\+.*["\']', content):
                issues.append("潜在SQL注入风险：使用字符串拼接SQL")
            
            # XSS风险
            if re.search(r'(innerHTML|document\.write)\s*=', content):
                issues.append("潜在XSS风险：直接操作innerHTML")
            
            # 不安全的反序列化
            if re.search(r'(pickle|yaml\.load|eval)\s*\(', content):
                issues.append("潜在安全风险：使用不安全的反序列化")
            
            # 明文密码存储
            if re.search(r'(password|secret)\s*[=:]\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                issues.append("安全风险：可能存在明文密码")
            
        except:
            pass
        
        return issues
    
    def evaluate_code_style(self, file_path: str) -> Dict:
        """评估代码风格"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            score = 100
            feedback = []
            
            # 检查缩进一致性
            indent_counts = {}
            for line in lines:
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces > 0:
                    indent_counts[leading_spaces] = indent_counts.get(leading_spaces, 0) + 1
            
            if len(indent_counts) > 2:
                score -= 10
                feedback.append("缩进不一致，建议统一使用4空格")
            
            # 检查空行规范
            empty_lines = 0
            for line in lines:
                if line.strip() == '':
                    empty_lines += 1
            
            if empty_lines > len(lines) * 0.3:
                score -= 5
                feedback.append("空行过多，建议适当精简")
            
            # 检查注释比例
            comment_lines = sum(1 for line in lines if line.strip().startswith('#') or '//' in line)
            comment_ratio = comment_lines / len(lines) if lines else 0
            
            if comment_ratio < 0.05:
                score -= 10
                feedback.append("注释不足，建议增加关键代码注释")
            elif comment_ratio > 0.3:
                score -= 5
                feedback.append("注释过多，建议精简不必要的注释")
            
            return {"score": max(0, score), "feedback": feedback}
        
        except:
            return {"score": 0, "feedback": ["文件分析失败"]}
    
    def generate_review_report(self, base_branch="main", compare_branch="HEAD") -> str:
        """生成完整的PR审查报告"""
        print("🔍 正在执行代码审查...")
        
        diff_output = self.run_git_diff(base_branch, compare_branch)
        
        if not diff_output:
            return "⚠️  未检测到代码变更或Git仓库未初始化"
        
        files_changed = self.analyze_diff(diff_output)
        
        total_additions = sum(v['additions'] for v in files_changed.values())
        total_deletions = sum(v['deletions'] for v in files_changed.values())
        
        report = f"""
🎯 PR代码审查报告
{'='*60}
📊 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🔀 比较分支: {base_branch}...{compare_branch}
📁 项目路径: {self.project_root}

📈 变更概览
-----------
- 修改文件数: {len(files_changed)}
- 新增代码: {total_additions} 行
- 删除代码: {total_deletions} 行
- 净增代码: {total_additions - total_deletions} 行

📋 文件变更详情
--------------
"""
        
        for file_path, stats in files_changed.items():
            report += f"\n📄 {file_path}"
            report += f"\n   ├── 新增: {stats['additions']} 行"
            report += f"\n   ├── 删除: {stats['deletions']} 行"
            
            full_path = self.project_root / file_path
            if full_path.exists():
                smells = self.detect_code_smells(full_path)
                security = self.check_security_issues(full_path)
                style = self.evaluate_code_style(full_path)
                
                if smells:
                    report += f"\n   ├── ⚠️  代码异味:"
                    for smell in smells:
                        report += f"\n   │      - {smell}"
                
                if security:
                    report += f"\n   ├── 🔒 安全风险:"
                    for issue in security:
                        report += f"\n   │      - {issue}"
                
                report += f"\n   └── 🎨 风格评分: {style['score']}/100"
                if style['feedback']:
                    for fb in style['feedback']:
                        report += f"\n          - {fb}"
        
        report += f"""

🎯 审查总结
-----------
"""
        
        # 计算总体评分
        total_score = 0
        file_count = 0
        for file_path in files_changed:
            full_path = self.project_root / file_path
            if full_path.exists():
                style = self.evaluate_code_style(full_path)
                total_score += style['score']
                file_count += 1
        
        avg_score = total_score / file_count if file_count else 0
        
        if avg_score >= 90:
            report += "✅ 代码质量优秀，建议合并"
        elif avg_score >= 70:
            report += "⚠️  代码质量良好，建议修复部分问题后合并"
        else:
            report += "❌ 代码质量需改进，建议重新审查"
        
        report += f"\n总体代码质量评分: {avg_score:.1f}/100"
        
        # 保存报告
        report_file = self.report_path / f"code-review-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 审查报告已保存: {report_file}")
        
        return report
    
    def run(self):
        """运行代码审查"""
        if len(sys.argv) > 2:
            base_branch = sys.argv[1]
            compare_branch = sys.argv[2]
        elif len(sys.argv) > 1:
            base_branch = "main"
            compare_branch = sys.argv[1]
        else:
            base_branch = "main"
            compare_branch = "HEAD"
        
        report = self.generate_review_report(base_branch, compare_branch)
        print(report)

if __name__ == "__main__":
    engineer = CodeReviewEngineer()
    engineer.run()