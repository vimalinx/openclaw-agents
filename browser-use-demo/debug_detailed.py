"""
详细 Debug 脚本 - 带超时配置和日志
"""
from browser_use import Agent, Browser
from browser_use.llm.models import ChatOpenAI
import asyncio

async def debug_agent():
    """带详细日志的 Agent 运行"""

    # 初始化 Qwen 客户端
    llm = ChatOpenAI(
        model="qwen-plus",
        api_key="sk-17ea43b2a6f64d0398123ee9cb7bcdfc",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        timeout=300,  # 增加 LLM 超时到 5 分钟
    )

    browser = Browser(
        headless=False,  # 显示浏览器窗口
        disable_security=True,  # 禁用某些安全检查
    )

    # 简化任务 - 只测试导航
    agent = Agent(
        task="""
        任务：打开小红书创作者平台发布页面

        步骤：
        1. 打开 https://creator.xiaohongshu.com/publish/publish
        2. 等待页面加载完成
        3. 查找"发布笔记"按钮
        4. 点击该按钮

        完成后报告页面状态。
        """,
        llm=llm,
        browser=browser,
        llm_timeout=300,  # LLM 超时 5 分钟
        step_timeout=300,  # 每步超时 5 分钟
        max_failures=1,  # 减少失败重试次数
        use_thinking=False,  # 禁用思考模式加快速度
        flash_mode=True,  # 启用快速模式
    )

    print("=" * 60)
    print("开始运行 Agent...")
    print("=" * 60)

    try:
        start_time = asyncio.get_event_loop().time()
        history = await agent.run()
        elapsed = asyncio.get_event_loop().time() - start_time
        print(f"\n✅ Agent 完成! 总耗时: {elapsed:.2f}秒")
        return history
    except Exception as e:
        print(f"\n❌ Agent 失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        # 注意: BrowserSession 没有 close 方法
        print("\nAgent 运行结束")


if __name__ == "__main__":
    asyncio.run(debug_agent())
