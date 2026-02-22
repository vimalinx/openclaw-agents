#!/usr/bin/env python3
"""
测试用 GLM-4 配置 browser-use
"""
import asyncio
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

async def test_with_glm():
    """使用 GLM-4 测试浏览器自动化"""
    print("🐺 Wilson 使用 GLM-4 测试...")

    browser = Browser()

    # 配置 GLM-4（智谱 AI）
    llm = ChatOpenAI(
        model="glm-4-flash",  # 使用快速版本
        base_url="https://open.bigmodel.cn/api/coding/paas/v4",
        api_key="9ac45d2e82df427dbef6467567e81753.2kF0sITkGWI2f54T",
        temperature=0.0,
    )

    agent = Agent(
        task="访问 https://www.example.com 并告诉我这个页面的标题和主要内容",
        llm=llm,
        browser=browser,
    )

    try:
        result = await agent.run()
        print("\n✅ 测试成功！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 可能需要：")
        print("1. 完整的 API key（从 OpenClaw 配置中获取）")
        print("2. 或者改用其他 LLM（OpenAI、本地 Ollama 等）")

if __name__ == "__main__":
    asyncio.run(test_with_glm())
