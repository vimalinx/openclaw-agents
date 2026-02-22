# UI/UX Pro Max 学习笔记

## 项目概述

**仓库**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
**类型**: AI-powered Design Intelligence Toolkit
**版本**: v2.0
**核心价值**: 数据驱动的设计系统生成器 + BM25 搜索引擎

---

## 核心架构

### 1. 数据驱动知识库

| 数据类型 | 数量 | 文件 | 用途 |
|---------|------|------|------|
| 产品类型 | 96 | products.csv | 行业特定推荐 |
| UI 风格 | 67 | styles.csv | 风格匹配 |
| 颜色调色板 | 96 | colors.csv | 配色方案 |
| 字体搭配 | 57 | typography.csv | 排版建议 |
| 图表类型 | 25 | charts.csv | 数据可视化 |
| UX 指南 | 99 | ux-guidelines.csv | 最佳实践 |
| 技术栈指南 | 13 | stacks/*.csv | 框架特定指南 |

### 2. BM25 搜索引擎

**核心特点**:
- 自实现 BM25 排序算法（Python）
- 多列搜索支持
- 自动域名检测
- 无外部依赖

**关键代码**:
```python
class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1  # 词频饱和度
        self.b = b    # 文档长度归一化

    def score(self, query):
        # 计算 BM25 分数
        for token in query_tokens:
            if token in self.idf:
                tf = term_freqs[token]
                idf = self.idf[token]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                score += idf * numerator / denominator
```

**自动域名检测**:
```python
domain_keywords = {
    "color": ["color", "palette", "hex", "#", "rgb"],
    "chart": ["chart", "graph", "visualization", "trend"],
    "landing": ["landing", "page", "cta", "conversion"],
    "product": ["saas", "ecommerce", "fintech", "healthcare"],
    "style": ["style", "design", "ui", "minimalism", "glassmorphism"],
    "ux": ["ux", "usability", "accessibility", "wcag"],
    "typography": ["font", "typography", "serif", "sans"],
}
```

### 3. 设计系统生成器（v2.0 旗舰功能）

**工作流程**:
```
用户请求
    ↓
多域搜索（5 个并行）
    ↓
产品类型匹配（100 categories）
    ↓
风格推荐（67 styles, BM25 ranking）
    ↓
颜色选择（96 palettes）
    ↓
着陆页模式（24 patterns）
    ↓
排版搭配（57 font combinations）
    ↓
推理引擎（行业规则 + BM25）
    ↓
完整设计系统输出
```

**输出内容**:
- Pattern（页面结构）
- Style（视觉风格）
- Colors（配色方案）
- Typography（字体）
- Effects（动画效果）
- Anti-patterns（避免的设计）
- Pre-delivery checklist（交付前检查）

### 4. Master + Overrides 模式

**设计理念**: 分层设计系统，支持页面级覆盖

**目录结构**:
```
design-system/
├── MASTER.md           # 全局设计系统（colors, typography, spacing）
└── pages/
    ├── dashboard.md     # 仪表盘页面覆盖
    ├── checkout.md      # 结账页面覆盖
    └── profile.md      # 个人资料页覆盖
```

**检索逻辑**:
1. 首先检查 `design-system/pages/[page-name].md`
2. 如果存在，其规则覆盖 MASTER.md
3. 如果不存在，使用 MASTER.md

**持久化命令**:
```bash
# 生成并持久化到 design-system/MASTER.md
python3 scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp"

# 创建页面特定覆盖文件
python3 scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp" --page "dashboard"
```

---

## 关键学习点

### 1. 数据库设计

**CSV 数据结构特点**:
- 结构化数据（Product Type, Keywords, Recommendations）
- 语义化字段（Primary Style, Secondary Styles, Landing Page Pattern）
- 可搜索列（Keywords, Best For, Notes）

**产品设计逻辑**（以 Beauty/Spa 为例）:
```csv
No,Product Type,Keywords,Primary Style Recommendation,Landing Page Pattern,Color Palette Focus
34,Beauty/Spa,"beauty,booking,spa,wellness",Soft UI Evolution + Neumorphism,Hero-Centric + Social Proof,Soft pastels + Cream + Gold accents
```

### 2. 搜索引擎设计

**BM25 优势**:
- 比 TF-IDF 更准确
- 考虑文档长度归一化
- 词频饱和度参数（k1）
- 可调节的 b 参数

**正则表达式分词**:
```python
def tokenize(self, text):
    text = re.sub(r'[^\w\s]', ' ', str(text).lower())
    return [w for w in text.split() if len(w) > 2]
```

### 3. 模板化生成系统

**架构**:
```
src/ui-ux-pro-max/          # Source of Truth
├── data/                    # CSV 数据库
├── scripts/                 # Python 脚本
└── templates/               # 模板文件

cli/                         # CLI 安装工具
├── src/
│   ├── commands/init.ts     # 初始化命令
│   └── utils/template.ts    # 模板渲染引擎
└── assets/                  # 打包的资源
```

**同步规则**:
- Source of Truth: `src/ui-ux-pro-max/`
- 修改数据/脚本 → 编辑 src/
- CLI assets → 同步到 cli/assets/
- Reference folders → 由 CLI 动态生成

### 4. 多平台支持

**支持的 AI 助手**:
- Claude Code
- Cursor
- Windsurf
- Antigravity
- Codex CLI
- Continue
- Gemini CLI
- OpenCode
- Qoder
- CodeBuddy
- Droid (Factory)

**安装方式**:
```bash
# CLI 安装（推荐）
npm install -g uipro-cli

# Claude Marketplace
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### 5. 行业特定推理规则

**100 个行业规则**（每个规则包含）:
- **Pattern** - 页面结构
- **Style Priority** - 风格优先级（BM25 ranking）
- **Color Mood** - 行业适合的配色
- **Typography Mood** - 字体性格匹配
- **Key Effects** - 动画和交互
- **Anti-Patterns** - 避免的设计

**行业分类**:
- Tech & SaaS
- Finance
- Healthcare
- E-commerce
- Services
- Creative
- Emerging Tech

---

## 可复用的设计模式

### 1. CSV 数据库模式

**优点**:
- 易于编辑（Excel, Google Sheets）
- 版本控制友好
- 易于迁移

**适用场景**:
- 产品配置
- 风格指南
- 最佳实践库
- FAQ 系统

### 2. BM25 搜索引擎

**优点**:
- 无外部依赖
- 快速准确
- 可调节参数

**适用场景**:
- 文档搜索
- 产品推荐
- 代码片段搜索
- FAQ 匹配

### 3. Master + Overrides 模式

**优点**:
- 分层设计系统
- 页面级覆盖
- 易于维护

**适用场景**:
- 设计系统
- 配置管理
- 主题系统
- 国际化

### 4. 模板化生成系统

**优点**:
- Source of Truth 单一
- 多平台生成
- 易于扩展

**适用场景**:
- 跨平台 CLI 工具
- 代码生成器
- SDK 开发
- 多语言项目

---

## 实践应用

### 小红书自动化系统优化

可以借鉴 UI/UX Pro Max 的设计：

1. **数据驱动**:
   - 建立 CSV 数据库（爆款笔记分析、关键词库）
   - 产品类型分类（美妆、美食、旅游等）

2. **BM25 搜索**:
   - 关键词匹配（搜索热度、竞品分析）
   - 风格推荐（封面设计、文案风格）

3. **设计系统生成**:
   - 行业特定推荐（不同产品的运营策略）
   - Master + Overrides（全局策略 + 页面级覆盖）

### AI 代理系统

可以借鉴：

1. **知识库**:
   - 建立 CSV 数据库（技能、最佳实践、常见问题）
   - BM25 搜索（快速匹配用户需求）

2. **推理引擎**:
   - 行业特定规则（不同领域的代理）
   - Master + Overrides（全局行为 + 任务特定）

3. **模板化**:
   - Source of Truth 单一
   - 多平台生成（不同 AI 助手）

### AI 代理系统

可以借鉴：

1. **知识库**:
   - 建立 CSV 数据库（技能、最佳实践、常见问题）
   - BM25 搜索（快速匹配用户需求）

2. **推理引擎**:
   - 行业特定规则（不同领域的代理）
   - Master + Overrides（全局行为 + 任务特定）

3. **模板化**:
   - Source of Truth 单一
   - 多平台生成（不同 AI 助手）

---

## 技术栈分析

### 前端
- **数据存储**: CSV（易于编辑、版本控制）
- **搜索引擎**: Python BM25（无依赖、快速）
- **模板引擎**: TypeScript（CLI 生成）

### 后端
- **无后端**: 完全本地运行
- **CLI**: Node.js + Bun（快速安装）

### 部署
- **NPM**: `uipro-cli`
- **GitHub Marketplace**: Claude Code 集成
- **Open Source**: MIT License

---

## 关键洞察

### 1. 数据 > 算法

**核心价值**: 高质量的结构化数据比复杂的算法更重要

**启示**:
- 投入时间构建数据
- 使用简单但有效的算法
- 持续更新和优化数据

### 2. 分层设计

**核心价值**: Master + Overrides 模式提供灵活性

**启示**:
- 定义全局规则（MASTER）
- 允许页面级覆盖（pages/*）
- 简化维护和更新

### 3. 模板化生成

**核心价值**: Source of Truth 单一，多平台生成

**启示**:
- 定义 canonical source
- 使用模板引擎生成
- 自动化同步流程

### 4. 行业特定

**核心价值**: 100 个行业特定推理规则

**启示**:
- 不同领域有不同的需求
- 专业化 > 通用化
- 深度理解每个行业

---

## 下一步行动

### 立即行动
1. **克隆仓库**: `git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git`
2. **安装 CLI**: `npm install -g uipro-cli`
3. **测试搜索**: `uipro init --ai opencode`

### 短期规划
1. **学习数据结构**: 分析 CSV 文件的设计
2. **测试 BM25**: 实现简单的 BM25 搜索
3. **设计系统**: 应用 Master + Overrides 模式

### 长期规划
1. **数据驱动**: 为小红书自动化建立 CSV 数据库
2. **搜索引擎**: 实现 BM25 搜索（关键词、竞品）
3. **推理引擎**: 行业特定推荐规则

---

## 总结

**UI/UX Pro Max 是一个优秀的数据驱动设计系统**:

- ✅ **高质量数据**: 96 产品类型 + 67 风格 + 96 配色 + 57 字体
- ✅ **BM25 搜索**: 自实现，无外部依赖
- ✅ **设计系统生成器**: 多域搜索 + 推理引擎
- ✅ **Master + Overrides**: 分层设计系统
- ✅ **模板化生成**: Source of Truth 单一
- ✅ **多平台支持**: 10+ AI 助手

**可复用的设计模式**:
1. CSV 数据库模式
2. BM25 搜索引擎
3. Master + Overrides 模式
4. 模板化生成系统

**应用到现有项目**:
- 小红书自动化系统（数据驱动）
- VimaOS 设计系统（Master + Overrides）
- AI 代理系统（知识库 + 搜索）

---

**学习时间**: 2026-02-22
**学习质量**: ⭐⭐⭐⭐⭐ (5/5)
**实践价值**: ⭐⭐⭐⭐⭐ (5/5)
**推荐程度**: ⭐⭐⭐⭐⭐ (5/5)

我是 Wilson，你的 AI 助手。🐺

**"Data is the new oil, but you need to refine it."**
