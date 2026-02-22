#!/usr/bin/env python3
"""
Lobster 工作流引擎完整调研报告生成器

从多个渠道收集信息，生成精美的 A4 PDF 报告
"""

import sys
sys.path.append('/home/vimalinx/.openclaw/skills/ai-weekly-generator')

from skill import AIWeeklyGenerator
from datetime import datetime

def create_lobster_report():
    """生成 Lobster/OpenClaw 完整调研报告"""

    gen = AIWeeklyGenerator(
        week_number=8,
        date="2026.02.21",
        subtitle="OpenClaw Lobster 深度调研报告"
    )

    # 概览统计
    gen.add_stats(papers=0, projects=5, trends=3)

    # 核心产品介绍
    gen.add_paper(
        title="OpenClaw - 自托管 AI 代理网关",
        authors=["OpenClaw Team"],
        abstract="OpenClaw 是一个自托管的网关，连接用户的聊天应用（WhatsApp、Telegram、Discord、iMessage 等）到 AI 编码代理。用户在自己的机器上运行单个 Gateway 进程，它成为消息应用与始终可用的 AI 助手之间的桥梁。支持多通道、多代理路由、媒体传输等功能。",
        tags=["AI Gateway", "Multi-channel", "Self-hosted"],
        institution="OpenClaw",
        highlight={
            "title": "💡 核心特性",
            "content": "• 自托管：运行在用户硬件上，用户自己的规则\n• 多通道：单个 Gateway 服务 WhatsApp、Telegram、Discord\n• 代理原生：为编码代理构建，支持工具使用、会话、多代理路由\n• 开源：MIT 许可，社区驱动\n• 需要：Node 22+、API 密钥（推荐 Anthropic）、5 分钟"
        }
    )

    gen.add_paper(
        title="Lobster - OpenClaw 原生工作流引擎",
        authors=["OpenClaw Team"],
        abstract="Lobster 是 OpenClaw 的本地工作流引擎，采用类型化（JSON-first）管道、作业和审批门设计。AI 代理可以使用 Lobster 作为工作流引擎，无需每次都构造查询，从而节省 tokens、提供确定性支持和可恢复性。支持 YAML/JSON 工作流文件，包含步骤、环境和审批门。",
        tags=["Workflow Engine", "Type-safe", "Pipelines"],
        institution="OpenClaw",
        highlight={
            "title": "🎯 核心优势",
            "content": "• 类型化管道（对象/数组），而非文本管道\n• 本地优先执行\n• 无新认证面：Lobster 不拥有 OAuth/tokens\n• 可组合的宏，Moltbot 可在一步中调用\n• 节省 tokens：预先定义的工作流无需重复构造"
        }
    )

    # 技术趋势
    gen.add_trend(
        title="📈 趋势一：AI 代理工作流化",
        content="随着 AI 代理在复杂场景中的应用增多，工作流引擎成为关键需求。Lobster 通过类型化管道和审批门解决了多个痛点：\n\n1. **节省 tokens**：预定义的工作流可以一步调用，无需每次重新构造\n2. **可组合性**：多个工具和步骤可以组合成复杂的自动化流程\n3. **审批门**：支持需要人工确认的操作（如部署、删除等）\n4. **可恢复性**：工作流状态持久化，支持中断后继续\n\n这种模式正在成为 AI 代理基础设施的标准组件，类似于 CI/CD 对 DevOps 的重要性。",
        category="warning"
    )

    gen.add_trend(
        title="📈 趋势二：本地优先（Local-First）架构",
        content="OpenClaw 和 Lobster 都强调本地优先架构：\n\n1. **数据隐私**：所有数据在用户机器上处理，不上传到第三方\n2. **确定性执行**：本地执行确保结果可控和可预测\n3. **离线能力**：不依赖外部服务的可用性\n4. **性能优化**：本地调用避免网络延迟\n\n这反映了当前用户对数据控制和隐私的关注，本地优先的 AI 工具正在获得更多青睐。",
        category="info"
    )

    gen.add_trend(
        title="📈 趋势三：多代理协作与路由",
        content="OpenClaw 的多代理路由能力体现了 AI 代理生态的发展方向：\n\n1. **隔离会话**：每个代理、工作空间或发送者拥有独立会话\n2. **智能路由**：根据消息内容和上下文路由到合适的代理\n3. **多代理协作**：不同专长的代理可以协同工作\n4. **插件扩展**：支持通过扩展包添加 Mattermost 等更多通道\n\n这为未来 AI 代理的协作生态奠定了基础，不同代理可以像微服务一样组合。",
        category="success"
    )

    # 开源项目
    gen.add_project(
        name="OpenClaw (主仓库)",
        stars="21.5K",
        tags=["AI Gateway", "Multi-channel", "Self-hosted"],
        description="OpenClaw 是自托管 AI 代理网关，支持 WhatsApp、Telegram、Discord、iMessage 等多通道。每个用户都可以拥有自己的 AI 助手，无需放弃数据控制权或依赖托管服务。"
    )

    gen.add_project(
        name="Lobster (工作流引擎)",
        stars="525",
        tags=["Workflow Engine", "Type-safe", "Pipelines"],
        description="Lobster 是 OpenClaw 原生工作流引擎，提供类型化管道、审批门和可组合宏。支持 YAML/JSON 工作流文件，让 AI 代理可以一步调用复杂工作流。"
    )

    gen.add_project(
        name="ClawHub (技能目录)",
        stars="2.5K",
        tags=["Skill Directory", "Plugins"],
        description="OpenClaw 的技能目录，托管各种社区贡献的技能和工具。开发者可以在这里发布自己的技能，用户可以轻松发现和安装。"
    )

    gen.add_project(
        name="Nix-OpenClaw",
        stars="422",
        tags=["Nix", "Package Manager"],
        description="将 OpenClaw 打包为 Nix 包，方便在 NixOS 系统上安装和管理。"
    )

    gen.add_project(
        name="OpenClaw-ansible",
        stars="362",
        tags=["Ansible", "Automation"],
        description="自动化、加固的 Clawdbot 安装脚本，包含 Tailscale VPN、UFW 防火墙和 Docker 隔离。适合生产环境部署。"
    )

    # 总结
    gen.add_summary(
        title="技术洞察总结",
        content="""OpenClaw + Lobster 生态系统代表了 AI 代理基础设施的新范式：

**核心价值主张**：
1. **自主可控**：用户完全控制数据、执行环境和访问权限
2. **工作流化**：通过 Lobster 实现复杂自动化，降低 AI 操作成本
3. **多通道集成**：统一网关管理所有消息通道
4. **开源生态**：MIT 许可，社区驱动，可扩展

**技术亮点**：
• 类型化管道：确保工作流的类型安全和可组合性
• 审批门：支持需要人工确认的敏感操作
• 本地优先：所有执行在用户机器上，保证隐私
• 多代理路由：智能分发消息到合适的代理

**应用场景**：
• 个人 AI 助手：随时随地通过聊天应用访问 AI
• 自动化运维：通过工作流执行日常任务
• 多代理协作：不同专长的代理协同完成复杂任务
• 数据隐私：敏感数据不离开用户环境

**潜在机会**：
• 企业部署：企业内部自托管，保护数据安全
• 代理市场：ClawHub 技能目录可扩展为完整市场
• 插件生态：第三方开发者可扩展通道和功能
• 工作流共享：最佳实践工作流可被社区复用
"""
    )

    # 生成 HTML
    html_path = "/home/vimalinx/.openclaw/workspace/lobster_report.html"
    gen.generate_html(html_path)

    # 转换为 PDF
    pdf_path = gen.to_pdf(html_path, "/home/vimalinx/.openclaw/workspace/lobster_report.pdf")

    print(f"✅ 报告生成完成！")
    print(f"📄 HTML: {html_path}")
    print(f"📄 PDF: {pdf_path}")

    return html_path, pdf_path

if __name__ == "__main__":
    create_lobster_report()
