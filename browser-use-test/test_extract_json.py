#!/usr/bin/env python3
"""尝试从 MiniMax 输出中提取 JSON"""
import asyncio
import json
import re
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI
from typing import Any

async def test_extract_json():
    """测试从输出中提取 JSON"""
    print("🐺 Wilson 测试 MiniMax M2.5（带 JSON 提取）...")

    browser = Browser()

    llm = ChatOpenAI(
        model="MiniMax-M2.5",
        base_url="https://api.minimax.chat/v1",
        api_key="sk-cp-oYeO0NZWc0r4VvbqfddZiAQUEwl3k_wK2rh9PqGOkE3daynKWQ6VkWHD7LrVlGkyvTMAw2iWPQykiZZJqbwPm81KHCB8eHSyDSqn_hQxEXMN7eblEGNDkgM",
        temperature=0.0,
    )

    agent = Agent(
        task="访问 https://www.example.com 并告诉我这个页面的标题",
        llm=llm,
        browser=browser,
    )

    try:
        # 先运行一次看看实际输出
        print("\n🔍 开始运行，查看实际输出...")
        result = await agent.run()
        print("\n✅ 成功！")
        print(f"结果: {result}")
    except Exception as e:
        error_msg = str(e)
        print(f"\n⚠️ 错误: {error_msg}")

        # 尝试从错误中提取 JSON
        if "input_value=" in error_msg:
            # 提取 input_value 后面的内容
            match = re.search(r"input_value='([^']+)'", error_msg)
            if match:
                raw_output = match.group(1)
                print(f"\n📤 原始输出:\n{raw_output[:500]}...")

                # 尝试找到 JSON 部分
                json_match = re.search(r'\{[^{}]*"action"[^{}]*\}', raw_output)
                if json_match:
                    json_str = json_match.group(0)
                    print(f"\n📦 提取的 JSON:\n{json_str}")

                    try:
                        parsed = json.loads(json_str)
                        print(f"\n✅ 解析成功: {parsed}")
                    except:
                        print(f"❌ JSON 解析失败")

if __name__ == "__main__":
    asyncio.run(test_extract_json())
