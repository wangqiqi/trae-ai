#!/usr/bin/env python3
"""
控制台工具 - 彩色输出和格式化
"""
import sys
from typing import Optional, Any

class Colors:
    """终端颜色常量"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def colored(text: str, color: str) -> str:
    """给文本添加颜色"""
    return f"{color}{text}{Colors.RESET}"

def print_success(text: str):
    """打印成功消息（绿色）"""
    print(colored(f"✅ {text}", Colors.GREEN))

def print_error(text: str):
    """打印错误消息（红色）"""
    print(colored(f"❌ {text}", Colors.RED), file=sys.stderr)

def print_warning(text: str):
    """打印警告消息（黄色）"""
    print(colored(f"⚠️  {text}", Colors.YELLOW))

def print_info(text: str):
    """打印信息消息（蓝色）"""
    print(colored(f"ℹ️  {text}", Colors.BLUE))

def print_header(text: str):
    """打印标题（加粗）"""
    print(colored(f"\n{text}", Colors.BOLD + Colors.CYAN))
    print(colored("=" * len(text), Colors.CYAN))

def print_section(title: str):
    """打印区域标题"""
    print(colored(f"\n📋 {title}", Colors.BOLD + Colors.MAGENTA))
    print(colored("─" * 40, Colors.DIM))

def print_banner(title: str, subtitle: Optional[str] = None):
    """打印横幅"""
    print(colored(f"\n{'=' * 60", Colors.CYAN + Colors.BOLD)
    print(colored(f"  {title}", Colors.CYAN + Colors.BOLD))
    if subtitle:
        print(colored(f"  {subtitle}", Colors.DIM))
    print(colored('=' * 60, Colors.CYAN))

def print_list(items: list, bullet: str = "•"):
    """打印列表"""
    for item in items:
        print(colored(f"  {bullet} {item}"))

def print_dict(data: dict, indent: int = 0):
    """打印字典"""
    for key, value in data.items():
        indent_str = "  " * indent
        if isinstance(value, dict):
            print(f"{indent_str}{colored(key + ':', Colors.BOLD)}")
            print_dict(value, indent + 1)
        else:
            print(f"{indent_str}{colored(key + ':', Colors.CYAN)} {value}")

def print_progress(current: int, total: int, width: int = 30):
    """打印进度条"""
    progress = int(width * current / total)
    bar = '█' * progress + '░' * (width - progress)
    percent = int(100 * current / total)
    print(f"\r{colored(f'[{bar}]', Colors.CYAN)} {colored(f'{percent}%', Colors.BOLD)}", end='', flush=True)
    if current == total:
        print()

def print_divider():
    """打印分隔线"""
    print(colored("─" * 60, Colors.DIM))
