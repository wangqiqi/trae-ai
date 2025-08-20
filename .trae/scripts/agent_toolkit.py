#!/usr/bin/env python3
"""
智能体文件统一工具包
支持 check, fix, optimize 三种操作，可组合使用

用法:
    python agent_toolkit.py check [文件名]          # 检查文件状态
    python agent_toolkit.py fix [文件名]            # 修复JSON格式
    python agent_toolkit.py optimize [文件名]       # 优化文件结构
    python agent_toolkit.py all [文件名]            # 执行所有操作
    python agent_toolkit.py check+fix [文件名]      # 组合操作
    python agent_toolkit.py --all-files check       # 对所有文件执行操作
"""

import json
import os
import sys
from pathlib import Path

class AgentToolkit:
    def __init__(self, agents_dir):
        self.agents_dir = Path(agents_dir)
        self.standard_fields = [
            'name', 'role', 'description', 'capabilities',
            'prompts', 'output_format', 'examples',
            'templates', 'review_checkpoints'
        ]
    
    def check_file(self, file_path):
        """检查单个文件状态"""
        result = {
            'file': file_path.name,
            'status': '✅',
            'issues': [],
            'missing_fields': [],
            'json_valid': True,
            'can_fix': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)
            
            # 检查必需字段
            for field in self.standard_fields:
                if field not in data:
                    result['missing_fields'].append(field)
                    result['status'] = '⚠️'
                    result['can_fix'].append(f"补充缺失字段: {field}")
            
            # 检查examples格式
            if 'examples' in data:
                examples = data['examples']
                if isinstance(examples, list) and len(examples) > 0:
                    first_example = examples[0]
                    if isinstance(first_example, dict) and 'input' not in first_example:
                        if 'scenario' in first_example:
                            result['issues'].append("examples格式需转换: scenario→input")
                            result['status'] = '⚠️'
                            result['can_fix'].append("转换examples格式")
            
            # 检查字段命名
            if 'core_responsibilities' in data:
                result['issues'].append("字段命名需修复: core_responsibilities→capabilities")
                result['status'] = '🔴'
                result['can_fix'].append("重命名字段")
            
            # 检查JSON格式
            lines = content.split('\n')
            if len(lines) > 2 and not lines[1].startswith('  '):
                result['issues'].append("JSON格式需美化")
                result['can_fix'].append("修复JSON格式")
            
        except json.JSONDecodeError as e:
            result['json_valid'] = False
            result['status'] = '❌'
            result['issues'].append(f"JSON格式错误: {e}")
            result['can_fix'].append("修复JSON格式")
        except Exception as e:
            result['status'] = '❌'
            result['issues'].append(f"文件读取错误: {e}")
        
        return result
    
    def fix_json_format(self, file_path):
        """修复JSON格式"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析并重新格式化
            data = json.loads(content)
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            
            print(f"   ✅ JSON格式已修复: {file_path.name}")
            return True
            
        except Exception as e:
            print(f"   ❌ 修复失败: {e}")
            return False
    
    def optimize_structure(self, file_path):
        """优化文件结构"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            changes = []
            
            # 1. 转换examples格式
            if 'examples' in data and isinstance(data['examples'], list):
                new_examples = []
                for example in data['examples']:
                    if isinstance(example, dict):
                        new_example = {}
                        if 'scenario' in example:
                            new_example['input'] = example['scenario']
                            changes.append("scenario→input")
                        if 'description' in example:
                            new_example['output'] = example['description']
                            changes.append("description→output")
                        for key, value in example.items():
                            if key not in ['scenario', 'description']:
                                new_example[key] = value
                        new_examples.append(new_example)
                if changes:
                    data['examples'] = new_examples
            
            # 2. 补充缺失字段
            missing_fields = []
            for field in self.standard_fields:
                if field not in data:
                    missing_fields.append(field)
                    if field == 'capabilities':
                        data[field] = ["待补充能力列表"]
                    elif field == 'prompts':
                        data[field] = {"general": "待补充提示词"}
                    elif field == 'output_format':
                        data[field] = {"main": "待补充输出格式"}
                    elif field == 'examples':
                        data[field] = [{"input": "示例输入", "output": "示例输出"}]
                    elif field == 'templates':
                        data[field] = {"basic": "templates/basic/"}
                    elif field == 'review_checkpoints':
                        data[field] = ["待补充检查点"]
                    else:
                        data[field] = f"待补充{field}"
            
            if missing_fields:
                changes.append(f"补充字段: {', '.join(missing_fields)}")
            
            # 3. 重命名字段
            if 'core_responsibilities' in data:
                if 'capabilities' not in data:
                    data['capabilities'] = data['core_responsibilities']
                del data['core_responsibilities']
                changes.append("core_responsibilities→capabilities")
            
            # 4. 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            if changes:
                print(f"   ✅ 优化完成: {', '.join(changes)}")
            else:
                print(f"   ✅ 无需优化: {file_path.name}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 优化失败: {e}")
            return False
    
    def process_file(self, file_path, operations):
        """处理单个文件的指定操作"""
        print(f"\n🔄 处理: {file_path.name}")
        
        if 'check' in operations:
            result = self.check_file(file_path)
            print(f"   {result['status']} 检查结果:")
            if result['issues']:
                for issue in result['issues']:
                    print(f"      - {issue}")
            if result['missing_fields']:
                print(f"      缺失字段: {', '.join(result['missing_fields'])}")
        
        if 'fix' in operations and file_path.exists():
            self.fix_json_format(file_path)
        
        if 'optimize' in operations and file_path.exists():
            self.optimize_structure(file_path)
    
    def process_all_files(self, operations):
        """处理所有JSON文件"""
        json_files = list(self.agents_dir.glob('*.json'))
        print(f"📊 发现 {len(json_files)} 个文件")
        
        for json_file in json_files:
            self.process_file(json_file, operations)
    
    def generate_summary(self):
        """生成检查汇总"""
        json_files = list(self.agents_dir.glob('*.json'))
        results = [self.check_file(f) for f in json_files]
        
        print("\n🎯 智能体文件状态汇总")
        print("=" * 50)
        
        status_counts = {'✅': 0, '⚠️': 0, '🔴': 0, '❌': 0}
        
        for result in results:
            status = result['status']
            status_counts[status] += 1
            print(f"{status} {result['file']}")
        
        print(f"\n📊 统计:")
        print(f"总文件数: {len(results)}")
        print(f"✅ 优秀: {status_counts['✅']} 个")
        print(f"⚠️ 需优化: {status_counts['⚠️']} 个")
        print(f"🔴 需修复: {status_counts['🔴']} 个")
        print(f"❌ 错误: {status_counts['❌']} 个")

