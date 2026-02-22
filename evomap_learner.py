#!/usr/bin/env python3
"""
EvoMap 学习器 - 从其他 AI 代理的经验中学习

功能：
1. 获取推广的 Capsule 和 Gene
2. 分析其他 AI 的策略模式
3. 提取可学习的经验
4. 生成学习报告
"""

import asyncio
import aiohttp
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter, defaultdict


class EvoMapLearner:
    """从 EvoMap 学习其他 AI 代理的经验"""

    def __init__(self, hub_url: str = "https://evomap.ai"):
        self.hub_url = hub_url
        self.sender_id = None  # 如果需要注册，可以生成一个
        self.session = None

    async def init(self):
        """初始化 HTTP 会话"""
        self.session = aiohttp.ClientSession()

    async def close(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()

    def _generate_sender_id(self) -> str:
        """生成唯一的 sender_id（只用于学习，不发布）"""
        import secrets
        return f"node_{secrets.token_hex(8)}"

    async def fetch_assets(
        self,
        asset_type: Optional[str] = "Capsule",
        limit: int = 100
    ) -> Dict:
        """
        获取推广的资产

        Args:
            asset_type: 资产类型（Capsule/Gene/EvolutionEvent）
            limit: 返回数量限制

        Returns:
            返回的资产数据
        """
        url = f"{self.hub_url}/a2a/fetch"

        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "fetch",
            "message_id": f"msg_{int(datetime.now().timestamp())}_{self._random_hex(4)}",
            "sender_id": self.sender_id or self._generate_sender_id(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "asset_type": asset_type,
                "local_id": None,
                "content_hash": None
            }
        }

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    text = await response.text()
                    print(f"❌ 请求失败: {response.status} - {text}")
                    return {}
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return {}

    async def fetch_promoted_assets_via_rest(
        self,
        asset_type: Optional[str] = "Capsule",
        limit: int = 100
    ) -> List[Dict]:
        """
        通过 REST API 获取推广的资产（无需协议信封）

        Args:
            asset_type: 资产类型
            limit: 返回数量

        Returns:
            资产列表
        """
        url = f"{self.hub_url}/a2a/assets"

        params = {
            "status": "promoted",
            "type": asset_type,
            "limit": limit,
            "sort": "ranked"  # 按 GDI 分数排名
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("assets", [])
                else:
                    text = await response.text()
                    print(f"❌ REST 请求失败: {response.status} - {text}")
                    return []
        except Exception as e:
            print(f"❌ REST 请求异常: {e}")
            return []

    def _random_hex(self, length: int) -> str:
        """生成随机十六进制字符串"""
        import secrets
        return secrets.token_hex(length)

    def analyze_capsules(self, capsules: List[Dict]) -> Dict:
        """
        分析 Capsule 数据，提取可学习的模式

        Args:
            capsules: Capsule 列表

        Returns:
            分析结果
        """
        if not capsules:
            return {}

        analysis = {
            "total_capsules": len(capsules),
            "categories": Counter(),
            "confidence_distribution": {
                "high (>=0.9)": 0,
                "medium (0.7-0.9)": 0,
                "low (<0.7)": 0
            },
            "blast_radius": {
                "avg_files": 0,
                "avg_lines": 0
            },
            "common_triggers": Counter(),
            "common_categories": Counter(),
            "high_confidence_examples": [],
            "unique_strategies": set(),
        }

        total_files = 0
        total_lines = 0
        total_confidence = 0

        for capsule in capsules:
            # 提取置信度
            confidence = capsule.get("confidence", 0)
            total_confidence += confidence

            if confidence >= 0.9:
                analysis["confidence_distribution"]["high (>=0.9)"] += 1
                if len(analysis["high_confidence_examples"]) < 5:
                    analysis["high_confidence_examples"].append({
                        "summary": capsule.get("summary", ""),
                        "confidence": confidence,
                        "trigger": capsule.get("trigger", []),
                        "blast_radius": capsule.get("blast_radius", {})
                    })
            elif confidence >= 0.7:
                analysis["confidence_distribution"]["medium (0.7-0.9)"] += 1
            else:
                analysis["confidence_distribution"]["low (<0.7)"] += 1

            # 提取触发信号
            triggers = capsule.get("trigger", [])
            for trigger in triggers:
                analysis["common_triggers"][trigger] += 1

            # 提取类别（从 Gene 引用中推断）
            gene_id = capsule.get("gene")
            if gene_id:
                analysis["unique_strategies"].add(gene_id)

            # 提取 blast_radius
            blast_radius = capsule.get("blast_radius", {})
            total_files += blast_radius.get("files", 0)
            total_lines += blast_radius.get("lines", 0)

        # 计算平均值
        if len(capsules) > 0:
            analysis["blast_radius"]["avg_files"] = round(total_files / len(capsules), 2)
            analysis["blast_radius"]["avg_lines"] = round(total_lines / len(capsules), 2)
            analysis["avg_confidence"] = round(total_confidence / len(capsules), 3)

        # 转换 Counter 为普通字典
        analysis["common_triggers"] = dict(analysis["common_triggers"].most_common(20))
        analysis["unique_strategies"] = list(analysis["unique_strategies"])

        return analysis

    def analyze_genes(self, genes: List[Dict]) -> Dict:
        """
        分析 Gene 数据，提取策略模式

        Args:
            genes: Gene 列表

        Returns:
            分析结果
        """
        if not genes:
            return {}

        analysis = {
            "total_genes": len(genes),
            "categories": Counter(),
            "common_signals": Counter(),
            "category_examples": defaultdict(list),
        }

        for gene in genes:
            # 提取类别
            category = gene.get("category", "unknown")
            analysis["categories"][category] += 1

            # 收集每类别的示例
            if len(analysis["category_examples"][category]) < 3:
                analysis["category_examples"][category].append({
                    "summary": gene.get("summary", ""),
                    "signals_match": gene.get("signals_match", [])
                })

            # 提取信号匹配
            signals = gene.get("signals_match", [])
            for signal in signals:
                analysis["common_signals"][signal] += 1

        # 转换 Counter 为普通字典
        analysis["categories"] = dict(analysis["categories"])
        analysis["common_signals"] = dict(analysis["common_signals"].most_common(20))

        return analysis

    def generate_learning_report(self, capsule_analysis: Dict, gene_analysis: Dict) -> str:
        """
        生成学习报告

        Args:
            capsule_analysis: Capsule 分析结果
            gene_analysis: Gene 分析结果

        Returns:
            Markdown 格式的学习报告
        """
        report = []
        report.append("# 🎓 EvoMap 学习报告")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Capsule 分析
        if capsule_analysis:
            report.append("## 📦 Capsule（验证的修复）分析")
            report.append(f"- **总数**: {capsule_analysis.get('total_capsules', 0)}")
            report.append(f"- **平均置信度**: {capsule_analysis.get('avg_confidence', 0):.3f}")
            report.append("")

            # 置信度分布
            report.append("### 📊 置信度分布")
            conf_dist = capsule_analysis.get("confidence_distribution", {})
            for level, count in conf_dist.items():
                report.append(f"- **{level}**: {count}")
            report.append("")

            # Blast Radius
            report.append("### 📏 影响范围（Blast Radius）")
            blast = capsule_analysis.get("blast_radius", {})
            report.append(f"- **平均文件数**: {blast.get('avg_files', 0)}")
            report.append(f"- **平均代码行数**: {blast.get('avg_lines', 0)}")
            report.append("")

            # 常见触发信号
            common_triggers = capsule_analysis.get("common_triggers", {})
            if common_triggers:
                report.append("### 🔍 常见触发信号（Top 20）")
                for trigger, count in common_triggers.items():
                    report.append(f"- `{trigger}` - 出现 {count} 次")
                report.append("")

            # 高置信度示例
            high_conf = capsule_analysis.get("high_confidence_examples", [])
            if high_conf:
                report.append("### ✅ 高置信度示例（confidence >= 0.9）")
                for i, ex in enumerate(high_conf, 1):
                    report.append(f"\n#### 示例 {i}")
                    report.append(f"**总结**: {ex['summary']}")
                    report.append(f"**置信度**: {ex['confidence']}")
                    report.append(f"**触发信号**: {', '.join(ex['trigger'])}")
                    report.append(f"**影响范围**: {ex['blast_radius'].get('files', 0)} files, {ex['blast_radius'].get('lines', 0)} lines")
                report.append("")

        # Gene 分析
        if gene_analysis:
            report.append("## 🧬 Gene（策略模板）分析")
            report.append(f"- **总数**: {gene_analysis.get('total_genes', 0)}")
            report.append("")

            # 类别分布
            categories = gene_analysis.get("categories", {})
            if categories:
                report.append("### 📂 策略类别")
                for category, count in categories.items():
                    report.append(f"- **{category}**: {count} 个策略")
                report.append("")

            # 类别示例
            examples = gene_analysis.get("category_examples", {})
            if examples:
                report.append("### 💡 策略示例")
                for category, ex_list in examples.items():
                    report.append(f"\n#### {category}")
                    for i, ex in enumerate(ex_list[:2], 1):
                        report.append(f"{i}. {ex['summary']}")
                        report.append(f"   信号匹配: `{', '.join(ex['signals_match'])}")
                report.append("")

            # 常见信号
            common_signals = gene_analysis.get("common_signals", {})
            if common_signals:
                report.append("### 🔔 常见信号模式")
                for signal, count in common_signals.items():
                    report.append(f"- `{signal}` - 出现 {count} 次")
                report.append("")

        # 学习要点
        report.append("## 🎯 学习要点")
        report.append("")
        report.append("### 从 Capsule 学到的")
        report.append("1. **高置信度的修复通常**:")
        if capsule_analysis.get("confidence_distribution", {}).get("high (>=0.9)", 0) > 0:
            report.append("   - 影响范围小而精确（小 Blast Radius）")
            report.append("   - 解决明确的问题（具体的触发信号）")
            report.append("   - 经过多次验证（Success Streak）")
        report.append("")

        report.append("### 从 Gene 学到的")
        report.append("1. **常见的策略类别**:")
        for category in gene_analysis.get("categories", {}).keys():
            desc = {
                "repair": "修复问题，最常见",
                "optimize": "性能优化",
                "innovate": "创新功能"
            }.get(category, category)
            report.append(f"   - **{category}**: {desc}")
        report.append("")

        report.append("2. **可借鉴的设计模式**:")
        report.append("   - 将修复抽象为可重用的 Gene")
        report.append("   - 每个修复记录验证过程（EvolutionEvent）")
        report.append("   - 量化修复的影响（Blast Radius）")
        report.append("   - 评估修复的置信度（Confidence）")
        report.append("")

        report.append("---")
        report.append(f"\n📚 报告生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(report)

    async def learn_from_evomap(self, limit: int = 100) -> str:
        """
        从 EvoMap 学习并生成报告

        Args:
            limit: 获取的资产数量

        Returns:
            学习报告
        """
        await self.init()

        try:
            print(f"📚 开始从 EvoMap 学习...")
            print(f"📦 获取推广的 Capsule（最多 {limit} 个）...")

            # 获取 Capsule
            capsules = await self.fetch_promoted_assets_via_rest(
                asset_type="Capsule",
                limit=limit
            )
            print(f"✅ 获取到 {len(capsules)} 个 Capsule")

            # 分析 Capsule
            capsule_analysis = self.analyze_capsules(capsules)
            print(f"✅ 分析完成：平均置信度 {capsule_analysis.get('avg_confidence', 0):.3f}")

            # 获取 Gene
            print(f"\n🧬 获取推广的 Gene（最多 {limit} 个）...")
            genes = await self.fetch_promoted_assets_via_rest(
                asset_type="Gene",
                limit=limit
            )
            print(f"✅ 获取到 {len(genes)} 个 Gene")

            # 分析 Gene
            gene_analysis = self.analyze_genes(genes)
            print(f"✅ 分析完成：{len(gene_analysis.get('categories', {}))} 个策略类别")

            # 生成报告
            print(f"\n📝 生成学习报告...")
            report = self.generate_learning_report(capsule_analysis, gene_analysis)

            print(f"\n✅ 学习完成！")

            return report

        finally:
            await self.close()


async def main():
    """主函数"""
    learner = EvoMapLearner()
    report = await learner.learn_from_evomap(limit=100)

    # 保存报告
    report_path = "/home/vimalinx/.openclaw/workspace/evomap_learning_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 报告已保存到: {report_path}")
    print("\n" + "="*60)
    print(report)
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
