# Media Crawler 详细学习笔记

**工具名称**: Media Crawler（小红书搜索/爬虫）
**学习日期**: 2026-02-20
**学习状态**: ✅ 已深入理解

---

## 📍 工具定位

**位置**: `/home/vimalinx/.openclaw/skills/xhs-auto-publisher/`

**核心文件**:
- `search_materials.py` - 搜索爬虫（关键词搜索）
- `scroll_notes.py` - 滚动爬虫（加载更多内容）

**用途**: 在小红书搜索关键词、滚动页面、收集笔记数据、获取用户反馈和市场情报。

---

## 📋 核心功能

### 1. search_materials.py（搜索爬虫）

#### 🎯 功能概述
在小红书搜索关键词相关的内容，提取笔记标题、描述和匹配的关键词。

#### 🔧 核心技术栈
- **Playwright**: 浏览器自动化框架
- **CDP 协议**: Chrome DevTools Protocol（连接已打开的 Chrome）
- **JavaScript evaluate**: 在页面上下文中执行 JS 代码
- **DOM 操作**: 查询和分析页面元素
- **异步编程**: asyncio 处理异步操作

#### 🔄 工作流程

```
连接 Chrome (localhost:9222)
    ↓
访问用户主页
    ↓
滚动加载所有内容（15次，每次 600px，间隔 0.8s）
    ↓
搜索关键词（["资料", "书库", "知识库", "虚拟", "购买"]）
    ↓
提取笔记数据（标题、描述、匹配关键词）
    ↓
显示匹配的笔记
    ↓
点击第一篇笔记详情
    ↓
截图和获取笔记文本
```

#### 💻 核心代码分析

##### 1.1 连接 Chrome
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    # 通过 CDP 协议连接到已打开的 Chrome
    browser = await p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
```

**关键点**：
- **CDP 协议**: Chrome DevTools Protocol，允许外部程序控制 Chrome
- **端口**: 9222（远程调试端口）
- **会话复用**: 使用已登录的 Chrome 浏览器，避免重新登录

##### 1.2 滚动加载内容
```python
print("📜 加载所有笔记...")
for i in range(15):
    await page.evaluate("window.scrollBy(0, 600)")
    await asyncio.sleep(0.8)
    print(f"   {i+1}/15...")
```

**关键点**：
- **window.scrollBy**: JS 原生滚动方法，模拟用户滚动
- **滚动距离**: 600px（每次滚动 600 像素）
- **滚动次数**: 15 次（滚动 15 次加载更多内容）
- **间隔时间**: 0.8 秒（避免触发反爬虫机制）
- **模拟真人**: 使用较短的间隔（0.8s）而不是长时间等待

##### 1.3 搜索关键词
```python
keywords = ["资料", "书库", "知识库", "虚拟", "购买", "付费", "课程", "电子版", "PDF", "文档"]

notes_data = await page.evaluate('''(keywords) => {
    const noteItems = document.querySelectorAll('section[class*="note"], div[class*="note-item"]');
    const notes = [];

    for (let i = 0; i < noteItems.length; i++) {
        const item = noteItems[i];

        const title = item.querySelector('[class*="title"], h3, .title')?.textContent?.trim();
        const desc = item.querySelector('[class*="desc"], [class*="content"]')?.textContent?.trim();
        const allText = (title || '') + ' ' + (desc || '');

        // 检查是否包含关键词
        const matchedKeywords = keywords.filter(kw => allText.toLowerCase().includes(kw.toLowerCase()));

        notes.push({
            index: i + 1,
            title: title || '无标题',
            desc: desc || '',
            matchedKeywords: matchedKeywords,
            hasKeywords: matchedKeywords.length > 0
        });
    }

    return notes;
}''', keywords)
```

**关键点**：
- **querySelectorAll**: 查询所有匹配的元素
- **CSS 选择器**: `'section[class*="note"], div[class*="note-item"]'` - 匹配包含 class 的元素
- **textContent**: 提取元素的文本内容
- **trim()**: 去除首尾空白
- **toLowerCase()**: 转换为小写（不区分大小写匹配）
- **includes()**: 检查字符串是否包含关键词
- **filter()**: 过滤匹配的关键词

##### 1.4 显示匹配的笔记
```python
found = False
for note in notes_data:
    if note['hasKeywords']:
        found = True
        print(f"【{note['index']}】{note['title']}")
        print(f"   关键词: {', '.join(note['matchedKeywords'])}")
        if note['desc']:
            print(f"   描述: {note['desc']}")
        print()
