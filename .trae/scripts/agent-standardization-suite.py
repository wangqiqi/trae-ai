#!/usr/bin/env python3
"""
智能体标准化完整套件
集创建、检查、修复、优化、报告生成于一体的统一工具

用法:
    python agent-standardization-suite.py create                 # 交互式创建新智能体
    python agent-standardization-suite.py check [文件名]         # 详细检查
    python agent-standardization-suite.py fix [文件名]           # 自动修复
    python agent-standardization-suite.py optimize [文件名]      # 结构优化
    python agent-standardization-suite.py report                # 生成报告
    python agent-standardization-suite.py all [文件名]         # 完整流程
    python agent-standardization-suite.py --all-files check     # 批量检查
    python agent-standardization-suite.py --all-files create    # 批量创建模式
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import datetime

class AgentStandardizationSuite:
    """智能体标准化完整套件"""
    
    def __init__(self, agents_dir: str):
        self.agents_dir = Path(agents_dir)
        self.required_fields = [
            "name", "role", "description", "capabilities",
            "prompts", "output_format", "examples", "templates",
            "review_checkpoints"
        ]
        
        self.templates_required = [
            "project_scaffold", "file_templates"
        ]
        
        self.project_scaffold_required = [
            "meta", "tech_stack", "structure", "package_json", "files"
        ]
        
        self.standard_fields = [
            'name', 'role', 'description', 'capabilities',
            'prompts', 'output_format', 'examples',
            'templates', 'review_checkpoints'
        ]

    def load_agent(self, filepath: Path) -> Tuple[Dict[str, Any], bool]:
        """加载智能体文件，返回数据和成功状态"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)
            return data, True
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {filepath.name} - {e}")
            return {}, False
        except Exception as e:
            print(f"❌ 文件读取错误: {filepath.name} - {e}")
            return {}, False

    def deep_check(self, agent: Dict[str, Any], filepath: Path) -> Dict[str, Any]:
        """深度检查单个文件"""
        result = {
            'file': filepath.name,
            'status': '✅',
            'issues': [],
            'missing_fields': [],
            'warnings': [],
            'json_valid': True,
            'can_fix': [],
            'score': 100
        }

        # 1. 检查必需字段
        missing_fields = []
        for field in self.required_fields:
            if field not in agent:
                missing_fields.append(field)
                result['score'] -= 10
        
        if missing_fields:
            result['missing_fields'] = missing_fields
            result['issues'].append(f"缺少必需字段: {missing_fields}")
            result['status'] = '🔴'
            result['can_fix'].append("补充缺失字段")

        # 2. 检查模板结构
        templates = agent.get('templates', {})
        
        if 'project_scaffold' not in templates:
            result['issues'].append("缺少 project_scaffold")
            result['status'] = '🔴'
            result['score'] -= 15
            result['can_fix'].append("创建project_scaffold")
        else:
            scaffold = templates['project_scaffold']
            missing_scaffold = []
            for field in self.project_scaffold_required:
                if field not in scaffold:
                    missing_scaffold.append(field)
            if missing_scaffold:
                result['issues'].append(f"project_scaffold 缺少: {missing_scaffold}")
                result['status'] = '🔴'
                result['score'] -= 10
                result['can_fix'].append("完善project_scaffold")

        if 'file_templates' not in templates:
            result['issues'].append("缺少 file_templates")
            result['status'] = '🔴'
            result['score'] -= 15
            result['can_fix'].append("创建file_templates")

        # 3. 检查字段类型
        type_checks = [
            ("capabilities", list),
            ("prompts", dict),
            ("output_format", dict),
            ("examples", list),
            ("templates", dict),
            ("review_checkpoints", list)
        ]
        
        for field, expected_type in type_checks:
            if field in agent and not isinstance(agent[field], expected_type):
                result['issues'].append(f"{field} 类型错误，期望 {expected_type}")
                result['status'] = '🔴'
                result['score'] -= 10
                result['can_fix'].append(f"修正{field}类型")

        # 4. 检查示例格式
        examples = agent.get('examples', [])
        if examples:
            for i, example in enumerate(examples):
                if not isinstance(example, dict):
                    result['issues'].append(f"示例 {i+1} 格式错误")
                    result['status'] = '⚠️'
                    result['score'] -= 5
                    result['can_fix'].append("修复示例格式")
                else:
                    required_keys = ["input", "output"]
                    missing_keys = [k for k in required_keys if k not in example]
                    if missing_keys:
                        result['issues'].append(f"示例 {i+1} 缺少: {missing_keys}")
                        result['status'] = '⚠️'
                        result['score'] -= 5
                        result['can_fix'].append("完善示例格式")
        else:
            result['warnings'].append("没有示例")
            result['score'] -= 5

        # 5. 检查旧字段
        if 'core_responsibilities' in agent:
            result['issues'].append("使用旧字段: core_responsibilities")
            result['status'] = '⚠️'
            result['can_fix'].append("重命名字段")

        # 6. 检查JSON格式
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.split('\n')
            if len(lines) > 2 and not lines[1].startswith('  '):
                result['warnings'].append("JSON格式需美化")
                result['can_fix'].append("美化JSON格式")
        except:
            pass

        # 根据分数确定最终状态
        if result['score'] >= 90:
            result['status'] = '✅'
        elif result['score'] >= 70:
            result['status'] = '⚠️'
        else:
            result['status'] = '🔴'

        return result

    def auto_fix(self, filepath: Path) -> bool:
        """自动修复文件"""
        try:
            agent, success = self.load_agent(filepath)
            if not success:
                return False

            changes = []
            
            # 1. 补充缺失字段
            for field in self.required_fields:
                if field not in agent:
                    if field == 'capabilities':
                        agent[field] = ["待补充能力列表"]
                    elif field == 'prompts':
                        agent[field] = {"general": "待补充提示词"}
                    elif field == 'output_format':
                        agent[field] = {"main": "待补充输出格式"}
                    elif field == 'examples':
                        agent[field] = [{"input": "示例输入", "output": "示例输出"}]
                    elif field == 'templates':
                        agent[field] = {
                            "project_scaffold": {
                                "meta": {"name": "待补充", "version": "1.0.0"},
                                "tech_stack": [],
                                "structure": {"src": "源代码目录"},
                                "package_json": {},
                                "files": []
                            },
                            "file_templates": {}
                        }
                    elif field == 'review_checkpoints':
                        agent[field] = ["代码质量检查", "功能测试", "文档完整性"]
                    else:
                        agent[field] = f"待补充{field}"
                    changes.append(f"补充{field}")

            # 2. 重命名字段
            if 'core_responsibilities' in agent:
                if 'capabilities' not in agent:
                    agent['capabilities'] = agent['core_responsibilities']
                del agent['core_responsibilities']
                changes.append("core_responsibilities→capabilities")

            # 3. 修复示例格式
            examples = agent.get('examples', [])
            new_examples = []
            for example in examples:
                if isinstance(example, dict):
                    new_example = {}
                    if 'scenario' in example:
                        new_example['input'] = example['scenario']
                        changes.append("scenario→input")
                    elif 'input' not in example:
                        new_example['input'] = "待补充输入"
                    
                    if 'description' in example:
                        new_example['output'] = example['description']
                        changes.append("description→output")
                    elif 'output' not in example:
                        new_example['output'] = "待补充输出"
                    
                    # 保留其他字段
                    for key, value in example.items():
                        if key not in ['scenario', 'description', 'input', 'output']:
                            new_example[key] = value
                    
                    new_examples.append(new_example)
                else:
                    new_examples.append({"input": str(example), "output": "待补充"})
            
            if examples != new_examples:
                agent['examples'] = new_examples
                changes.append("修复示例格式")

            # 4. 美化JSON格式
            if changes:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(agent, f, ensure_ascii=False, indent=2)
                print(f"   ✅ 修复完成: {', '.join(changes)}")
                return True
            else:
                print(f"   ✅ 无需修复: {filepath.name}")
                return True

        except Exception as e:
            print(f"   ❌ 修复失败: {e}")
            return False

    def optimize_structure(self, filepath: Path) -> bool:
        """优化文件结构"""
        try:
            agent, success = self.load_agent(filepath)
            if not success:
                return False

            changes = []
            
            # 1. 优化capabilities格式
            capabilities = agent.get('capabilities', [])
            if isinstance(capabilities, str):
                agent['capabilities'] = [capabilities]
                changes.append("capabilities字符串转数组")
            
            # 2. 优化prompts结构
            prompts = agent.get('prompts', {})
            if isinstance(prompts, str):
                agent['prompts'] = {"general": prompts}
                changes.append("prompts字符串转对象")

            # 3. 优化examples结构
            examples = agent.get('examples', [])
            if examples and isinstance(examples[0], dict):
                for example in examples:
                    # 确保有category字段
                    if 'category' not in example and 'input' in example:
                        example['category'] = 'general'
                        changes.append("添加示例分类")

            # 4. 优化templates结构
            templates = agent.get('templates', {})
            if 'project_scaffold' in templates:
                scaffold = templates['project_scaffold']
                # 确保tech_stack是数组
                if 'tech_stack' in scaffold and isinstance(scaffold['tech_stack'], str):
                    scaffold['tech_stack'] = [scaffold['tech_stack']]
                    changes.append("tech_stack字符串转数组")

            # 5. 添加时间戳
            if 'metadata' not in agent:
                agent['metadata'] = {
                    "created_at": datetime.datetime.now().isoformat(),
                    "version": "1.0.0",
                    "standardized": True
                }
                changes.append("添加元数据")

            if changes:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(agent, f, ensure_ascii=False, indent=2)
                print(f"   ✅ 优化完成: {', '.join(changes)}")
                return True
            else:
                print(f"   ✅ 无需优化: {filepath.name}")
                return True

        except Exception as e:
            print(f"   ❌ 优化失败: {e}")
            return False

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合报告"""
        json_files = list(self.agents_dir.glob("*.json"))
        results = []
        
        for filepath in json_files:
            if filepath.name.startswith("_") or filepath.name.startswith("."):
                continue
                
            agent, success = self.load_agent(filepath)
            if success:
                result = self.deep_check(agent, filepath)
                results.append(result)

        # 统计信息
        total_files = len(results)
        status_counts = {'✅': 0, '⚠️': 0, '🔴': 0}
        total_score = 0
        
        for result in results:
            status_counts[result['status']] += 1
            total_score += result['score']

        report = {
            "generated_at": datetime.datetime.now().isoformat(),
            "summary": {
                "total_files": total_files,
                "excellent": status_counts['✅'],
                "warning": status_counts['⚠️'],
                "error": status_counts['🔴'],
                "average_score": round(total_score / total_files, 1) if total_files > 0 else 0
            },
            "details": results,
            "recommendations": []
        }

        # 生成建议
        if status_counts['🔴'] > 0:
            report["recommendations"].append("需要修复错误文件")
        if status_counts['⚠️'] > 0:
            report["recommendations"].append("需要优化警告文件")
        if report["summary"]["average_score"] < 90:
            report["recommendations"].append("整体标准化程度有待提升")

        return report

    def process_file(self, filepath: Path, operations: List[str]) -> bool:
        """处理单个文件"""
        filename = filepath.name
        
        if 'check' in operations:
            print(f"\n🔍 深度检查: {filename}")
            agent, success = self.load_agent(filepath)
            if success:
                result = self.deep_check(agent, filepath)
                print(f"   状态: {result['status']} (得分: {result['score']})")
                if result['issues']:
                    for issue in result['issues']:
                        print(f"   ⚠️ {issue}")
                if result['warnings']:
                    for warning in result['warnings']:
                        print(f"   💡 {warning}")

        if 'fix' in operations:
            self.auto_fix(filepath)

        if 'optimize' in operations:
            self.optimize_structure(filepath)

        return True

    def process_all_files(self, operations: List[str]) -> None:
        """处理所有文件"""
        json_files = [f for f in self.agents_dir.glob("*.json") 
                     if not f.name.startswith("_") and not f.name.startswith(".")]
        
        print(f"📊 发现 {len(json_files)} 个智能体文件")
        
        for filepath in json_files:
            self.process_file(filepath, operations)

    def load_template(self) -> Dict[str, Any]:
        """加载标准模板"""
        template_path = Path(__file__).parent / "templates" / "agent-template.json"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 模板加载失败: {e}")
            return {}

    def create_agent_interactive(self) -> None:
        """交互式创建新智能体"""
        print("🤖 AI工具人创建器")
        print("=" * 50)
        
        # 获取基本信息
        tech_field = input("请输入技术领域 (如: react, python, java): ").strip()
        if not tech_field:
            print("❌ 技术领域不能为空!")
            return
            
        chinese_name = input("请输入中文名称 (如: React工程师): ").strip()
        if not chinese_name:
            chinese_name = f"{tech_field.title()}工程师"
            
        description = input("请输入描述 (可选): ").strip()
        if not description:
            description = f"专精{tech_field}开发，负责{tech_field}应用的架构设计、开发实现、测试部署"
        
        # 确认信息
        print("\n📋 创建信息确认:")
        print(f"技术领域: {tech_field}")
        print(f"中文名称: {chinese_name}")
        print(f"描述: {description}")
        
        confirm = input("\n确认创建? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ 取消创建")
            return
        
        # 创建智能体
        self.create_agent(tech_field, chinese_name, description)

    def create_agent(self, tech_field: str, chinese_name: str, description: str) -> str:
        """创建智能体配置文件"""
        template = self.load_template()
        if not template:
            print("❌ 模板加载失败，无法创建智能体")
            return ""
        
        # 替换模板中的占位符
        agent_config = self.fill_template(template, tech_field, chinese_name, description)
        
        # 生成文件名
        filename = f"{tech_field.lower()}-engineer-standardized.json"
        filepath = self.agents_dir / filename
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(agent_config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 成功创建: {filename}")
        print(f"📁 文件位置: {filepath}")
        
        # 自动检查新创建的文件
        print("\n🔍 对新创建的文件进行标准化检查...")
        agent, success = self.load_agent(filepath)
        if success:
            result = self.deep_check(agent, filepath)
            print(f"   标准化得分: {result['score']} 分")
            if result['score'] < 100:
                print("   💡 建议运行: python agent-standardization-suite.py all", filename)
        
        return str(filepath)

    def fill_template(self, template: Dict[str, Any], tech_field: str, chinese_name: str, description: str) -> Dict[str, Any]:
        """填充模板内容"""
        config = template.copy()
        
        # 基础信息
        config["name"] = chinese_name
        config["role"] = f"{tech_field.lower()}-engineer"
        config["description"] = description
        
        # 技术栈特定内容
        tech_stack_map = {
            "react": ["React 18+", "Next.js 14+", "TypeScript", "Tailwind CSS", "Zustand", "React Query"],
            "vue": ["Vue 3", "Nuxt 3", "TypeScript", "Pinia", "Vue Router", "Tailwind CSS"],
            "python": ["Python 3.11+", "FastAPI", "Django", "Pandas", "NumPy", "SQLAlchemy"],
            "nodejs": ["Node.js 20+", "Express", "NestJS", "TypeScript", "Prisma", "Socket.io"],
            "java": ["Java 17+", "Spring Boot", "Spring Cloud", "MyBatis", "Maven", "Docker"],
            "go": ["Go 1.21+", "Gin", "Echo", "GORM", "Wire", "Kubernetes"],
            "rust": ["Rust 1.75+", "Tokio", "Actix-web", "Diesel", "Serde", "Cargo"],
            "flutter": ["Flutter 3.16+", "Dart", "GetX", "Provider", "Firebase", "Hive"],
            "angular": ["Angular 17+", "TypeScript", "RxJS", "NgRx", "Angular Material", "Jest"]
        }
        
        # 获取技术栈
        tech_stack = tech_stack_map.get(tech_field.lower(), 
                                     [f"{tech_field.title()}", "相关技术栈", "最佳实践"])
        
        # 更新技术栈
        if "templates" in config and "project_scaffold" in config["templates"]:
            config["templates"]["project_scaffold"]["tech_stack"] = tech_stack
        
        return config

    def list_existing_agents(self) -> None:
        """列出已存在的智能体"""
        print("\n📋 已存在的智能体:")
        try:
            files = [f for f in os.listdir(self.agents_dir) 
                    if f.endswith('-standardized.json')]
            if not files:
                print("   暂无智能体文件")
                return
                
            for i, file in enumerate(files, 1):
                print(f"{i:2d}. {file}")
        except Exception as e:
            print(f"获取文件列表失败: {e}")

def parse_operations(command: str) -> List[str]:
    """解析操作命令"""
    command_map = {
        'all': ['check', 'fix', 'optimize'],
        'report': ['check']
    }
    
    if command in command_map:
        return command_map[command]
    elif '+' in command:
        return command.split('+')
    else:
        return [command]

def main():
    """主函数"""
    agents_dir = Path(__file__).parent.parent / "agents"
    suite = AgentStandardizationSuite(agents_dir)
    
    if len(sys.argv) < 2:
        print("""
