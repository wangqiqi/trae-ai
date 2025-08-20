#!/usr/bin/env python3
"""
批量优化智能体文件脚本
功能：
1. 转换examples格式 (scenario→input, description→output)
2. 补充缺失的标准字段
3. 保持原有内容，仅标准化格式

用法: python batch_optimize.py [文件名]  # 优化单个文件
       python batch_optimize.py --all    # 优化所有文件
"""

import json
import os
import sys
from pathlib import Path

class BatchOptimizer:
    def __init__(self, agents_dir):
        self.agents_dir = Path(agents_dir)
        self.standard_fields = [
            'name', 'role', 'description', 'capabilities',
            'prompts', 'output_format', 'examples',
            'templates', 'review_checkpoints'
        ]
        
    def optimize_single_file(self, file_path):
        """优化单个文件"""
        print(f"🔄 优化文件: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1. 转换examples格式
            if 'examples' in data and isinstance(data['examples'], list):
                new_examples = []
                for example in data['examples']:
                    if isinstance(example, dict):
                        new_example = {}
                        # 转换字段名
                        if 'scenario' in example:
                            new_example['input'] = example['scenario']
                        if 'description' in example:
                            new_example['output'] = example['description']
                        # 保留其他字段
                        for key, value in example.items():
                            if key not in ['scenario', 'description']:
                                new_example[key] = value
                        new_examples.append(new_example)
                data['examples'] = new_examples
                print(f"   ✅ examples格式已转换")
            
            # 2. 补充缺失的标准字段
            missing_fields = []
            for field in self.standard_fields:
                if field not in data:
                    missing_fields.append(field)
                    # 根据字段类型提供合适的默认值
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
                print(f"   ✅ 补充字段: {', '.join(missing_fields)}")
            
            # 3. 重命名字段 (core_responsibilities → capabilities)
            if 'core_responsibilities' in data:
                if 'capabilities' not in data:
                    data['capabilities'] = data['core_responsibilities']
                del data['core_responsibilities']
                print(f"   ✅ 重命名: core_responsibilities → capabilities")
            
            # 4. 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return False
    
    def optimize_all_files(self):
        """优化所有JSON文件"""
        json_files = list(self.agents_dir.glob('*.json'))
        print(f"📊 发现 {len(json_files)} 个文件需要优化")
        
        success_count = 0
        for json_file in json_files:
            if self.optimize_single_file(json_file):
                success_count += 1
        
        print(f"\n✅ 完成: {success_count}/{len(json_files)} 个文件优化成功")
        return success_count
    
    def preview_changes(self, file_path):
        """预览将要做的更改"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📋 文件: {file_path.name}")
            
            # 检查examples格式
            if 'examples' in data and isinstance(data['examples'], list) and len(data['examples']) > 0:
                example = data['examples'][0]
                if isinstance(example, dict) and 'scenario' in example:
                    print("   🔧 examples格式: scenario/description → input/output")
                    print(f"   原格式: {{'scenario': '{example.get('scenario', '')}', 'description': '{example.get('description', '')}'}}")
                    print(f"   新格式: {{'input': '{example.get('scenario', '')}', 'output': '{example.get('description', '')}'}}")
            
            # 检查缺失字段
            missing = [f for f in self.standard_fields if f not in data]
            if missing:
                print(f"   🔧 缺失字段: {', '.join(missing)}")
            
            # 检查字段命名
            if 'core_responsibilities' in data:
                print("   🔧 字段重命名: core_responsibilities → capabilities")
            
            if not missing and 'examples' not in data and 'core_responsibilities' not in data:
                print("   ✅ 文件已优化，无需更改")
                
        except Exception as e:
            print(f"   ❌ 读取错误: {e}")

if __name__ == "__main__":
    agents_dir = Path(__file__).parent.parent / "agents"
    optimizer = BatchOptimizer(agents_dir)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            optimizer.optimize_all_files()
        elif sys.argv[1] == "--preview" and len(sys.argv) > 2:
            file_name = sys.argv[2]
            file_path = agents_dir / file_name
            if file_path.exists():
                optimizer.preview_changes(file_path)
            else:
                print(f"文件 {file_name} 不存在")
        else:
            file_name = sys.argv[1]
            file_path = agents_dir / file_name
            if file_path.exists():
                optimizer.optimize_single_file(file_path)
            else:
                print(f"文件 {file_name} 不存在")
    else:
        print("用法:")
        print("  python batch_optimize.py 文件名.json    # 优化单个文件")
        print("  python batch_optimize.py --all         # 优化所有文件")
        print("  python batch_optimize.py --preview 文件名.json  # 预览更改")