"""
将 input.py 打包为可执行文件的构建脚本
使用方法: python3 build.py
注意: 在 macOS 上生成的是 .app 应用程序，而非 Windows 的 .exe
"""

import subprocess
import sys

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

def build():
    """执行打包"""
    print("🚀 开始打包自动输入工具...")
    print("-" * 40)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 打包为单个文件
        "--windowed",                   # 不显示终端窗口（GUI 程序）
        "--name", "自动输入工具",          # 输出文件名
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
        print("📦 可执行文件: dist/自动输入工具")
        print("   (macOS 上为 Unix 可执行文件或 .app 应用)")
    else:
        print("-" * 40)
        print("❌ 打包失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    if check_pyinstaller():
        build()