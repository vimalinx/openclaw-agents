#!/usr/bin/env python3
"""
高端旅行攻略生成器 V3 - 使用在线图片
采集小红书旅行攻略 + 高质量配图（在线）→ 设计精美网页 → 导出PDF
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class TravelGuideGeneratorV3:
    """旅行攻略生成器 V3 - 使用在线图片"""

    def __init__(self, output_dir: str = "./travel_guides_v3"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.guides = []

    # Unsplash Source API - 动态生成高质量旅行图片
    # 格式: https://source.unsplash.com/1600x900/?<keyword>
    # 精准匹配的旅行图片（来自Unsplash）
    IMAGE_MAPPINGS = {
        "云南": {
            "hero": "https://images.unsplash.com/photo-1568571950750-087508822d56?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1537588236776-8d0518b0d0ba?w=600&h=400&fit=crop",
                "https://images.unsplash.com/photo-1568571950750-087508822d56?w=600&h=400&fit=crop",
            ]
        },
        "日本京都": {
            "hero": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1528360983277-13d9b152c6d4?w=600&h=400&fit=crop",
                "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop",
            ]
        },
        "新疆": {
            "hero": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&h=400&fit=crop",
                "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600&h=400&fit=crop",
            ]
        },
        "四川成都": {
            "hero": "https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=600&h=400&fit=crop",
                "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=600&h=400&fit=crop",
            ]
        },
        "泰国清迈": {
            "hero": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1599960277428-4342628a890e?w=600&h=400&fit=crop",
                "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&h=400&fit=crop",
            ]
        },
        "封面": {
            "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&h=900&fit=crop",
            "images": []
        }
    }

    # 高质量旅行攻略
    SAMPLE_GUIDES = [
        {
            "title": "云南7天6晚完美攻略｜大理丽江香格里拉",
            "author": "旅行博主小A",
            "location": "云南",
            "days": 7,
            "cover": "#FF6B6B",
            "content": """
## 📍 Day 1-2: 大理｜风花雪月的浪漫

### 必去景点
- **洱海**：租一辆电瓶车环湖，全程130公里，沿途美景不断
- **双廊古镇**：艺术家聚集地，文艺气息浓厚
- **喜洲古镇**：品尝喜洲粑粑，体验白族文化

### 住宿推荐
- 大理古城：180-300元/晚，方便逛吃逛喝
- 双廊海边：400-800元/晚，推窗即是洱海

### 美食清单
- 喜洲粑粑 10元
- 酸辣鱼 68元
- 铜锅洋芋饭 25元
- 白族三道茶 38元

### 拍照机位
- 龙龛码头日出 6:30-7:00
- 双廊古镇下午 16:00-18:00
- 喜洲稻田黄昏 18:30-19:30
            """,
            "tips": "大理紫外线强，记得涂防晒！带墨镜和帽子拍照更出片。",
            "budget": "人均 3000-5000元"
        },
        {
            "title": "日本京都深度游｜千年古都的静美时光",
            "author": "日本旅行达人",
            "location": "日本京都",
            "days": 5,
            "cover": "#4ECDC4",
            "content": """
## 📍 Day 1: 伏见稻荷大社 + 清水寺

### 伏见稻荷大社
- **最佳时间**：清晨7点前，避开人流
- **拍照机位**：千本鸟居半山腰，光线最柔和
- **时长**：2-3小时

### 清水寺
- **必看**：悬空舞台的壮丽景色
- **和服体验**：清水寺周边3000日元/天
- **周边**：二年坂三年坂逛街

## 📍 Day 2: 岚山竹林 + 金阁寺

### 岚山竹林
- **最佳时间**：清晨或傍晚，光线最美
- **拍照**：竹林小径使用人像模式
- **必吃**：岚山豆腐料理

### 金阁寺
- **门票**：400日元
- **最佳拍摄**：湖面倒影，晴天效果最好

## 📍 Day 3: 奈良喂鹿 + 大阪美食

### 奈良公园
- **鹿仙贝**：150日元/包，小心小鹿很贪吃！
- **东大寺**：世界最大木造建筑，必看
- **春日大社**：朱红色建筑，拍照出片

### 大阪美食
- **道顿堀**：章鱼烧、大阪烧、拉面
- **黑门市场**：新鲜海鲜和水果
- **推荐店铺**：一兰拉面、千房大阪烧

