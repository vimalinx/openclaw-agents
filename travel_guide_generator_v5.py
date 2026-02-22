#!/usr/bin/env python3
"""
旅行攻略生成器 V5 - A4标准精确排版
按照A4尺寸（794px x 1123px）精确设计
"""

import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class TravelGuideGeneratorV5:
    """旅行攻略生成器 V5 - A4标准排版"""

    def __init__(self, output_dir: str = "./travel_guides_v5"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.guides = []

    # 图片映射
    IMAGE_MAPPINGS = {
        "云南": "https://images.unsplash.com/photo-1568571950750-087508822d56?w=1200&h=800&fit=crop",
        "日本京都": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=1200&h=800&fit=crop",
        "新疆": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=800&fit=crop",
        "四川成都": "https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=1200&h=800&fit=crop",
        "泰国清迈": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1200&h=800&fit=crop",
        "封面": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&h=900&fit=crop",
    }

    # 简化的旅行攻略
    SAMPLE_GUIDES = [
        {
            "title": "云南7天6晚完美攻略｜大理丽江香格里拉",
            "author": "旅行博主小A",
            "location": "云南",
            "days": 7,
            "best_time": "3-5月、9-11月",
            "budget": "3000-5000元",
            "transport": "飞机直达大理/丽江",
            "days_detail": [
                {"day": "D1-2", "title": "大理", "spots": "洱海·双廊·喜洲", "tip": "租电瓶车环湖"},
                {"day": "D3-4", "title": "丽江", "spots": "古城·束河·玉龙雪山", "tip": "住古城方便逛街"},
                {"day": "D5-7", "title": "香格里拉", "spots": "普达措·松赞林·纳帕海", "tip": "注意高反"},
            ],
            "hotels": "大理古城180-300 | 双廊海景400-800 | 丽江客栈200-400",
            "foods": "喜洲粑粑10元 | 酸辣鱼68元 | 铜锅洋芋饭25元",
            "photos": "龙龛码头日出 | 双廊下午 | 喜洲稻田黄昏",
            "essentials": "防晒霜·墨镜·帽子·氧气瓶·保暖外套",
            "tips": "大理紫外线强！香格里拉海拔3300米注意高反。丽江古城商业较重，推荐束河。",
        },
        {
            "title": "日本京都深度游｜千年古都的静美时光",
            "author": "日本旅行达人",
            "location": "日本京都",
            "days": 5,
            "best_time": "3-4月樱花季、11月红叶季",
            "budget": "8000-12000元",
            "transport": "JR Pass 7日券29370日元",
            "days_detail": [
                {"day": "D1", "title": "伏见稻荷+清水寺", "spots": "伏见稻荷大社·清水寺·二年坂", "tip": "7点前去避开人流"},
                {"day": "D2", "title": "岚山+金阁寺", "spots": "岚山竹林·金阁寺·天龙寺", "tip": "岚山清晨最美"},
                {"day": "D3", "title": "奈良+大阪", "spots": "奈良公园·东大寺·道顿堀", "tip": "鹿仙贝150日元"},
                {"day": "D4", "title": "祇园+二条城", "spots": "祇园·八坂神社·二条城", "tip": "傍晚可能有艺伎"},
                {"day": "D5", "title": "锦市场+返程", "spots": "锦市场·京都站", "tip": "被称为'京都的厨房'"},
            ],
            "hotels": "京都站500-800 | 祇园日式800-1500 | 岚山温泉1000-2000",
            "foods": "怀石料理300-800 | 抹茶甜点30-60 | 章鱼烧25元",
            "photos": "伏见稻荷清晨 | 岚山竹林 | 金阁寺晴天",
            "essentials": "JR Pass·Suica卡·转换插头·护照·现金",
            "tips": "建议购买JR Pass！日本酒店提前1个月预订。进入寺庙需脱鞋，衣着得体。",
        },
        {
            "title": "新疆自驾30天｜穿越天山南北的壮美",
            "author": "户外探险家",
            "location": "新疆",
            "days": 30,
            "best_time": "6-10月",
            "budget": "15000-20000元",
            "transport": "自驾SUV，独库公路6-10月开放",
            "days_detail": [
                {"day": "D1-12", "title": "北疆环线", "spots": "乌鲁木齐·布尔津·喀纳斯·禾木", "tip": "喀纳斯三湾必看"},
                {"day": "D13-20", "title": "独库公路", "spots": "克拉玛依·赛里木湖·那拉提·库车", "tip": "一日四季，海拔3400米"},
                {"day": "D21-30", "title": "南疆人文", "spots": "库车·喀什·帕米尔高原", "tip": "喀什老城活着的千年古城"},
            ],
            "hotels": "喀纳斯400-800 | 禾木200-400 | 赛里木湖300 | 喀什150-300",
            "foods": "大盘鸡88元 | 手抓饭45元 | 烤包子8元 | 馕3元",
            "photos": "喀纳斯全天 | 禾木日出日落 | 赛里木湖镜面",
            "essentials": "SUV租车·厚外套·防晒·氧气瓶·应急工具",
            "tips": "昼夜温差大带厚外套！独库公路弯道多小心驾驶。安检较多预留时间。",
        },
        {
            "title": "四川成都深度游｜熊猫火锅慢生活",
            "author": "川渝吃货",
            "location": "四川成都",
            "days": 4,
            "best_time": "3-4月、9-10月",
            "budget": "2000-3000元",
            "transport": "地铁方便，机场大巴30分钟到市区",
            "days_detail": [
                {"day": "D1", "title": "熊猫基地+春熙路", "spots": "熊猫基地·春熙路·IFS太古里", "tip": "8-10点熊猫最活跃"},
                {"day": "D2", "title": "宽窄巷子+武侯祠", "spots": "宽窄巷子·武侯祠·锦里", "tip": "锦里18:30后灯笼亮起"},
                {"day": "D3", "title": "青城山+都江堰", "spots": "青城山·都江堰", "tip": "都江堰16:00看夕阳"},
                {"day": "D4", "title": "杜甫草堂+人民公园", "spots": "杜甫草堂·人民公园", "tip": "鹤鸣茶社百年老茶馆"},
            ],
            "hotels": "春熙路200-400 | 太古里400-800 | 宽窄巷子300-600",
            "foods": "火锅80-120 | 兔头15元 | 冒菜35元 | 冰粉8元",
            "photos": "熊猫基地8-10点 | IFS爬墙熊猫 | 锦里夜景",
            "essentials": "防晒霜·雨伞·步行鞋·充电宝·相机",
            "tips": "慢节奏每天只安排2-3个景点。火锅中午吃避开排队。人民公园喝茶必体验！",
        },
        {
            "title": "泰国清迈慢生活｜古城寺庙与夜市美食",
            "author": "东南亚旅行家",
            "location": "泰国清迈",
            "days": 5,
            "best_time": "11-2月（雨季后）",
            "budget": "3000-5000元",
            "transport": "落地签2000泰铢，红色双条车20-40泰铢",
            "days_detail": [
                {"day": "D1", "title": "古城寺庙巡礼", "spots": "契迪龙寺·帕辛寺·周日夜市", "tip": "周日夜市17-22点"},
                {"day": "D2", "title": "双龙寺+宁曼路", "spots": "双龙寺·宁曼路·咖啡馆", "tip": "双龙寺16点看日落"},
                {"day": "D3", "title": "大象营+SPA", "spots": "Patara大象营·泰式SPA", "tip": "大象营6000泰铢，保护式体验"},
                {"day": "D4", "title": "湄平河+瓦洛洛", "spots": "湄平河·瓦洛洛市场", "tip": "瓦洛洛本地人市场"},
                {"day": "D5", "title": "古城悠闲+返程", "spots": "塔佩门·古城墙", "tip": "塔佩门喂鸽子"},
            ],
            "hotels": "古城300-500 | 宁曼路400-600 | Rimping300-500",
            "foods": "泰北咖喱面25元 | 芒果糯米饭12元 | 泰式奶茶8元",
            "photos": "契迪龙寺清晨 | 双龙寺日落 | 周日夜市",
            "essentials": "防晒霜·驱蚊水·清凉油·夏装·现金泰铢",
            "tips": "11-2月最佳季节！尊重佛教文化，进入寺庙脱鞋，衣着得体。很多小店不支持刷卡。",
        }
    ]

    def load_guides(self, guides=None):
        if guides:
            self.guides = guides
        else:
            self.guides = self.SAMPLE_GUIDES
        print(f"✅ 加载了 {len(self.guides)} 篇攻略")

    def get_images(self, location):
        return self.IMAGE_MAPPINGS.get(location, self.IMAGE_MAPPINGS["封面"])

    def generate_html(self):
        """生成A4标准排版HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
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
            font-size: 13px;
            line-height: 1.5;
            color: #2C3E50;
            background: white;
        }}

        .container {{
            width: 794px;  /* A4宽度 @ 96 DPI */
            margin: 0 auto;
            background: white;
        }}

        /* 封面 */
        .cover {{
            width: 794px;
            height: 1123px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: url('{self.IMAGE_MAPPINGS["封面"]}') center/cover;
            position: relative;
            color: white;
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
            font-size: 56px;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: 4px;
        }}

        .cover .subtitle {{
            font-size: 24px;
            font-weight: 300;
            margin-bottom: 40px;
            letter-spacing: 2px;
            opacity: 0.95;
        }}

        .cover .info {{
            font-size: 16px;
            opacity: 0.9;
            text-align: center;
        }}

        .cover .divider {{
            width: 100px;
            height: 2px;
            background: rgba(255,255,255,0.6);
            margin: 30px auto;
        }}

        /* 目录 */
        .toc {{
            width: 794px;
            min-height: 1123px;
            padding: 50px;
            page-break-after: always;
        }}

        .toc h2 {{
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

        .toc-card .info {{
            flex: 1;
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

        /* 攻略页 */
        .guide-page {{
            width: 794px;
            min-height: 1123px;
            page-break-after: always;
        }}

        /* 标题栏 + 半透明背景图 */
        .guide-header {{
            height: 180px;
            position: relative;
            display: flex;
            align-items: center;
            padding: 25px 40px;
            border-bottom: 3px solid #667eea;
        }}

        .guide-header-bg {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.12;
            z-index: 0;
        }}

        .guide-info {{
            position: relative;
            z-index: 1;
            flex: 1;
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
            gap: 12px;
            flex-wrap: wrap;
            font-size: 12px;
            color: #7F8C8D;
        }}

        .guide-info .meta span {{
            background: #F8F9FA;
            padding: 4px 10px;
            border-radius: 12px;
        }}

        /* 两栏内容 */
        .guide-content {{
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 20px;
            padding: 20px;
            height: 680px;
        }}

        .col {{
            background: #FDFDFD;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #F0F0F0;
            overflow: hidden;
        }}

        .col-header {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 2px solid #E8E8E8;
        }}

        .col-header h4 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 16px;
            font-weight: 600;
            color: #2C3E50;
        }}

        /* 行程卡片 */
        .day-card {{
            background: #F8F9FA;
            border-radius: 6px;
            padding: 10px;
            margin-bottom: 8px;
        }}

        .day-card .title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 6px;
            font-size: 13px;
        }}

        .day-card .detail {{
            font-size: 12px;
            color: #34495E;
            margin-bottom: 4px;
        }}

        .day-card .tip {{
            font-size: 11px;
            color: #7F8C8D;
            font-style: italic;
        }}

        /* 信息块 */
        .info-block {{
            margin-bottom: 15px;
        }}

        .info-block h5 {{
            font-size: 14px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 8px;
        }}

        .info-block p {{
            font-size: 12px;
            color: #34495E;
            line-height: 1.4;
            margin-bottom: 5px;
        }}

        /* 贴士框 */
        .tip-box {{
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-left: 4px solid #FFA726;
            padding: 12px;
            border-radius: 6px;
            font-size: 12px;
            color: #6D4C41;
            line-height: 1.4;
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
                <p style="margin-top: 25px;">生成时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
            </div>
        </div>

        <!-- 目录 -->
        <div class="toc">
            <h2>目录 CONTENTS</h2>
            <div class="toc-grid">
"""

        # 添加目录
        for i, guide in enumerate(self.guides, 1):
            html_content += f"""
                <div class="toc-card">
                    <div class="info">
                        <div class="title">{i}. {guide['title']}</div>
                        <div class="meta">📍 {guide['location']} · ⏱️ {guide['days']}天</div>
                        <div class="meta">💰 {guide['budget']} · 📅 {guide['best_time']}</div>
                    </div>
                </div>
"""

        html_content += """
            </div>
        </div>
"""

        # 添加攻略
        for i, guide in enumerate(self.guides, 1):
            bg_image = self.get_images(guide['location'])
            
            # 行程HTML
            days_html = ""
            for day in guide['days_detail']:
                days_html += f"""
                    <div class="day-card">
                        <div class="title">{day['day']} - {day['title']}</div>
                        <div class="detail">📍 {day['spots']}</div>
                        <div class="tip">💡 {day['tip']}</div>
                    </div>
                """

            html_content += f"""
        <!-- 攻略 {i} -->
        <div class="guide-page">
            <div class="guide-header">
                <div class="guide-header-bg" style="background-image: url('{bg_image}')"></div>
                <div class="guide-info">
                    <span class="tag">{guide['location']}</span>
                    <h3>{guide['title']}</h3>
                    <div class="meta">
                        <span>✍️ {guide['author']}</span>
                        <span>⏱️ {guide['days']}天</span>
                        <span>📅 {guide['best_time']}</span>
                        <span>💰 {guide['budget']}</span>
                        <span>🚗 {guide['transport'][:25]}...</span>
                    </div>
                </div>
            </div>

            <div class="guide-content">
                <div class="col">
                    <div class="col-header">
                        <h4>📍 行程安排</h4>
                    </div>
                    {days_html}
                </div>

                <div class="col">
                    <div class="info-block">
                        <h5>🏨 住宿推荐</h5>
                        <p>{guide['hotels']}</p>
                    </div>

                    <div class="info-block">
                        <h5>🍜 美食清单</h5>
                        <p>{guide['foods']}</p>
                    </div>

                    <div class="info-block">
                        <h5>📸 拍照机位</h5>
                        <p>{guide['photos']}</p>
                    </div>

                    <div class="info-block">
                        <h5>🎒 必备物品</h5>
                        <p>{guide['essentials']}</p>
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
        html_content = self.generate_html()
        html_file = self.output_dir / "travel_guides.html"
        html_file.write_text(html_content, encoding='utf-8')
        print(f"✅ HTML已保存: {html_file}")
        return html_file

    async def export_pdf(self):
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
        print("🚀 开始生成旅行攻略 V5（A4标准排版）...")
        print(f"📁 输出目录: {self.output_dir}")

        self.load_guides()
        html_file = self.save_html()

        if export_pdf:
            pdf_file = await self.export_pdf()
            return html_file, pdf_file
        else:
            return html_file, None


async def main():
    generator = TravelGuideGeneratorV5()
    html_file, pdf_file = await generator.generate(export_pdf=True)
    print("\n" + "="*60)
    print("✅ 生成完成！")
    print(f"📄 HTML: {html_file}")
    print(f"📄 PDF: {pdf_file}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
