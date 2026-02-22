#!/usr/bin/env python3
"""使用 ChatBrowserUse（官方推荐）测试"""
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

async def test_with_chatbrowseruse():
    """使用 ChatBrowserUse 测试（专为浏览器优化）"""
    print("🐺 Wilson 使用 ChatBrowserUse 测试...")

    browser = Browser()

    # ChatBrowserUse 需要 API key
    # 注册: https://cloud.browser-use.com/new-api-key
    # 新用户有 $10 免费额度
    llm = ChatBrowserUse(
        api_key="你的API-key-here"  # 需要注册获取
    )

    agent = Agent(
        task="访问 https://www.example.com 并告诉我这个页面的标题",
        llm=llm,
        browser=browser,
    )

    try:
        result = await agent.run()
        print("\n✅ 成功！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 ChatBrowserUse 优势:")
        print("  - 专为浏览器任务优化")
        print("  - 速度快 3-5 倍")
        print("  - 更高的成功率")
        print("  - 新用户 $10 免费额度")
        print("\n获取 API key: https://cloud.browser-use.com/new-api-key")

if __name__ == "__main__":
    asyncio.run(test_with_chatbrowseruse())