### 住宿推荐
- 京都站周边：交通便利，性价比高
- 祇园区域：传统日式旅馆，体验满分
- 岚山区域：环境清幽，适合放松
            """,
            "tips": "建议购买JR Pass，7日券29370日元，非常划算！日本酒店需要提前1个月预订。",
            "budget": "人均 8000-12000元"
        },
        {
            "title": "新疆自驾30天｜穿越天山南北的壮美",
            "author": "户外探险家",
            "location": "新疆",
            "days": 30,
            "cover": "#FFE66D",
            "content": """
## 🚗 路线规划（乌鲁木齐往返）

### 第一段：北疆环线（12天）
乌鲁木齐 → 布尔津 → 喀纳斯 → 禾木 → 魔鬼城 → 克拉玛依

**喀纳斯湖**：中国最美湖泊之一，三湾必去
- 神仙湾：晨雾最美
- 月亮湾：经典机位
- 卧龙湾：拍照出片

**禾木村**：童话小屋，日出日落绝美
- 住宿：图瓦人小木屋
- 拍照：观景台全景

### 第二段：赛里木湖 + 独库公路（8天）
克拉玛依 → 赛里木湖 → 那拉提 → 巴音布鲁克 → 库车

**赛里木湖**：大西洋最后一滴眼泪
- 湖边露营：看星空银河
- 环湖公路：全程92公里
- 最佳时间：6-7月薰衣草盛开

**独库公路**：最美景观公路，566公里
- 一日四季：从戈壁到雪山
- 最高点：哈希勒根达坂（海拔3400米）
- 注意：仅6-10月开放

### 第三段：南疆人文（10天）
库车 → 喀什 → 帕米尔高原 → 喀什 → 乌鲁木齐

**喀什老城**：活着的千年古城
- 艾提尕尔清真寺
- 香妃园
- 百年老茶馆

**帕米尔高原**：世界屋脊
- 白沙湖：湖面如镜
- 卡拉库里湖：慕士塔格峰倒影
- 塔县：石头城遗址

## 🏠 住宿推荐
- 喀纳斯：湖边木屋 400-800元/晚
- 禾木：图瓦人家 200-400元/晚
- 赛里木湖：湖边房车营地 300元/晚
- 喀什：老城民宿 150-300元/晚

## 🍜 必吃美食
- 大盘鸡（沙湾最正宗）
- 手抓饭（和田最地道）
- 烤包子（喀什街头）
- 烤全羊（那拉提草原）
- 酸奶疙瘩（自制）
            """,
            "tips": "新疆昼夜温差大，一定要带厚外套！高原地区注意防晒和补水。自驾SUV最佳，独库公路弯道多需小心驾驶。",
            "budget": "人均 15000-20000元（租车+油费+住宿+门票）"
        },
        {
            "title": "四川成都深度游｜熊猫火锅慢生活",
            "author": "川渝吃货",
            "location": "四川成都",
            "days": 4,
            "cover": "#95E1D3",
            "content": """
## 📍 Day 1: 大熊猫基地 + 春熙路

### 大熊猫繁育研究基地
- **开放时间**：7:30-18:00
- **最佳时间**：8:00-10:00（熊猫最活跃）
- **门票**：58元，建议网上预订
- **必看**：太阳产房、月亮产房（小熊猫）

### 春熙路 + IFS太古里
- **IFS国际金融中心**：爬墙熊猫必打卡
- **太古里**：潮流商圈，适合逛街
- **小酒馆**：玉林路分店，网红打卡

## 📍 Day 2: 宽窄巷子 + 武侯祠 + 锦里

### 宽窄巷子
- **宽巷子**：老成都生活体验
- **窄巷子**：文艺小店集合
- **井巷子**：创意街区

### 武侯祠
- **门票**：50元
- **最佳游览**：下午，避开人流高峰

### 锦里
- **夜景**：18:30后灯笼亮起最美
- **小吃**：三大炮、糖油果子、钵钵鸡

## 📍 Day 3: 青城山 + 都江堰

### 青城山
- **门票**：80元，索道往返80元
- **推荐路线**：前山索道上山，步行下山
- **必看**：天师洞、上清宫、老君阁
- **时长**：4-5小时

