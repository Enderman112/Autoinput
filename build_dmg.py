"""
将 PyInstaller 生成的 .app 打包为 DMG 安装包
DMG 中包含应用程序和"应用程序"文件夹的快捷方式，方便拖拽安装

使用方法:
  1. 先运行 build.py 生成 .app
  2. 再运行 python3 build_dmg.py 生成 DMG
"""

import subprocess
import sys
import os
import shutil

APP_NAME = "自动输入工具"
DMG_NAME = "自动输入工具安装包"
DMG_VOLUME_NAME = "自动输入工具"
DMG_OUTPUT = f"dist/{DMG_NAME}.dmg"
APP_PATH = f"dist/{APP_NAME}.app"
STAGING_DIR = "dist/dmg_staging"
DMG_VOLUME_SIZE = "50m"

def check_app():
    """检查 .app 是否存在"""
    if not os.path.exists(APP_PATH):
        print(f"❌ 未找到 {APP_PATH}")
        print("   请先运行 build.py 生成 .app 应用")
        sys.exit(1)
    print(f"✅ 找到应用: {APP_PATH}")

def setup_staging():
    """创建 DMG 临时目录，放入应用和快捷方式"""
    # 清理旧的临时目录
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    os.makedirs(STAGING_DIR)

    # 复制 .app 到临时目录
    app_dest = os.path.join(STAGING_DIR, f"{APP_NAME}.app")
    shutil.copytree(APP_PATH, app_dest)
    print(f"✅ 已复制应用到临时目录")

    # 创建"应用程序"文件夹的符号链接（拖拽安装用）
    apps_link = os.path.join(STAGING_DIR, "Applications")
    os.symlink("/Applications", apps_link)
    print("✅ 已创建 Applications 快捷方式")

def build_dmg():
    """使用 hdiutil 创建 DMG"""
    # 删除旧的 DMG
    if os.path.exists(DMG_OUTPUT):
        os.remove(DMG_OUTPUT)
        print(f"✅ 已删除旧的 DMG: {DMG_OUTPUT}")

    cmd = [
        "hdiutil", "create",
        "-volname", DMG_VOLUME_NAME,
        "-srcfolder", STAGING_DIR,
        "-ov",
        "-format", "UDZO",         # 压缩格式
        DMG_OUTPUT
    ]

    print("-" * 40)
    print("🚀 开始打包 DMG...")
    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 40)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("-" * 40)
        print("🎉 DMG 打包成功！")
        print(f"📦 输出文件: {DMG_OUTPUT}")

        # 获取文件大小
        size_mb = os.path.getsize(DMG_OUTPUT) / (1024 * 1024)
        print(f"📐 文件大小: {size_mb:.1f} MB")
    else:
        print("-" * 40)
        print("❌ DMG 打包失败！")
        print(f"错误信息: {result.stderr}")
        sys.exit(1)

def cleanup():
    """清理临时目录"""
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
        print("✅ 已清理临时目录")

if __name__ == "__main__":
    print("=" * 40)
    print(f"  DMG 打包工具 - {APP_NAME}")
    print("=" * 40)
    print()

    check_app()
    setup_staging()
    build_dmg()
    cleanup()

    print()
    print("=" * 40)
    print("  完成！双击 DMG 即可安装")
    print("=" * 40)