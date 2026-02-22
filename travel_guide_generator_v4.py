#!/usr/bin/env python3
"""
高端旅行攻略生成器 V4 - 高密度布局
采集小红书旅行攻略 + 高质量配图 → 紧凑分栏设计 → 导出PDF
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class TravelGuideGeneratorV4:
    """旅行攻略生成器 V4 - 高密度分栏布局"""

    def __init__(self, output_dir: str = "./travel_guides_v4"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.guides = []

    # 精准匹配的旅行图片
    IMAGE_MAPPINGS = {
        "云南": {
            "hero": "https://images.unsplash.com/photo-1568571950750-087508822d56?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1537588236776-8d0518b0d0ba?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=400&h=300&fit=crop",
        },
        "日本京都": {
            "hero": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1528360983277-13d9b152c6d4?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&h=300&fit=crop",
        },
        "新疆": {
            "hero": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400&h=300&fit=crop",
        },
        "四川成都": {
            "hero": "https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=400&h=300&fit=crop",
        },
        "泰国清迈": {
            "hero": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1599960277428-4342628a890e?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1528181304800-259b08848526?w=400&h=300&fit=crop",
        },
        "封面": {
            "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&h=900&fit=crop",
            "small1": "",
            "small2": "",
        }
    }

    # 丰富的旅行攻略
    SAMPLE_GUIDES = [
        {
            "title": "云南7天6晚完美攻略｜大理丽江香格里拉",
            "author": "旅行博主小A",
            "location": "云南",
            "days": 7,
            "cover": "#FF6B6B",
            "best_time": "3-5月、9-11月",
            "budget": "人均 3000-5000元",
            "transport": "飞机直达大理/丽江，高铁3小时可达昆明",
            "days_detail": [
                {
                    "day": "Day 1-2",
                    "title": "大理｜风花雪月",
                    "spots": ["洱海", "双廊古镇", "喜洲古镇"],
                    "time": "2天",
                    "tips": "租电瓶车环湖，全程130公里，建议早上出发"
                },
                {
                    "day": "Day 3-4",
                    "title": "丽江｜古城韵味",
                    "spots": ["丽江古城", "束河古镇", "玉龙雪山"],
                    "time": "2天",
                    "tips": "玉龙雪山需提前订票，建议住古城方便逛街"
                },
                {
                    "day": "Day 5-7",
                    "title": "香格里拉｜高原秘境",
                    "spots": ["普达措公园", "松赞林寺", "纳帕海"],
                    "time": "3天",
                    "tips": "海拔较高，注意高反，提前准备氧气瓶"
                }
            ],
            "hotels": [
                {"name": "大理古城民宿", "price": "180-300元/晚", "feature": "方便逛吃逛喝"},
                {"name": "双廊海景房", "price": "400-800元/晚", "feature": "推窗即是洱海"},
                {"name": "丽江客栈", "price": "200-400元/晚", "feature": "纳西风情"},
                {"name": "香格里拉酒店", "price": "300-500元/晚", "feature": "藏式特色"},
            ],
            "foods": [
                {"name": "喜洲粑粑", "price": "10元", "feature": "外酥内嫩"},
                {"name": "酸辣鱼", "price": "68元", "feature": "酸辣开胃"},
                {"name": "铜锅洋芋饭", "price": "25元", "feature": "香糯可口"},
                {"name": "白族三道茶", "price": "38元", "feature": "一苦二甜三回味"},
                {"name": "丽江粑粑", "price": "8元", "feature": "油而不腻"},
                {"name": "牦牛火锅", "price": "88元", "feature": "高原特色"},
            ],
            "photo_spots": [
                {"name": "龙龛码头", "time": "6:30-7:00", "tip": "日出最佳"},
                {"name": "双廊古镇", "time": "16:00-18:00", "tip": "下午光线柔"},
                {"name": "喜洲稻田", "time": "18:30-19:30", "tip": "黄昏金色光线"},
                {"name": "玉龙雪山", "time": "上午", "tip": "避开下午云层"},
            ],
            "essentials": ["防晒霜", "墨镜", "帽子", "氧气瓶（香格里拉）", "保暖外套", "充电宝", "相机"],
            "tips": "大理紫外线强，一定涂防晒！香格里拉海拔3300米，注意高反。丽江古城商业化较重，推荐住束河古镇。带学生证部分景点有优惠。"
        },
        {
            "title": "日本京都深度游｜千年古都的静美时光",
            "author": "日本旅行达人",
            "location": "日本京都",
            "days": 5,
            "cover": "#4ECDC4",
            "best_time": "3-4月樱花季、11月红叶季",
            "budget": "人均 8000-12000元",
            "transport": "JR Pass 7日券29370日元，从东京新干线2.5小时",
            "days_detail": [
                {
                    "day": "Day 1",
                    "title": "伏见稻荷 + 清水寺",
                    "spots": ["伏见稻荷大社", "清水寺", "二年坂三年坂"],
                    "time": "1天",
                    "tips": "伏见稻荷7点前去避开人流，清水寺可体验和服"
                },
                {
                    "day": "Day 2",
                    "title": "岚山 + 金阁寺",
                    "spots": ["岚山竹林", "金阁寺", "天龙寺"],
                    "time": "1天",
                    "tips": "岚山竹林早晨最美，金阁寺晴天拍照效果佳"
                },
                {
                    "day": "Day 3",
                    "title": "奈良 + 大阪",
                    "spots": ["奈良公园", "东大寺", "道顿堀"],
                    "time": "1天",
                    "tips": "鹿仙贝150日元，小心小鹿很贪吃！"
                },
                {
                    "day": "Day 4",
                    "title": "祇园 + 二条城",
                    "spots": ["祇园", "八坂神社", "二条城"],
                    "time": "1天",
                    "tips": "傍晚可能有艺伎出没，但请勿拍照"
                },
                {
                    "day": "Day 5",
                    "title": "锦市场 + 返程",
                    "spots": ["锦市场", "京都站"],
                    "time": "半天",
                    "tips": "锦市场被称为'京都的厨房'，可品尝各种小吃"
                }
            ],
            "hotels": [
                {"name": "京都站周边酒店", "price": "500-800元/晚", "feature": "交通便利"},
                {"name": "祇园日式旅馆", "price": "800-1500元/晚", "feature": "传统体验"},
                {"name": "岚山温泉酒店", "price": "1000-2000元/晚", "feature": "含温泉"},
                {"name": "Airbnb民宿", "price": "400-600元/晚", "feature": "性价比高"},
            ],
            "foods": [
                {"name": "怀石料理", "price": "300-800元", "feature": "精致日式"},
                {"name": "抹茶甜点", "price": "30-60元", "feature": "宇治抹茶"},
                {"name": "章鱼烧", "price": "25元", "feature": "大阪特色"},
                {"name": "一兰拉面", "price": "45元", "feature": "拉面连锁"},
                {"name": "寿司", "price": "80-200元", "feature": "新鲜海产"},
                {"name": "天妇罗", "price": "60-120元", "feature": "酥脆口感"},
            ],
            "photo_spots": [
                {"name": "伏见稻荷", "time": "清晨", "tip": "千本鸟居半山腰"},
                {"name": "岚山竹林", "time": "早晨/傍晚", "tip": "光线最美"},
                {"name": "金阁寺", "time": "晴天上午", "tip": "湖面倒影"},
                {"name": "清水寺", "time": "下午", "tip": "悬空舞台"},
            ],
            "essentials": ["JR Pass", "Suica卡", "转换插头", "护照", "现金（很多地方不支持刷卡）", "舒适步行鞋", "便携Wi-Fi"],
            "tips": "建议购买JR Pass，7日券非常划算。日本酒店需提前1个月预订。进入寺庙需脱鞋，衣着得体。日本电车很准时，但末班车很早。"
        },
        {
            "title": "新疆自驾30天｜穿越天山南北的壮美",
            "author": "户外探险家",
            "location": "新疆",
            "days": 30,
            "cover": "#FFE66D",
            "best_time": "6-10月",
            "budget": "人均 15000-20000元",
            "transport": "自驾SUV，乌鲁木齐机场取还车，独库公路仅6-10月开放",
            "days_detail": [
                {
                    "day": "Day 1-12",
                    "title": "北疆环线",
                    "spots": ["乌鲁木齐", "布尔津", "喀纳斯", "禾木", "魔鬼城", "克拉玛依"],
                    "time": "12天",
                    "tips": "喀纳斯三湾必看（神仙湾、月亮湾、卧龙湾），禾木看日出日落"
                },
                {
                    "day": "Day 13-20",
                    "title": "独库公路",
                    "spots": ["克拉玛依", "赛里木湖", "那拉提", "巴音布鲁克", "库车"],
                    "time": "8天",
                    "tips": "一日四季，最高点哈希勒根达坂海拔3400米，注意高反"
                },
                {
                    "day": "Day 21-30",
                    "title": "南疆人文",
                    "spots": ["库车", "喀什", "帕米尔高原", "塔县", "返回乌鲁木齐"],
                    "time": "10天",
                    "tips": "喀什老城活着的千年古城，帕米尔高原世界屋脊"
                }
            ],
            "hotels": [
                {"name": "喀纳斯湖边木屋", "price": "400-800元/晚", "feature": "湖景房"},
                {"name": "禾木图瓦人家", "price": "200-400元/晚", "feature": "特色小木屋"},
                {"name": "赛里木湖房车营地", "price": "300元/晚", "feature": "看星空"},
                {"name": "喀什老城民宿", "price": "150-300元/晚", "feature": "民俗体验"},
            ],
            "foods": [
                {"name": "大盘鸡", "price": "88元", "feature": "沙湾最正宗"},
                {"name": "手抓饭", "price": "45元", "feature": "和田最地道"},
                {"name": "烤包子", "price": "8元", "feature": "喀什街头"},
                {"name": "烤全羊", "price": "388元", "feature": "那拉提草原"},
                {"name": "酸奶疙瘩", "price": "15元", "feature": "自制"},
                {"name": "馕", "price": "3元", "feature": "主食必备"},
            ],
            "photo_spots": [
                {"name": "喀纳斯", "time": "全天", "tip": "三湾必拍"},
                {"name": "禾木", "time": "日出日落", "tip": "观景台全景"},
                {"name": "赛里木湖", "time": "日出日落", "tip": "湖面如镜"},
                {"name": "帕米尔高原", "time": "上午", "tip": "雪山倒影"},
            ],
            "essentials": ["SUV租车", "自驾保险", "厚外套", "防晒用品", "氧气瓶", "高原药物", "备用轮胎", "应急工具箱"],
            "tips": "新疆昼夜温差大，带厚外套！高原地区注意防晒补水。独库公路弯道多需小心驾驶。新疆安检较多，预留充足时间。部分地区信号不好，提前下载离线地图。"
        },
        {
            "title": "四川成都深度游｜熊猫火锅慢生活",
            "author": "川渝吃货",
            "location": "四川成都",
            "days": 4,
            "cover": "#95E1D3",
            "best_time": "3-4月、9-10月",
            "budget": "人均 2000-3000元",
            "transport": "地铁方便，机场大巴30分钟到市区",
            "days_detail": [
                {
                    "day": "Day 1",
                    "title": "熊猫基地 + 春熙路",
                    "spots": ["大熊猫基地", "春熙路", "IFS太古里"],
                    "time": "1天",
                    "tips": "熊猫8:00-10:00最活跃，春熙路网红小酒馆打卡"
                },
                {
                    "day": "Day 2",
                    "title": "宽窄巷子 + 武侯祠",
                    "spots": ["宽窄巷子", "武侯祠", "锦里"],
                    "time": "1天",
                    "tips": "锦里18:30后灯笼亮起最美，小吃一条街"
                },
                {
                    "day": "Day 3",
                    "title": "青城山 + 都江堰",
                    "spots": ["青城山", "都江堰"],
                    "time": "1天",
                    "tips": "青城山索道上山步行下山，都江堰16:00看夕阳"
                },
                {
                    "day": "Day 4",
                    "title": "杜甫草堂 + 人民公园",
                    "spots": ["杜甫草堂", "人民公园"],
                    "time": "半天",
                    "tips": "人民公园鹤鸣茶社百年老茶馆，体验慢生活"
                }
            ],
            "hotels": [
                {"name": "春熙路商圈酒店", "price": "200-400元/晚", "feature": "交通方便"},
                {"name": "太古里周边", "price": "400-800元/晚", "feature": "潮流商圈"},
                {"name": "宽窄巷子附近", "price": "300-600元/晚", "feature": "文化氛围"},
                {"name": "天府广场", "price": "250-450元/晚", "feature": "中心位置"},
            ],
            "foods": [
                {"name": "火锅（蜀九香）", "price": "80-120元/人", "feature": "本地人最爱"},
                {"name": "兔头", "price": "15元/个", "feature": "双流老妈兔头"},
                {"name": "冒菜", "price": "35元", "feature": "冒椒火辣"},
                {"name": "冰粉", "price": "8元", "feature": "玫瑰冰粉"},
                {"name": "钟水饺", "price": "18元", "feature": "老字号"},
                {"name": "甜水面", "price": "12元", "feature": "甜辣口味"},
            ],
            "photo_spots": [
                {"name": "熊猫基地", "time": "8:00-10:00", "tip": "太阳月亮产房"},
                {"name": "IFS爬墙熊猫", "time": "全天", "tip": "经典打卡点"},
                {"name": "锦里夜景", "time": "18:30后", "tip": "灯笼夜景"},
                {"name": "宽窄巷子", "time": "下午", "tip": "人文建筑"},
            ],
            "essentials": ["防晒霜", "雨伞", "舒适步行鞋", "充电宝", "相机"],
            "tips": "成都慢节奏，建议每天只安排2-3个景点。火锅建议中午吃避开排队高峰。人民公园喝茶是必体验，鹤鸣茶社15-30元/杯。3-4月和9-10月是最佳季节。"
        },
        {
            "title": "泰国清迈慢生活｜古城寺庙与夜市美食",
            "author": "东南亚旅行家",
            "location": "泰国清迈",
            "days": 5,
            "cover": "#DDA0DD",
            "best_time": "11-2月（雨季后）",
            "budget": "人均 3000-5000元",
            "transport": "落地签2000泰铢，Grab打车方便，红色双条车20-40泰铢",
            "days_detail": [
                {
                    "day": "Day 1",
                    "title": "古城寺庙巡礼",
                    "spots": ["契迪龙寺", "帕辛寺", "周日夜市"],
                    "time": "1天",
                    "tips": "周日夜市17:00-22:00，必买手工工艺品"
                },
                {
                    "day": "Day 2",
                    "title": "双龙寺 + 宁曼路",
                    "spots": ["双龙寺", "宁曼路", "咖啡馆"],
                    "time": "1天",
                    "tips": "双龙寺16:00看日落，宁曼路文艺街区"
                },
                {
                    "day": "Day 3",
                    "title": "大象营 + SPA",
                    "spots": ["Patara大象营", "泰式SPA"],
                    "time": "1天",
                    "tips": "大象营6000泰铢/人，保护式体验不骑象"
                },
                {
                    "day": "Day 4",
                    "title": "湄平河 + 瓦洛洛市场",
                    "spots": ["湄平河", "瓦洛洛市场"],
                    "time": "1天",
                    "tips": "瓦洛洛市场本地人市场，物价便宜"
                },
                {
                    "day": "Day 5",
                    "title": "古城悠闲 + 返程",
                    "spots": ["塔佩门", "古城墙", "咖啡馆"],
                    "time": "半天",
                    "tips": "塔佩门喂鸽子，古城墙骑行"
                }
            ],
            "hotels": [
                {"name": "Rimping Village", "price": "300-500元/晚", "feature": "精品酒店"},
                {"name": "Buri Tara", "price": "200-350元/晚", "feature": "传统风格"},
                {"name": "Suriwongse Hotel", "price": "150-250元/晚", "feature": "位置极佳"},
                {"name": "Akyra Manor", "price": "800-1200元/晚", "feature": "设计感酒店"},
            ],
            "foods": [
                {"name": "Khao Soi泰北咖喱面", "price": "25元", "feature": "泰北特色"},
                {"name": "芒果糯米饭", "price": "12元", "feature": "甜品经典"},
                {"name": "泰式炒河粉", "price": "12元", "feature": "街头小吃"},
                {"name": "椰子冰淇淋", "price": "10元", "feature": "清凉解暑"},
                {"name": "泰式奶茶", "price": "8元", "feature": "橙色奶茶"},
                {"name": "烤肉串", "price": "3元/串", "feature": "夜市必吃"},
            ],
            "photo_spots": [
                {"name": "契迪龙寺", "time": "清晨/黄昏", "tip": "古寺遗址"},
                {"name": "双龙寺", "time": "16:00", "tip": "日落俯瞰"},
                {"name": "周日夜市", "time": "17:00后", "tip": "夜市氛围"},
                {"name": "宁曼路", "time": "下午", "tip": "文艺街区"},
            ],
            "essentials": ["防晒霜", "驱蚊水", "清凉油", "轻便夏装", "人字拖", "充电宝", "护照复印件", "现金泰铢"],
            "tips": "11-2月是最佳季节，6-10月是雨季。尊重佛教文化，进入寺庙脱鞋，衣着得体。建议提前电子签证300泰铢。Grab打车方便，下载APP。很多小店不支持刷卡，带现金。1元人民币≈5泰铢。"
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
            "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1200&h=600&fit=crop",
            "small1": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=400&h=300&fit=crop",
            "small2": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400&h=300&fit=crop",
        })

    def generate_html(self):
        """生成高密度布局HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>旅行攻略精选 | Travel Guides Collection</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #FAFAFA;
            color: #2C3E50;
            line-height: 1.6;
            font-size: 14px;
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
            padding: 40px;
            page-break-after: always;
        }}

        .cover::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        }}

        .cover > * {{
            position: relative;
            z-index: 1;
        }}

        .cover h1 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: 4px;
        }}

        .cover .subtitle {{
            font-size: 24px;
            font-weight: 300;
            opacity: 0.95;
            margin-bottom: 40px;
            letter-spacing: 2px;
        }}

        .cover .info {{
            font-size: 16px;
            opacity: 0.9;
            text-align: center;
        }}

        .cover .info .divider {{
            width: 100px;
            height: 2px;
            background: rgba(255,255,255,0.6);
            margin: 30px auto;
        }}

        /* 目录页 */
        .toc-page {{
            min-height: 100vh;
            padding: 50px 60px;
            page-break-after: always;
        }}

        .toc-page h2 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 40px;
            margin-bottom: 40px;
            color: #667eea;
        }}

        .toc-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}

        .toc-card {{
            display: flex;
            gap: 20px;
            padding: 20px;
            background: #F8F9FA;
            border-radius: 10px;
            border: 1px solid #E9ECEF;
        }}

        .toc-card img {{
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
        }}

        .toc-card .text {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .toc-card .title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
        }}

        .toc-card .meta {{
            font-size: 13px;
            color: #7F8C8D;
            line-height: 1.4;
        }}

        /* 攻略页 - 高密度三栏布局（不分页）*/
        .guide-page {{
            min-height: 100vh;
            padding: 0;
            page-break-inside: avoid;
        }}

        .guide-header {{
            padding: 25px 40px;
            display: flex;
            align-items: center;
            gap: 20px;
            border-bottom: 3px solid #667eea;
            position: relative;
            min-height: 200px;
        }}

        /* 半透明背景图片 */
        .guide-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.15;
            z-index: 0;
        }}

        .guide-info {{
            flex: 1;
            position: relative;
            z-index: 1;
        }}

        .guide-info .tag {{
            display: inline-block;
            padding: 6px 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 13px;
            font-weight: 500;
            border-radius: 20px;
            margin-bottom: 12px;
        }}

        .guide-info h3 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.3;
        }}

        .guide-info .meta {{
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: #7F8C8D;
            flex-wrap: wrap;
        }}

        .guide-info .meta span {{
            display: flex;
            align-items: center;
            gap: 5px;
            background: #F8F9FA;
            padding: 4px 10px;
            border-radius: 15px;
        }}

        /* 两栏主内容区 */
        .guide-content {{
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 25px;
            padding: 25px;
        }}

        .col {{
            background: #FDFDFD;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #F0F0F0;
        }}

        .col-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #E8E8E8;
        }}

        .col-header h4 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
        }}

        .day-card {{
            background: #F8F9FA;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 10px;
        }}

        .day-card .day-title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 15px;
        }}

        .day-card .spots {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 8px;
        }}

        .day-card .spots span {{
            background: #E8EAF6;
            color: #3F51B5;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
        }}

        .day-card .tip {{
            font-size: 12px;
            color: #7F8C8D;
            line-height: 1.4;
        }}

        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #F0F0F0;
            font-size: 14px;
        }}

        .info-item:last-child {{
            border-bottom: none;
        }}

        .info-item .label {{
            color: #7F8C8D;
        }}

        .info-item .value {{
            color: #2C3E50;
            font-weight: 500;
        }}

        .essentials-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
        }}

        .essential-item {{
            background: #FFF3E0;
            color: #E65100;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            text-align: center;
        }}

        .tip-box {{
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-left: 4px solid #FFA726;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 13px;
            color: #6D4C41;
            line-height: 1.5;
        }}

        /* 底部信息 */
        .footer-info {{
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 15px;
            padding: 15px;
            background: #F8F9FA;
            border-radius: 8px;
            margin-top: 15px;
        }}

        .footer-col h5 {{
            font-size: 16px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 12px;
        }}

        .footer-col .item {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 13px;
            border-bottom: 1px solid #E8E8E8;
        }}

        .footer-col .item:last-child {{
            border-bottom: none;
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
                <p style="margin-top: 30px;">生成时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
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
                    <img src="{images['hero']}" alt="{guide['location']}" onerror="this.src='https://via.placeholder.com/120x120/667eea/ffffff?text={guide['location']}'">
                    <div class="text">
                        <div class="title">{i}. {guide['title']}</div>
                        <div class="meta">📍 {guide['location']} · ⏱️ {guide['days']}天</div>
                        <div class="meta">💰 {guide['budget']}</div>
                        <div class="meta">📅 {guide['best_time']}</div>
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
            
            # 行程信息
            days_html = ""
            for day in guide['days_detail']:
                spots_html = "".join([f"<span>{s}</span>" for s in day['spots']])
                days_html += f"""
                    <div class="day-card">
                        <div class="day-title">{day['day']} - {day['title']}</div>
                        <div class="spots">{spots_html}</div>
                        <div class="tip">💡 {day['tips']}</div>
                    </div>
                """

            # 住宿信息
            hotels_html = ""
            for hotel in guide['hotels']:
                hotels_html += f"""
                    <div class="info-item">
                        <span class="label">{hotel['name']}</span>
                        <span class="value">{hotel['price']}</span>
                    </div>
                """

            # 美食信息
            foods_html = ""
            for food in guide['foods']:
                foods_html += f"""
                    <div class="info-item">
                        <span class="label">{food['name']}</span>
                        <span class="value">{food['price']}</span>
                    </div>
                """

            # 拍照机位
            photo_html = ""
            for spot in guide['photo_spots']:
                photo_html += f"""
                    <div class="day-card">
                        <div class="day-title">📷 {spot['name']}</div>
                        <div class="tip">⏰ {spot['time']} | {spot['tip']}</div>
                    </div>
                """

            # 必备物品
            essentials_html = "".join([f"<div class='essential-item'>{e}</div>" for e in guide['essentials']])

            html_content += f"""
        <!-- 攻略 {i} -->
        <div class="guide-page">
            <div class="guide-header">
                <style>
                    .guide-header-bg-{i}::before {{
                        background-image: url('{images['hero']}');
                    }}
                </style>
                <div class="guide-info guide-header-bg-{i}">
                    <span class="tag">{guide['location']}</span>
                    <h3>{guide['title']}</h3>
                    <div class="meta">
                        <span>✍️ {guide['author']}</span>
                        <span>⏱️ {guide['days']}天</span>
                        <span>📅 {guide['best_time']}</span>
                        <span>💰 {guide['budget']}</span>
                        <span>🚗 {guide['transport'][:30]}...</span>
                    </div>
                </div>
            </div>

            <div class="guide-content">
                <!-- 左栏：行程安排 -->
                <div class="col">
                    <div class="col-header">
                        <h4>📍 行程安排</h4>
                    </div>
                    {days_html}
                </div>

                <!-- 中栏：住宿+美食 -->
                <div class="col">
                    <div class="col-header">
                        <h4>🏨 住宿推荐</h4>
                    </div>
                    {hotels_html}
                    <div class="col-header" style="margin-top: 20px;">
                        <h4>🍜 美食清单</h4>
                    </div>
                    {foods_html}
                </div>

                <!-- 右栏：拍照+必备+贴士 -->
                <div class="col">
                    <div class="col-header">
                        <h4>📸 拍照机位</h4>
                    </div>
                    {photo_html}
                    <div class="col-header" style="margin-top: 15px;">
                        <h4>🎒 必备物品</h4>
                    </div>
                    <div class="essentials-grid">
                        {essentials_html}
                    </div>
                    <div class="tip-box">
                        <strong>💡 旅行贴士</strong><br>
                        {guide['tips']}
                    </div>
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

    def save_html(self):
        """保存HTML文件"""
        html_content = self.generate_html()
        html_file = self.output_dir / "travel_guides.html"
        html_file.write_text(html_content, encoding='utf-8')
        print(f"✅ HTML已保存: {html_file}")
        return html_file

    async def export_pdf(self):
        """导出PDF"""
        html_file = self.output_dir / "travel_guides.html"
        pdf_file = self.output_dir / "travel_guides.pdf"

        if not html_file.exists():
            raise FileNotFoundError(f"HTML文件不存在: {html_file}")

        print("📄 开始导出PDF...")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto(f"file://{html_file.absolute()}", wait_until="networkidle")

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
        print(f"📊 文件大小: {pdf_file.stat().st_size / (1024*1024):.2f} MB")
        return pdf_file

    async def generate(self, export_pdf=True):
        """完整生成流程"""
        print("🚀 开始生成旅行攻略 V4（高密度布局）...")
        print(f"📁 输出目录: {self.output_dir}")

        self.load_guides()
        html_file = self.save_html()

        if export_pdf:
            pdf_file = await self.export_pdf()
            return html_file, pdf_file
        else:
            return html_file, None


async def main():
    generator = TravelGuideGeneratorV4()
    html_file, pdf_file = await generator.generate(export_pdf=True)
    print("\n" + "="*60)
    print("✅ 生成完成！")
    print(f"📄 HTML: {html_file}")
    print(f"📄 PDF: {pdf_file}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
