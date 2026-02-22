#!/usr/bin/env python3
"""
旅行攻略生成器 V6 - 超高密度内容
每页塞满信息，字体更小，间距更紧凑
"""

import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class TravelGuideGeneratorV6:
    """旅行攻略生成器 V6 - 超高密度"""

    def __init__(self, output_dir: str = "./travel_guides_v6"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.guides = []

    # 图片映射
    IMAGE_MAPPINGS = {
        "云南": {
            "hero": "https://images.unsplash.com/photo-1568571950750-087508822d56?w=1200&h=800&fit=crop",
            "corner1": "https://images.unsplash.com/photo-1537588236776-8d0518b0d0ba?w=300&h=200&fit=crop",
            "corner2": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=300&h=200&fit=crop",
        },
        "日本京都": {
            "hero": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=1200&h=800&fit=crop",
            "corner1": "https://images.unsplash.com/photo-1528360983277-13d9b152c6d4?w=300&h=200&fit=crop",
            "corner2": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=300&h=200&fit=crop",
        },
        "新疆": {
            "hero": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=800&fit=crop",
            "corner1": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=300&h=200&fit=crop",
            "corner2": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=300&h=200&fit=crop",
        },
        "四川成都": {
            "hero": "https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=1200&h=800&fit=crop",
            "corner1": "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=300&h=200&fit=crop",
            "corner2": "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=300&h=200&fit=crop",
        },
        "泰国清迈": {
            "hero": "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1200&h=800&fit=crop",
            "corner1": "https://images.unsplash.com/photo-1599960277428-4342628a890e?w=300&h=200&fit=crop",
            "corner2": "https://images.unsplash.com/photo-1528181304800-259b08848526?w=300&h=200&fit=crop",
        },
        "封面": {
            "hero": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&h=900&fit=crop",
        },
    }

    # 超丰富的旅行攻略
    SAMPLE_GUIDES = [
        {
            "title": "云南7天6晚完美攻略｜大理丽江香格里拉",
            "author": "旅行博主小A",
            "location": "云南",
            "days": 7,
            "best_time": "3-5月、9-11月",
            "budget": "3000-5000元",
            "transport": "飞机直达大理/丽江，高铁3小时可达昆明",
            "visa": "无需签证",
            "timezone": "GMT+8",
            "weather": "15-25°C",
            "language": "汉语",
            "currency": "人民币（RMB）",
            "days_detail": [
                {"day": "D1-2", "title": "大理｜风花雪月", "spots": "洱海·双廊古镇·喜洲古镇·崇圣寺三塔·小普陀", "time": "2天", "tips": "租电瓶车环湖全程130公里，建议早上出发。洱海骑行最美路段是龙龛码头到双廊。喜洲粑粑必尝外酥内嫩！"},
                {"day": "D3-4", "title": "丽江｜古城韵味", "spots": "丽江古城·束河古镇·玉龙雪山·蓝月谷·白沙古镇", "time": "2天", "tips": "玉龙雪山需提前订票，建议住古城方便逛街。蓝月谷拍照最佳时间上午10-11点。束河古镇比丽江更安静"},
                {"day": "D5-7", "title": "香格里拉｜高原秘境", "spots": "普达措公园·松赞林寺·纳帕海·独克宗古城·白水台", "time": "3天", "tips": "海拔3300米，注意高反，提前准备氧气瓶。松赞林寺是小布达拉宫。普达措最美季节6-8月"},
            ],
            "hotels": [
                {"name": "大理古城民宿", "price": "180-300元/晚", "feature": "方便逛吃逛喝，推荐三月街周边", "rating": "4.2"},
                {"name": "双廊海景房", "price": "400-800元/晚", "feature": "推窗即是洱海，推窗见海", "rating": "4.6"},
                {"name": "丽江古城客栈", "price": "200-400元/晚", "feature": "纳西风情，古城中心位置", "rating": "4.3"},
                {"name": "束河古镇客栈", "price": "150-280元/晚", "feature": "安静舒适，比古城更安静", "rating": "4.4"},
                {"name": "香格里拉酒店", "price": "300-500元/晚", "feature": "藏式特色，有供氧设备", "rating": "4.1"},
            ],
            "foods": [
                {"name": "喜洲粑粑", "price": "10元", "feature": "外酥内嫩，传统白族小吃", "must_try": "✓"},
                {"name": "酸辣鱼", "price": "68元", "feature": "酸辣开胃，洱海特色", "must_try": "✓"},
                {"name": "铜锅洋芋饭", "price": "25元", "feature": "香糯可口，特色主食", "must_try": "✓"},
                {"name": "白族三道茶", "price": "38元", "feature": "一苦二甜三回味", "must_try": "✓"},
                {"name": "丽江粑粑", "price": "8元", "feature": "油而不腻，外酥里嫩", "must_try": "✓"},
                {"name": "牦牛火锅", "price": "88元", "feature": "高原特色，肉质鲜嫩", "must_try": "✓"},
                {"name": "酥油茶", "price": "15元", "feature": "藏族特色，补充能量", "must_try": "✓"},
                {"name": "青稞酒", "price": "20元", "feature": "藏族传统酒类", "must_try": "✓"},
            ],
            "photos": [
                {"name": "龙龛码头日出", "time": "6:30-7:00", "tip": "最佳日出点，拍倒影美", "equipment": "广角镜头"},
                {"name": "双廊古镇下午", "time": "16:00-18:00", "tip": "下午光线柔和", "equipment": "标准镜头"},
                {"name": "喜洲稻田黄昏", "time": "18:30-19:30", "tip": "黄昏金色光线", "equipment": "广角镜头"},
                {"name": "玉龙雪山", "time": "上午", "tip": "避开下午云层", "equipment": "长焦镜头"},
                {"name": "蓝月谷", "time": "10:00-11:00", "tip": "湖水碧绿如玉", "equipment": "广角镜头"},
                {"name": "松赞林寺", "time": "下午", "tip": "金色光线照金顶", "equipment": "标准镜头"},
            ],
            "essentials": ["防晒霜SPF50+", "墨镜", "帽子", "氧气瓶（香格里拉）", "保暖外套", "充电宝", "相机", "舒适步行鞋", "防蚊液", "雨伞"],
            "tips": "大理紫外线强，一定涂防晒！香格里拉海拔3300米，注意高反，备氧气瓶。丽江古城商业化较重，推荐住束河古镇。带学生证部分景点有优惠。云南口味偏酸辣，吃不了可提前告知。3-5月和9-11月是最佳季节，避开7-8月雨季。租车建议SUV，山路较多。准备些现金，部分地区信号不好。",
        },
        {
            "title": "日本京都深度游｜千年古都的静美时光",
            "author": "日本旅行达人",
            "location": "日本京都",
            "days": 5,
            "best_time": "3-4月樱花季、11月红叶季",
            "budget": "8000-12000元",
            "transport": "JR Pass 7日券29370日元，从东京新干线2.5小时",
            "visa": "免签（15天）",
            "timezone": "GMT+9",
            "weather": "10-20°C",
            "language": "日语、英语",
            "currency": "日元（JPY）",
            "days_detail": [
                {"day": "D1", "title": "伏见稻荷+清水寺", "spots": "伏见稻荷大社·清水寺·二年坂三年坂·八坂神社", "time": "1天", "tips": "伏见稻荷7点前去避开人流，清水寺可体验和服。千本鸟居最美在半山腰。二年坂三年坂逛吃逛喝，很多特色小店"},
                {"day": "D2", "title": "岚山+金阁寺", "spots": "岚山竹林·金阁寺·天龙寺·渡月桥", "time": "1天", "tips": "岚山竹林早晨最美，金阁寺晴天拍照效果佳。岚山小火车推荐坐到龟山公园。天龙寺枯山水值得看"},
                {"day": "D3", "title": "奈良+大阪", "spots": "奈良公园·东大寺·春日大社·道顿堀·黑门市场", "time": "1天", "tips": "鹿仙贝150日元，小心小鹿很贪吃！东大寺世界最大木造建筑。大阪道顿堀是美食天堂，章鱼烧、大阪烧必尝"},
                {"day": "D4", "title": "祇园+二条城", "spots": "祇园·八坂神社·二条城·锦市场", "time": "1天", "tips": "傍晚可能有艺伎出没，但请勿拍照。二条城是德川家康的居城。锦市场被称为'京都的厨房'"},
                {"day": "D5", "title": "锦市场+返程", "spots": "锦市场·京都站", "time": "半天", "tips": "锦市场可品尝各种小吃，章鱼烧、玉子烧必尝。京都站购物方便，很多伴手礼"},
            ],
            "hotels": [
                {"name": "京都站周边酒店", "price": "500-800元/晚", "feature": "交通便利，购物方便", "rating": "4.3"},
                {"name": "祇园日式旅馆", "price": "800-1500元/晚", "feature": "传统体验，有温泉", "rating": "4.7"},
                {"name": "岚山温泉酒店", "price": "1000-2000元/晚", "feature": "含温泉，环境清幽", "rating": "4.5"},
                {"name": "Airbnb民宿", "price": "400-600元/晚", "feature": "性价比高，有厨房", "rating": "4.2"},
                {"name": "锦市场周边", "price": "600-900元/晚", "feature": "美食环绕，夜市方便", "rating": "4.4"},
            ],
            "foods": [
                {"name": "怀石料理", "price": "300-800元", "feature": "精致日式，一菜一味", "must_try": "✓"},
                {"name": "抹茶甜点", "price": "30-60元", "feature": "宇治抹茶，口感细腻", "must_try": "✓"},
                {"name": "章鱼烧", "price": "25元", "feature": "大阪特色，外酥里嫩", "must_try": "✓"},
                {"name": "一兰拉面", "price": "45元", "feature": "拉面连锁，品质稳定", "must_try": "✓"},
                {"name": "寿司", "price": "80-200元", "feature": "新鲜海产，传统日式", "must_try": "✓"},
                {"name": "天妇罗", "price": "60-120元", "feature": "酥脆口感，油炸食品", "must_try": "✓"},
                {"name": "玉子烧", "price": "15元", "feature": "甜蛋卷，京都特色", "must_try": "✓"},
                {"name": "关东煮", "price": "35元", "feature": "煮物，暖胃美食", "must_try": "✓"},
            ],
            "photos": [
                {"name": "伏见稻荷", "time": "清晨", "tip": "千本鸟居半山腰，光线最美", "equipment": "广角镜头"},
                {"name": "岚山竹林", "time": "早晨/傍晚", "tip": "光线最美，绿色治愈", "equipment": "标准镜头"},
                {"name": "金阁寺", "time": "晴天上午", "tip": "湖面倒影最佳", "equipment": "标准镜头"},
                {"name": "清水寺", "time": "下午", "tip": "悬空舞台壮丽", "equipment": "广角镜头"},
                {"name": "奈良公园", "time": "上午", "tip": "小鹿最活跃", "equipment": "长焦镜头"},
                {"name": "祇园街景", "time": "傍晚", "tip": "可能有艺伎", "equipment": "标准镜头"},
            ],
            "essentials": ["JR Pass", "Suica卡", "转换插头", "护照", "现金（很多地方不支持刷卡）", "舒适步行鞋", "便携Wi-Fi", "雨伞"],
            "tips": "建议购买JR Pass，7日券非常划算。日本酒店需提前1个月预订。进入寺庙需脱鞋，衣着得体。日本电车很准时，但末班车很早（11点左右）。建议下载Google Maps和换乘案内APP。日本很多地方不支持刷卡，带现金。1元人民币≈5日元。樱花季和红叶季住宿提前3-6个月预订。日本便利店7-11、Lawson很方便，可买饭团、便当。",
        },
        {
            "title": "新疆自驾30天｜穿越天山南北的壮美",
            "author": "户外探险家",
            "location": "新疆",
            "days": 30,
            "best_time": "6-10月",
            "budget": "15000-20000元",
            "transport": "自驾SUV，乌鲁木齐机场取还车，独库公路仅6-10月开放",
            "visa": "无需签证",
            "timezone": "GMT+8",
            "weather": "5-25°C",
            "language": "汉语、维吾尔语",
            "currency": "人民币（RMB）",
            "days_detail": [
                {"day": "D1-12", "title": "北疆环线", "spots": "乌鲁木齐·布尔津·喀纳斯·禾木·魔鬼城·克拉玛依", "time": "12天", "tips": "喀纳斯三湾必看（神仙湾、月亮湾、卧龙湾），禾木看日出日落。布尔津是进入喀纳斯的门户，可在此休整。魔鬼城风蚀地貌，日落时分最美"},
                {"day": "D13-20", "title": "独库公路", "spots": "克拉玛依·赛里木湖·那拉提·巴音布鲁克·库车", "time": "8天", "tips": "一日四季，最高点哈希勒根达坂海拔3400米，注意高反。赛里木湖大西洋最后一滴眼泪，湖边露营看星空。那拉提草原6月最美"},
                {"day": "D21-30", "title": "南疆人文", "spots": "库车·喀什·帕米尔高原·塔县·返回乌鲁木齐", "time": "10天", "tips": "喀什老城活着的千年古城，帕米尔高原世界屋脊。白沙湖湖面如镜，卡拉库里湖慕士塔格峰倒影。塔县石头城遗址值得一看"},
            ],
            "hotels": [
                {"name": "喀纳斯湖边木屋", "price": "400-800元/晚", "feature": "湖景房，早起看日出", "rating": "4.2"},
                {"name": "禾木图瓦人家", "price": "200-400元/晚", "feature": "特色小木屋，图瓦人体验", "rating": "4.4"},
                {"name": "赛里木湖房车营地", "price": "300元/晚", "feature": "湖边露营，看星空", "rating": "4.3"},
                {"name": "那拉提草原毡房", "price": "250-450元/晚", "feature": "草原毡房，草原体验", "rating": "4.1"},
                {"name": "喀什老城民宿", "price": "150-300元/晚", "feature": "民俗体验，老城中心", "rating": "4.5"},
                {"name": "帕米尔高原民宿", "price": "200-350元/晚", "feature": "高原民宿，含供氧", "rating": "4.2"},
            ],
            "foods": [
                {"name": "大盘鸡", "price": "88元", "feature": "沙湾最正宗，鸡肉入味", "must_try": "✓"},
                {"name": "手抓饭", "price": "45元", "feature": "和田最地道，羊肉香", "must_try": "✓"},
                {"name": "烤包子", "price": "8元", "feature": "喀什街头，皮脆肉嫩", "must_try": "✓"},
                {"name": "烤全羊", "price": "388元", "feature": "那拉提草原，仪式感", "must_try": "✓"},
                {"name": "酸奶疙瘩", "price": "15元", "feature": "自制，酸甜开胃", "must_try": "✓"},
                {"name": "馕", "price": "3元", "feature": "主食必备，可保存", "must_try": "✓"},
                {"name": "油塔子", "price": "18元", "feature": "新疆特色，层层酥脆", "must_try": "✓"},
                {"name": "烤羊肉串", "price": "12元/串", "feature": "新疆夜市，必吃", "must_try": "✓"},
            ],
            "photos": [
                {"name": "喀纳斯", "time": "全天", "tip": "三湾必拍，神仙湾晨雾", "equipment": "广角+长焦"},
                {"name": "禾木", "time": "日出日落", "tip": "观景台全景，童话小屋", "equipment": "广角镜头"},
                {"name": "赛里木湖", "time": "日出日落", "tip": "湖面如镜，雪山倒影", "equipment": "广角镜头"},
                {"name": "帕米尔高原", "time": "上午", "tip": "雪山倒影，高原风光", "equipment": "长焦镜头"},
                {"name": "魔鬼城", "time": "傍晚", "tip": "风蚀地貌，日落最美", "equipment": "标准镜头"},
                {"name": "独库公路", "time": "全天", "tip": "一日四季，壮丽景观", "equipment": "标准镜头"},
            ],
            "essentials": ["SUV租车", "自驾保险", "厚外套", "防晒用品", "氧气瓶", "高原药物", "备用轮胎", "应急工具箱", "热水壶", "充电宝"],
            "tips": "新疆昼夜温差大，带厚外套！高原地区注意防晒补水。独库公路弯道多需小心驾驶。新疆安检较多，预留充足时间。部分地区信号不好，提前下载离线地图。新疆紫外线强，防晒！新疆干燥，多喝水。新疆时区GMT+8，但作息比内地晚2小时。新疆景点间距远，注意加油。新疆美食偏重口味，吃不了可提前告知。新疆人热情好客，尊重当地文化。",
        },
        {
            "title": "四川成都深度游｜熊猫火锅慢生活",
            "author": "川渝吃货",
            "location": "四川成都",
            "days": 4,
            "best_time": "3-4月、9-10月",
            "budget": "2000-3000元",
            "transport": "地铁方便，机场大巴30分钟到市区",
            "visa": "无需签证",
            "timezone": "GMT+8",
            "weather": "15-25°C",
            "language": "汉语、四川话",
            "currency": "人民币（RMB）",
            "days_detail": [
                {"day": "D1", "title": "熊猫基地+春熙路", "spots": "大熊猫基地·春熙路·IFS太古里", "time": "1天", "tips": "熊猫8:00-10:00最活跃，春熙路网红小酒馆打卡。IFS爬墙熊猫必打卡，太古里逛吃逛喝"},
                {"day": "D2", "title": "宽窄巷子+武侯祠", "spots": "宽窄巷子·武侯祠·锦里", "time": "1天", "tips": "锦里18:30后灯笼亮起最美，小吃一条街。武侯祠三国文化，必看。宽窄巷子老成都体验，窄巷文艺小店多"},
                {"day": "D3", "title": "青城山+都江堰", "spots": "青城山·都江堰", "time": "1天", "tips": "青城山索道上山步行下山，都江堰16:00看夕阳。青城山道教名山，前山景点多。都江堰古代水利工程奇迹"},
                {"day": "D4", "title": "杜甫草堂+人民公园", "spots": "杜甫草堂·人民公园", "time": "半天", "tips": "人民公园鹤鸣茶社百年老茶馆，体验慢生活。杜甫草堂幽静雅致，适合慢游"},
            ],
            "hotels": [
                {"name": "春熙路商圈酒店", "price": "200-400元/晚", "feature": "交通方便，购物方便", "rating": "4.3"},
                {"name": "太古里周边", "price": "400-800元/晚", "feature": "潮流商圈，品牌云集", "rating": "4.5"},
                {"name": "宽窄巷子附近", "price": "300-600元/晚", "feature": "文化氛围，方便逛吃", "rating": "4.4"},
                {"name": "天府广场", "price": "250-450元/晚", "feature": "中心位置，交通枢纽", "rating": "4.2"},
                {"name": "文殊院周边", "price": "180-350元/晚", "feature": "安静舒适，性价比高", "rating": "4.1"},
            ],
            "foods": [
                {"name": "火锅（蜀九香）", "price": "80-120元/人", "feature": "本地人最爱，麻辣鲜香", "must_try": "✓"},
                {"name": "兔头", "price": "15元/个", "feature": "双流老妈兔头，麻辣入味", "must_try": "✓"},
                {"name": "冒菜", "price": "35元", "feature": "冒椒火辣，香辣过瘾", "must_try": "✓"},
                {"name": "冰粉", "price": "8元", "feature": "玫瑰冰粉，清凉解暑", "must_try": "✓"},
                {"name": "钟水饺", "price": "18元", "feature": "老字号，甜红油辣", "must_try": "✓"},
                {"name": "甜水面", "price": "12元", "feature": "甜辣口味，特色小吃", "must_try": "✓"},
                {"name": "担担面", "price": "15元", "feature": "麻辣面条，传统美食", "must_try": "✓"},
                {"name": "麻婆豆腐", "price": "28元", "feature": "川菜经典，麻婆豆腐", "must_try": "✓"},
            ],
            "photos": [
                {"name": "熊猫基地", "time": "8:00-10:00", "tip": "太阳月亮产房，小熊猫最可爱", "equipment": "长焦镜头"},
                {"name": "IFS爬墙熊猫", "time": "全天", "tip": "经典打卡点，必拍", "equipment": "标准镜头"},
                {"name": "锦里夜景", "time": "18:30后", "tip": "灯笼夜景，氛围感", "equipment": "广角镜头"},
                {"name": "宽窄巷子", "time": "下午", "tip": "人文建筑，老成都", "equipment": "标准镜头"},
                {"name": "都江堰", "time": "16:00", "tip": "夕阳下水利工程", "equipment": "广角镜头"},
                {"name": "青城山", "time": "上午", "tip": "道教名山，绿树成荫", "equipment": "标准镜头"},
            ],
            "essentials": ["防晒霜", "雨伞", "舒适步行鞋", "充电宝", "相机", "驱蚊液", "常用药品"],
            "tips": "成都慢节奏，建议每天只安排2-3个景点。火锅建议中午吃避开排队高峰。人民公园喝茶是必体验，鹤鸣茶社15-30元/杯。3-4月和9-10月是最佳季节，避开7-8月高温。成都口味偏麻辣，吃不了可提前告知。成都火锅分麻辣火锅、清汤火锅，根据口味选择。成都茶馆文化浓厚，建议体验。成都小吃丰富，担担面、钟水饺、甜水面必尝。成都方言四川话，当地人说话快。成都地铁方便，建议下载天府通APP。",
        },
        {
            "title": "泰国清迈慢生活｜古城寺庙与夜市美食",
            "author": "东南亚旅行家",
            "location": "泰国清迈",
            "days": 5,
            "best_time": "11-2月（雨季后）",
            "budget": "3000-5000元",
            "transport": "落地签2000泰铢，Grab打车方便，红色双条车20-40泰铢",
            "visa": "落地签2000泰铢 / 电子签证300泰铢",
            "timezone": "GMT+7",
            "weather": "25-35°C",
            "language": "泰语、英语",
            "currency": "泰铢（THB），1元≈5泰铢",
            "days_detail": [
                {"day": "D1", "title": "古城寺庙巡礼", "spots": "契迪龙寺·帕辛寺·周日夜市", "time": "1天", "tips": "周日夜市17:00-22:00，必买手工工艺品。契迪龙寺宏大的古寺遗址，拍照出片。帕辛寺兰纳风格建筑，金碧辉煌"},
                {"day": "D2", "title": "双龙寺+宁曼路", "spots": "双龙寺·宁曼路·咖啡馆", "time": "1天", "tips": "双龙寺16:00看日落，俯瞰清迈全景。宁曼路文艺街区，咖啡馆和设计店聚集。Ristr8to世界级拉花咖啡"},
                {"day": "D3", "title": "大象营+SPA", "spots": "Patara大象营·泰式SPA", "time": "1天", "tips": "大象营6000泰铢/人，保护式体验不骑大象。泰式SPA推荐Lila Thai Massage，由前囚犯提供培训就业"},
                {"day": "D4", "title": "湄平河+瓦洛洛", "spots": "湄平河·瓦洛洛市场", "time": "1天", "tips": "瓦洛洛市场本地人市场，物价便宜。湄平河The Good View河边晚餐，人均300-500泰铢"},
                {"day": "D5", "title": "古城悠闲+返程", "spots": "塔佩门·古城墙·咖啡馆", "time": "半天", "tips": "塔佩门喂鸽子，古城墙骑行一周。古城咖啡馆发呆，体验慢生活"},
            ],
            "hotels": [
                {"name": "Rimping Village", "price": "300-500元/晚", "feature": "精品酒店，设计感", "rating": "4.5"},
                {"name": "Buri Tara", "price": "200-350元/晚", "feature": "传统风格，性价比", "rating": "4.3"},
                {"name": "Suriwongse Hotel", "price": "150-250元/晚", "feature": "位置极佳，方便", "rating": "4.1"},
                {"name": "Akyra Manor", "price": "800-1200元/晚", "feature": "设计感酒店，高端", "rating": "4.7"},
                {"name": "宁曼路酒店", "price": "400-600元/晚", "feature": "文艺街区，环境好", "rating": "4.4"},
            ],
            "foods": [
                {"name": "Khao Soi泰北咖喱面", "price": "25元", "feature": "泰北特色，香辣", "must_try": "✓"},
                {"name": "芒果糯米饭", "price": "12元", "feature": "甜品经典，甜糯", "must_try": "✓"},
                {"name": "泰式炒河粉", "price": "12元", "feature": "街头小吃，经典", "must_try": "✓"},
                {"name": "椰子冰淇淋", "price": "10元", "feature": "清凉解暑，甜品", "must_try": "✓"},
                {"name": "泰式奶茶", "price": "8元", "feature": "橙色奶茶，特色", "must_try": "✓"},
                {"name": "烤肉串", "price": "3元/串", "feature": "夜市必吃，便宜", "must_try": "✓"},
                {"name": "泰式炒饭", "price": "15元", "feature": "街头小吃，简单", "must_try": "✓"},
                {"name": "春卷", "price": "5元", "feature": "街头小吃，脆口", "must_try": "✓"},
            ],
            "photos": [
                {"name": "契迪龙寺", "time": "清晨/黄昏", "tip": "古寺遗址，拍照出片", "equipment": "广角镜头"},
                {"name": "双龙寺", "time": "16:00", "tip": "日落俯瞰，全景", "equipment": "标准镜头"},
                {"name": "周日夜市", "time": "17:00后", "tip": "夜市氛围，热闹", "equipment": "标准镜头"},
                {"name": "宁曼路", "time": "下午", "tip": "文艺街区，咖啡馆", "equipment": "标准镜头"},
                {"name": "塔佩门", "time": "下午", "tip": "喂鸽子，打卡", "equipment": "标准镜头"},
                {"name": "帕辛寺", "time": "上午", "tip": "金碧辉煌，建筑", "equipment": "标准镜头"},
            ],
            "essentials": ["防晒霜", "驱蚊水", "清凉油", "轻便夏装", "人字拖", "充电宝", "护照复印件", "现金泰铢"],
            "tips": "11-2月是最佳季节，6-10月是雨季。尊重佛教文化，进入寺庙脱鞋，衣着得体。建议提前电子签证300泰铢。Grab打车方便，下载APP。很多小店不支持刷卡，带现金。1元人民币≈5泰铢。泰国小费文化，一般给20-50泰铢。泰国电压220V，两孔圆插头。泰国时间GMT+7，比中国晚1小时。泰国语言泰语，简单英语：你好Sawasdee，谢谢Khob Khun Krub。泰国交通Grab和红色双条车方便。泰国美食偏甜辣，吃不了可提前告知。泰国佛教文化浓厚，尊重当地。",
        }
    ]

    def load_guides(self, guides=None):
        if guides:
            self.guides = guides
        else:
            self.guides = self.SAMPLE_GUIDES
        print(f"✅ 加载了 {len(self.guides)} 篇攻略")

    def get_images(self, location):
        images = self.IMAGE_MAPPINGS.get(location, self.IMAGE_MAPPINGS["封面"])
        if isinstance(images, dict):
            return images
        return {"hero": images, "corner1": images, "corner2": images}

    def generate_html(self):
        """生成超高密度HTML"""
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
            font-size: 11px;
            line-height: 1.4;
            color: #2C3E50;
            background: white;
        }}

        .container {{
            width: 794px;
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
            font-size: 52px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: 4px;
        }}

        .cover .subtitle {{
            font-size: 22px;
            font-weight: 300;
            margin-bottom: 30px;
            letter-spacing: 2px;
            opacity: 0.95;
        }}

        .cover .info {{
            font-size: 14px;
            opacity: 0.9;
            text-align: center;
        }}

        .cover .divider {{
            width: 80px;
            height: 2px;
            background: rgba(255,255,255,0.6);
            margin: 25px auto;
        }}

        /* 目录 */
        .toc {{
            width: 794px;
            min-height: 1123px;
            padding: 40px;
            page-break-after: always;
        }}

        .toc h2 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 36px;
            margin-bottom: 30px;
            color: #667eea;
        }}

        .toc-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .toc-card {{
            display: flex;
            gap: 15px;
            padding: 15px;
            background: #F8F9FA;
            border-radius: 8px;
            border: 1px solid #E9ECEF;
        }}

        .toc-card .info {{
            flex: 1;
        }}

        .toc-card .title {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .toc-card .meta {{
            font-size: 11px;
            color: #7F8C8D;
            line-height: 1.3;
        }}

        /* 攻略页 */
        .guide-page {{
            width: 794px;
            min-height: 1123px;
            page-break-after: always;
        }}

        .guide-header {{
            height: 140px;
            position: relative;
            display: flex;
            align-items: center;
            padding: 18px 35px;
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
            padding: 5px 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 11px;
            font-weight: 500;
            border-radius: 15px;
            margin-bottom: 8px;
        }}

        .guide-info h3 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 6px;
            line-height: 1.2;
        }}

        .guide-info .meta {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            font-size: 10px;
            color: #7F8C8D;
        }}

        .guide-info .meta span {{
            background: #F8F9FA;
            padding: 3px 8px;
            border-radius: 10px;
        }}

        /* 两栏内容 */
        .guide-content {{
            display: grid;
            grid-template-columns: 1.35fr 0.65fr;
            gap: 15px;
            padding: 15px;
            height: 780px;
        }}

        .col {{
            background: #FDFDFD;
            border-radius: 6px;
            padding: 12px;
            border: 1px solid #F0F0F0;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .col-header {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 2px solid #E8E8E8;
            flex-shrink: 0;
        }}

        .col-header h4 {{
            font-family: 'Noto Serif SC', serif;
            font-size: 13px;
            font-weight: 600;
            color: #2C3E50;
        }}

        /* 行程卡片 */
        .day-card {{
            background: #F8F9FA;
            border-radius: 5px;
            padding: 8px;
            margin-bottom: 6px;
            flex-shrink: 0;
        }}

        .day-card .title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 4px;
            font-size: 12px;
        }}

        .day-card .detail {{
            font-size: 11px;
            color: #34495E;
            margin-bottom: 3px;
        }}

        .day-card .tip {{
            font-size: 10px;
            color: #7F8C8D;
            font-style: italic;
            line-height: 1.2;
        }}

        /* 信息块 */
        .info-block {{
            margin-bottom: 10px;
            flex-shrink: 0;
        }}

        .info-block h5 {{
            font-size: 12px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 5px;
        }}

        .info-item {{
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
            border-bottom: 1px solid #F0F0F0;
            font-size: 10px;
        }}

        .info-item:last-child {{
            border-bottom: none;
        }}

        .info-item .name {{
            flex: 1;
            color: #34495E;
        }}

        .info-item .price {{
            color: #667eea;
            font-weight: 500;
        }}

        /* 拍照机位 */
        .photo-item {{
            background: #F0F7FF;
            border-radius: 4px;
            padding: 5px;
            margin-bottom: 4px;
        }}

        .photo-item .name {{
            font-weight: 600;
            color: #667eea;
            font-size: 11px;
        }}

        .photo-item .detail {{
            font-size: 9px;
            color: #34495E;
            margin-top: 2px;
        }}

        /* 左下角图片 */
        .corner-images {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 10px;
            z-index: 0;
        }}

        .corner-images img {{
            width: 150px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            opacity: 0.3;
        }}

        /* 必备物品 */
        .essentials-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 3px;
        }}

        .essential-item {{
            background: #FFF3E0;
            color: #E65100;
            padding: 4px 6px;
            border-radius: 3px;
            font-size: 9px;
            text-align: center;
        }}

        /* 贴士框 */
        .tip-box {{
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-left: 3px solid #FFA726;
            padding: 10px;
            border-radius: 5px;
            font-size: 10px;
            color: #6D4C41;
            line-height: 1.3;
            margin-top: 5px;
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
                <p style="margin-top: 20px;">生成时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
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
                        <div class="detail">⏱️ {day['time']}</div>
                        <div class="tip">💡 {day['tips']}</div>
                    </div>
                """

            # 住宿HTML
            hotels_html = ""
            for hotel in guide['hotels']:
                hotels_html += f"""
                    <div class="info-item">
                        <span class="name">{hotel['name']} ({hotel['rating']}★)</span>
                        <span class="price">{hotel['price']}</span>
                    </div>
                    <div class="info-item" style="font-size: 9px; color: #7F8C8D; padding-left: 5px;">
                        {hotel['feature']}
                    </div>
                """

            # 美食HTML
            foods_html = ""
            for food in guide['foods']:
                must_try = " ✓" if food.get('must_try') == "✓" else ""
                foods_html += f"""
                    <div class="info-item">
                        <span class="name">{food['name']}{must_try}</span>
                        <span class="price">{food['price']}</span>
                    </div>
                """

            # 拍照HTML
            photos_html = ""
            for photo in guide['photos']:
                photos_html += f"""
                    <div class="photo-item">
                        <div class="name">📸 {photo['name']}</div>
                        <div class="detail">⏰ {photo['time']} | {photo['tip']}</div>
                        <div class="detail">📷 {photo['equipment']}</div>
                    </div>
                """

            # 必备物品
            essentials_html = "".join([f"<div class='essential-item'>{e}</div>" for e in guide['essentials']])

            html_content += f"""
        <!-- 攻略 {i} -->
        <div class="guide-page">
            <div class="guide-header">
                <div class="guide-header-bg" style="background-image: url('{bg_image['hero']}')"></div>
                <div class="guide-info">
                    <span class="tag">{guide['location']}</span>
                    <h3>{guide['title']}</h3>
                    <div class="meta">
                        <span>✍️ {guide['author']}</span>
                        <span>⏱️ {guide['days']}天</span>
                        <span>📅 {guide['best_time']}</span>
                        <span>💰 {guide['budget']}</span>
                        <span>🚗 {guide['transport'][:20]}...</span>
                        <span>🌍 {guide['timezone']}</span>
                        <span>🌡️ {guide['weather']}</span>
                        <span>💬 {guide['language']}</span>
                    </div>
                </div>
            </div>

            <div class="guide-content">
                <div class="col">
                    <div class="col-header">
                        <h4>📍 行程安排</h4>
                    </div>
                    <div style="flex: 1; overflow-y: auto;">
                        {days_html}
                    </div>
                </div>

                <div class="col">
                    <div class="col-header">
                        <h4>🏨 住宿推荐</h4>
                    </div>
                    <div class="info-block" style="flex: 0;">
                        {hotels_html}
                    </div>

                    <div class="col-header" style="margin-top: 10px;">
                        <h4>🍜 美食清单</h4>
                    </div>
                    <div class="info-block" style="flex: 0;">
                        {foods_html}
                    </div>

                    <div class="col-header" style="margin-top: 10px;">
                        <h4>📸 拍照机位</h4>
                    </div>
                    <div class="info-block" style="flex: 0;">
                        {photos_html}
                    </div>

                    <div class="col-header" style="margin-top: 10px;">
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

            <!-- 左下角图片 -->
            <div class="corner-images">
                <img src="{bg_image['corner1']}" alt="风景1" onerror="this.style.display='none'">
                <img src="{bg_image['corner2']}" alt="风景2" onerror="this.style.display='none'">
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
        print("🚀 开始生成旅行攻略 V6（超高密度）...")
        print(f"📁 输出目录: {self.output_dir}")

        self.load_guides()
        html_file = self.save_html()

        if export_pdf:
            pdf_file = await self.export_pdf()
            return html_file, pdf_file
        else:
            return html_file, None


async def main():
    generator = TravelGuideGeneratorV6()
    html_file, pdf_file = await generator.generate(export_pdf=True)
    print("\n" + "="*60)
    print("✅ 生成完成！")
    print(f"📄 HTML: {html_file}")
    print(f"📄 PDF: {pdf_file}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
