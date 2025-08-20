#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def fix_json_file(file_path):
    """修复JSON文件中的格式问题"""
    try:
        # 读取原始文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析JSON
        data = json.loads(content)
        
        # 重新格式化输出
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        print(f"✅ 已修复: {file_path}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON错误: {file_path} - {e}")
        return False
    except Exception as e:
        print(f"❌ 处理错误: {file_path} - {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # 默认修复cpp-ai-deployment-engineer.json
        files = [".trae/agents/cpp-ai-deployment-engineer.json"]
    
    for file_path in files:
        fix_json_file(file_path)