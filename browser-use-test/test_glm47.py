#!/usr/bin/env python3
"""测试 GLM-4.7 推理模型（带 reasoning）"""
import asyncio
from browser_use import Agent, Browser
from browser_use.llm.openai.chat import ChatOpenAI

async def test_with_reasoning():
    """测试 GLM-4.7 推理模型"""
    print("🐺 Wilson 测试 GLM-4.7 推理模型...")

    browser = Browser()

    # GLM-4.7 是推理模型，需要特殊配置
    llm = ChatOpenAI(
        model="glm-4.7",
        base_url="https://open.bigmodel.cn/api/coding/paas/v4",
        api_key="9ac45d2e82df427dbef6467567e81753.2kF0sITkGWI2f54T",
        temperature=0.0,
    )

    # 更简单的任务
    agent = Agent(
        task="访问 https://www.example.com，找到页面标题，然后使用 done 动作结束",
        llm=llm,
        browser=browser,
        max_actions_per_step=1,  # 限制每次只有一个动作
        use_thinking=True,  # 启用思考模式
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
    asyncio.run(test_with_reasoning())