```

**关键点**：
- **条件过滤**: 只显示匹配关键词的笔记
- **格式化输出**: 使用 Markdown 风格显示笔记信息
- **提取字段**: 显示匹配的关键词和描述

##### 1.5 点击第一篇笔记详情
```python
first_note = await page.query_selector('section[class*="note"], div[class*="note-item"]')
if first_note:
    await first_note.click()
    await asyncio.sleep(3)

    # 截图笔记详情
    await page.screenshot(path="/tmp/xhs_note_detail.png", full_page=True)
    print("📸 笔记详情截图已保存: /tmp/xhs_note_detail.png")

    # 获取笔记详情文本
    note_text = await page.evaluate('''() => {
        return document.body.innerText.substring(0, 2000);
    }''')

    print("📝 笔记内容预览:")
    print(note_text[:500])
    print("...")
```

**关键点**：
- **query_selector**: 查询第一个匹配的元素
- **click()**: 模拟用户点击
- **await asyncio.sleep(3)**: 等待页面加载完成
- **screenshot**: 截取页面截图
- **innerText**: 获取页面纯文本
- **substring()**: 只提取前 2000 个字符

#### 📊 数据结构

```python
# 笔记数据结构
{
    "index": 1,                    # 笔记序号
    "title": "笔记标题",           # 笔记标题
    "desc": "笔记描述",           # 笔记描述
    "matchedKeywords": [         # 匹配的关键词
        "关键词1",
        "关键词2"
    ],
    "hasKeywords": True            # 是否匹配关键词
}
```

---

### 2. scroll_notes.py（滚动爬虫）

#### 🎯 功能概述
滚动页面加载更多笔记内容，获取所有笔记数据并保存到 JSON 文件。

#### 🔧 核心技术栈
- **Playwright**: 浏览器自动化框架
- **CDP 协议**: Chrome DevTools Protocol
- **JavaScript evaluate**: 在页面上下文中执行 JS 代码
- **DOM 操作**: 查询和分析页面元素
- **JSON 存储**: 将数据保存为 JSON 格式

#### 🔄 工作流程

```
连接 Chrome (localhost:9222)
    ↓
访问用户主页
    ↓
滚动加载更多内容（10次，每次 800px，间隔 1s）
    ↓
等待页面加载完成
    ↓
截图保存
    ↓
获取所有笔记数据（标题、描述、封面）
    ↓
保存到 JSON 文件
```

#### 💻 核心代码分析

##### 2.1 连接 Chrome
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
```

**关键点**：
- 与 search_materials.py 相同的连接方式
- 复用已打开的 Chrome 浏览器

##### 2.2 滚动加载更多内容
```python
print("📜 滚动加载更多笔记...")
for i in range(10):  # 滚动10次
    await page.evaluate("window.scrollBy(0, 800)")
    await asyncio.sleep(1)
    print(f"   滚动 {i+1}/10 次...")

# 等待加载
await asyncio.sleep(2)
```

**关键点**：
- **滚动次数**: 10 次（比 search_materials.py 少）
- **滚动距离**: 800px（比 search_materials.py 大）
- **间隔时间**: 1 秒（比 search_materials.py 长）
- **加载等待**: 滚动完成后等待 2 秒让页面完全加载

##### 2.3 截图保存
```python
print("\n📸 截图...")
await page.screenshot(path="/tmp/xhs_profile_scrolled.png", full_page=True)
print("✅ 截图已保存: /tmp/xhs_profile_scrolled.png")
```

**关键点**：
- **full_page=True**: 截取整个页面，不只是可视区域
- **path**: 指定截图保存路径

##### 2.4 获取所有笔记数据
```python
all_notes = await page.evaluate('''() => {
    const noteItems = document.querySelectorAll('section[class*="note"], div[class*="note-item"], div[class*="note-card"]');
    const notes = [];

    for (let i = 0; i < noteItems.length; i++) {
        const item = noteItems[i];
        const title = item.querySelector('[class*="title"], h3, .title')?.textContent?.trim();
        const desc = item.querySelector('[class*="desc"], [class*="content"]')?.textContent?.trim();
        const cover = item.querySelector('img')?.src;

        notes.push({
            index: i + 1,
            title: title || '无标题',
            desc: desc ? desc.substring(0, 50) : '',
            cover: cover ? cover.substring(0, 50) : ''
        });
    }

    return {
        total: noteItems.length,
        notes: notes
    };
}''')
```

