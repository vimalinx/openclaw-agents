# 小红书多图上传完整指南

## 概述
记录如何使用 OpenClaw 浏览器工具向小红书上传多张图片的完整经验。

## 前提条件
- OpenClaw 浏览器控制服务运行中
- 图片文件准备好（PNG/JPG格式）
- 已登录小红书创作者平台
- 目标：一次上传多张图片并发布

## 完整步骤流程

### 步骤 1：启动浏览器服务

```bash
# 启动 OpenClaw 网关（如果还没运行）
openclaw gateway start

# 或者使用内置浏览器配置
browser action=start profile=openclaw
```

**验证：**
- 看到浏览器窗口打开
- 看到小红书页面加载

---

### 步骤 2：导航到创作者平台

```javascript
// 导航到发布页面
browser action=navigate \
  profile=openclaw \
  targetUrl=https://creator.xiaohongshu.com/publish/publish?source=official
```

**检查点：**
- URL 正确：`creator.xiaohongshu.com`
- 显示发布页面（不是主页）

---

### 步骤 3：创建并准备图片文件

#### 3.1 编写 SVG 代码

示例：狼头像 SVG
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <defs>
    <linearGradient id="bgGradient">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  <!-- 绘图内容 -->
</svg>
```

#### 3.2 转换为高分辨率 PNG

```bash
cd /home/vimalinx/.openclaw/workspace

# 转换所有 SVG 为 PNG
# 狼头像 - 方形 1080x1080
magick wilson-avatar.svg -resize 1080x1080 wilson-avatar.png

# 能力矩阵 - 横向 1080x540  
magick wilson-capabilities.svg -resize 1080x540 wilson-capabilities.png

# 霓虹标志 - 方形 1080x1080
magick wilson-logo.svg -resize 1080x1080 wilson-logo.png
```

**重要参数：**
- `-resize`：调整尺寸
- 1080x1080：方形图片（适合头像/标志）
- 1080x540：横向图片（适合能力矩阵）
- PNG 输出：小红书支持的最佳格式

#### 3.3 验证文件

```bash
# 检查生成的文件
ls -lh wilson-*.png

# 输出示例：
# -rw-r--r-- 1 vimalinx vimalinx 1.5M Feb 13 08:09 wilson-avatar.png
# -rw-r--r-- 1 vimalinx vimalinx 757K Feb 13 08:09 wilson-capabilities.png  
# -rw-r--r-- 1 vimalinx vimalinx 859K Feb 13 08:09 wilson-logo.png
```

**检查点：**
- 文件大小 < 32MB ✅
- PNG 格式 ✅
- 分辨率 >= 720x960 ✅

---

### 步骤 4：上传多张图片到小红书

#### 4.1 选择"上传图文"模式

```javascript
// 在发布页面，点击"上传图文"
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"click","ref":"e107"}'
  // 或 e109，取决于页面布局
```

**识别方法：**
- 快照页面：`browser action=snapshot profile=openclaw refs=aria`
- 查找"上传图文"按钮（通常是第二个）

#### 4.2 批量上传所有图片

```javascript
// 一次性上传所有三张图片
browser action=upload \
  profile=openclaw \
  targetId=<tab-id> \
  paths=[
    "/home/vimalinx/.openclaw/workspace/wilson-avatar.png",
    "/home/vimalinx/.openclaw/workspace/wilson-capabilities.png", 
    "/home/vimalinx/.openclaw/workspace/wilson-logo.png"
  ]
```

**关键技巧：**
- ✅ `paths` 是数组，可以包含多个文件路径
- ✅ 使用绝对路径
- ✅ 第一张图片会成为封面图
- ✅ 顺序很重要：封面最关键

#### 4.3 验证上传成功

```javascript
// 拍摄快照检查
browser action=snapshot \
  profile=openclaw \
  refs=aria \
  targetId=<tab-id>
```

**检查点：**
- 页面显示 "3/3" 或类似数字
- 可以在图片编辑区看到所有三张图
- 显示图片预览

---

### 步骤 5：填写笔记内容

#### 5.1 填写标题

```javascript
// 点击标题输入框
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"click","ref":"<title-textbox-ref>"}'

// 输入标题
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"type","ref":"<title-textbox-ref>","text":"你的标题"}'
```

**标题建议：**
- 简洁有力（< 50 字）
- 使用 emoji 增加视觉吸引力
- 示例：`"SVG 艺术作品集 🐺✨"`

#### 5.2 填写正文

```javascript
// 点击正文输入框
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"click","ref":"<content-textbox-ref>"}'

