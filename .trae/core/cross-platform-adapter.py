#!/usr/bin/env python3
# 🌍 .trae 跨平台命令适配器
# 自动识别系统并返回正确命令

import platform
import os
import subprocess

class CrossPlatformAdapter:
    def __init__(self):
        self.system = platform.system()
        self.commands = {
            "Windows": {
                "create_dir": "New-Item -ItemType Directory -Path '{path}' -Force",
                "create_file": "New-Item -ItemType File -Path '{path}' -Force",
                "remove": "Remove-Item -Path '{path}' -Recurse -Force",
                "copy": "Copy-Item -Path '{src}' -Destination '{dst}' -Recurse -Force",
                "list_dir": "Get-ChildItem -Path '{path}'",
                "shell": "powershell"
            },
            "Linux": {
                "create_dir": "mkdir -p '{path}'",
                "create_file": "touch '{path}'",
                "remove": "rm -rf '{path}'",
                "copy": "cp -r '{src}' '{dst}'",
                "list_dir": "ls -la '{path}'",
                "shell": "bash"
            },
            "Darwin": {  # macOS
                "create_dir": "mkdir -p '{path}'",
                "create_file": "touch '{path}'",
                "remove": "rm -rf '{path}'",
                "copy": "cp -r '{src}' '{dst}'",
                "list_dir": "ls -la '{path}'",
                "shell": "zsh"
            }
        }
    
    def get_command(self, action, **kwargs):
        """获取当前系统的正确命令"""
        if self.system not in self.commands:
            raise ValueError(f"不支持的操作系统: {self.system}")
        
        cmd_template = self.commands[self.system][action]
        return cmd_template.format(**kwargs)
    
    def get_system_info(self):
        """获取系统详细信息"""
        return {
            "system": self.system,
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    
    def execute_command(self, action, **kwargs):
        """执行跨平台命令"""
        cmd = self.get_command(action, **kwargs)
        
        if self.system == "Windows":
            # Windows 使用 PowerShell
            result = subprocess.run(["powershell", "-Command", cmd], 
                                  capture_output=True, text=True)
        else:
            # Linux/Mac 使用 shell
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        return {
            "command": cmd,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

# 使用示例
if __name__ == "__main__":
    adapter = CrossPlatformAdapter()
    
    print("🌍 系统识别结果:")
    print("=" * 30)
    info = adapter.get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print(f"\n📋 当前系统命令示例:")
    print(f"创建目录: {adapter.get_command('create_dir', path='test-dir')}")
    print(f"创建文件: {adapter.get_command('create_file', path='test.txt')}")
    print(f"删除文件: {adapter.get_command('remove', path='old-file')}")