# 自动输入工具

一个简单的桌面自动输入工具，使用 Python + tkinter + pyautogui + pypinyin 构建。

## 功能

- 图形化界面输入要自动打字的文本
- 可调节输入前的延迟时间（0.5-10秒）
- 支持开始/停止控制
- 实时状态显示
- 支持中文输入（通过 pypinyin 转拼音后模拟键入）
- 可打包为 macOS 应用、DMG 安装包及 Windows EXE

## 环境要求

- Python 3.6+
- pyautogui
- pypinyin
- tkinter（Python 标准库）
- PyInstaller（打包时需要）

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/Enderman112/Autoinput.git
cd Autoinput
```

2. 安装依赖：
```bash
pip install pyautogui pypinyin
```

## 使用

直接运行：
```bash
python3 input.py
```

## 构建可执行文件

### macOS 应用
```bash
python3 build.py
```
生成文件位于 `dist/自动输入工具`

### macOS DMG 安装包
```bash
# 先生成 .app
python3 build.py
# 再打包为 DMG
python3 build_dmg.py
```
生成文件位于 `dist/自动输入工具安装包.dmg`，双击打开后将应用拖入 Applications 即可安装。

### Windows EXE
在 Windows 系统上运行：
```bash
python build_exe.py
```
生成文件位于 `dist/AutoInput.exe`

### Linux
在 Linux 系统上同样可以使用 `build.py` 生成可执行文件：
```bash
python3 build.py
```
生成文件位于 `dist/自动输入工具`


## 操作说明

1. 在文本框中输入要自动打字的内容
2. 调整延迟时间滑块（默认 2 秒）
3. 点击「开始自动输入」
4. 在延迟时间内将鼠标焦点切换到目标输入框
5. 等待自动输入完成，或点击「停止」中断

> **注意**：中文内容会通过 pypinyin 转换为拼音后输入。

## 文件说明

- `input.py` - 主程序（GUI + 自动输入逻辑）
- `requirements.txt` - Python 依赖列表
- `build.py` - macOS 应用构建脚本
- `build_exe.py` - Windows EXE 构建脚本

## 自动构建

项目配置了 GitHub Actions，每次 push 到 main 分支会自动：

1. 生成版本号（格式：`v20250510-abc1234`）
2. 构建 Linux、macOS、Windows 三端程序
3. 发布到 [GitHub Releases](https://github.com/Enderman112/Autoinput/releases)