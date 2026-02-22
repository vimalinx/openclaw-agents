@echo off
chcp 65001 >nul
echo ============================================================
echo 小红书自动评论回复系统
echo ============================================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖
echo 📦 检查依赖...
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  缺少依赖，正在安装...
    pip install -r requirements.txt
)

REM 检查配置
echo 📝 检查配置...
if not exist "config.json" (
    echo ❌ 错误: 未找到配置文件 config.json
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 选择操作：
echo ============================================================
echo 1. 运行自动回复系统
echo 2. 查看统计信息
echo 3. 查看客户列表
echo 4. 运行测试
echo 5. 退出
echo.
set /p choice="请输入选项 (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 启动自动回复系统...
    echo.
    python auto_reply.py
    pause
) else if "%choice%"=="2" (
    echo.
    python auto_reply.py --stats
    pause
) else if "%choice%"=="3" (
    echo.
    echo 选择客户类型:
    echo   1 - 所有客户
    echo   2 - VIP客户
    echo   3 - 活跃客户
    echo   4 - 新客户
    set /p customer_type="请输入选项 (1-4): "

    if "%customer_type%"=="1" python auto_reply.py --customers all
    if "%customer_type%"=="2" python auto_reply.py --customers vip
    if "%customer_type%"=="3" python auto_reply.py --customers active
    if "%customer_type%"=="4" python auto_reply.py --customers new

    pause
) else if "%choice%"=="4" (
    echo.
    echo 🧪 运行测试套件...
    echo.
    python test.py
    pause
) else if "%choice%"=="5" (
    echo 👋 再见！
    exit /b 0
) else (
    echo ❌ 无效选项
    pause
)
