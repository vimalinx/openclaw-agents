#!/usr/bin/env python3
"""
Algora 学习器和监控工具

功能：
1. 监控 Algora 上的开源悬赏任务
2. 查找适合技术栈的高价值任务
3. 跟踪项目和贡献者
4. 生成机会报告
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, quote


class AlgoraMonitor:
    """Algora 悬赏任务监控"""

    def __init__(self):
        self.base_url = "https://algora.io"
        self.session = None

    async def init(self):
        """初始化 HTTP 会话"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
        )

    async def close(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()

    async def fetch_repository_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        labels: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        获取 GitHub 仓库的 issues

        Args:
            owner: 仓库所有者
            repo: 仓库名称
            state: open/closed
            labels: 标签过滤

        Returns:
            Issue 列表
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {"state": state}
        if labels:
            params["labels"] = ",".join(labels)

        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"❌ GitHub API 错误: {response.status}")
                    return []
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []

    async def fetch_algora_bounty_info(self, issue_url: str) -> Optional[Dict]:
        """
        尝试获取 Algora 悬赏信息

        Args:
            issue_url: GitHub issue URL

        Returns:
            悬赏信息
        """
        # Algora 可能有 API 或页面展示悬赏信息
        # 这里我们假设可以通过 issue URL 获取
        try:
            # 尝试访问可能的 Algora API 端点
            # 具体实现需要根据 Algora 的实际 API 结构调整
            return None
        except Exception as e:
            print(f"⚠️ 无法获取悬赏信息: {e}")
            return None

    def filter_issues_by_tech_stack(
        self,
        issues: List[Dict],
        tech_stack: List[str]
    ) -> List[Dict]:
        """
        根据技术栈过滤 issues

        Args:
            issues: Issue 列表
            tech_stack: 技术栈列表

        Returns:
            匹配的 issues
        """
        matched = []
        tech_stack_lower = [t.lower() for t in tech_stack]

        for issue in issues:
            title = issue.get("title", "").lower()
            body = issue.get("body", "").lower()
            labels = [label.get("name", "").lower() for label in issue.get("labels", [])]

            # 检查是否包含技术栈关键词
            for tech in tech_stack_lower:
                if tech in title or tech in body or tech in str(labels):
                    matched.append(issue)
                    break

        return matched

    def analyze_issue(self, issue: Dict) -> Dict:
        """
        分析 issue 的潜在价值

        Args:
            issue: GitHub issue

        Returns:
            分析结果
        """
        title = issue.get("title", "")
        body = issue.get("body", "")
        labels = [label.get("name", "") for label in issue.get("labels", [])]
        reactions = issue.get("reactions", {})
        comments = issue.get("comments", 0)

        # 评估指标
        score = 0
        reasons = []

        # 有标签表示有组织
        if labels:
            score += 10
            reasons.append("有标签，可能有优先级标记")

        # 关注度高（reactions）
        if reactions and isinstance(reactions, dict):
            total_reactions = sum(v for v in reactions.values() if isinstance(v, int))
        else:
            total_reactions = 0

        if total_reactions > 10:
            score += 20
            reasons.append(f"高关注度（{total_reactions} reactions）")

        # 讨论活跃
        if comments > 5:
            score += 15
            reasons.append(f"讨论活跃（{comments} 评论）")

        # 标签分析
        high_value_labels = [
            "good first issue",
            "help wanted",
            "enhancement",
            "feature request",
            "bug"
        ]
        for label in labels:
            if label.lower() in [l.lower() for l in high_value_labels]:
                score += 10
                reasons.append(f"高价值标签: {label}")

        # 标题长度适中（太短太长都不好）
        if 20 <= len(title) <= 80:
            score += 5
            reasons.append("描述清晰")

        return {
            "score": score,
            "reasons": reasons,
            "total_reactions": total_reactions,
            "comments": comments,
            "labels": labels
        }

    def generate_opportunity_report(
        self,
        issues: List[Dict],
        repo_name: str,
        tech_stack: Optional[List[str]] = None
    ) -> str:
        """
        生成机会报告

        Args:
            issues: Issue 列表
            repo_name: 仓库名称
            tech_stack: 技术栈

        Returns:
            Markdown 报告
        """
        report = []
        report.append("# 🎯 Algora 悬赏机会报告")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**仓库**: {repo_name}")
        if tech_stack:
            report.append(f"**技术栈**: {', '.join(tech_stack)}")
        report.append(f"**总 Issue 数**: {len(issues)}\n")

        # 分析所有 issues
        analyzed = []
        for issue in issues:
            analysis = self.analyze_issue(issue)
            analyzed.append({
                "issue": issue,
                "analysis": analysis
            })

        # 按分数排序
        analyzed.sort(key=lambda x: x["analysis"]["score"], reverse=True)

        # 高分 issues（>= 30）
        high_score = [x for x in analyzed if x["analysis"]["score"] >= 30]
        if high_score:
            report.append("## ⭐ 高价值 Issues（评分 >= 30）")
            for i, item in enumerate(high_score[:5], 1):
                issue = item["issue"]
                analysis = item["analysis"]
                report.append(f"\n### {i}. {issue['title']}")
                report.append(f"**评分**: {analysis['score']}")
                report.append(f"**URL**: {issue['html_url']}")
                report.append(f"**Reactions**: {analysis['total_reactions']}")
                report.append(f"**评论数**: {analysis['comments']}")
                report.append(f"**标签**: {', '.join(analysis['labels'][:5])}")
                report.append("**推荐理由**:")
                for reason in analysis["reasons"]:
                    report.append(f"- {reason}")
            report.append("")

        # 中等分数 issues（15-29）
        medium_score = [x for x in analyzed if 15 <= x["analysis"]["score"] < 30]
        if medium_score:
            report.append("## 📊 值得关注（评分 15-29）")
            for i, item in enumerate(medium_score[:10], 1):
                issue = item["issue"]
                analysis = item["analysis"]
                report.append(f"{i}. **{issue['title']}** - 评分: {analysis['score']}")
                report.append(f"   URL: {issue['html_url']}")
            report.append("")

        # 标签统计
        all_labels = []
        for issue in issues:
            all_labels.extend([label.get("name", "") for label in issue.get("labels", [])])

        if all_labels:
            from collections import Counter
            label_counts = Counter(all_labels)
            report.append("## 🏷️ 常见标签")
            for label, count in label_counts.most_common(10):
                report.append(f"- **{label}**: {count} 次")
            report.append("")

        # 行动建议
        report.append("## 💡 行动建议")

        if high_score:
            report.append("### 优先处理")
            report.append("1. 选择高评分 issues，这些通常有清晰的描述和活跃的社区")
            report.append("2. 优先选择有 'good first issue' 或 'help wanted' 标签的")
            report.append("3. 检查 issue 的评论，了解预期的工作量和复杂度")
            report.append("")

        if tech_stack:
            report.append("### 技术栈匹配")
            report.append(f"你关注的技术栈: {', '.join(tech_stack)}")
            matched_issues = self.filter_issues_by_tech_stack(issues, tech_stack)
            if matched_issues:
                report.append(f"找到 {len(matched_issues)} 个匹配的 issues")
            else:
                report.append("未找到完全匹配的技术栈，可以考虑扩展技术范围")
            report.append("")

        report.append("### 下一步")
        report.append("1. 访问高评分 issues，仔细阅读需求")
        report.append("2. 检查是否已有活跃的 PR（避免重复工作）")
        report.append("3. 在 issue 中表达你的兴趣和计划")
        report.append("4. 分阶段实现，及时反馈进度")
        report.append("")

        report.append("---")
        report.append(f"\n📚 报告生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(report)

    async def monitor_repository(
        self,
        owner: str,
        repo: str,
        tech_stack: Optional[List[str]] = None
    ) -> str:
        """
        监控一个仓库并生成报告

        Args:
            owner: 仓库所有者
            repo: 仓库名称
            tech_stack: 技术栈（可选）

        Returns:
            报告
        """
        await self.init()

        try:
            print(f"📊 开始监控 {owner}/{repo}...")

            # 获取 open issues
            print(f"🔍 获取 open issues...")
            issues = await self.fetch_repository_issues(owner, repo, state="open")
            print(f"✅ 获取到 {len(issues)} 个 open issues")

            # 如果指定了技术栈，过滤
            if tech_stack:
                print(f"🔧 过滤技术栈: {', '.join(tech_stack)}...")
                issues = self.filter_issues_by_tech_stack(issues, tech_stack)
                print(f"✅ 过滤后剩余 {len(issues)} 个 issues")

            # 生成报告
            print(f"📝 生成报告...")
            report = self.generate_opportunity_report(issues, f"{owner}/{repo}", tech_stack)

            print(f"✅ 监控完成！")

            return report

        finally:
            await self.close()

    async def monitor_multiple_repos(
        self,
        repos: List[Dict],  # [{"owner": "...", "repo": "..."}]
        tech_stack: Optional[List[str]] = None
    ) -> str:
        """
        监控多个仓库

        Args:
            repos: 仓库列表
            tech_stack: 技术栈

        Returns:
            综合报告
        """
        await self.init()

        all_reports = []

        try:
            print(f"📊 开始监控 {len(repos)} 个仓库...")

            for i, repo_info in enumerate(repos, 1):
                owner = repo_info["owner"]
                repo = repo_info["repo"]
                print(f"\n[{i}/{len(repos)}] 监控 {owner}/{repo}...")

                # 获取 issues
                issues = await self.fetch_repository_issues(owner, repo, state="open")

                # 技术栈过滤
                if tech_stack:
                    issues = self.filter_issues_by_tech_stack(issues, tech_stack)

                # 为每个仓库生成简要报告
                if issues:
                    analyzed = [self.analyze_issue(issue) for issue in issues]
                    high_score = sum(1 for a in analyzed if a["score"] >= 30)

                    all_reports.append({
                        "repo": f"{owner}/{repo}",
                        "total": len(issues),
                        "high_score": high_score,
                        "top_issues": sorted(issues, key=lambda x: self.analyze_issue(x)["score"], reverse=True)[:3]
                    })

            # 生成综合报告
            print(f"\n📝 生成综合报告...")
            return self.generate_comprehensive_report(all_reports, tech_stack)

        finally:
            await self.close()

    def generate_comprehensive_report(
        self,
        reports: List[Dict],
        tech_stack: Optional[List[str]] = None
    ) -> str:
        """
        生成综合报告

        Args:
            reports: 单个仓库的报告
            tech_stack: 技术栈

        Returns:
            Markdown 报告
        """
        output = []
        output.append("# 🎯 Algora 多仓库机会报告")
        output.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**监控仓库数**: {len(reports)}")
        if tech_stack:
            output.append(f"**技术栈**: {', '.join(tech_stack)}")
        output.append("")

        # 总览
        total_issues = sum(r["total"] for r in reports)
        total_high_score = sum(r["high_score"] for r in reports)

        output.append("## 📊 总览")
        output.append(f"- **总 Issues**: {total_issues}")
        output.append(f"- **高价值 Issues**: {total_high_score}")
        output.append("")

        # 仓库详情
        output.append("## 📦 仓库详情")
        for i, report in enumerate(reports, 1):
            output.append(f"\n### {i}. {report['repo']}")
            output.append(f"- **总 Issues**: {report['total']}")
            output.append(f"- **高价值 Issues**: {report['high_score']}")

            if report["top_issues"]:
                output.append("\n**Top 3 Issues**:")
                for j, issue in enumerate(report["top_issues"], 1):
                    analysis = self.analyze_issue(issue)
                    output.append(f"{j}. **{issue['title']}** - 评分: {analysis['score']}")
                    output.append(f"   URL: {issue['html_url']}")

        # 推荐
        output.append("\n## 💡 推荐行动")

        best_repo = max(reports, key=lambda x: x["high_score"])
        if best_repo["high_score"] > 0:
            output.append(f"### 优先关注仓库")
            output.append(f"**{best_repo['repo']}** 有 {best_repo['high_score']} 个高价值 issues")

        output.append("\n### 下一步")
        output.append("1. 从高价值 issues 开始，选择你感兴趣的")
        output.append("2. 检查 issue 是否有活跃的 PR")
        output.append("3. 在 issue 中评论表达兴趣")
        output.append("4. 实现后提交 PR")

        output.append("\n---")
        output.append(f"\n📚 报告生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(output)


# 推荐监控的热门仓库
RECOMMENDED_REPOS = [
    {"owner": "vercel", "repo": "next.js"},
    {"owner": "facebook", "repo": "react"},
    {"owner": "vuejs", "repo": "vue"},
    {"owner": "microsoft", "repo": "typescript"},
    {"owner": "openclaw", "repo": "openclaw"},
]


async def main():
    """主函数 - 示例用法"""
    monitor = AlgoraMonitor()

    # 示例1: 监控单个仓库
    # report = await monitor.monitor_repository(
    #     owner="openclaw",
    #     repo="openclaw",
    #     tech_stack=["TypeScript", "Python"]
    # )

    # 示例2: 监控多个仓库
    report = await monitor.monitor_multiple_repos(
        repos=[
            {"owner": "openclaw", "repo": "openclaw"},
            {"owner": "vercel", "repo": "next.js"},
        ],
        tech_stack=["TypeScript", "Python", "JavaScript"]
    )

    # 保存报告
    report_path = "/home/vimalinx/.openclaw/workspace/algora_opportunity_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 报告已保存到: {report_path}")
    print("\n" + "="*60)
    print(report)
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
