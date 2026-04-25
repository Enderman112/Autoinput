"""
打包为 Windows EXE 的构建脚本
使用方法: 在 Windows 系统上运行 python build_exe.py
"""

import subprocess
import sys
import platform

def check_pyinstaller():
    """检查 PyInstaller 是否已安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller 已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("⚠️  PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安装完成")
        return True

def build_exe():
    """执行打包"""
    print("-" * 40)
    print("🚀 开始打包为 Windows EXE...")
    print("-" * 40)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 打包为单个文件
        "--windowed",                   # 不显示终端窗口（GUI 程序）
        "--name", "AutoInput",          # 输出文件名
        "--icon", "NONE",               # 无图标
        "--clean",                      # 清理临时文件
        "--noconfirm",                  # 不确认覆盖
        "input.py"
    ]

    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 40)

    result = subprocess.run(cmd, cwd=".")

    if result.returncode == 0:
        print("-" * 40)
        print("🎉 打包成功！")
        print("📁 输出目录: dist/")
        print("📦 可执行文件: dist/AutoInput.exe")
    else:
        print("-" * 40)
        print("❌ 打包失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    current_os = platform.system()
    
    if current_os != "Windows":
        print("⚠️  注意: 当前系统是 macOS，无法直接生成 .exe 文件")
        print("   PyInstaller 只能在目标系统上打包对应格式的可执行文件")
        print("-" * 40)
        print("   要生成 .exe 文件，请:")
        print("   1. 将 input.py 和此脚本复制到 Windows 电脑")
        print("   2. 在 Windows 上运行: python build_exe.py")
        print("-" * 40)
        
        # 仍然尝试打包（会生成 macOS 可执行文件）
        print("📦 当前将生成 macOS 可执行文件到 dist/ 目录")
        print("-" * 40)
    
    check_pyinstaller()
    build_exe()