### 都江堰
- **门票**：80元
- **必看**：鱼嘴、飞沙堰、宝瓶口
- **最佳时间**：16:00，夕阳下最美

## 📍 Day 4: 杜甫草堂 + 人民公园喝茶

### 杜甫草堂
- **门票**：50元
- **氛围**：幽静雅致，适合慢游
- **必看**：诗史堂、工部祠

### 人民公园
- **鹤鸣茶社**：百年老茶馆，必体验
- **茶价**：15-30元/杯
- **时间**：2-3小时，体验成都慢生活

## 🍲 美食清单

### 火锅必吃
- **蜀九香**：本地人最爱
- **大龙燚**：全国连锁，品质稳定
- **小龙坎**：人气网红店

### 成都小吃
- 兔头（双流老妈兔头）
- 冒菜（冒椒火辣）
- 冰粉（玫瑰冰粉）
- 钟水饺
- 龙抄手
- 甜水面

### 咖啡馆推荐
- 无早（太古里）
- 浮生（九眼桥）
- 一山杂物（芳沁街）

### 住宿推荐
- 春熙路商圈：200-400元/晚
- 太古里周边：400-800元/晚
- 宽窄巷子附近：300-600元/晚
            """,
            "tips": "成都慢节奏，建议每天只安排2-3个景点。火锅建议中午吃，避开排队高峰。3-4月和9-10月是最佳旅行季节。",
            "budget": "人均 2000-3000元"
        },
        {
            "title": "泰国清迈慢生活｜古城寺庙与夜市美食",
            "author": "东南亚旅行家",
            "location": "泰国清迈",
            "days": 5,
            "cover": "#DDA0DD",
            "content": """
## 📍 Day 1: 古城寺庙巡礼

### 契迪龙寺
- **门票**：40泰铢
- **特色**：宏大的古寺遗址，拍照出片
- **最佳时间**：清晨或黄昏

### 帕辛寺
- **门票**：20泰铢
- **特色**：兰纳风格建筑，金碧辉煌
- **必拍**：正殿佛像和白象

### 周日夜市（周日必去）
- **时间**：17:00-22:00
- **地点**：Ratchadamnoen Road
- **必买**：手工工艺品、泰丝、街头美食
- **推荐美食**：
  - 芒果糯米饭 60泰铢
  - 泰式炒河粉 50泰铢
  - 泰式奶茶 40泰铢
  - 椰子冰淇淋 50泰铢

## 📍 Day 2: 素贴山双龙寺 + 宁曼路

### 双龙寺
- **交通**：红色双条车上山 40泰铢
- **门票**：30泰铢
- **特色**：俯瞰清迈全景
- **最佳时间**：16:00，看日落

### 宁曼路（Nimman）
- **氛围**：文艺街区，咖啡馆和设计店聚集
- **必去**：
  - One Nimman 商场
  - Mayfair Shopping Mall
  - 各种咖啡馆

### 宁曼路咖啡馆推荐
- **Ristr8to**：世界级拉花咖啡
- **Cheevit Cheeva**：网红Bingsu（刨冰）
- **The Baristro**：手冲咖啡

## 📍 Day 3: 大象保护营 + 泰式SPA

### 大象保护营（推荐）
**Patara Elephant Farm**（需提前预约）
- **价格**：6000泰铢/人
- **体验**：喂大象、给大象洗澡、与大象互动
- **特色**：不骑大象，保护式体验

### 泰式SPA
**推荐店铺**：
- Lila Thai Massage（由前囚犯提供培训就业）
- Fah Lanna Spa（高端SPA）
- Let's Relax Spa（连锁，品质稳定）
- **价格**：500-1500泰铢/小时

## 📍 Day 4: 湄平河 + 瓦洛洛市场

### 湄平河
- **活动**：游船、日落餐厅
- **推荐餐厅**：The Good View，河边晚餐
- **价格**：人均 300-500泰铢

### 瓦洛洛市场
- **特色**：本地人市场，物价便宜
- **必买**：
  - 热带水果（榴莲 60-80泰铢/公斤）
  - 干货香料
  - 泰式甜点

## 📍 Day 5: 悠闲古城 + 离开

### 古城漫步
- 塔佩门：喂鸽子拍照
- 古城墙：骑行一周
- 咖啡馆发呆

