# AI前沿信息周报生成器

自动采集 AI 领域最新动态，生成精美 PDF 周报。

## 功能特性

- 📚 **arXiv论文**: 自动抓取最新AI/ML/ML/NLP/CV领域论文
- 💬 **Hacker News**: 获取社区热门AI讨论
- 🐙 **GitHub**: 收集热门AI开源项目
- 🎨 **精美排版**: A4尺寸，专业设计，支持打印PDF

## 快速开始

### 1. 安装依赖

```bash
cd /home/vimalinx/.openclaw/workspace/ai_insights
pip install -r requirements.txt
```

### 2. 采集数据

```bash
python fetch_ai_insights.py
```

会采集：
- 15篇最新arXiv论文（7天内）
- 8条Hacker News热门讨论
- 6个GitHub热门项目

数据保存在 `data/ai_insights_YYYYMMDD.json`

### 3. 生成HTML

```bash
python generate_html.py
```

生成 `ai_insights_YYYYMMDD.html`，可在浏览器中预览。

### 4. 导出PDF

在浏览器中打开HTML文件，按 `Ctrl+P` (或 `Cmd+P`)，选择"保存为PDF"。

## 目录结构

```
ai_insights/
├── fetch_ai_insights.py    # 数据采集脚本
├── generate_html.py        # HTML生成脚本
├── requirements.txt         # Python依赖
├── README.md               # 说明文档
└── data/                   # 数据输出目录
    └── ai_insights_*.json  # 采集的数据
```

## 设计要点

参考 `travel_guides` 的设计：

✅ A4标准尺寸 (794px × 1123px)
✅ 高信息密度 (11px-14px字体)
✅ 半透明背景图 (12-15%透明度)
✅ 装饰图增强视觉效果
✅ 严禁分页破坏 (page-break-inside: avoid)
✅ 紫色主色调 (#667eea)

## 自定义配置

编辑 `fetch_ai_insights.py`:

- 采集天数: `days_back=7`
- 论文数量: `limit=15`
- 论文分类: 修改 `categories` 列表

## 数据源

- **arXiv API**: http://export.arxiv.org/api/query
- **Hacker News API**: https://github.com/HackerNews/API
- **GitHub**: 搜索API或手动维护热门列表

## 未来扩展

- [ ] 添加更多数据源（AI新闻网站）
- [ ] 实现自动定时任务
- [ ] 添加邮件/飞书推送
- [ ] 支持PDF自动生成（weasyprint）
- [ ] 添加历史趋势分析
