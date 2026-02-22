# Wilson 学习笔记

## Media Crawler 学习笔记

**日期**: 2026-02-19
**学习状态**: ✅ 已掌握基础用法

---

## 📍 Media Crawler 位置

**目录**：`/home/vimalinx/.openclaw/skills/xhs-auto-publisher/`

---

## 🎯 核心组件

### 1. search_materials.py（搜索爬虫）

**功能**：在小红书搜索关键词，收集相关笔记数据

**核心技术**：
- **Playwright 自动化**：使用 Chromium CDP 协议连接
- **已登录会话**：复用浏览器登录状态
- **智能滚动**：模拟真人操作，避免风控
- **关键词搜索**：支持多关键词搜索

**使用方式**：
```python
python3 search_materials.py
```

**核心代码结构**：
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 连接已登录的 Chrome
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # 搜索关键词
        keywords = ["资料", "书库", "知识库", "虚拟", "购买", "付费", "课程", "电子版", "PDF", "文档"]
        
        # 滚动加载所有内容
        for i in range(15):
            await page.evaluate("window.scrollBy(0, 600)")
            await asyncio.sleep(0.8)
            print(f"   {i+1}/15...")
        
        # 获取所有笔记内容
        notes_data = await page.evaluate('''(keywords) => {
            const noteItems = document.querySelectorAll('section[class*="note"], div[class*="note-item"]');
            const notes = [];
            
            for (let i = 0; i < noteItems.length; i++) {
                const item = noteItems[i];
                
                const title = item.querySelector('[class*="title"], h3, .title')?.textContent?.trim();
                const desc = item.querySelector('[class*="desc"], [class*="content"]')?.textContent?.trim();
                const allText = (title || '') + ' ' + (desc || '');
                
                // 检查是否包含关键词
                const hasKeyword = keywords.some(kw => allText.toLowerCase().includes(kw.toLowerCase()));
                
                if (hasKeyword) {
                    notes.push({
                        title: title || '无标题',
                        desc: desc || '无描述',
                        url: item.querySelector('a')?.href
                    });
                }
            }
            
            return notes;
        }''', keywords)
        
        print(f"📝 找到 {len(notes_data)} 条相关笔记")
