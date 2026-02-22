#!/usr/bin/env python3
"""
Wilson 的 browser-use agent
使用自己的 LLM API 进行长对话任务
"""

import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

load_dotenv()

async def run_agent(task: str, model: str = "gpt-4o-mini", use_cloud: bool = False):
    """
    运行 browser-use agent

    Args:
        task: 要执行的任务描述
        model: LLM 模型名称
        use_cloud: 是否使用 browser-use cloud（隐身浏览器）
    """
    print(f"🐺 Wilson 接到任务: {task}")
    print(f"   使用模型: {model}")

    # 创建浏览器实例
    browser = Browser(use_cloud=use_cloud)

    # 配置 LLM（支持任何 OpenAI 兼容的 API）
    api_key = os.getenv("OPENAI_API_KEY", "sk-placeholder")
    base_url = os.getenv("OPENAI_BASE_URL")

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,  # None 表示使用默认 OpenAI endpoint
        temperature=0.0,
    )

    # 创建 agent
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
    )

    try:
        print("🚀 开始执行任务...")
        result = await agent.run()
        print("\n✅ 任务完成！")
        print(f"结果: {result}")
        return result
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return None

# ========== 示例任务 ==========

async def example_search():
    """示例：搜索并总结"""
    task = """
    访问 https://www.google.com
    搜索 'browser-use github'
    找到并访问 browser-use 的 GitHub 仓库
    告诉我这个项目的主要功能是什么
    """
    return await run_agent(task)

async def example_price_check():
    """示例：价格检查"""
    task = """
    访问 https://www.example.com
    查看页面内容
    总结这个页面的主要信息
    """
    return await run_agent(task)

async def example_form_filling():
    """示例：表单填写（需要实际网站）"""
    task = """
    访问一个表单页面
    填写姓名为 "Wilson"
    提交表单
    """
    return await run_agent(task)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 从命令行读取任务
        task = " ".join(sys.argv[1:])
        asyncio.run(run_agent(task))
    else:
        # 默认运行示例
        print("🐺 Wilson Browser-Use Agent")
        print("用法: python wilson_agent.py '任务描述'")
        print("\n示例任务:")
        asyncio.run(example_price_check())
