#!/usr/bin/env python3
# 🧹 .trae 智能清理工具
# 安全识别并清理不需要的文件

import os
import shutil
from datetime import datetime

class SmartCleanup:
    def __init__(self):
        self.trae_path = ".trae"
        self.cleanup_candidates = {
            "old_principles": {
                "files": ["principles.md"],
                "reason": "已更新为principles.md",
                "action": "backup_and_remove"
            },
            "broken_scripts": {
                "files": ["tools/quick-checklist.ps1"],
                "reason": "编码问题，已有fixed版本",
                "action": "backup_and_remove"
            },
            "redundant_starters": {
                "files": ["start-principle-mode.bat"],
                "reason": "功能重复，可用start.bat替代",
                "action": "backup_and_remove"
            }
        }
        self.backup_dir = f".trae/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def analyze_system(self):
        """分析当前系统状态"""
        print("🔍 开始智能分析...")
        
        found_files = []
        for category, info in self.cleanup_candidates.items():
            for file_path in info["files"]:
                full_path = os.path.join(self.trae_path, file_path)
                if os.path.exists(full_path):
                    found_files.append({
                        "path": full_path,
                        "category": category,
                        "reason": info["reason"],
                        "size": os.path.getsize(full_path)
                    })
        
        return found_files
    
    def create_backup(self, files_to_cleanup):
        """创建备份"""
        if not files_to_cleanup:
            return
        
        os.makedirs(self.backup_dir, exist_ok=True)
        print(f"📁 创建备份目录: {self.backup_dir}")
        
        for file_info in files_to_cleanup:
            src_path = file_info["path"]
            dst_path = os.path.join(self.backup_dir, os.path.basename(src_path))
            
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
            else:
                shutil.copytree(src_path, dst_path)
            
            print(f"✅ 已备份: {os.path.basename(src_path)}")
    
    def safe_cleanup(self, files_to_cleanup):
        """安全清理文件"""
        if not files_to_cleanup:
            print("🎉 没有需要清理的文件")
            return
        
        print("\n🧹 准备清理以下文件:")
        for i, file_info in enumerate(files_to_cleanup, 1):
            print(f"{i}. {file_info['path']} ({file_info['size']} bytes)")
            print(f"   原因: {file_info['reason']}")
        
        # 模拟确认（实际使用时需要用户确认）
        print(f"\n📋 已创建备份，可安全清理")
        print(f"🔄 如需恢复，备份在: {self.backup_dir}")
        
        return files_to_cleanup
    
    def run_cleanup_analysis(self):
        """运行完整清理分析"""
        print("🧠 .trae 智能清理分析")
        print("=" * 40)
        
        # 分析系统
        files_to_cleanup = self.analyze_system()
        
        if files_to_cleanup:
            # 创建备份
            self.create_backup(files_to_cleanup)
            
            # 安全清理
            return self.safe_cleanup(files_to_cleanup)
        else:
            print("🎉 系统已优化，无需清理")
            return []

# 使用示例
if __name__ == "__main__":
    cleanup = SmartCleanup()
    result = cleanup.run_cleanup_analysis()
    
    if result:
        print(f"\n📊 发现 {len(result)} 个可清理文件")
    else:
        print("\n✅ 系统状态良好")