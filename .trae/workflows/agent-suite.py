#!/usr/bin/env python3
"""
智能体套件 - 基于agent-template.json的现代化管理工具
支持完整的DevOps生命周期管理、团队协作、云原生部署等高级功能

用法:
    python agent-suite.py create                    # 交互式创建
    python agent-suite.py check [文件]             # 深度检查
    python agent-suite.py generate [技术栈]        # 快速生成
    python agent-suite.py dashboard                # 可视化仪表板
    python agent-suite.py batch --action=check     # 批量检查
"""

import json
import os
import sys
import webbrowser
import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple

class AgentSuite:
    """智能体套件 - 现代化DevOps智能体管理"""
    
    def __init__(self, agents_dir: str):
        self.base_dir = Path(__file__).parent.parent  # 指向 .trae 目录
        self.agents_dir = Path(agents_dir) if agents_dir else self.base_dir / "agent"
        self.template_path = self.base_dir / "templates" / "agent-template.json"
        
        # 确保输出目录存在
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        # 核心字段验证
        self.schema = {
            "required": ["schema_version", "agent_info", "technical_stack", "capabilities"],
            "lifecycle": ["analysis", "development", "deployment"],
            "infrastructure": ["local", "cloud", "edge"],
            "quality": ["code_quality", "performance", "compliance"],
            "collaboration": ["version_control", "communication", "tools"],
            "observability": ["monitoring", "chaos_engineering", "cost_optimization"],
            "security": ["development", "runtime", "compliance"]
        }

    def load_template(self) -> Dict[str, Any]:
        """加载标准模板"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 模板加载失败: {e}")
            return {}

    def load_agent(self, filepath: Path) -> Tuple[Dict[str, Any], bool]:
        """加载智能体配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f), True
        except Exception as e:
            print(f"❌ 文件读取失败: {e}")
            return {}, False

    def create_agent_interactive(self) -> str:
        """交互式创建智能体"""
        print("🚀 智能体创建器")
        print("=" * 60)
        
        # 基础信息采集
        tech_info = self._collect_tech_info()
        lifecycle_info = self._collect_lifecycle_info()
        infrastructure_info = self._collect_infrastructure_info()
        
        # 生成配置
        config = self._generate_config(tech_info, lifecycle_info, infrastructure_info)
        
        # 保存文件
        filename = f"{tech_info['tech_stack']}-engineer.json"
        filepath = self.agents_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 智能体创建成功: {filename}")
        return str(filepath)

    def _collect_tech_info(self) -> Dict[str, Any]:
        """收集技术栈信息"""
        print("\n📋 技术栈配置")
        tech_stack = input("主要技术栈 (如: react, python, go): ").strip()
        primary_lang = input(f"主要语言 (默认: {self._guess_language(tech_stack)}): ").strip() or self._guess_language(tech_stack)
        framework = input("主要框架: ").strip()
        
        return {
            "tech_stack": tech_stack,
            "primary_language": primary_lang,
            "framework": framework,
            "role_name": f"{tech_stack.title()}工程师"
        }

    def _collect_lifecycle_info(self) -> Dict[str, Any]:
        """收集生命周期信息"""
        print("\n🔄 项目生命周期")
        deployment_strategy = input("部署策略 (blue-green/rolling/canary): ").strip() or "blue-green"
        environments = input("环境列表 (用逗号分隔): ").strip() or "dev,staging,prod"
        
        return {
            "deployment_strategy": deployment_strategy,
            "environments": [e.strip() for e in environments.split(",")]
        }

    def _collect_infrastructure_info(self) -> Dict[str, Any]:
        """收集基础设施信息"""
        print("\n🏗️ 基础设施配置")
        cloud_provider = input("云服务商 (aws/azure/gcp): ").strip() or "aws"
        container_tool = input("容器工具 (docker/podman): ").strip() or "docker"
        
        return {
            "cloud_provider": cloud_provider,
            "container_tool": container_tool,
            "iac_tool": "terraform"
        }

    def _generate_config(self, tech_info: Dict, lifecycle: Dict, infra: Dict) -> Dict[str, Any]:
        """生成完整的配置"""
        template = self.load_template()
        if not template:
            return {}
            
        # 填充模板
        config = template.copy()
        
        # 基础信息
        config["agent_info"]["name"] = tech_info["role_name"]
        config["agent_info"]["role"] = f"{tech_info['tech_stack']}-specialist"
        config["agent_info"]["description"] = f"专精{tech_info['tech_stack']}技术栈的现代化开发专家"
        
        # 技术栈
        config["technical_stack"]["primary"]["language"] = tech_info["primary_language"]
        config["technical_stack"]["primary"]["framework"] = tech_info["framework"]
        
        # 部署配置
        config["project_lifecycle"]["deployment"]["strategy"] = lifecycle["deployment_strategy"]
        config["project_lifecycle"]["deployment"]["environments"] = lifecycle["environments"]
        
        # 基础设施
        config["infrastructure"]["cloud"]["provider"] = infra["cloud_provider"]
        config["infrastructure"]["local"]["containerization"] = infra["container_tool"]
        config["infrastructure"]["cloud"]["infrastructure_as_code"] = infra["iac_tool"]
        
        return config

    def check_compliance(self, filepath: Path) -> Dict[str, Any]:
        """检查标准合规性"""
        agent, success = self.load_agent(filepath)
        if not success:
            return {"status": "error", "message": "文件读取失败"}
        
        report = {
            "file": filepath.name,
            "compliant": True,
            "score": 100,
            "missing_sections": [],
            "recommendations": [],
            "modern_features": []
        }
        
        # 检查schema版本
        if "schema_version" not in agent:
            report["compliant"] = False
            report["missing_sections"].append("schema_version")
            report["score"] -= 20
        
        # 检查核心模块
        for section, subsections in self.schema.items():
            if section not in agent:
                report["missing_sections"].append(section)
                report["score"] -= 15
                report["compliant"] = False
            elif isinstance(subsections, list):
                missing = [sub for sub in subsections if sub not in agent.get(section, {})]
                if missing:
                    report["missing_sections"].extend([f"{section}.{sub}" for sub in missing])
                    report["score"] -= 10
        
        # 检查现代功能
        modern_checks = [
            ("observability", "可观测性配置"),
            ("chaos_engineering", "混沌工程"),
            ("infrastructure_as_code", "基础设施即代码"),
            ("cost_optimization", "成本优化"),
            ("security.compliance", "安全合规")
        ]
        
        for key, feature in modern_checks:
            if self._check_nested_key(agent, key):
                report["modern_features"].append(feature)
        
        return report

    def generate_dashboard(self) -> None:
        """生成可视化仪表板"""
        report = self.generate_comprehensive_report()
        
        html_content = self._generate_dashboard_html(report)
        
        dashboard_path = self.agents_dir / "dashboard.html"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 仪表板已生成: {dashboard_path}")
        webbrowser.open(str(dashboard_path))

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合报告"""
        json_files = list(self.agents_dir.glob("*.json"))
        results = []
        
        for filepath in json_files:
            if filepath.name.startswith(("_", ".", "dashboard")):
                continue
                
            report = self.check_compliance(filepath)
            results.append(report)
        
        return {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_files": len(results),
            "compliant": sum(1 for r in results if r["compliant"]),
            "average_score": sum(r["score"] for r in results) / len(results) if results else 0,
            "details": results
        }

    def create_agent(self, tech_stack: str, name: str, description: str) -> str:
        """快速创建智能体"""
        print(f"🚀 快速创建: {tech_stack} 智能体")
        
        config = self.load_template()
        if not config:
            return ""
            
        # 填充模板
        config["agent_info"]["name"] = name
        config["agent_info"]["role"] = f"{tech_stack}-specialist"
        config["agent_info"]["description"] = description
        
        # 技术栈
        config["technical_stack"]["primary"]["language"] = self._guess_language(tech_stack)
        config["technical_stack"]["primary"]["framework"] = tech_stack
        
        # 保存文件
        filename = f"{tech_stack}-engineer.json"
        filepath = self.agents_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 快速创建成功: {filename}")
        return str(filepath)

    def process_all_files(self, actions: List[str]) -> None:
        """批量处理文件"""
        json_files = list(self.agents_dir.glob("*.json"))
        
        for filepath in json_files:
            if filepath.name.startswith(("_", ".", "dashboard")):
                continue
                
            print(f"\n📁 处理: {filepath.name}")
            
            for action in actions:
                if action == "check":
                    report = self.check_compliance(filepath)
                    print(f"   合规性: {report['score']}分")

    def _guess_language(self, tech_stack: str) -> str:
        """根据技术栈猜测语言"""
        mapping = {
            "react": "TypeScript", "vue": "TypeScript", "angular": "TypeScript",
            "python": "Python", "nodejs": "JavaScript", "java": "Java",
            "go": "Go", "rust": "Rust", "flutter": "Dart"
        }
        return mapping.get(tech_stack.lower(), "JavaScript")

    def _check_nested_key(self, data: Dict, key: str) -> bool:
        """检查嵌套键是否存在"""
        keys = key.split(".")
        current = data
        for k in keys:
            if not isinstance(current, dict) or k not in current:
                return False
            current = current[k]
        return True

    def _generate_dashboard_html(self, report: Dict[str, Any]) -> str:
        """生成仪表板HTML"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>智能体仪表板</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .file-list {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .file-item {{ padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }}
        .score {{ padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .score-high {{ background: #d4edda; color: #155724; }}
        .score-medium {{ background: #fff3cd; color: #856404; }}
        .score-low {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 智能体仪表板</h1>
        <p>生成时间: {report['generated_at']}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>{report['total_files']}</h3>
            <p>总文件数</p>
        </div>
        <div class="stat-card">
            <h3>{report['compliant']}</h3>
            <p>兼容</p>
        </div>
        <div class="stat-card">
            <h3>{report['average_score']:.1f}</h3>
            <p>平均得分</p>
        </div>
    </div>
    
    <div class="file-list">
        <h3 style="padding: 15px; margin: 0; background: #f8f9fa;">文件详情</h3>
        {''.join(f'''
        <div class="file-item">
            <span>{detail['file']}</span>
            <span class="score score-{'high' if detail['score'] >= 80 else 'medium' if detail['score'] >= 60 else 'low'}">
                {detail['score']}分
            </span>
        </div>
        ''' for detail in report['details'])}
    </div>
</body>
</html>
"""

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
🚀 智能体套件 - 现代化DevOps智能体管理

📁 默认输出目录: .trae/agent/ (便于复用)

用法:
    python agent-suite.py create                    # 交互式创建智能体
    python agent-suite.py check [文件]             # 检查合规性
    python agent-suite.py generate [技术栈]        # 快速生成
    python agent-suite.py dashboard                # 生成仪表板
    python agent-suite.py batch --action=check     # 批量检查
    
高级用法:
    python agent-suite.py create --output ./custom-dir  # 自定义输出目录
    python agent-suite.py generate python --output ../agents
        
示例:
    python agent-suite.py create                    # 创建到 .trae/agent/
    python agent-suite.py check environment-manager.json
    python agent-suite.py generate python           # 创建python专家
    python agent-suite.py dashboard                # 生成可视化仪表板
        """)
        return

    # 使用 .trae/agent 作为标准输出目录，便于复用
    project_root = Path(__file__).parent.parent
    agents_dir = project_root / "agent"
    
    # 确保agent目录存在
    agents_dir.mkdir(exist_ok=True)
    
    # 也支持自定义输出目录
    if len(sys.argv) > 3 and sys.argv[2] == "--output":
        agents_dir = Path(sys.argv[3])
        sys.argv.pop(2)  # 移除--output参数
        sys.argv.pop(2)  # 移除路径参数
    
    suite = AgentSuite(str(agents_dir))
    
    command = sys.argv[1]
    
    if command == "create":
        suite.create_agent_interactive()
    elif command == "check" and len(sys.argv) > 2:
        filepath = agents_dir / sys.argv[2]
        report = suite.check_compliance(filepath)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif command == "generate" and len(sys.argv) > 2:
        tech_stack = sys.argv[2]
        suite.create_agent(tech_stack, f"{tech_stack.title()}工程师", f"专精{tech_stack}的现代化开发专家")
    elif command == "dashboard":
        suite.generate_dashboard()
    elif command == "batch" and len(sys.argv) > 2:
        action = sys.argv[2].split("=")[1] if "=" in sys.argv[2] else "check"
        suite.process_all_files([action])
    else:
        print("❌ 无效的命令或参数")
if __name__ == "__main__":
    main()