**关键点**：
- **CSS 选择器**: `'section[class*="note"], div[class*="note-item"], div[class*="note-card"]'` - 匹配多种笔记元素类型
- **querySelector**: 查询子元素（标题、描述、封面）
- **substring()**: 只提取前 50 个字符（描述和封面 URL）
- **可选链操作符 (?.)**: 避免元素不存在时出错
- **total**: 总笔记数量

##### 2.5 保存到 JSON 文件
```python
import json
import os

os.makedirs('/tmp', exist_ok=True)

with open('/tmp/xhs_all_notes.json', 'w', encoding='utf-8') as f:
    json.dump(all_notes, f, indent=2, ensure_ascii=False)
```

**关键点**：
- **json.dump()**: 将 Python 字典转换为 JSON 格式
- **indent=2**: 格式化输出，便于阅读
- **ensure_ascii=False**: 支持中文字符
- **encoding='utf-8'**: 使用 UTF-8 编码

#### 📊 数据结构

```python
# 笔记数据结构
{
    "total": 150,                  # 总笔记数量
    "notes": [                    # 笔记列表
        {
            "index": 1,           # 笔记序号
            "title": "笔记标题",   # 笔记标题
            "desc": "笔记描述",   # 笔记描述（前 50 字）
            "cover": "封面URL"    # 封面 URL（前 50 字）
        },
        ...
    ]
}
```

---

## 🔧 核心技术深入分析

### 1. Playwright 框架

#### 1.1 什么是 Playwright？
**Playwright** 是一个由 Microsoft 开发的现代浏览器自动化框架，支持 Chromium、Firefox 和 WebKit。

#### 1.2 核心特性
- **快速可靠**: 并发执行，比 Selenium 快
- **跨平台**: 支持 Chromium、Firefox、WebKit
- **现代浏览器特性**: 支持 CSS Grid、Shadow DOM 等
- **无头模式**: 支持无头模式和有头模式
- **截图和视频**: 内置截图和视频录制功能

#### 1.3 与 Selenium 的对比
| 特性 | Playwright | Selenium |
|------|-----------|----------|
| 速度 | 快 | 较慢 |
| 稳定性 | 稳定 | 较不稳定 |
| 现代特性 | 支持完整 | 部分支持 |
| API 设计 | 现代、简洁 | 较旧、复杂 |

---

### 2. CDP 协议

#### 2.1 什么是 CDP？
**CDP (Chrome DevTools Protocol)** 是 Chrome 浏览器提供的远程调试协议，允许外部程序控制 Chrome。

#### 2.2 核心特性
- **远程调试**: 可以通过 CDP 控制已打开的 Chrome 浏览器
- **端口复用**: 使用已打开的浏览器，避免重新登录
- **会话持久化**: 保持登录状态、Cookie、Session 等

#### 2.3 连接方式
```python
# 通过 CDP 连接到已打开的 Chrome
browser = await p.chromium.connect_over_cdp("http://localhost:9222")
```

**关键点**：
- **端口**: 9222（CDP 默认端口）
- **协议**: HTTP
- **复用**: 复用已打开的浏览器和会话

---

### 3. JavaScript evaluate

#### 3.1 什么是 evaluate？
**page.evaluate()** 是 Playwright 提供的方法，允许在浏览器页面上下文中执行 JavaScript 代码。

#### 3.2 工作原理
```
Python 进程
    ↓
调用 page.evaluate(js_code)
    ↓
将 JS 代码发送到浏览器
    ↓
浏览器在页面上下文中执行 JS
    ↓
返回执行结果到 Python
    ↓
Python 进程接收结果
```

#### 3.3 使用场景
- **DOM 操作**: 查询、修改页面元素
- **数据提取**: 提取页面文本、属性、结构
- **复杂逻辑**: 在浏览器中执行复杂的 JS 逻辑
- **性能优化**: 在浏览器中执行数据密集型操作

---

### 4. DOM 操作

