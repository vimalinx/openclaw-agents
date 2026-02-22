# 小红书自动回复系统 - 部署检查清单

使用系统前，请确认以下事项：

## ✅ 环境准备

- [ ] Python 3.7+ 已安装
- [ ] pip 命令可用
- [ ] 网络连接正常
- [ ] 有小红书账号

## ✅ 依赖安装

运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

检查以下包是否成功安装：

- [ ] requests
- [ ] schedule
- [ ] python-dotenv
- [ ] jieba
- [ ] pyyaml

## ✅ 配置设置

编辑 `config.json` 文件：

### 小红书配置

```json
{
  "xiaohongshu": {
    "cookies": "你的Cookies",         // ✅ 已填写
    "user_agent": "浏览器UA",          // ✅ 已配置（可选）
    "monitor_interval": 300,           // ✅ 已设置监控间隔
    "note_ids": ["笔记ID1", "笔记ID2"] // ✅ 已添加笔记ID
  }
}
```

检查清单：

- [ ] cookies 已填写（必需）
- [ ] user_agent 已配置（可选）
- [ ] monitor_interval 已设置（默认300秒）
- [ ] note_ids 已添加至少一个笔记ID（必需）

### 回复配置

```json
{
  "reply": {
    "auto_reply": true,               // ✅ 是否启用自动回复
    "max_reply_per_note": 20,          // ✅ 每日回复上限
    "reply_delay": 5,                  // ✅ 回复延迟（秒）
    "follow_after_reply": true        // ✅ 回复后是否引导关注
  }
}
```

检查清单：

- [ ] auto_reply 已设置
- [ ] max_reply_per_note 已设置（建议20-50）
- [ ] reply_delay 已设置（建议5-10秒）
- [ ] follow_after_reply 已设置

### 策略配置

```json
{
  "strategy": {
    "keyword_based": true,             // ✅ 启用关键词分类
    "sentiment_analysis": false,       // ✅ 情感分析（可选）
    "random_selection": true           // ✅ 随机选择模板
  }
}
```

检查清单：

- [ ] keyword_based 已启用
- [ ] random_selection 已启用

### 转化配置

```json
{
  "conversion": {
    "private_message_threshold": 3,    // ✅ 私信引导阈值
    "follow_suggestion_rate": 0.5,    // ✅ 关注建议概率（0-1）
    "cta_phrases": [                   // ✅ 转化关键词
      "想了解更多",
      "感兴趣",
      "咨询",
      "了解"
    ]
  }
}
```

检查清单：

- [ ] private_message_threshold 已设置
- [ ] follow_suggestion_rate 已设置（0-1）
- [ ] cta_phrases 已配置

### 存储配置

```json
{
  "storage": {
    "customer_db": "./data/customers.json",  // ✅ 客户数据库路径
    "reply_log": "./logs/reply.log"           // ✅ 回复日志路径
  }
}
```

检查清单：

- [ ] customer_db 路径正确
- [ ] reply_log 路径正确
- [ ] data/ 目录存在
- [ ] logs/ 目录存在

## ✅ 获取Cookies

### 步骤说明：

1. 打开浏览器（推荐Chrome）
2. 访问 https://www.xiaohongshu.com
3. 登录你的小红书账号
4. 按 `F12` 打开开发者工具
5. 切换到 `Network`（网络）标签
6. 刷新页面（F5）
7. 点击任意请求
8. 查看 `Request Headers` 中的 `Cookie`
9. 复制完整的Cookie值

检查清单：

- [ ] 已成功获取Cookie
- [ ] Cookie已完整复制到config.json
- [ ] Cookie格式正确（key=value; key2=value2）

## ✅ 获取笔记ID

### 步骤说明：

1. 打开你的笔记页面
2. 查看浏览器地址栏
3. URL格式：`https://www.xiaohongshu.com/explore/笔记ID`
4. 复制 `explore/` 后面的部分

示例：
```
https://www.xiaohongshu.com/explore/64f1a2b3c4d5e6f7
```
笔记ID为：`64f1a2b3c4d5e6f7`

检查清单：

- [ ] 已获取至少一个笔记ID
- [ ] 笔记ID已添加到config.json的note_ids数组
- [ ] 笔记ID格式正确

## ✅ 测试系统

运行测试套件：

```bash
python test.py
```

检查测试结果：

- [ ] 模板库测试通过
- [ ] 配置文件测试通过
- [ ] 回复策略测试通过
- [ ] 客户跟踪测试通过

## ✅ 功能验证

### 1. 回复模板验证

查看 `templates/reply_templates.json`：

- [ ] 各类别模板数量充足
- [ ] 模板内容符合你的需求
- [ ] 已自定义需要的模板

### 2. 客户跟踪验证

首次运行后：

- [ ] data/customers.json 文件已创建
- [ ] 客户数据正确记录
- [ ] 统计功能正常

### 3. 日志记录验证

首次回复后：

- [ ] logs/reply.log 文件已创建
- [ ] 日志格式正确
- [ ] 日志内容完整

## ✅ 运行测试

### 基础功能测试

```bash
# 运行测试套件
python test.py

# 查看帮助
python auto_reply.py --help
```

### 单模块测试

```bash
# 测试回复策略
python test.py strategy

# 测试客户跟踪
python test.py tracker

# 测试模板加载
python test.py templates

# 测试配置文件
python test.py config
```

检查清单：

- [ ] 所有测试通过
- [ ] 无错误提示
- [ ] 无警告信息

## ✅ 安全检查

- [ ] Cookies未分享给他人
- [ ] config.json未上传到公开仓库
- [ ] 客户数据已做好备份
- [ ] 回复内容符合平台规范

## ✅ 性能检查

- [ ] 监控间隔合理（建议300-600秒）
- [ ] 回复延迟充足（建议5-10秒）
- [ ] 每日回复量适中（建议20-50条）
- [ ] 系统资源占用正常

## ✅ 合规检查

- [ ] 了解小红书平台规则
- [ ] 回复内容不包含敏感词
- [ ] 不进行恶意刷屏
- [ ] 遵守反爬虫规则

## 🚀 启动系统

所有检查通过后，启动系统：

```bash
# 使用启动脚本（Linux/Mac）
./start.sh

# 使用启动脚本（Windows）
start.bat

# 或直接运行
python auto_reply.py
```

## 📋 常见问题

### Q: 提示Cookie无效？
A: Cookie会过期，需要重新获取。

### Q: 无法获取评论？
A: 检查网络连接，确认笔记ID正确，确认Cookie有效。

### Q: 回复发送失败？
A: 检查回复内容是否包含敏感词，确认账号状态正常。

### Q: 系统运行后没有响应？
A: 系统在监控中，有新评论会自动处理，可查看日志确认状态。

## 📞 获取帮助

如遇到问题：
1. 查看日志文件 `logs/reply.log`
2. 运行测试 `python test.py`
3. 查看文档 `README.md`
4. 检查配置文件格式

---

**检查通过后，系统即可投入使用！** 🎉
