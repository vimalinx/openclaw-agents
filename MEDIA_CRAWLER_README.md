# MediaCrawler - 自媒体平台爬虫 🕷️

**项目地址**: `/home/vimalinx/.openclaw/workspace/mediacrawler/`

**说明**: 这个项目是从 VimaOS_old 复制过来的，放在 workspace 中更安全，避免误删。

## 快速开始

### 1. 进入目录

```bash
cd /home/vimalinx/.openclaw/workspace/mediacrawler
```

### 2. 查看配置

```bash
cat config/base_config.py
```

### 3. 运行爬虫

```bash
# 爬取创作者主页数据
python3 main.py --platform xhs --type creator --creator_id <用户ID>

# 搜索关键词
python3 main.py --platform xhs --type search --keywords "<关键词>"

# 爬取指定笔记
python3 main.py --platform xhs --type detail --specified_id <笔记ID>
```

## 数据保存

数据保存在以下目录：

- **创作者信息**: `store/xhs/creator_*.json`
- **笔记数据**: `store/xhs/note_*.json`
- **图片**: `data/xhs/images/`
- **登录态**: `browser_data/cdp_xhs_user_data_dir/`

## 支持

- 小红书 (xhs)
- 抖音 (dy)
- 快手 (ks)
- B站 (bili)
- 微博 (wb)
- 贴吧 (tieba)
- 知乎 (zhihu)

## 注意事项

⚠️ 本项目仅供学习研究使用，禁止用于商业用途或非法活动。

## 更多信息

查看 README.md 获取详细文档。