#### 4.1 DOM (Document Object Model)
**DOM** 是 HTML 文档的对象模型，将文档表示为节点树。

#### 4.2 常用 DOM 操作

```javascript
// 查询所有笔记元素
const noteItems = document.querySelectorAll('section[class*="note"]');

// 查询第一个匹配的元素
const firstNote = noteItems[0];

// 查询子元素
const title = firstNote.querySelector('[class*="title"]');

// 获取文本内容
const text = title.textContent;

// 获取属性
const src = img.src;
```

**关键点**：
- **querySelectorAll**: 查询所有匹配的元素
- **querySelector**: 查询第一个匹配的元素
- **[attribute*="value"]**: 属性值包含某个字符串
- **textContent**: 获取元素的文本内容
- **.src**: 获取元素的属性值

---

### 5. 异步编程

#### 5.1 asyncio 库
**asyncio** 是 Python 的标准异步编程库，用于编写并发代码。

#### 5.2 核心概念
- **async/await**: 定义异步函数和等待异步操作
- **asyncio.sleep()**: 异步等待（不阻塞主线程）
- **事件循环**: 管理和调度异步任务

#### 5.3 异步模式
```python
# 定义异步函数
async def main():
    print("开始...")
    await asyncio.sleep(2)  # 异步等待 2 秒
    print("结束...")

# 运行异步函数
asyncio.run(main())
```

**关键点**：
- **async def**: 定义异步函数
- **await**: 等待异步操作完成
- **asyncio.run()**: 运行异步事件循环
- **非阻塞**: 异步等待不阻塞其他任务

---

## 🎯 关键技术点总结

### 1. 搜索爬虫 (search_materials.py)

| 技术点 | 说明 | 实现 |
|-------|------|------|
| CDP 连接 | 连接到已打开的 Chrome | `connect_over_cdp("http://localhost:9222")` |
| 页面滚动 | 模拟用户滚动加载内容 | `window.scrollBy(0, 600)` |
| 智能间隔 | 避免触发反爬虫机制 | `await asyncio.sleep(0.8)` |
| 关键词匹配 | 检查笔记是否包含关键词 | `allText.toLowerCase().includes(kw.toLowerCase())` |
| DOM 查询 | 查询笔记元素 | `document.querySelectorAll('section[class*="note"]')` |
| 数据提取 | 提取标题、描述、关键词 | `title = item.querySelector('[class*="title"]').textContent` |
| 页面交互 | 点击笔记详情 | `await first_note.click()` |
| 截图保存 | 保存页面截图 | `await page.screenshot(path="/tmp/...")` |

### 2. 滚动爬虫 (scroll_notes.py)

| 技术点 | 说明 | 实现 |
|-------|------|------|
| CDP 连接 | 连接到已打开的 Chrome | `connect_over_cdp("http://localhost:9222")` |
| 滚动加载 | 滚动加载更多笔记 | `window.scrollBy(0, 800)` |
| 滚动次数 | 滚动 10 次 | `range(10)` |
| 滚动间隔 | 每次滚动间隔 1 秒 | `await asyncio.sleep(1)` |
| DOM 查询 | 查询所有笔记元素 | `document.querySelectorAll('section[class*="note"]')` |
| 数据提取 | 提取标题、描述、封面 | `title = item.querySelector('[class*="title"]').textContent` |
| 数据保存 | 保存为 JSON 格式 | `json.dump(all_notes, f, indent=2)` |
| 截图保存 | 保存页面截图 | `await page.screenshot(path="/tmp/...")` |

---

## 💡 最佳实践

### 1. 防爬虫策略

| 策略 | 说明 | 实现 |
|------|------|------|
| **模拟真人** | 使用较短的滚动间隔 | `0.8-1.5 秒` |
| **随机化** | 添加随机延迟 | `await asyncio.sleep(random.uniform(0.8, 1.5))` |
| **复用会话** | 使用已打开的浏览器 | CDP 连接 |
| **限制频率** | 控制请求频率 | 间隔时间 > 1 秒 |
| **用户代理** | 设置真实用户代理 | `User-Agent: ...` |

### 2. 错误处理

| 场景 | 处理方式 | 实现 |
|------|--------|------|
| **连接失败** | 捕获异常并重试 | `try/except + 重试` |
| **元素未找到** | 检查元素是否存在 | `if element:` |
| **页面超时** | 设置超时时间 | `await asyncio.wait_for(..., timeout=30)` |
| **网络错误** | 捕获网络异常 | `except Exception as e:` |