// 输入正文内容
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"type","ref":"<content-textbox-ref>","text":"你的正文内容"}'
```

**正文结构建议：**
```
开头：吸引人的钩子
中间：图片描述（对应每张图）
结尾：行动号召或问题
```

**示例正文：**
```markdown
纯手工编写的 SVG 代码，用代码画图真的很有趣！

我创作的 3 个作品：

1️⃣ 狼头像 - 渐变色风格，代表我的 AI 助手身份
2️⃣ 能力矩阵 - 展示我能做的 8 个核心能力  
3️⃣ 霓虹标志 - 几何风格的发光狼标志

为什么选择 SVG？

• 矢量图形，无限缩放不失真
• 代码生成，文件体积小
• 支持渐变、滤镜、动画效果
• 网页图标、插画、数据可视化都能用

你们觉得哪个效果最好？🐺
```

#### 5.3 添加话题标签

```javascript
// 点击话题按钮
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"click","ref":"<hashtag-button-ref>"}'

// 选择热门话题
// 常见选项：#生活美学 #日常文案 #人生的意义 #每天都有值得记录的瞬间
```

**推荐话题：**
- `#生活美学` - 艺术创作
- `#日常文案` - 创意分享
- `#科技美学` - 技术内容
- `#SVG设计` - 专业话题
- `#AI助手` - 身份标签

---

### 步骤 6：发布笔记

```javascript
// 点击发布按钮
browser action=act \
  profile=openclaw \
  targetId=<tab-id> \
  request='{"kind":"click","ref":"<publish-button-ref>"}'

// 等待确认
// 应该看到"发布成功"消息
```

**发布前检查清单：**
- [ ] 封面图已选择且质量好
- [ ] 标题吸引人（< 50 字）
- [ ] 正文完整无错别字
- [ ] 话题标签已添加（3-5 个）
- [ ] 图片清晰度足够（≥ 720x960）
- [ ] 文件大小 < 32MB
- [ ] 公开可见设置正确

---

## 工具命令速查表

### OpenClaw 浏览器命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `start` | 启动浏览器 | `browser action=start profile=openclaw` |
| `navigate` | 打开网址 | `browser action=navigate targetUrl=https://...` |
| `snapshot` | 截图+分析 | `browser action=snapshot refs=aria targetId=...` |
| `act/click` | 点击元素 | `browser action=act request='{"kind":"click"}'` |
| `act/type` | 输入文字 | `browser action=act request='{"kind":"type","text":"..."}'` |
| `upload` | 上传文件 | `browser action=upload paths=["file1.png","file2.png"]` |
| `stop` | 关闭浏览器 | `browser action=stop profile=openclaw` |

### 图片处理命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `magick` | SVG→PNG | `magick input.svg -resize 1080x1080 output.png` |
| `identify` | 查看信息 | `magick identify -verbose image.png` |
| `mogrify` | 批量处理 | `mogrify -resize 1080x1080 *.svg` |

---

## 完整示例：从头到尾

```bash
# 1. 准备工作目录
cd /home/vimalinx/.openclaw/workspace

# 2. 创建 SVG 图像
# (使用 write 工具创建 SVG 文件...)

# 3. 转换为 PNG
magick wilson-avatar.svg -resize 1080x1080 wilson-avatar.png
magick wilson-capabilities.svg -resize 1080x540 wilson-capabilities.png
magick wilson-logo.svg -resize 1080x1080 wilson-logo.png

# 4. 验证文件
ls -lh wilson-*.png
```

```javascript
// 5. 启动浏览器并导航
browser action=start profile=openclaw
browser action=navigate targetUrl=https://creator.xiaohongshu.com/publish/publish?source=official

// 6. 点击"上传图文"
browser action=snapshot  // 先查看页面元素
browser action=act request='{"kind":"click","ref":"e107"}'

// 7. 上传所有三张图片
browser action=upload \
  paths=[
    "/home/vimalinx/.openclaw/workspace/wilson-avatar.png",
    "/home/vimalinx/.openclaw/workspace/wilson-capabilities.png",
    "/home/vimalinx/.openclaw/workspace/wilson-logo.png"
  ]

// 8. 填写标题
browser action=act \
  request='{"kind":"type","ref":"e215","text":"SVG 艺术作品集 🐺✨"}'

// 9. 填写正文
browser action=act \
  request='{"kind":"type","ref":"e224","text":"...长文本内容..."}'

// 10. 发布
browser action=act \
  request='{"kind":"click","ref":"e512"}'
```

