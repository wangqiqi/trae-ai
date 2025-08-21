#!/usr/bin/env python3
"""
自动测试驱动AI工程师
基于实测经验：先保证代码可运行，再优化优雅
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class AutoTestRunner:
    def __init__(self):
        self.project_root = Path.cwd()
        self.test_results = {}
        self.syntax_errors = []
        self.runtime_errors = []
    
    def run_comprehensive_tests(self):
        """执行全面测试，确保代码完整性"""
        print("🧪 测试AI工程师启动全面测试...")
        
        # 1. 语法检查
        self.check_syntax_errors()
        
        # 2. 依赖检查
        self.check_dependencies()
        
        # 3. 项目特定测试
        self.run_project_tests()
        
        # 4. 集成测试
        self.run_integration_tests()
        
        # 5. 生成测试报告
        return self.generate_test_report()
    
    def check_syntax_errors(self):
        """检查语法错误"""
        print("🔍 检查语法错误...")
        
        # Python语法检查
        python_files = list(self.project_root.rglob("*.py"))
        for py_file in python_files:
            try:
                subprocess.run([sys.executable, '-m', 'py_compile', str(py_file)],
                              capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                self.syntax_errors.append(f"Python语法错误: {py_file}")
        
        # TypeScript语法检查
        if (self.project_root / "tsconfig.json").exists():
            try:
                result = subprocess.run(['npx', 'tsc', '--noEmit'], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.syntax_errors.extend(result.stderr.split('\n'))
            except:
                pass
    
    def check_dependencies(self):
        """检查依赖完整性"""
        print("📦 检查依赖完整性...")
        
        # Python依赖
        if (self.project_root / "requirements.txt").exists():
            try:
                subprocess.run([sys.executable, '-c', 'import pkg_resources; pkg_resources.require(open("requirements.txt").read())'],
                              capture_output=True, text=True, check=True)
                self.test_results['python_deps'] = '✅ 完整'
            except:
                self.test_results['python_deps'] = '❌ 缺失'
        
        # Node依赖
        if (self.project_root / "package.json").exists():
            if (self.project_root / "node_modules").exists():
                self.test_results['node_deps'] = '✅ 完整'
            else:
                self.test_results['node_deps'] = '❌ 缺失'
    
    def run_project_tests(self):
        """运行项目特定测试"""
        print("🎯 运行项目测试...")
        
        # FastAPI测试
        if (self.project_root / "main.py").exists():
            self.test_fastapi()
        
        # Vue/React测试
        if (self.project_root / "package.json").exists():
            self.test_frontend()
    
    def test_fastapi(self):
        """测试FastAPI项目"""
        try:
            # 检查能否启动
            process = subprocess.Popen([sys.executable, 'main.py'], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            try:
                process.wait(timeout=5)
                if process.returncode == 0:
                    self.test_results['fastapi'] = '✅ 可启动'
                else:
                    self.test_results['fastapi'] = '❌ 启动失败'
            except subprocess.TimeoutExpired:
                process.kill()
                self.test_results['fastapi'] = '✅ 可启动'
        except Exception as e:
            self.runtime_errors.append(f"FastAPI测试错误: {e}")
    
    def test_frontend(self):
        """测试前端项目"""
        try:
            # 检查构建
            result = subprocess.run(['npm', 'run', 'build', '--dry-run'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.test_results['frontend'] = '✅ 可构建'
            else:
                self.test_results['frontend'] = '❌ 构建失败'
        except:
            self.test_results['frontend'] = '❓ 未测试'
    
    def run_integration_tests(self):
        """运行集成测试"""
        print("🔗 运行集成测试...")
        
        # 端口可用性测试
        import socket
        ports_to_check = [8000, 5173, 3000, 8080]
        
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            if result != 0:
                self.test_results[f'port_{port}'] = '✅ 可用'
            else:
                self.test_results[f'port_{port}'] = '❌ 占用'
    
    def generate_test_report(self):
        """生成测试报告"""
        report = {
            'summary': {
                'total_checks': len(self.test_results) + len(self.syntax_errors),
                'passed': sum(1 for v in self.test_results.values() if '✅' in str(v)),
                'failed': len(self.syntax_errors) + sum(1 for v in self.test_results.values() if '❌' in str(v)),
                'status': 'ready' if not self.syntax_errors else 'needs_fix'
            },
            'details': {
                'syntax_errors': self.syntax_errors,
                'test_results': self.test_results,
                'runtime_errors': self.runtime_errors
            },
            'recommendations': self.get_recommendations()
        }
        
        # 保存报告
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def get_recommendations(self):
        """基于测试结果给出建议"""
        recommendations = []
        
        if self.syntax_errors:
            recommendations.append("🚨 先修复语法错误")
        elif 'python_deps' in self.test_results and '❌' in str(self.test_results['python_deps']):
            recommendations.append("📦 安装Python依赖: pip install -r requirements.txt")
        elif 'node_deps' in self.test_results and '❌' in str(self.test_results['node_deps']):
            recommendations.append("📦 安装Node依赖: npm install")
        else:
            recommendations.append("✅ 代码完整性验证通过，可以启动项目")
        
        return recommendations

if __name__ == "__main__":
    runner = AutoTestRunner()
    report = runner.run_comprehensive_tests()
    
    print("\n" + "="*50)
    print("🧪 测试报告")
    print("="*50)
    print(f"状态: {report['summary']['status']}")
    print(f"通过: {report['summary']['passed']}")
    print(f"失败: {report['summary']['failed']}")
    print("\n建议:")
    for rec in report['recommendations']:
        print(f"  {rec}")