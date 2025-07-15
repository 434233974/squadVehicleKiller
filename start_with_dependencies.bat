@echo off
chcp 65001 >nul
cls
echo ==========================================
echo    自动按键程序 - 依赖检查和启动工具
echo ==========================================
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python
    echo 请先安装Python：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

REM 检查主程序文件是否存在
if not exist "auto_key_presser_gui.py" (
    echo ❌ 错误：找不到 auto_key_presser_gui.py 文件
    echo 请确保在程序目录中运行此脚本
    echo.
    pause
    exit /b 1
)

echo ✅ 程序文件检查通过
echo.

REM 检查并安装依赖
echo 正在检查Python依赖包...
python -c "import pyautogui, pynput, PIL" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  检测到缺少依赖包，正在安装...
    echo.
    
    REM 安装依赖包
    echo 正在安装 pyautogui...
    pip install pyautogui
    if errorlevel 1 (
        echo ❌ pyautogui 安装失败
        pause
        exit /b 1
    )
    
    echo 正在安装 pynput...
    pip install pynput
    if errorlevel 1 (
        echo ❌ pynput 安装失败
        pause
        exit /b 1
    )
    
    echo 正在安装 Pillow...
    pip install Pillow
    if errorlevel 1 (
        echo ❌ Pillow 安装失败
        pause
        exit /b 1
    )
    
    echo ✅ 所有依赖包安装完成
    echo.
) else (
    echo ✅ 所有依赖包已就绪
    echo.
)

REM 启动程序
echo 正在启动自动按键程序...
echo.
echo 📋 使用说明：
echo - 程序启动后有3秒准备时间
echo - 按 ESC 键可随时停止程序
echo - 将鼠标移到屏幕左上角也可停止程序
echo.
echo 🚀 程序即将启动...
timeout /t 2 /nobreak >nul

python auto_key_presser_gui.py

echo.
echo 程序已退出
pause 