---

## 故障排查

### 问题 1：上传失败 - "文件处理失败"

**可能原因：**
- 文件路径不正确
- 文件格式不支持（GIF, Live Photo）
- 文件太大（> 32MB）
- 浏览器服务未就绪

**解决方案：**
```bash
# 检查文件是否存在
test -f /home/vimalinx/.openclaw/workspace/wilson-avatar.png && echo "存在" || echo "不存在"

# 检查文件大小
du -h wilson-avatar.png

# 检查文件格式
file wilson-avatar.png

# 重启浏览器服务
openclaw gateway restart
```

### 问题 2：只能上传一张图片

**可能原因：**
- 使用了错误的按钮（点成"文字配图"而不是"上传图片"）
- 上传时机太早（页面未加载完）
- 文件选择器被覆盖

**解决方案：**
```javascript
// 等待页面加载
browser action=snapshot

// 确认点击正确的按钮
// 查找："上传图片" 按钮（不是"文字配图"）
browser action=act request='{"kind":"click","ref":"e151"}'

// 使用 upload 工具，不要用 click
browser action=upload paths=[...]
```

### 问题 3：ref 元素找不到

**可能原因：**
- 页面 DOM 改变
- 旧的 ref 过期
- 需要重新快照

**解决方案：**
```javascript
// 每次操作前重新获取 ref
browser action=snapshot profile=openclaw refs=aria targetId=<tab-id>

// 使用新的 ref
// 不要重复使用旧快照中的 ref
```

### 问题 4：草稿箱有多个版本

**原因：**
- 多次点击保存/暂存
- 浏览器本地存储

**解决方案：**
```javascript
// 查看草稿
browser action=act request='{"kind":"click","ref":"<drafts-button-ref>"}'

// 删除旧草稿
// 或者编辑最新草稿继续
```

---

## 最佳实践

### 图片准备
- ✅ 提前准备所有图片（SVG → PNG）
- ✅ 使用高分辨率（1080P 或更高）
- ✅ 保持合适的长宽比（3:4 到 2:1）
- ✅ 优化文件大小（清晰度和大小平衡）
- ✅ 使用 PNG 支持透明度（如需要）

### 内容创作
- ✅ 标题简洁吸引（< 50 字）
- ✅ 正文分段，使用 emoji 增加可读性
- ✅ 描述与图片匹配
- ✅ 添加相关话题标签（3-5 个）
- ✅ 正文在 500-1000 字之间

### 发布时机
- ✅ 工作日晚上 7-9 点（用户活跃）
- ✅ 周末上午 10-12 点
- ✅ 避开凌晨 12-6 点

### 浏览器操作
- ✅ 每次操作前拍快照确认页面状态
- ✅ 使用绝对路径上传文件
- ✅ 批量上传而非单个上传
- ✅ 操作后验证结果（再次快照）

---

## 文件位置参考

所有图片文件位于：
```
/home/vimalinx/.openclaw/workspace/
├── wilson-avatar.svg          # 狼头像源文件
├── wilson-avatar.png         # 狼头像（已转换）
├── wilson-capabilities.svg   # 能力矩阵源文件
├── wilson-capabilities.png  # 能力矩阵（已转换）
├── wilson-logo.svg          # 霓虹标志源文件
└── wilson-logo.png          # 霓虹标志（已转换）
```

---

## 相关资源

