#!/usr/bin/env python3
"""创建自定义 LLM 包装器，从输出中提取 JSON"""
import asyncio
import json
import re
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI
from browser_use.llm.base import BaseChatModel, BaseMessage
from typing import Any, Optional
from pydantic import BaseModel

class JSONExtractingChatOpenAI(ChatOpenAI):
    """
    包装 ChatOpenAI，自动从输出中提取 JSON
    """

    def _extract_json_from_text(self, text: str) -> str:
        """从文本中提取 JSON 部分"""
        # 尝试匹配 JSON 对象
        # 查找 {"action": ...} 格式
        patterns = [
            r'\{[^{}]*"action"[^{}]*\}',  # 简单的 action JSON
            r'\{[^{}]*"done"[^{}]*\}',     # done 动作
            r'\{[^{}]*"navigate"[^{}]*\}',  # navigate 动作
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                json_str = match.group(0)
                print(f"\n🔧 提取 JSON: {json_str[:200]}...")
                return json_str

        # 如果没找到，返回原文本
        return text

async def test_json_extraction():
    """测试带 JSON 提取的 LLM"""
    print("🐺 Wilson 测试 MiniMax M2.5（自动 JSON 提取）...")

    # 先看看能否直接用包装类
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
        result = await agent.run()
        print("\n✅ 成功！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"\n⚠️ 运行错误: {e}")

        # 查看是否有任何可用的输出
        if hasattr(agent, 'history') and agent.history:
            print(f"\n📜 历史记录存在，共 {len(agent.history)} 步")

if __name__ == "__main__":
    asyncio.run(test_json_extraction())
