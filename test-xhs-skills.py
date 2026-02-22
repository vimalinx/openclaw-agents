#!/usr/bin/env python3
"""
小红书自动化闭环 - Skill 可用性测试脚本
测试各个组件的安装和可用性状态
"""

import sys
import importlib
from pathlib import Path

def test_skill(name, import_path):
    """测试 skill 是否可以导入"""
    try:
        module = importlib.import_module(import_path)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def check_file_exists(path):
    """检查文件是否存在"""
    return Path(path).exists()

def main():
    print("=" * 80)
    print("🧪 小红书自动化闭环 - Skill 可用性测试")
    print("=" * 80)
    print()

    # 测试结果记录
    results = []

    # 1. 测试 MediaCrawler skill（热点监控）
    print("📋 1. MediaCrawler Skill（热点监控）")
    print("-" * 80)
    skill_path = Path("/home/vimalinx/.openclaw/skills/media-crawler")
    skill_exists = skill_path.exists()
    print(f"   Skill 目录: {skill_path} {'✅' if skill_exists else '❌'}")
    print(f"   SKILL.md: {skill_path / 'SKILL.md'} {'✅' if (skill_path / 'SKILL.md').exists() else '❌'}")
    print(f"   skill.py: {skill_path / 'skill.py'} {'✅' if (skill_path / 'skill.py').exists() else '❌'}")

    if skill_exists:
        success, error = test_skill("MediaCrawler", "skills.media_crawler.skill")
        print(f"   可导入: {'✅' if success else '❌'}")
        if error:
            print(f"   错误: {error}")
        results.append({
            "name": "MediaCrawler（热点监控）",
            "installed": skill_exists,
            "importable": success,
            "status": "✅ 可用" if success else "⚠️ 部分可用",
            "notes": "需要 Chrome 远程调试（CDP）"
        })
    else:
        results.append({
            "name": "MediaCrawler（热点监控）",
            "installed": False,
            "importable": False,
            "status": "❌ 未安装",
            "notes": "需要安装 media-crawler skill"
        })
    print()

    # 2. 测试 AI 内容生成
    print("📋 2. AI 内容生成")
    print("-" * 80)
    generator_path = Path("/home/vimalinx/.openclaw/skills/xhs-auto-publisher/content_generator_v2.py")
    print(f"   文档生成器: {generator_path} {'✅' if generator_path.exists() else '❌'}")

    if generator_path.exists():
        success, error = test_skill("XHSContentGenerator", "skills.xhs_auto_publisher.content_generator_v2")
        print(f"   可导入: {'✅' if success else '❌'}")
        if error:
            print(f"   错误: {error}")
        results.append({
            "name": "AI 内容生成",
            "installed": generator_path.exists(),
            "importable": success,
            "status": "✅ 可用" if success else "⚠️ 部分可用",
            "notes": "内置模板生成器，无需外部 API"
        })
    else:
        results.append({
            "name": "AI 内容生成",
            "installed": False,
            "importable": False,
            "status": "❌ 未安装",
            "notes": "需要安装 content_generator"
        })
    print()

    # 3. 测试配图生成
    print("📋 3. 配图生成（Grsai API 或替代方案）")
    print("-" * 80)
    cover_path = Path("/home/vimalinx/.openclaw/skills/xhs-auto-publisher/cover_generator.py")
    print(f"   封面生成器: {cover_path} {'✅' if cover_path.exists() else '❌'}")

    if cover_path.exists():
        success, error = test_skill("CoverGenerator", "skills.xhs_auto_publisher.cover_generator")
        print(f"   可导入: {'✅' if success else '❌'}")
        if error:
            print(f"   错误: {error}")

        # 检查 API 密钥配置
        import os
        api_key = os.environ.get("VOLCENGINE_API_KEY") or os.environ.get("GRSAI_API_KEY")
        print(f"   API 密钥: {'✅ 已配置' if api_key else '❌ 未配置'}")

        results.append({
            "name": "配图生成",
            "installed": cover_path.exists(),
            "importable": success,
            "status": "⚠️ 需要配置" if success and not api_key else "✅ 可用" if success and api_key else "❌ 未配置",
            "notes": "使用火山引擎豆包绘图 API（非 Grsai），需要 API 密钥"
        })
    else:
        results.append({
            "name": "配图生成",
            "installed": False,
            "importable": False,
            "status": "❌ 未安装",
            "notes": "需要安装 cover_generator"
        })
    print()

    # 4. 测试自动发布
    print("📋 4. 自动发布（xhs-auto-publisher）")
    print("-" * 80)
    publisher_path = Path("/home/vimalinx/.openclaw/skills/xhs-auto-publisher")
    print(f"   Skill 目录: {publisher_path} {'✅' if publisher_path.exists() else '❌'}")
    print(f"   publisher.py: {publisher_path / 'publisher.py'} {'✅' if (publisher_path / 'publisher.py').exists() else '❌'}")

    if publisher_path.exists():
        success, error = test_skill("XiaohongshuPublisher", "skills.xhs_auto_publisher.publisher")
        print(f"   可导入: {'✅' if success else '❌'}")
        if error:
            print(f"   错误: {error}")
        results.append({
            "name": "自动发布",
            "installed": publisher_path.exists(),
            "importable": success,
            "status": "✅ 可用" if success else "⚠️ 部分可用",
            "notes": "需要 Chrome 远程调试（CDP）和小红书登录"
        })
    else:
        results.append({
            "name": "自动发布",
            "installed": False,
            "importable": False,
            "status": "❌ 未安装",
            "notes": "需要安装 xhs-auto-publisher skill"
        })
    print()

    # 5. 测试数据反馈功能
    print("📋 5. 数据反馈功能")
    print("-" * 80)
    print(f"   MediaCrawler 监控: {'⚠️ 未实现' if not skill_exists else '✅ 可用'}")
    print(f"   主脚本集成: {'✅ 已集成' if check_file_exists('/home/vimalinx/.openclaw/workspace/xhs-auto-pipeline.py') else '❌ 未集成'}")

    # 检查主脚本中的反馈功能实现
    pipeline_path = Path("/home/vimalinx/.openclaw/workspace/xhs-auto-pipeline.py")
    if pipeline_path.exists():
        content = pipeline_path.read_text(encoding='utf-8')
        has_collect_feedback = "async def collect_feedback" in content
        print(f"   collect_feedback 函数: {'✅ 已定义' if has_collect_feedback else '❌ 未定义'}")
        is_mock = "TODO: 集成 MediaCrawler 监控" in content
        print(f"   实现状态: {'⚠️ 模拟数据' if is_mock else '✅ 实际集成'}")

    results.append({
        "name": "数据反馈",
        "installed": True,
        "importable": True,
        "status": "⚠️ 未完全实现",
        "notes": "主脚本中函数已定义但返回模拟数据，需集成 MediaCrawler 监控功能"
    })
    print()

    # 6. 测试主脚本
    print("📋 6. 主脚本（xhs-auto-pipeline.py）")
    print("-" * 80)
    pipeline_path = Path("/home/vimalinx/.openclaw/workspace/xhs-auto-pipeline.py")
    print(f"   主脚本: {pipeline_path} {'✅' if pipeline_path.exists() else '❌'}")

    if pipeline_path.exists():
        try:
            # 检查脚本语法
            with open(pipeline_path, 'r', encoding='utf-8') as f:
                compile(f.read(), pipeline_path, 'exec')
            print(f"   语法检查: ✅ 通过")
            results.append({
                "name": "主脚本",
                "installed": True,
                "importable": True,
                "status": "✅ 可用",
                "notes": "可运行 test 模式"
            })
        except SyntaxError as e:
            print(f"   语法检查: ❌ 失败 - {e}")
            results.append({
                "name": "主脚本",
                "installed": True,
                "importable": False,
                "status": "❌ 语法错误",
                "notes": str(e)
            })
    else:
        results.append({
            "name": "主脚本",
            "installed": False,
            "importable": False,
            "status": "❌ 未找到",
            "notes": "需要创建 xhs-auto-pipeline.py"
        })
    print()

    # 生成测试报告摘要
    print("=" * 80)
    print("📊 测试结果摘要")
    print("=" * 80)
    print()

    for i, result in enumerate(results, 1):
        status = result["status"]
        print(f"{i}. {result['name']:30s} {status}")
        if result.get("notes"):
            print(f"   └─ {result['notes']}")

    print()

    # 统计
    total = len(results)
    available = sum(1 for r in results if "✅" in r["status"])
    partial = sum(1 for r in results if "⚠️" in r["status"])
    unavailable = sum(1 for r in results if "❌" in r["status"])

    print(f"总计: {total} 个组件")
    print(f"  ✅ 可用: {available} 个")
    print(f"  ⚠️ 需配置: {partial} 个")
    print(f"  ❌ 不可用: {unavailable} 个")
    print()

    # 配置需求
    print("=" * 80)
    print("⚙️ 配置需求")
    print("=" * 80)
    print()
    print("1. Chrome 远程调试（CDP）")
    print("   - 启动命令: google-chrome --remote-debugging-port=9222")
    print("   - 需求: MediaCrawler, xhs-auto-publisher")
    print()
    print("2. 小红书登录状态")
    print("   - 在 Chrome 中登录小红书")
    print("   - 需求: MediaCrawler, xhs-auto-publisher")
    print()
    print("3. API 密钥")
    print("   - VOLCENGINE_API_KEY 或 GRSAI_API_KEY")
    print("   - 需求: 配图生成（封面生成器）")
    print("   - 获取: 火山引擎豆包绘图 API")
    print()
    print("4. Python 依赖")
    print("   - playwright")
    print("   - aiohttp")
    print("   - 安装: pip install -r requirements.txt")
    print()

    # 下一步建议
    print("=" * 80)
    print("💡 下一步建议")
    print("=" * 80)
    print()
    print("高优先级：")
    print("  1. 配置 Chrome 远程调试并登录小红书")
    print("  2. 获取并配置图像生成 API 密钥")
    print("  3. 实际测试 MediaCrawler 和 xhs-auto-publisher 的真实功能")
    print()
    print("中优先级：")
    print("  4. 实现 collect_feedback 函数的真实数据监控")
    print("  5. 创建完整的端到端测试")
    print("  6. 编写使用文档和配置指南")
    print()
    print("低优先级：")
    print("  7. 添加错误处理和重试机制")
    print("  8. 实现定时任务（cron）")
    print("  9. 添加数据持久化和历史记录")
    print()

    return results

if __name__ == "__main__":
    results = main()
    sys.exit(0)