### 纪念品推荐
- 泰丝围巾（100-200泰铢）
- 手工香皂（50-100泰铢）
- 泰式茶具（200-400泰铢）
- 调料包（50-100泰铢）

## 🏠 住宿推荐

### 古城区域
- **Rimping Village**：精品酒店，300-500元/晚
- **Buri Tara**：传统风格，200-350元/晚
- **Suriwongse Hotel**：位置极佳，150-250元/晚

### 宁曼路区域
- **Akyra Manor Chiang Mai**：设计感酒店，800-1200元/晚
- **MYSTIQUE Chiang Mai**：精品设计，400-600元/晚
- **X2 Chiang Mai**：现代风格，300-500元/晚

## 🍜 必吃美食清单

### 泰北菜必吃
- **Khao Soi（泰北咖喱面）**：Khao Soi Maesai
- **Sai Oua（泰北香肠）**：古城夜市
- **Nam Prik Ong（肉酱）**：配糯米饭吃

### 街头小吃
- **泰式炒粉**：50-60泰铢
- **烤肉串**：10-20泰铢/串
- **椰子汤**：60-80泰铢
- **烤鱼**：80-120泰铢

### 高端餐厅
- **David's Kitchen**：法泰融合
- **The House**：清迈老牌西餐厅
- **Huen Phen**：传统泰北菜

## 💡 旅行贴士

### 签证
- 中国公民落地签，2000泰铢
- 建议提前电子签证，300泰铢

### 交通
- **机场到古城**：红色双条车 80-100泰铢
- **Grab打车**：方便便宜，建议下载APP
- **双条车**：古城内主要交通工具，20-40泰铢

### 语言
- 英语通用，简单泰语：
  - 你好：Sawasdee Krub
  - 谢谢：Khob Khun Krub
  - 多少钱：Tao Rai Krub

