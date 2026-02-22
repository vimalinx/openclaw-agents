#!/usr/bin/env python3
"""快速测试：用 GLM-4 控制 browser-use"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

async def test():
    print("🐺 Wilson 用 GLM-4 测试 browser-use...")

    browser = Browser()

    # 使用 browser-use 的 ChatOpenAI（支持自定义 base_url）
    llm = ChatOpenAI(
        model="glm-4.7",
        base_url="https://open.bigmodel.cn/api/coding/paas/v4",
        api_key="9ac45d2e82df427dbef6467567e81753.2kF0sITkGWI2f54T",
        temperature=0.0,
    )

    # 简单任务
    agent = Agent(
        task="访问 https://www.example.com 并告诉我这个页面的标题",
        llm=llm,
        browser=browser,
    )

    try:
        result = await agent.run()
        print("\n✅ 成功！")
        print(f"LLM 理解的结果:\n{result}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
