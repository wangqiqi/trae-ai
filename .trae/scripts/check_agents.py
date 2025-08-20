#!/usr/bin/env python3
"""
智能体文件统一性检查脚本
用法: python check_agents.py
"""

import json
import os
from pathlib import Path

class AgentChecker:
    def __init__(self, agents_dir):
        self.agents_dir = Path(agents_dir)
        self.required_fields = [
            'name', 'role', 'description', 'capabilities',
            'prompts', 'output_format', 'examples',
            'templates', 'review_checkpoints'
        ]
        
    def check_all_agents(self):
        """检查所有智能体文件"""
        results = []
        for json_file in self.agents_dir.glob('*.json'):
            result = self.check_single_agent(json_file)
            results.append(result)
        return results
    
    def check_single_agent(self, file_path):
        """检查单个智能体文件"""
        result = {
            'file': file_path.name,
            'status': '✅',
            'issues': [],
            'missing_fields': [],
            'json_valid': True
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必需字段
            for field in self.required_fields:
                if field not in data:
                    result['missing_fields'].append(field)
                    result['status'] = '⚠️'
            
            # 检查examples格式
            if 'examples' in data:
                examples = data['examples']
                if isinstance(examples, list) and len(examples) > 0:
                    first_example = examples[0]
                    if not isinstance(first_example, dict) or 'input' not in first_example:
                        result['issues'].append("examples格式应为对象数组")
                        result['status'] = '⚠️'
            
            # 检查字段命名
            if 'core_responsibilities' in data:
                result['issues'].append("应使用'capabilities'而非'core_responsibilities'")
                result['status'] = '🔴'
            
        except json.JSONDecodeError as e:
            result['json_valid'] = False
            result['status'] = '❌'
            result['issues'].append(f"JSON格式错误: {e}")
        except Exception as e:
            result['status'] = '❌'
            result['issues'].append(f"文件读取错误: {e}")
        
        return result
    
    def generate_report(self):
        """生成检查报告"""
        results = self.check_all_agents()
        
        print("🎯 智能体文件检查报告")
        print("=" * 50)
        
        status_counts = {'✅': 0, '⚠️': 0, '🔴': 0, '❌': 0}
        
        for result in results:
            status = result['status']
            status_counts[status] += 1
            
            print(f"{status} {result['file']}")
            if result['issues'] or result['missing_fields']:
                if result['missing_fields']:
                    print(f"   缺失字段: {', '.join(result['missing_fields'])}")
                if result['issues']:
                    print(f"   问题: {'; '.join(result['issues'])}")
            print()
        
        print("📊 统计汇总")
        print(f"总文件数: {len(results)}")
        print(f"✅ 优秀: {status_counts['✅']} 个")
        print(f"⚠️ 需优化: {status_counts['⚠️']} 个")
        print(f"🔴 需修复: {status_counts['🔴']} 个")
        print(f"❌ 错误: {status_counts['❌']} 个")

if __name__ == "__main__":
    import sys
    
    # 默认检查当前目录下的agents文件夹
    agents_dir = Path(__file__).parent.parent / "agents"
    
    if not agents_dir.exists():
        print(f"错误: 找不到目录 {agents_dir}")
        sys.exit(1)
    
    checker = AgentChecker(agents_dir)
    checker.generate_report()