# 自动输入工具

一个简单的桌面自动输入工具，使用 Python + tkinter + pyautogui 构建。

## 功能

- 图形化界面输入要自动打字的文本
- 可调节输入前的延迟时间（0.5-10秒）
- 支持开始/停止控制
- 实时状态显示
- 可打包为 macOS 和 Windows 可执行文件

## 环境要求

- Python 3.6+
- pyautogui
- tkinter（Python 标准库）
- PyInstaller（打包时需要）

## 安装

1. 克隆仓库：
```bash
git clone <仓库地址>
cd input
```

2. 安装依赖：
```bash
pip install pyautogui
```

## 使用

直接运行：
```bash
python input.py
```

## 构建可执行文件

### macOS
```bash
python build.py
```
生成文件位于 `dist/自动输入工具`

### Windows
```bash
python build_exe.py
```
生成文件位于 `dist/AutoInput.exe`

**注意**：PyInstaller 只能在目标系统上打包对应格式。在 macOS 上无法生成 .exe 文件。

## 操作说明

1. 在文本框中输入要自动打字的内容
2. 调整延迟时间滑块（默认 2 秒）
3. 点击「开始自动输入」
4. 在延迟时间内将鼠标焦点切换到目标输入框
5. 等待自动输入完成，或点击「停止」中断

## 文件说明

- `input.py` - 主程序
- `build.py` - macOS 构建脚本
- `build_exe.py` - Windows 构建脚本
- `自动输入工具.spec` - PyInstaller 配置文件