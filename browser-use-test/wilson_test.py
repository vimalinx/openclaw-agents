#!/usr/bin/env python3
"""
Wilson's browser-use test script
测试简单的浏览器自动化任务
"""

import asyncio
import os
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

async def simple_test():
    """简单的浏览器测试：访问 example.com 并获取标题"""
    print("🐺 Wilson: 启动浏览器测试...")
    
    # 使用本地浏览器（非云端）
    browser = Browser()
    
    # 使用 OpenAI 兼容的 API
    # 你可以替换成任何兼容的 API endpoint
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # 或者其他可用模型
        api_key=os.getenv("OPENAI_API_KEY", "not-needed"),  # 如果用本地模型可以设为假值
        base_url=os.getenv("OPENAI_BASE_URL"),  # 可选：自定义 endpoint
        temperature=0.0,
    )
    
    agent = Agent(
        task="Go to https://www.example.com, read the page title, and summarize what you see",
        llm=llm,
        browser=browser,
    )
    
    try:
        result = await agent.run()
        print(f"\n✅ 测试完成！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    print("🐺 Wilson 的浏览器自动化测试")
    print("=" * 50)
    asyncio.run(simple_test())