def parse_operations(command):
    """解析操作命令"""
    if command == 'all':
        return ['check', 'fix', 'optimize']
    elif '+' in command:
        return command.split('+')
    else:
        return [command]

def main():
    agents_dir = Path(__file__).parent.parent / "agents"
    
    if len(sys.argv) < 2:
        print("""
智能体文件统一工具包

用法:
    python agent_toolkit.py check [文件名]          # 检查文件状态
    python agent_toolkit.py fix [文件名]            # 修复JSON格式
    python agent_toolkit.py optimize [文件名]       # 优化文件结构
    python agent_toolkit.py all [文件名]            # 执行所有操作
    python agent_toolkit.py check+fix [文件名]      # 组合操作
    python agent_toolkit.py --all-files check       # 对所有文件执行操作
    
示例:
    python agent_toolkit.py check angular-engineer.json
    python agent_toolkit.py fix angular-engineer.json
    python agent_toolkit.py optimize angular-engineer.json
    python agent_toolkit.py all angular-engineer.json
    python agent_toolkit.py check+fix+optimize angular-engineer.json
    python agent_toolkit.py --all-files check
    python agent_toolkit.py --all-files all
        """)
        return
    
    toolkit = AgentToolkit(agents_dir)
    
    # 检查是否是--all-files模式
    if sys.argv[1] == '--all-files':
        if len(sys.argv) < 3:
            print("错误: --all-files 需要指定操作")
            return
        
        operations = parse_operations(sys.argv[2])
        toolkit.process_all_files(operations)
        
        if 'check' in operations:
            toolkit.generate_summary()
    
    # 处理单个文件
    else:
        command = sys.argv[1]
        operations = parse_operations(command)
        
        if len(sys.argv) > 2:
            file_name = sys.argv[2]
            file_path = agents_dir / file_name
            if file_path.exists():
                toolkit.process_file(file_path, operations)
                if 'check' in operations:
                    toolkit.generate_summary()
            else:
                print(f"错误: 文件 {file_name} 不存在")
        else:
            # 如果没有指定文件，处理所有文件
            toolkit.process_all_files(operations)
            if 'check' in operations:
                toolkit.generate_summary()

if __name__ == "__main__":
    main()