### 货币
- 1元人民币 ≈ 5泰铢
- 建议携带现金，很多小店不支持刷卡
            """,
            "tips": "清迈6-10月是雨季，11-2月是最佳旅游季节。尊重佛教文化，进入寺庙需脱鞋，衣着得体。",
            "budget": "人均 3000-5000元"
        }
    ]

    def load_guides(self, guides=None):
        """加载攻略内容"""
        if guides:
            self.guides = guides
        else:
            self.guides = self.SAMPLE_GUIDES
        print(f"✅ 加载了 {len(self.guides)} 篇攻略")

    def get_images(self, location):
        """获取指定地点的图片URL"""
        return self.IMAGE_MAPPINGS.get(location, {
            "hero": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1600&h=900&fit=crop",
            "images": [
                "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&h=400&fit=crop"
            ]
        })

    def generate_html(self):
        """生成带图片的高端HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旅行攻略精选 | Travel Guides Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #FAFAFA;
            color: #2C3E50;
            line-height: 1.8;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
        }}

        /* 封面页 */
        .cover {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: url('{self.IMAGE_MAPPINGS['封面']['hero']}') center/cover no-repeat;
            position: relative;
            color: white;
            padding: 60px;
            page-break-after: always;
        }}

        .cover::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.88) 0%, rgba(118, 75, 162, 0.88) 100%);
        }}

        .cover > * {{
            position: relative;
            z-index: 1;
        }}

        .cover h1 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 72px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: 4px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        }}

        .cover .subtitle {{
            font-size: 28px;
            font-weight: 300;
            opacity: 0.95;
            margin-bottom: 60px;
            letter-spacing: 2px;
        }}

        .cover .info {{
            font-size: 18px;
            opacity: 0.9;
            text-align: center;
        }}

        .cover .info .divider {{
            width: 100px;
            height: 2px;
            background: rgba(255,255,255,0.6);
            margin: 40px auto;
        }}

        /* 目录页 */
        .toc-page {{
            min-height: 100vh;
            padding: 80px 100px;
            page-break-after: always;
        }}

        .toc-page h2 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 48px;
            margin-bottom: 60px;
            color: #667eea;
        }}

        .toc-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 35px;
        }}

        .toc-card {{
            display: flex;
            gap: 25px;
            padding: 25px;
            background: #F8F9FA;
            border-radius: 16px;
            transition: all 0.3s;
            border: 1px solid #E9ECEF;
        }}

        .toc-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.15);
            border-color: #667eea;
        }}

        .toc-card img {{
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        .toc-card .text {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .toc-card .title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 12px;
            color: #2C3E50;
        }}

        .toc-card .meta {{
            font-size: 15px;
            color: #7F8C8D;
        }}

        /* 攻略页 */
        .guide-page {{
            min-height: 100vh;
            padding: 0;
            page-break-after: always;
        }}

        .hero-image {{
            height: 45vh;
            background-size: cover;
            background-position: center;
            position: relative;
        }}

        .hero-image::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%);
        }}

        .guide-header {{
            padding: 35px 80px;
            display: flex;
            align-items: center;
            gap: 30px;
        }}

        .guide-info {{
            flex: 1;
        }}

        .guide-info .tag {{
            display: inline-block;
            padding: 10px 22px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 14px;
            font-weight: 500;
            border-radius: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}

        .guide-info h3 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 15px;
            line-height: 1.3;
            color: #2C3E50;
        }}

        .guide-info .meta {{
            display: flex;
            gap: 25px;
            font-size: 15px;
            color: #7F8C8D;
        }}

        .guide-content {{
            padding: 40px 80px 60px;
        }}

        .guide-content h4 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 28px;
            color: #2C3E50;
            margin: 40px 0 18px;
            padding-bottom: 14px;
            border-bottom: 3px solid #667eea;
        }}

        .guide-content p {{
            font-size: 17px;
            margin-bottom: 18px;
            color: #34495E;
            text-align: justify;
            line-height: 1.9;
        }}

        .guide-content ul {{
            margin-bottom: 25px;
            padding-left: 28px;
        }}

        .guide-content li {{
            font-size: 17px;
            margin-bottom: 12px;
            color: #34495E;
            line-height: 1.7;
        }}

        .guide-content strong {{
            color: #667eea;
            font-weight: 600;
        }}

        /* 图片画廊 */
        .gallery {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin: 40px 0;
        }}

        .gallery img {{
            width: 100%;
            height: 280px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
            transition: transform 0.3s;
        }}

        .gallery img:hover {{
            transform: scale(1.03);
        }}

        .highlight-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8f4f8 100%);
            border-left: 5px solid #667eea;
            padding: 28px 32px;
            margin: 35px 0;
            border-radius: 12px;
        }}

        .highlight-box h5 {{
            font-size: 19px;
            color: #667eea;
            margin-bottom: 16px;
        }}

        .highlight-box p {{
            font-size: 16px;
            margin-bottom: 12px;
        }}

        .tips-box {{
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-left: 5px solid #FFA726;
            padding: 28px 32px;
            margin: 35px 0;
            border-radius: 12px;
        }}

        .tips-box h5 {{
            font-size: 18px;
            color: #F57C00;
            margin-bottom: 12px;
        }}

        .tips-box p {{
            font-size: 16px;
            color: #6D4C41;
            margin-bottom: 8px;
        }}

        .budget-box {{
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-left: 5px solid #66BB6A;
            padding: 24px 32px;
            margin: 25px 0;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 18px;
            box-shadow: 0 4px 12px rgba(102, 187, 106, 0.2);
        }}

        .budget-box .icon {{
            font-size: 38px;
        }}

        .budget-box .text {{
            font-size: 18px;
            font-weight: 600;
            color: #2E7D32;
        }}

        /* 打印优化 */
        @media print {{
            @page {{
                margin: 0;
                size: A4;
            }}

            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 封面 -->
        <div class="cover">
            <h1>旅行攻略精选</h1>
            <p class="subtitle">TRAVEL GUIDES COLLECTION</p>
            <div class="info">
                <div class="divider"></div>
                <p>精选 {len(self.guides)} 篇深度旅行攻略</p>
                <p>从国内到国际，从城市到自然</p>
                <p>探索世界，发现美好</p>
                <p style="margin-top: 40px;">生成时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
            </div>
        </div>

        <!-- 目录 -->
        <div class="toc-page">
            <h2>目录 CONTENTS</h2>
            <div class="toc-grid">
"""

        # 添加目录卡片
        for i, guide in enumerate(self.guides, 1):
            images = self.get_images(guide['location'])
            html_content += f"""
                <div class="toc-card">
                    <img src="{images['hero']}" alt="{guide['location']}" onerror="this.src='https://via.placeholder.com/150x150/667eea/ffffff?text={guide['location']}'">
                    <div class="text">
                        <div class="title">{i}. {guide['title']}</div>
                        <div class="meta">📍 {guide['location']} · ⏱️ {guide['days']}天</div>
                    </div>
                </div>
"""

        html_content += """
            </div>
        </div>
"""

        # 添加攻略内容
        for i, guide in enumerate(self.guides, 1):
            images = self.get_images(guide['location'])
            html_content += f"""
        <!-- 攻略 {i} -->
        <div class="guide-page">
            <div class="hero-image" style="background-image: url('{images['hero']}')">
            </div>

            <div class="guide-header">
                <div class="guide-info">
                    <span class="tag">{guide['location']}</span>
                    <h3>{guide['title']}</h3>
                    <div class="meta">
                        <span>✍️ {guide['author']}</span>
                        <span>⏱️ {guide['days']}天</span>
                    </div>
                </div>
            </div>

            <div class="guide-content">
                {self._format_content(guide['content'])}

                <!-- 相关图片 -->
                <div class="gallery">
                    <img src="{images['images'][0]}"
                         onerror="this.src='https://via.placeholder.com/600x400/667eea/ffffff?text=风景'"
                         alt="风景">
                    <img src="{images['images'][1] if len(images['images']) > 1 else images['images'][0]}"
                         onerror="this.src='https://via.placeholder.com/600x400/764ba2/ffffff?text=美食'"
                         alt="风景">
                </div>

                <div class="tips-box">
                    <h5>💡 旅行贴士</h5>
                    <p>{guide['tips']}</p>
                </div>

                <div class="budget-box">
                    <span class="icon">💰</span>
                    <span class="text">{guide['budget']}</span>
                </div>
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        return html_content

    def _format_content(self, content):
        """格式化内容"""
        import re

        lines = content.strip().split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            line = line.strip()

            if line.startswith('##'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h4>{line[2:].strip()}</h4>')

            elif line.startswith('###'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h5>{line[3:].strip()}</h5>')

            elif line.startswith('-'):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                html_lines.append(f'<li>{line[1:].strip().replace("**", "<strong>").replace("**", "</strong>")}</li>')

            elif line.startswith('**'):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                text = line.replace('**', '').strip()
                html_lines.append(f'<p><strong>{text}</strong></p>')

            elif line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                text = line.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p>{text}</p>')

        if in_list:
            html_lines.append('</ul>')

        return '\n'.join(html_lines)

    def save_html(self):
        """保存HTML文件"""
        html_content = self.generate_html()
        html_file = self.output_dir / "travel_guides.html"
        html_file.write_text(html_content, encoding='utf-8')
        print(f"✅ HTML已保存: {html_file}")
        return html_file

    async def export_pdf(self):
        """导出PDF（使用Playwright）"""
        html_file = self.output_dir / "travel_guides.html"
        pdf_file = self.output_dir / "travel_guides.pdf"

        if not html_file.exists():
            raise FileNotFoundError(f"HTML文件不存在: {html_file}")

        print("📄 开始导出PDF...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto(f"file://{html_file.absolute()}", wait_until="networkidle")

            # 导出PDF
            await page.pdf(
                path=str(pdf_file),
                format="A4",
                print_background=True,
                margin={
                    "top": "0",
                    "bottom": "0",
                    "left": "0",
                    "right": "0"
                }
            )

            await browser.close()

        print(f"✅ PDF已导出: {pdf_file}")
        return pdf_file

    async def generate(self, export_pdf=True):
        """完整生成流程"""
        print("🚀 开始生成旅行攻略 V3（带真实图片）...")
        print(f"📁 输出目录: {self.output_dir}")

        # 加载攻略
        self.load_guides()

        # 生成HTML
        html_file = self.save_html()

        # 导出PDF
        if export_pdf:
            pdf_file = await self.export_pdf()
            return html_file, pdf_file
        else:
            return html_file, None


async def main():
    """主函数"""
    generator = TravelGuideGeneratorV3()

    # 生成
    html_file, pdf_file = await generator.generate(export_pdf=True)

    print("\n" + "="*60)
    print("✅ 生成完成！")
    print(f"📄 HTML: {html_file}")
    print(f"📄 PDF: {pdf_file}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