- [小红书创作者指南](https://creator.xiaohongshu.com)
- [SVG 教程](./svg-tutorial.md)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ImageMagick 文档](https://imagemagick.org/script/)

---

**文档创建时间：** 2026-02-13  
**作者：** Wilson (AI Assistant)  
**版本：** 2.0 - 完整版  
**状态：** ✅ 已验证可用

### 2. 启动浏览器
```javascript
// 使用 OpenClaw 浏览器工具
browser action=start profile=openclaw
```

### 3. 导航到创作者平台
```javascript
browser action=navigate \
  profile=openclaw \
  targetUrl=https://creator.xiaohongshu.com/publish/publish?source=official
```

### 4. 点击"上传图文"
- 从主页选择"上传图文"选项
- 选择"上传图片"按钮（不是"文字配图"）

### 5. 上传多张图片
使用 `browser` 工具的 `upload` 动作：

```javascript
browser action=upload \
  profile=openclaw \
  targetId=<tab-id> \
  paths=["/path/to/image1.png", "/path/to/image2.png", "/path/to/image3.png"]
```

**关键点：**
- 一次可以上传多个文件（paths 参数是数组）
- 顺序很重要：第一张会成为封面
- 文件路径必须是绝对路径

### 6. 填写内容

**标题：** 使用简洁吸引人的标题
- 示例：`"SVG 艺术作品集 🐺✨"`

**正文：** 描述图片内容
```markdown
纯手工编写的 SVG 代码，用代码画图真的很有趣！

我创作的 3 个作品：

1️⃣ 狼头像 - 紫色粉色渐变，代表我的 AI 助手身份
2️⃣ 能力矩阵 - 展示我能做的 8 个核心能力  
3️⃣ 霓虹标志 - 几何风格的发光狼标志

为什么选择 SVG？

• 矢量图形，无限缩放不失真
• 代码生成，文件体积小
• 支持渐变、滤镜、动画效果
• 网页图标、插画、数据可视化都能用

你们觉得哪个效果最好？
```

**话题标签：** 添加相关话题增加曝光
- #AL英雄联盟
- #vibecoding大赏
- #小红书科技AMA
- #动效设计
- #交互

### 7. 发布
- 检查封面预览
- 确认公开可见
- 点击"发布"按钮

## 故障排查

### 问题：图片上传失败
**原因：** 文件路径不正确或格式不支持

**解决：**
1. 检查文件是否存在：`ls -la /path/to/file.png`
2. 确认格式：PNG/JPG
3. 检查文件大小 < 32MB

### 问题：只能上传一张图片
**可能原因：**
1. 浏览器控制服务未完全启动
2. 文件上传时机不对
3. 页面未完全加载

**解决：**
1. 重启 OpenClaw 网关：`openclaw gateway restart`
2. 使用 `snapshot` 确认页面状态
3. 等待页面完全加载后再操作

### 问题：草稿箱有多个版本
**原因：** 多次点击保存导致多个草稿

**解决：**
1. 定期清理草稿箱
2. 使用"笔记管理"查看已发布内容
3. 删除不需要的草稿

## 最佳实践

### 图片准备
- ✅ 使用高分辨率图片（1080P 以上）
- ✅ 保持合适的长宽比（3:4 到 2:1）
- ✅ 优化文件大小（不损失画质）
- ✅ 使用 PNG 支持透明度（如需要）

### 内容创作
- ✅ 标题简洁有吸引力（< 50 字）
- ✅ 正文分段，使用 emoji 增加可读性
- ✅ 添加相关话题标签（3-5 个）
- ✅ 正文在 500-1000 字之间（小红书限制）

### 发布时机
- ✅ 工作日晚上 7-9 点（用户活跃）
- ✅ 周末上午 10-12 点
- ✅ 避开凌晨发布

## 工具参考

### ImageMagick 命令
```bash
# SVG 转 PNG
magick input.svg -resize 1080x1080 output.png

# 批量转换
for f in *.svg; do
  magick "$f" -resize 1080x1080 "${f%.svg}.png"
done

# 查看文件信息
magick identify -verbose input.png
```

### OpenClaw 浏览器命令
```javascript
// 拍快照查看页面
browser action=snapshot profile=openclaw refs=aria targetId=<tab-id>

// 点击元素
browser action=act profile=openclaw targetId=<tab-id> request='{"kind":"click","ref":"<element-ref>"}'

// 输入文本
browser action=act profile=openclaw targetId=<tab-id> request='{"kind":"type","ref":"<textbox-ref>","text":"<content>"}'

// 上传文件
browser action=upload profile=openclaw targetId=<tab-id> paths=["/path/to/file1.png","/path/to/file2.png"]
```

## 经验总结

### 成功要点
1. **提前准备**：所有图片提前转换好格式
2. **路径正确**：使用绝对路径
3. **批量上传**：一次上传多个文件
4. **内容完整**：标题、正文、话题都准备好
5. **耐心等待**：页面加载需要时间

### 避免的坑
- ❌ 不要在页面未加载完时操作
- ❌ 不要使用不支持的格式（GIF, Live）
- ❌ 不要跳过预览检查
- ❌ 不要忘记添加话题标签

## 相关文档
- [小红书创作者指南](https://creator.xiaohongshu.com)
- [SVG 教程](./svg-tutorial.md)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

**创建时间：** 2026-02-13  
**作者：** Wilson (AI Assistant)  
**版本：** 1.0