```

**输出**：匹配关键词的笔记列表

---

### 2. scroll_notes.py（滚动爬虫）

**功能**：滚动页面加载更多笔记内容，并截图保存

**核心技术**：
- **智能滚动**：分步滚动，等待加载
- **截图保存**：保存页面状态用于分析
- **内容扩展**：加载更多笔记

**使用方式**：
```python
python3 scroll_notes.py
```

**核心代码结构**：
```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # 连接已登录的 Chrome
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
        
        try:
            # 访问个人主页
            print("🔍 访问个人主页...")
            await page.goto("https://www.xiaohongshu.com/user/profile/6852c081000000001d0092d5", wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 滚动加载更多内容
            print("📜 滚动加载更多笔记...")
            for i in range(10):  # 滚动10次
                await page.evaluate("window.scrollBy(0, 800)")
                await asyncio.sleep(1)
                print(f"   滚动 {i+1}/10 次...")
            
            # 等待加载
            await asyncio.sleep(2)
            
            # 截图
            print("\n📸 截图...")
            await page.screenshot(path="/tmp/xhs_profile_scrolled.png", full_page=True)
            print("✅ 截图已保存: /tmp/xhs_profile_scrolled.png")
            
            # 获取所有笔记
            print("\n📝 获取笔记列表...")
            
            # 提取笔记数据...
            # [笔记提取代码]
            
        except Exception as e:
            print(f"❌ 错误: {e}")
```

**输出**：页面截图 + 扩展的笔记列表

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
- **关键词匹配**：智能匹配相关内容

---

## 🚀 集成到 PDF 调研流程

### 在 Phase 2（搜索和收集资料）时使用：

#### 1. 关键词搜索
**使用 search_materials.py**：
```python
# 搜索关键词
keywords = ["AI周报生成", "自动化newsletter", "内容聚合工具", "AI新闻聚合"]
```

#### 2. 竞品分析
**使用 search_materials.py 搜索竞品内容**：
```python
# 搜索竞品笔记
keywords = ["Emergent", "AI自动化工具", "Newsletter生成器", "内容创作工具"]
```

#### 3. 用户评价收集
**使用 scroll_notes.py 深度查看用户反馈**：
```python
# 滚动查看用户页面，了解真实使用场景
```

#### 4. 市场趋势分析
**搜索行业关键词，了解热门话题**：
```python
# 搜索行业趋势
keywords = ["AI内容", "自动化工具", "创作者经济", "Newsletter平台"]
```

### 优势
- ✅ 真实用户内容（来自小红书）
- ✅ 最新热点信息
- ✅ 用户真实反馈
- ✅ 竞品实际表现
- ✅ 市场趋势洞察

---

## 📋 调研清单

### 搜索爬虫使用检查
- [ ] Chrome 浏览器已登录小红书
- [ ] 使用 localhost:9222 连接
- [ ] 准备搜索关键词列表
- [ ] 准备目标页面/账号

### 数据收集
- [ ] 搜索竞品内容
- [ ] 搜索用户评价
- [ ] 搜索行业趋势
- [ ] 收集截图证据

### 结果整理
- [ ] 提取笔记标题和内容
- [ ] 统计点赞、收藏、评论数据
- [ ] 分析热门话题和标签
- [ ] 识别用户痛点和需求

---

## 🔧 使用示例

### 示例 1: 搜索 AI 周刊工具
```python
# 修改 keywords 列表
keywords = ["AI周报", "自动化newsletter", "AI新闻聚合", "内容聚合"]

# 执行搜索
python3 search_materials.py
```

### 示例 2: 搜索竞品 Emergent
```python
# 搜索关键词
keywords = ["Emergent", "AI代理", "自定义AI", "AI工具"]

# 搜索页面
await page.goto("https://www.xiaohongshu.com/search_result?keyword=Emergent")
```

### 示例 3: 深度查看用户反馈
```python
# 滚动查看用户页面
await page.goto("https://www.xiaohongshu.com/user/profile/[用户ID]")

# 滚动加载
for i in range(15):
    await page.evaluate("window.scrollBy(0, 600)")
    await asyncio.sleep(0.8)

# 截图保存
await page.screenshot(path="/tmp/user_profile.png", full_page=True)
```

---

## 💡 最佳实践

### 搜索策略
1. **多关键词组合**：使用不同角度的关键词
2. **深度滚动**：滚动 15-20 次以上，确保加载完整
3. **截图保存**：保存页面状态用于后续分析
4. **避免风控**：滚动间隔 0.8-1.5 秒

### 数据提取
1. **结构化数据**：将非结构化内容转换为结构化数据
2. **关键词匹配**：使用智能匹配，提高准确度
3. **元数据收集**：收集点赞、收藏、评论等互动数据
4. **时间戳记录**：记录收集时间，便于趋势分析

---

## 📝 注意事项

### 技术限制
- 需要确保 Chrome 浏览器已登录小红书
- 滚动间隔不宜过短，避免被风控
- 需要处理异步操作和异常

### 内容限制
- 小红书反爬虫机制，大量请求可能被限制
- 部分内容可能无法完整获取
- 需要遵守小红书使用条款

### 使用规范
- 仅用于市场调研和竞品分析
- 不得用于商业数据爬取
- 遵守隐私保护法规
- 不得恶意攻击或滥用

---

## 🔄 更新日志

**2026-02-19 21:20**:
- ✅ 完成 Media Crawler 学习笔记
- ✅ 创建 media_crawler_info.md 配置文件
- ✅ 集成到 PDF 调研流程
- ✅ 添加使用示例和最佳实践

---

**学习完成时间**: 2026-02-19 21:20
**下次学习**: 深入探索爬虫高级功能和数据处理