🎯 智能体标准化完整套件 - 统一入口

📋 核心功能:
    create                    # 交互式创建新智能体
    check [文件名]             # 详细检查智能体
    fix [文件名]               # 自动修复问题
    optimize [文件名]          # 结构优化
    all [文件名]               # 完整流程(检查+修复+优化)
    report                    # 生成完整报告

📊 批量操作:
    --all-files check         # 批量检查所有文件
    --all-files fix           # 批量修复所有文件
    --all-files optimize      # 批量优化所有文件
    --all-files all           # 批量完整流程
    --all-files report        # 生成完整报告

🎮 交互模式:
    python agent-standardization-suite.py create
    
📝 示例:
    python agent-standardization-suite.py create                 # 创建新智能体
    python agent-standardization-suite.py check react-engineer.json
    python agent-standardization-suite.py all python-ai-engineer.json
    python agent-standardization-suite.py --all-files report
    python agent-standardization-suite.py --all-files fix+optimize
        """)
        return
    
    command = sys.argv[1]
    
    # 创建新智能体
    if command == "create":
        if len(sys.argv) > 2 and sys.argv[2] == "--interactive":
            suite.create_agent_interactive()
        else:
            # 提供创建菜单
            print("🚀 AI工具人创建器")
            print("=" * 30)
            
            while True:
                print("\n请选择操作:")
                print("1. 创建新智能体")
                print("2. 查看已有智能体")
                print("3. 返回主菜单")
                
                choice = input("\n请输入选项 (1-3): ").strip()
                
                if choice == "1":
                    suite.create_agent_interactive()
                elif choice == "2":
                    suite.list_existing_agents()
                elif choice == "3":
                    print("👋 返回主菜单!")
                    break
                else:
                    print("❌ 无效选项，请重新选择")
        return
    
    # 检查是否是--all-files模式
    if len(sys.argv) > 2 and sys.argv[1] == '--all-files':
        sub_command = sys.argv[2]
        
        if sub_command == "create":
            # 批量创建示例智能体
            print("🚀 批量创建示例智能体...")
            examples = [
                ("react", "React工程师", "专精React开发，负责React应用的架构设计、开发实现、测试部署"),
                ("python", "Python工程师", "专精Python开发，负责后端服务、数据处理、AI应用开发"),
                ("nodejs", "Node.js工程师", "专精Node.js开发，负责后端API、微服务、实时应用开发")
            ]
            
            for tech_field, chinese_name, description in examples:
                filepath = suite.agents_dir / f"{tech_field}-engineer-standardized.json"
                if not filepath.exists():
                    suite.create_agent(tech_field, chinese_name, description)
                else:
                    print(f"   ⏭️  {filepath.name} 已存在，跳过")
            return
            
        operations = parse_operations(sub_command)
        if 'report' in operations:
            report = suite.generate_comprehensive_report()
            print(f"\n📊 标准化报告")
            print("=" * 50)
            print(f"总文件数: {report['summary']['total_files']}")
            print(f"优秀: {report['summary']['excellent']} 个")
            print(f"警告: {report['summary']['warning']} 个") 
            print(f"错误: {report['summary']['error']} 个")
            print(f"平均分: {report['summary']['average_score']} 分")
            
            if report['recommendations']:
                print(f"\n💡 建议:")
                for rec in report['recommendations']:
                    print(f"   - {rec}")
            
            # 保存报告
            report_file = suite.agents_dir / "_standardization-report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n📄 报告已保存: {report_file}")
        else:
            suite.process_all_files(operations)
    
    # 处理单个文件
    else:
        operations = parse_operations(command)
        
        if len(sys.argv) > 2:
            file_name = sys.argv[2]
            filepath = agents_dir / file_name
            if filepath.exists():
                suite.process_file(filepath, operations)
                if 'check' in operations or 'report' in operations:
                    report = suite.generate_comprehensive_report()
                    print(f"\n📊 标准化报告已生成")
            else:
                print(f"错误: 文件 {file_name} 不存在")
        else:
            # 如果没有指定文件，处理所有文件
            suite.process_all_files(operations)
            if 'report' in operations or 'check' in operations:
                report = suite.generate_comprehensive_report()
                print(f"\n📊 标准化报告已生成")

if __name__ == "__main__":
    main()