#!/usr/bin/env python3
"""测试 MiniMax M2.5 模型"""
import asyncio
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI

async def test_with_minimax():
    """测试 MiniMax M2.5"""
    print("🐺 Wilson 测试 MiniMax M2.5...")

    browser = Browser()

    # MiniMax M2.5 使用 OpenAI 兼容接口
    llm = ChatOpenAI(
        model="MiniMax-M2.5",  # 或其他 MiniMax 模型名
        base_url="https://api.minimax.chat/v1",  # MiniMax API endpoint
        api_key="sk-cp-oYeO0NZWc0r4VvbqfddZiAQUEwl3k_wK2rh9PqGOkE3daynKWQ6VkWHD7LrVlGkyvTMAw2iWPQykiZZJqbwPm81KHCB8eHSyDSqn_hQxEXMN7eblEGNDkgM",
        temperature=0.0,
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_minimax())