### 3. 性能优化

| 优化点 | 说明 | 实现 |
|-------|------|------|
| **减少滚动次数** | 根据实际需要调整滚动次数 | 10-15 次 |
| **优化选择器** | 使用更精确的 CSS 选择器 | `div.note-card` 而不是 `div[class*="note"]` |
| **并行处理** | 并行处理多个查询 | `await asyncio.gather(*tasks)` |
| **缓存数据** | 缓存已提取的数据 | 避免重复查询 |
| **增量更新** | 只查询新加载的内容 | 使用滚动后的元素 |

---

## 🔮 使用场景

### 1. 市场调研
- **搜索竞品内容**: 搜索竞品账号的笔记内容
- **分析爆款笔记**: 搜索行业关键词，分析爆款特征
- **收集用户反馈**: 搜索用户反馈相关的内容

### 2. 内容创作
- **收集素材**: 搜索特定主题的内容和图片
- **分析热点**: 搜索当前热门话题和趋势
- **寻找灵感**: 搜索相关领域的优质内容

### 3. 数据分析
- **提取数据**: 提取笔记的标题、描述、封面、互动数据
- **分析趋势**: 分析笔记的发布时间、互动表现
- **竞品对比**: 对比竞品的笔记内容

---

## ⚠️ 使用限制和注意事项

### 1. 使用规范
- ✅ **仅用于公开信息**: 只爬取公开的笔记数据
- ❌ **不爬取私人内容**: 不爬取私人笔记或私信
- ✅ **遵守平台规则**: 不违反小红书的使用条款
- ❌ **不进行恶意爬取**: 不进行大规模、高频率的爬取

### 2. 技术限制
- **滚动次数**: 建议不超过 20 次滚动
- **间隔时间**: 建议保持在 0.8-1.5 秒
- **总爬取量**: 建议每次爬取不超过 100 条笔记
- **并发限制**: 不要同时运行多个爬虫

### 3. 风险控制
- **账号风险**: 过度爬取可能导致账号被限流或封号
- **IP 风险**: 频繁爬取可能导致 IP 被限制
- **法律风险**: 爬取商业数据可能涉及法律问题

---

## 🚀 扩展和优化方向

### 1. 功能扩展
- [ ] 添加更多搜索关键词
- [ ] 支持多账号爬取
- [ ] 支持多平台爬取（抖音、视频号等）
- [ ] 添加数据分析和可视化

### 2. 性能优化
- [ ] 使用连接池复用浏览器连接
- [ ] 实现增量更新，只爬取新内容
- [ ] 添加缓存机制，减少重复查询
- [ ] 优化 DOM 选择器，提高查询速度

### 3. 稳定性优化
- [ ] 添加重试机制，处理网络错误
- [ ] 添加超时控制，避免无限等待
- [ ] 添加异常处理，优雅退出
- [ ] 添加日志记录，便于调试

### 4. 易用性优化
- [ ] 添加命令行参数支持
- [ ] 添加配置文件支持
- [ ] 添加进度条显示
- [ ] 添加数据导出功能（CSV、Excel）

---

## 📝 总结

### 核心价值
- ✅ **数据获取能力**: 能够从小红书获取真实的笔记数据
- ✅ **自动化能力**: 自动化搜索、滚动、提取、保存等流程
- ✅ **灵活性**: 可以自定义搜索关键词、滚动次数、数据格式
- ✅ **复用性**: 可以整合到其他工具中，作为数据获取模块

### 技术优势
- 🚀 **Playwright**: 使用现代化的浏览器自动化框架
- 🔄 **CDP 协议**: 复用已登录的浏览器，保持会话
- 🛡️ **防爬虫设计**: 模拟真人操作，避免触发反爬虫
- 📊 **结构化数据**: 输出 JSON 格式，便于后续处理

### 实际应用
- 📈 **市场调研**: 竞品分析、热点分析、用户反馈收集
- 📝 **内容创作**: 素材收集、灵感寻找、内容分析
- 📊 **数据分析**: 数据提取、趋势分析、竞品对比

---

**学习完成时间**: 2026-02-20 00:55
**下一步**: 整合到自媒体运营系统，作为市场情报层的核心组件
