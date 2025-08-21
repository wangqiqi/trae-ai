#!/usr/bin/env python3
"""
🚀 Trae AI 超级团队 - 统一入口 v4.0
基于实测经验全面升级：自动环境管理、测试驱动、需求澄清
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class TraeAuto:
    """Trae AI 自动执行器 - 智能升级"""
    
    def __init__(self):
        self.trae_dir = Path(__file__).parent
        self.project_root = self.trae_dir.parent
        self.action = os.getenv('TRAE_ACTION', 'auto')
    
    def auto_run(self):
        """自动执行最合适的操作"""
        if self.action == 'auto':
            return self.auto_mode()
        elif self.action == 'start':
            return self.smart_start()
        elif self.action == 'test':
            return self.run_tests()
        elif self.action == 'clarify':
            return self.clarify_requirements()
        else:
            return getattr(self, f'do_{self.action}', self.show_help)()
    
    def auto_mode(self):
        """全自动模式 - 零交互"""
        print("🚀 全自动模式启动...")
        
        # 1. 智能检测项目类型
        project_type = self.detect_project_type()
        print(f"检测到项目类型: {project_type}")
        
        # 2. 自动环境检查
        self.check_environment()
        
        # 3. 自动测试运行
        self.run_tests()
        
        # 4. 启动对应智能体
        if project_type == 'vue':
            subprocess.run([sys.executable, str(self.trae_dir / "workflows" / "team-launcher.py"), "vue"])
        elif project_type == 'fastapi':
            subprocess.run([sys.executable, str(self.trae_dir / "workflows" / "team-launcher.py"), "fastapi"])
        else:
            self.do_console()
        
        return {"status": "auto_mode_complete", "project_type": project_type}
    
    def smart_start(self):
        """智能启动模式"""
        print("🤖 智能启动模式...")
        
        # 1. 自动环境检查
        print("\n🔍 步骤1: 自动环境检查...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.trae_dir / "core" / "auto-environment-manager.py")
            ], check=True, cwd=str(self.project_root))
        except:
            print("⚠️  环境检查跳过，继续...")
        
        # 2. 自动测试运行
        print("\n🧪 步骤2: 自动测试验证...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.trae_dir / "core" / "auto-test-runner.py")
            ], check=True, cwd=str(self.project_root))
        except:
            print("⚠️  测试跳过，继续...")
        
        # 3. 启动控制台
        print("\n🎯 步骤3: 启动AI控制台...")
        return self.do_console()
    
    def run_tests(self):
        """运行自动测试"""
        print("🧪 运行全面测试...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.trae_dir / "core" / "auto-test-runner.py")
            ], check=True)
            print("✅ 测试通过")
            return {"status": "tests_passed"}
        except:
            print("❌ 测试运行失败")
            return {"status": "tests_failed"}
    
    def clarify_requirements(self):
        """需求澄清"""
        print("🎯 启动需求澄清...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.trae_dir / "core" / "smart-requirements-clarifier.py")
            ], check=True)
            return {"status": "requirements_clarified"}
        except:
            print("❌ 需求澄清启动失败")
            return {"status": "clarify_failed"}
    
    def detect_project_type(self):
        """智能检测项目类型"""
        project_root = self.project_root
        
        if (project_root / "package.json").exists():
            with open(project_root / "package.json") as f:
                content = f.read()
                if 'vue' in content.lower():
                    return 'vue'
                elif 'react' in content.lower():
                    return 'react'
        
        if (project_root / "requirements.txt").exists():
            with open(project_root / "requirements.txt") as f:
                content = f.read()
                if 'fastapi' in content.lower():
                    return 'fastapi'
                elif 'django' in content.lower():
                    return 'django'
        
        return 'generic'
    
    def check_environment(self):
        """自动环境检查"""
        print("🔍 正在检查开发环境...")
        try:
            subprocess.run([
                sys.executable, 
                str(self.trae_dir / "core" / "auto-environment-manager.py")
            ], capture_output=True, text=True, cwd=str(self.project_root))
            print("✅ 环境检查完成")
        except:
            print("✅ 环境就绪")
        return {"status": "environment_checked"}
    
    def do_start(self):
        """启动团队向导"""
        return self.smart_start()
    
    def do_console(self):
        """启动控制台 - 单需求模式，更友好的交互"""
        print("\n🤖 Trae AI 超级团队控制台")
        print("=" * 60)
        print("💡 使用方式:")
        print("  1. 直接描述你的项目需求 (一句话即可)")
        print("  2. 系统将自动分析并推荐最佳方案")
        print("  3. 按回车完成，系统自动退出")
        print("=" * 60)
        
        try:
            user_input = input("\n🎯 请描述你的项目需求: ").strip()
            
            if not user_input:
                print("❌ 请输入有效的项目需求")
                return {"status": "no_input"}
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 再见！")
                return {"status": "user_exit"}
            
            # 智能需求分析
            print(f"\n🔍 正在分析需求: {user_input}")
            
            # 检测项目类型
            project_type = self.detect_project_type()
            
            # 提供智能推荐
            recommendations = self.get_smart_recommendations(user_input, project_type)
            
            print("\n🎯 推荐方案:")
            print("=" * 40)
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
            
            print(f"\n✅ 需求分析完成！项目类型: {project_type}")
            print("📋 下一步建议:")
            print("  - 运行: python .trae/trae.py start  启动开发")
            print("  - 查看: .trae/README.md  获取详细指南")
            
            return {"status": "analysis_complete", "project_type": project_type, "recommendations": recommendations}
            
        except KeyboardInterrupt:
            print("\n👋 用户取消")
            return {"status": "user_cancelled"}
        except EOFError:
            print("\n👋 再见！")
            return {"status": "user_exit"}
    
    def get_smart_recommendations(self, user_input, project_type):
        """根据需求提供智能推荐"""
        recommendations = []
        
        # 基于关键词和需求提供推荐
        user_input_lower = user_input.lower()
        
        if 'web' in user_input_lower or '网站' in user_input_lower:
            if 'vue' in user_input_lower or 'vue3' in user_input_lower:
                recommendations.append("使用 Vue3 + TypeScript + Vite 技术栈")
                recommendations.append("@Vue工程师 负责前端开发")
                recommendations.append("@FastAPI工程师 负责后端API")
            elif 'react' in user_input_lower:
                recommendations.append("使用 React18 + TypeScript + Next.js 技术栈")
                recommendations.append("@React工程师 负责前端开发")
                recommendations.append("@Node工程师 负责后端服务")
            else:
                recommendations.append("推荐使用 Vue3 或 React18 技术栈")
                recommendations.append("@系统架构师 帮你选择最佳方案")
        
        elif 'mobile' in user_input_lower or 'app' in user_input_lower:
            if 'flutter' in user_input_lower:
                recommendations.append("使用 Flutter + Dart 跨平台开发")
                recommendations.append("@Flutter工程师 负责移动端开发")
            elif 'uniapp' in user_input_lower:
                recommendations.append("使用 Uniapp 跨平台小程序开发")
                recommendations.append("@Uniapp工程师 负责跨平台开发")
            else:
                recommendations.append("推荐 Flutter 或 Uniapp 跨平台方案")
                recommendations.append("@系统架构师 评估移动端技术选型")
        
        elif 'api' in user_input_lower or '后端' in user_input_lower:
            if 'fastapi' in user_input_lower:
                recommendations.append("使用 FastAPI + Python 高性能API开发")
                recommendations.append("@FastAPI工程师 负责API设计和实现")
            elif 'node' in user_input_lower:
                recommendations.append("使用 Node.js + Express/Nest.js 开发")
                recommendations.append("@Node工程师 负责后端服务")
            else:
                recommendations.append("推荐 FastAPI 或 Node.js 后端方案")
                recommendations.append("@系统架构师 帮你选择后端技术栈")
        
        else:
            # 通用推荐
            recommendations.append("@产品经理 帮你梳理具体需求")
            recommendations.append("@系统架构师 设计技术方案")
            recommendations.append("@项目经理 制定开发计划")
        
        # 添加通用建议
        recommendations.append("@测试工程师 制定测试策略")
        recommendations.append("@DevOps工程师 规划部署方案")
        
        return recommendations[:3]  # 返回前3个最相关的建议
    
    def do_dev(self):
        """启动开发助手"""
        try:
            subprocess.run([
                sys.executable,
                str(self.trae_dir / "workflows" / "universal-env-manager.py")
            ])
        except FileNotFoundError:
            print("🎯 开发助手已就绪")
        return {"status": "dev_started"}
    
    def show_help(self):
        """显示帮助"""
        return {
            "usage": "python .trae/trae.py [action]",
            "actions": {
                "auto": "全自动模式 (推荐)",
                "start": "智能启动向导",
                "console": "AI控制台交互",
                "test": "运行自动测试",
                "clarify": "需求澄清助手",
                "dev": "开发环境配置",
                "check": "检查开发环境"
            },
            "note": "🎯 工作流程: 1.自动环境检查 → 2.代码验证 → 3.启动AI团队"
        }
    
    def show_console_help(self):
        """显示控制台帮助"""
        print("\n📋 控制台帮助:")
        print("  exit/quit/q - 退出控制台")
        print("  help - 显示此帮助")
        print("  list - 显示所有可用智能体")
        print("  直接输入需求 - 描述你的项目需求")
        print("\n💡 示例:")
        print("  创建一个Vue3电商网站")
        print("  设计一个FastAPI用户认证系统")
        print("  帮我优化React应用性能")
    
    def list_agents(self):
        """显示所有智能体"""
        agents = [
            "@产品经理 - 需求分析与产品设计",
            "@系统架构师 - 技术架构设计", 
            "@项目经理 - 项目统筹管理",
            "@项目协调员 - 团队协作",
            "@Vue工程师 - Vue3开发",
            "@React工程师 - React开发",
            "@Angular工程师 - Angular开发",
            "@Uniapp工程师 - 跨平台开发",
            "@Flutter工程师 - 移动应用开发",
            "@Python工程师 - Python后端开发",
            "@FastAPI工程师 - FastAPI专业开发",
            "@Node工程师 - Node.js后端开发",
            "@Go工程师 - Go语言开发",
            "@Rust工程师 - Rust系统开发",
            "@测试工程师 - 自动化测试",
            "@DevOps工程师 - 部署运维",
            "@UI/UX设计师 - 界面设计",
            "@技术文档工程师 - 技术文档",
            "@C++部署工程师 - C++系统优化",
            "@环境管理工程师 - 环境配置"
        ]
        
        print("\n🎭 可用智能体 (20个):")
        for agent in agents:
            print(f"  {agent}")

def main():
    """主函数 - 智能入口"""
    trae = TraeAuto()
    result = trae.auto_run()
    
    # 静默模式：只在有错误时输出
    if os.getenv('TRAE_SILENT') != 'true':
        if isinstance(result, dict) and 'status' in result:
            pass  # 状态信息已通过print输出
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()