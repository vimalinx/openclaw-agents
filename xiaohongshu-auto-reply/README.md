# 小红书自动评论回复系统

智能监控小红书笔记评论，自动回复并引导转化。

## 功能特性

✅ **评论监控** - 实时监控已发布笔记的新评论
✅ **智能回复** - 基于关键词和AI策略自动选择回复模板
✅ **转化引导** - 智能引导用户私信、关注
✅ **客户管理** - 记录客户互动历史，支持客户分级
✅ **模板管理** - 灵活的回复模板库

## 目录结构

```
xiaohongshu-auto-reply/
├── auto_reply.py          # 主程序
├── monitor.py             # 评论监控模块
├── reply_strategy.py      # 智能回复策略
├── customer_tracker.py    # 客户跟踪模块
├── test.py                # 测试脚本
├── config.json            # 配置文件
├── requirements.txt       # 依赖包
├── templates/             # 回复模板
│   └── reply_templates.json
├── data/                  # 数据目录（自动创建）
│   └── customers.json
└── logs/                  # 日志目录（自动创建）
    └── reply.log
```

## 快速开始

### 1. 安装依赖

```bash
cd xiaohongshu-auto-reply
pip install -r requirements.txt
```

### 2. 配置系统

编辑 `config.json` 文件：

```json
{
  "xiaohongshu": {
    "cookies": "your_cookies_here",        // 必填：你的小红书Cookies
    "user_agent": "Mozilla/5.0 ...",       // 用户代理
    "monitor_interval": 300,               // 监控间隔（秒）
    "note_ids": ["note_id_1", "note_id_2"] // 必填：要监控的笔记ID列表
  },
  "reply": {
    "auto_reply": true,                    // 是否自动回复
    "max_reply_per_note": 20,              // 每日回复上限
    "reply_delay": 5                       // 回复延迟（秒）
  }
}
```

#### 获取Cookies方法

1. 打开浏览器，登录小红书网页版
2. 按F12打开开发者工具
3. 切换到Network（网络）标签
4. 刷新页面
5. 找到任意请求，查看Headers中的Cookie
6. 复制完整的Cookie到配置文件

#### 获取笔记ID方法

1. 打开你的笔记页面
2. 查看浏览器地址栏
3. URL格式为：`https://www.xiaohongshu.com/explore/笔记ID`
4. 复制 `explore/` 后面的ID到配置文件

### 3. 运行系统

```bash
# 启动自动回复系统
python auto_reply.py

# 查看统计信息
python auto_reply.py --stats

# 查看客户列表
python auto_reply.py --customers all      # 所有客户
python auto_reply.py --customers vip      # VIP客户
python auto_reply.py.py --customers active  # 活跃客户
python auto_reply.py --customers new      # 新客户
```

### 4. 测试系统

```bash
# 运行所有测试
python test.py

# 运行单个测试
python test.py strategy    # 测试回复策略
python test.py tracker     # 测试客户跟踪
python test.py templates   # 测试模板加载
python test.py config      # 测试配置文件
```

## 回复模板管理

编辑 `templates/reply_templates.json` 来自定义回复模板：

```json
{
  "question": {
    "name": "疑问类",
    "templates": [
      "有具体想了解的吗？可以私信我详细聊聊~",
      "关于这个问题，我可以私信详细和你说明哦"
    ]
  },
  "praise": {
    "name": "赞美类",
    "templates": [
      "谢谢你的喜欢！欢迎关注我~",
      "开心你喜欢！多互动哦"
    ]
  }
}
```

### 支持的模板类别

- `greeting` - 问候类
- `question` - 疑问类
- `praise` - 赞美类
- `product` - 产品相关
- `price` - 价格相关
- `default` - 默认回复

## 智能策略说明

### 评论分类

系统自动识别评论类型：

- 包含"怎么"、"如何"、"吗" → 疑问类
- 包含"价格"、"多少钱" → 价格相关
- 包含"产品"、"怎么样"、"好用" → 产品相关
- 包含"棒"、"好"、"赞"、"喜欢" → 赞美类
- 包含"你好"、"哈喽" → 问候类

### 转化引导

满足以下条件时自动添加转化引导：

1. 评论包含转化关键词（"想了解更多"、"感兴趣"、"咨询"）
2. 首次互动且为疑问类评论
3. 满足随机概率（可配置）

转化引导示例：
- "👉 私信我，有惊喜等着你~"
- "🎁 关注我不迷路，后续有更多福利哦"

### 客户分级

根据互动次数自动分级：

| 互动次数 | 客户状态 |
|---------|---------|
| 0       | new（新客户） |
| 1-2     | contacted（已接触） |
| 3-4     | active（活跃客户） |
| ≥5      | vip（VIP客户） |

## 使用场景

### 场景1：产品推广

1. 发布产品笔记，将笔记ID添加到配置
2. 配置产品相关的回复模板
3. 启动系统，自动回复用户咨询
4. 引导用户私信了解详情

### 场景2：内容创作者

1. 监控所有笔记的评论
2. 使用赞美类模板感谢用户互动
3. 引导关注，增加粉丝
4. 通过客户统计了解粉丝活跃度

### 场景3：电商运营

1. 监控爆款笔记评论
2. 快速回复价格、购买问题
3. 记录高意向客户
4. 导出VIP客户进行精准营销

## 注意事项

⚠️ **使用限制**

- 小红书有反爬机制，频繁操作可能被限制
- 建议设置合理的回复延迟（5-10秒）
- 每日回复量不宜过大（建议20-50条）
- 注意维护账号健康度

⚠️ **内容合规**

- 回复内容需符合平台规范
- 避免过于营销化的语言
- 尊重用户，避免骚扰
- 定期检查回复日志

⚠️ **数据安全**

- Cookies包含敏感信息，注意保管
- 客户数据存储在本地，做好备份
- 不要分享包含个人信息的配置文件

## 常见问题

### Q: 系统无法获取评论？

A: 检查以下几点：
1. Cookies是否过期或错误
2. 笔记ID是否正确
3. 网络连接是否正常
4. 是否被小红书限制访问

### Q: 回复发送失败？

A: 可能原因：
1. 回复内容包含敏感词
2. 账号被限制发帖
3. Cookie失效
4. 网络超时

### Q: 如何停止系统？

A: 按 `Ctrl+C` 停止监控系统

### Q: 如何导出客户数据？

A: 客户数据存储在 `data/customers.json`，可直接复制使用

## 更新日志

### v1.0.0 (2026-02-20)

- ✅ 评论监控功能
- ✅ 智能回复策略
- ✅ 转化引导系统
- ✅ 客户跟踪记录
- ✅ 回复模板管理
- ✅ 完整的测试套件

## 技术支持

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件

## 免责声明

本工具仅供学习和研究使用。使用本工具产生的任何后果由使用者自行承担。请遵守小红书平台规则和相关法律法规。

---

**祝你运营顺利！** 🎉
