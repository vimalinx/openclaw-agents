#!/usr/bin/env python3
"""Simple browser-use test script for Wilson"""

import asyncio
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

async def test_browser():
    """Test browser automation with a simple task"""
    # 使用本地浏览器（不需要 cloud）
    browser = Browser()
    
    # 使用 OpenAI 或其他兼容的 LLM
    # 需要在 .env 或环境变量中设置 API key
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # 或其他可用模型
        temperature=0.0
    )
    
    agent = Agent(
        task="Go to https://www.example.com and tell me the page title",
        llm=llm,
        browser=browser,
    )
    
    result = await agent.run()
    return result

if __name__ == "__main__":
    print("🐺 Wilson testing browser-use...")
    result = asyncio.run(test_browser())
    print(f"\nResult: {result}")
