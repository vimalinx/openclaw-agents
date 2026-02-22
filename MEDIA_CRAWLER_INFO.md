# Media Crawler 配置说明

## 📍 位置
`/home/vimalinx/.openclaw/skills/xhs-auto-publisher/`

## 🎯 核心功能

### 1. search_materials.py（搜索爬虫）

**功能**：在小红书搜索关键词，收集相关笔记数据

**使用方式**：
```python
python3 search_materials.py
```

**核心代码**：
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 连接已登录的Chrome
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # 搜索关键词
        keywords = ["资料", "书库", "知识库", "虚拟", "购买", "付费", "课程"]
        
        # 滚动加载所有内容
        for i in range(15):
            await page.evaluate("window.scrollBy(0, 600)")
            await asyncio.sleep(0.8)
```

**输出**：匹配关键词的笔记数据

---

### 2. scroll_notes.py（滚动爬虫）

**功能**：滚动页面加载更多笔记内容

**使用方式**：
```python
python3 scroll_notes.py
```

**核心代码**：
```python
# 滚动加载更多内容
for i in range(10):
    await page.evaluate("window.scrollBy(0, 800)")
    await asyncio.sleep(1)
    print(f"   滚动 {i+1}/10 次...")

# 截图保存
await page.screenshot(path="/tmp/xhs_profile_scrolled.png", full_page=True)
```

**输出**：页面截图 + 扩展内容

---

## 🔄 工作流程

### Phase 1: 搜索内容
```
访问主页 → 搜索关键词 → 滚动加载 → 提取笔记数据
```

### Phase 2: 扩展内容
```
滚动页面 → 加载更多 → 截图保存 → 数据提取
```

---

## 🎯 使用场景

1. **市场调研**：搜索竞品的笔记内容
2. **热点分析**：搜索行业关键词，了解热门内容
3. **素材收集**：搜索特定主题的笔记和图片
4. **用户调研**：查看目标用户的发布内容

---

## ⚙️ 技术特点

- **Playwright 自动化**：使用 Chrome CDP 协议连接
- **已登录会话**：复用浏览器登录状态
- **智能滚动**：模拟真人操作，避免风控
- **截图保存**：保存页面状态用于分析

---

## 🚀 集成到 PDF 调研流程

在 Phase 2（搜索和收集资料）时，可以使用：

1. **关键词搜索**：用 search_materials.py 搜索相关工具
2. **内容收集**：收集工具的官网、博客、社交媒体内容
3. **用户评价**：搜索工具的用户评价和反馈
4. **竞品分析**：搜索竞品的营销页面和定价页面

**优势**：
- ✅ 真实用户内容（来自小红书）
- ✅ 最新热点信息
- ✅ 用户真实反馈
- ✅ 竞品实际表现

---

## 📋 快速参考

### 搜索示例
```python
# 修改 keywords 列表
keywords = ["AI工具", "自动化", "效率", "生产力"]

# 搜索页面
await page.goto("https://www.xiaohongshu.com/search_result?keyword=AI工具")
```

### 滚动示例
```python
# 滚动更多内容
await page.evaluate("window.scrollBy(0, 800)")
await page.screenshot(path="/tmp/search_results.png")
```

---

**注意**：
- 需要确保 Chrome 浏览器已登录小红书
- 使用 localhost:9222 连接已打开的浏览器
- 滚动间隔保持在 0.8-1.5 秒，避免被风控
