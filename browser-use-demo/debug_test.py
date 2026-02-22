"""
Debug 脚本 - 测试 LLM 响应时间和浏览器连接
"""
import time
import asyncio
from openai import OpenAI

# 测试 Qwen API 响应时间
print("=" * 60)
print("测试 1: Qwen API 响应时间")
print("=" * 60)

client = OpenAI(
    api_key="sk-17ea43b2a6f64d0398123ee9cb7bcdfc",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 简单请求
start = time.time()
try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=50
    )
    elapsed = time.time() - start
    print(f"✅ 简单请求成功: {elapsed:.2f}秒")
    print(f"   响应: {response.choices[0].message.content}")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ 简单请求失败 ({elapsed:.2f}秒): {e}")

# 复杂请求（模拟浏览器任务）
start = time.time()
try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{
            "role": "user",
            "content": """分析以下 HTML 元素并告诉我该点击哪个按钮:
            <div class="header">
                <button class="publish">发布</button>
                <button class="cancel">取消</button>
                <button class="save">保存</button>
            </div>
            任务：点击发布按钮"""
        }],
        max_tokens=100
    )
    elapsed = time.time() - start
    print(f"✅ 复杂请求成功: {elapsed:.2f}秒")
    print(f"   响应: {response.choices[0].message.content}")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ 复杂请求失败 ({elapsed:.2f}秒): {e}")

# 超长请求（模拟真实页面分析）
start = time.time()
try:
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{
            "role": "user",
            "content": """你是一个浏览器自动化 AI。当前页面是小红书创作者平台的发布页面。
页面 HTML 结构如下（简化版）:
<html>
<body>
  <div class="creator-platform">
    <nav class="sidebar">
      <a href="/publish" class="active">发布笔记</a>
      <a href="/videos">视频</a>
    </nav>
    <main class="content">
      <div class="editor">
        <input type="text" placeholder="请输入标题" class="title-input" index="1">
        <textarea placeholder="请输入正文" class="content-input" index="2"></textarea>
        <div class="tags-input" index="3"></div>
        <button class="publish-btn" index="4">发布</button>
      </div>
    </main>
  </div>
</body>
</html>

任务：
1. 点击标题输入框
2. 输入标题："我的第一篇笔记"
3. 点击内容输入框
4. 输入内容："这是笔记内容"

请按步骤输出操作指令。"""
        }],
        max_tokens=200
    )
    elapsed = time.time() - start
    print(f"✅ 超长请求成功: {elapsed:.2f}秒")
    print(f"   响应: {response.choices[0].message.content[:100]}...")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ 超长请求失败 ({elapsed:.2f}秒): {e}")

print("\n" + "=" * 60)
print("测试 2: 检查 Browser-Use Agent 超时配置")
print("=" * 60)

from browser_use.agent.service import Agent
import inspect

print("\nAgent 类初始化参数（与超时相关）:")
sig = inspect.signature(Agent.__init__)
timeout_params = {
    'llm_timeout': 'LLM 调用超时（秒）',
    'step_timeout': '每步超时（秒）',
}
for param_name, description in timeout_params.items():
    if param_name in sig.parameters:
        param = sig.parameters[param_name]
        default = param.default if param.default != inspect.Parameter.empty else 'None'
        print(f"  - {param_name}: {default} ({description})")

print("\n" + "=" * 60)
print("Debug 完成")
print("=" * 60)
