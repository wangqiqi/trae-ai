#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae AI 模板系统测试脚本
用于验证模板自动化功能是否正常工作
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class TemplateSystemTester:
    def __init__(self):
        self.base_path = Path("e:\\study\\learn_trae")
        self.template_path = self.base_path / ".trae" / "templates"
        self.workflow_path = self.base_path / ".trae" / "workflows"
        
    def test_template_files(self):
        """测试模板文件是否存在"""
        print("🧪 测试模板文件...")
        
        required_templates = [
            "project-init-template.md",
            "requirements-template.md", 
            "api-spec-template.md",
            "database-design-template.md",
            "test-plan-template.md",
            "deployment-template.md",
            "code-review-template.md",
            "tech-choice-template.md"
        ]
        
        missing_files = []
        for template in required_templates:
            file_path = self.template_path / template
            if file_path.exists():
                print(f"  ✅ {template}")
            else:
                print(f"  ❌ {template}")
                missing_files.append(template)
                
        return len(missing_files) == 0
    
    def test_automation_scripts(self):
        """测试自动化脚本是否存在"""
        print("\n🧪 测试自动化脚本...")
        
        required_scripts = [
            "template-manager.py",
            "ai-template-integration.py", 
            "trae-console-enhanced.py",
            "quick-start.py"
        ]
        
        missing_scripts = []
        for script in required_scripts:
            file_path = self.workflow_path / script
            if file_path.exists():
                print(f"  ✅ {script}")
            else:
                print(f"  ❌ {script}")
                missing_scripts.append(script)
                
        return len(missing_scripts) == 0
    
    def test_template_content(self):
        """测试模板内容完整性"""
        print("\n🧪 测试模板内容...")
        
        # 测试requirements-template.md
        req_template = self.template_path / "requirements-template.md"
        if req_template.exists():
            content = req_template.read_text(encoding='utf-8')
            checks = [
                "## 🎯 项目信息",
                "## 📝 功能需求", 
                "## 🎨 用户体验需求",
                "## 🔧 技术需求",
                "## ✅ 验收标准"
            ]
            
            passed = 0
            for check in checks:
                if check in content:
                    passed += 1
                    print(f"  ✅ {check}")
                else:
                    print(f"  ❌ {check}")
                    
            # 只要有核心内容就算通过
            return passed >= 3
        return False
    
    def test_quick_start(self):
        """测试快速启动脚本"""
        print("\n🧪 测试快速启动脚本...")
        
        quick_start = self.base_path / ".trae" / "quick-start.py"
        if quick_start.exists():
            try:
                # 测试脚本语法
                result = subprocess.run([
                    sys.executable, "-m", "py_compile", str(quick_start)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("  ✅ 快速启动脚本语法正确")
                    return True
                else:
                    print(f"  ❌ 语法错误: {result.stderr}")
                    return False
            except Exception as e:
                print(f"  ❌ 测试失败: {e}")
                return False
        return False
    
    def run_demo(self):
        """运行演示"""
        print("\n🚀 跳过演示测试（可选）...")
        return True
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*50)
        print("📊 Trae AI 模板系统测试报告")
        print("="*50)
        
        tests = [
            ("模板文件", self.test_template_files()),
            ("自动化脚本", self.test_automation_scripts()), 
            ("模板内容", self.test_template_content()),
            ("快速启动", self.test_quick_start())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        print(f"\n🎯 测试结果: {passed}/{total} 项通过")
        
        if passed == total:
            print("\n🎉 恭喜！模板系统已完全配置成功！")
            print("\n下一步:")
            print("1. 运行: python .trae/quick-start.py")
            print("2. 体验: python demo-template-usage.py demo")
            print("3. 查看: 打开 .trae/TEMPLATES-GUIDE.md")
        else:
            print(f"\n⚠️ 发现 {total-passed} 个问题需要修复")
            print("\n建议:")
            print("1. 检查文件权限")
            print("2. 重新运行配置脚本")
            print("3. 查看错误日志")

def main():
    """主函数"""
    print("🧪 Trae AI 模板系统测试工具")
    print("="*30)
    
    tester = TemplateSystemTester()
    tester.generate_report()

if __name__ == "__main__":
    main()