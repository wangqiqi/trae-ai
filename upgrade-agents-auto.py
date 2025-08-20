#!/usr/bin/env python3
"""
自动批量升级 .trae\agents2 目录下的所有智能体到v2.0标准
无需用户确认，直接执行升级
"""

import os
import json
import shutil
from pathlib import Path
import sys
from datetime import datetime

class AutoAgentUpgrader:
    def __init__(self, agents_dir):
        self.agents_dir = Path(agents_dir)
        self.backup_dir = self.agents_dir / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def scan_agents(self):
        """扫描所有需要升级的智能体文件"""
        agents = []
        for file in self.agents_dir.glob("*-engineer-v2.json"):
            if file.is_file():
                agents.append(file)
        return agents
    
    def check_compliance_direct(self, agent_file):
        """直接检查文件内容判断合规性"""
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必需字段
            required_fields = ["required", "lifecycle", "quality"]
            missing = []
            
            for field in required_fields:
                if field not in data:
                    missing.append(field)
            
            score = 100 - (len(missing) * 15)
            return {
                "file": agent_file,
                "score": max(score, 0),
                "compliant": len(missing) == 0,
                "missing": missing
            }
        except Exception as e:
            return {
                "file": agent_file,
                "score": 0,
                "compliant": False,
                "error": str(e)
            }
    
    def backup_agents(self, agents):
        """备份原始文件"""
        if not agents:
            return
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"[备份] 创建备份目录: {self.backup_dir}")
        
        for agent_file in agents:
            backup_file = self.backup_dir / agent_file.name
            shutil.copy2(agent_file, backup_file)
            print(f"[备份] 已备份: {agent_file.name}")
    
    def extract_tech_stack(self, agent_file):
        """从文件名提取技术栈"""
        name = agent_file.stem
        tech_stack = name.replace("-engineer-v2", "")
        return tech_stack
    
    def build_agent_content(self, tech_stack):
        """构建符合v2.0标准的智能体内容"""
        # 根据技术栈定制内容
        tech_configs = {
            "angular": {
                "primary_language": "TypeScript",
                "frameworks": ["Angular", "RxJS", "NgRx"],
                "tools": ["Angular CLI", "Webpack", "Jest"]
            },
            "react": {
                "primary_language": "JavaScript",
                "frameworks": ["React", "Redux", "React Router"],
                "tools": ["Create React App", "Webpack", "Jest"]
            },
            "vue": {
                "primary_language": "JavaScript",
                "frameworks": ["Vue.js", "Vuex", "Vue Router"],
                "tools": ["Vue CLI", "Webpack", "Jest"]
            },
            "python": {
                "primary_language": "Python",
                "frameworks": ["Django", "Flask", "FastAPI"],
                "tools": ["pip", "pytest", "black"]
            },
            "go": {
                "primary_language": "Go",
                "frameworks": ["Gin", "Echo", "Fiber"],
                "tools": ["go mod", "go test", "gofmt"]
            },
            "java": {
                "primary_language": "Java",
                "frameworks": ["Spring Boot", "Spring Cloud", "Hibernate"],
                "tools": ["Maven", "Gradle", "JUnit"]
            },
            "nodejs": {
                "primary_language": "JavaScript",
                "frameworks": ["Express", "Koa", "NestJS"],
                "tools": ["npm", "yarn", "jest"]
            },
            "rust": {
                "primary_language": "Rust",
                "frameworks": ["Actix", "Rocket", "Tide"],
                "tools": ["cargo", "rustfmt", "clippy"]
            },
            "flutter": {
                "primary_language": "Dart",
                "frameworks": ["Flutter", "Provider", "Bloc"],
                "tools": ["flutter", "dart", "flutter_test"]
            },
            "devops": {
                "primary_language": "YAML",
                "frameworks": ["Kubernetes", "Terraform", "Ansible"],
                "tools": ["docker", "kubectl", "helm"]
            }
        }
        
        # 默认配置
        config = tech_configs.get(tech_stack, {
            "primary_language": tech_stack.title(),
            "frameworks": [f"{tech_stack.title()}"],
            "tools": ["git", "docker"]
        })
        
        return {
            "schema_version": "2.0",
            "agent_info": {
                "name": f"{tech_stack.title()}工程师",
                "description": f"专精{tech_stack}的现代化开发专家，具备全栈开发能力",
                "version": "2.0.0",
                "author": "AI升级系统"
            },
            "technical_stack": {
                "primary_language": config["primary_language"],
                "frameworks": config["frameworks"],
                "tools": config["tools"],
                "version_constraint": ">=1.0.0"
            },
            "required": {
                "role_name": f"{tech_stack.title()}工程师",
                "expertise": [
                    f"{tech_stack}核心开发",
                    "现代化工程实践",
                    "代码质量保证",
                    "性能优化",
                    "安全防护"
                ],
                "mandatory_tools": [
                    "代码编辑器/IDE",
                    "版本控制(Git)",
                    "调试工具",
                    "测试框架",
                    "构建工具"
                ],
                "constraints": [
                    "遵循官方最佳实践",
                    "保证代码质量和可维护性",
                    "及时文档化和知识分享",
                    "遵守安全开发规范"
                ]
            },
            "lifecycle": {
                "project_phases": [
                    "需求分析与设计",
                    "技术方案制定",
                    "代码开发与实现",
                    "测试验证与质量保证",
                    "部署发布与运维",
                    "监控告警与优化",
                    "文档编写与知识传承"
                ],
                "deployment_strategy": "滚动部署",
                "environments": ["开发环境", "测试环境", "预生产环境", "生产环境"],
                "rollback_plan": "蓝绿部署+快速回滚",
                "maintenance_plan": "定期更新+安全补丁"
            },
            "quality": {
                "code_standards": f"{tech_stack}官方最佳实践+团队规范",
                "testing_requirements": [
                    "单元测试覆盖率>80%",
                    "集成测试覆盖核心业务流程",
                    "E2E测试覆盖用户关键路径",
                    "性能测试确保系统稳定性"
                ],
                "review_process": "代码审查+自动化检查+同行评审",
                "documentation": "代码注释+API文档+架构说明+用户手册",
                "quality_gates": [
                    "代码规范检查通过",
                    "所有测试用例通过",
                    "性能指标达标",
                    "安全扫描无高危漏洞"
                ]
            },
            "infrastructure": {
                "cloud_provider": "支持多云部署(AWS/GCP/Azure)",
                "container_tools": ["Docker", "Kubernetes", "Helm"],
                "monitoring": ["Prometheus", "Grafana", "ELK Stack"],
                "logging": ["结构化日志", "集中式日志管理", "实时日志分析"],
                "cicd": ["GitHub Actions", "GitLab CI", "Jenkins"]
            },
            "observability": {
                "metrics": ["业务指标", "技术指标", "用户体验指标"],
                "tracing": ["分布式链路追踪", "错误追踪", "性能剖析"],
                "alerts": ["智能告警", "异常检测", "容量预警"],
                "dashboards": ["业务仪表板", "技术监控面板", "用户行为分析"]
            },
            "security": {
                "dependency_scanning": True,
                "vulnerability_management": True,
                "compliance_standards": ["SOC2", "ISO27001", "GDPR"],
                "security_testing": ["静态代码分析", "动态安全测试", "渗透测试"],
                "access_control": ["身份认证", "权限管理", "审计日志"]
            }
        }
    
    def upgrade_all(self):
        """执行自动批量升级"""
        print("[自动升级] 开始批量升级智能体到v2.0标准...")
        print("=" * 60)
        
        # 1. 扫描文件
        agents = self.scan_agents()
        if not agents:
            print("[警告] 没有找到需要升级的智能体文件")
            return
        
        print(f"[统计] 发现 {len(agents)} 个智能体文件")
        
        # 2. 检查当前状态
        need_upgrade = []
        print("\n[检查] 当前合规性状态:")
        print("-" * 40)
        
        for agent_file in agents:
            result = self.check_compliance_direct(agent_file)
            score = result.get("score", 0)
            compliant = result.get("compliant", False)
            
            status = "[合规]" if compliant else "[需升级]"
            print(f"  {agent_file.name}: {score}分 {status}")
            
            if not compliant:
                need_upgrade.append(agent_file)
        
        if not need_upgrade:
            print("\n[完成] 所有智能体已经是100分合规版本！")
            return
        
        print(f"\n[计划] 即将升级 {len(need_upgrade)} 个智能体")
        
        # 3. 备份原始文件
        self.backup_agents(need_upgrade)
        
        # 4. 自动升级（无需确认）
        success_count = 0
        print("\n[升级] 开始自动升级...")
        print("-" * 40)
        
        for i, agent_file in enumerate(need_upgrade, 1):
            print(f"[{i:2d}/{len(need_upgrade):2d}] 升级: {agent_file.name}")
            
            # 重新生成
            tech_stack = self.extract_tech_stack(agent_file)
            new_content = self.build_agent_content(tech_stack)
            
            try:
                with open(agent_file, 'w', encoding='utf-8') as f:
                    json.dump(new_content, f, indent=2, ensure_ascii=False)
                
                # 验证结果
                result = self.check_compliance_direct(agent_file)
                score = result.get("score", 0)
                compliant = result.get("compliant", False)
                
                if compliant and score == 100:
                    success_count += 1
                    print(f"    [成功] 升级到100分合规版本 ✓")
                else:
                    print(f"    [警告] 升级后分数: {score}分")
                    
            except Exception as e:
                print(f"    [失败] 错误: {str(e)}")
        
        # 5. 最终统计
        print("\n" + "=" * 60)
        print("[总结] 自动升级完成:")
        print(f"   总文件数: {len(agents)}")
        print(f"   升级成功: {success_count}")
        print(f"   备份位置: {self.backup_dir}")
        
        if success_count == len(need_upgrade):
            print("\n🎉 所有智能体已成功升级到v2.0标准！")
        else:
            print(f"\n⚠️  {len(need_upgrade) - success_count} 个文件需要手动处理")

def main():
    agents_dir = "e:\\study\\learn_trae\\.trae\\agents2"
    
    if not os.path.exists(agents_dir):
        print(f"[错误] 智能体目录不存在: {agents_dir}")
        return
    
    upgrader = AutoAgentUpgrader(agents_dir)
    upgrader.upgrade_all()

if __name__ == "__main__":
    main()