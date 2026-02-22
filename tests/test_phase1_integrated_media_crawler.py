#!/usr/bin/env python3
"""
阶段 1: 趋势研究功能测试 - 集成 Media Crawler

测试内容:
1. Media Crawler 搜索测试
2. Media Crawler 滚动测试
3. 趋势分析和热点识别
"""

import asyncio
import sys
import time
import json
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, '/home/vimalinx/.openclaw/workspace/tests')

from media_crawler_wrapper import MediaCrawlerWrapper


class IntegratedTrendTester:
    """集成 Media Crawler 的趋势研究测试器"""
    
    def __init__(self):
        self.crawler = MediaCrawlerWrapper()
        self.test_results = []
        self.test_log = []
        
    async def test_crawler_search(self):
        """测试 1.1: Media Crawler 搜索功能"""
        print("\n" + "="*60)
        print("🔍 步骤 1.1: Media Crawler 搜索功能测试")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # 测试搜索功能
            result = await self.crawler.search_materials(
                profile_id="6852c081000000001d0092d5",
                keywords=["AI工具", "自媒体运营", "爆款文案", "涨粉技巧"],
                scroll_times=10,
                timeout=180
            )
            
            # 验证结果
            if result and result.get('notes_count', 0) > 0:
                print(f"\n✅ 搜索功能测试通过")
                print(f"   搜索到 {result['notes_count']} 条笔记")
                print(f"   匹配关键词: {result['matched_keywords_count']} 个")
                print(f"   搜索耗时: {result['search_time']:.2f} 秒")
                print(f"   滚动次数: {result['scroll_times']}")
                
                status = "passed"
            else:
                print(f"\n❌ 搜索功能测试失败")
                print(f"   未找到任何笔记")
                status = "failed"
            
            # 记录测试结果
            test_result = {
                "test_name": "Media Crawler 搜索功能",
                "status": status,
                "notes_count": result.get('notes_count', 0) if result else 0,
                "matched_keywords_count": result.get('matched_keywords_count', 0) if result else 0,
                "search_time": result.get('search_time', 0) if result else 0,
                "scroll_times": result.get('scroll_times', 0) if result else 0,
                "keywords": result.get('keywords', []) if result else [],
                "notes": result.get('notes', [])[:10] if result else []
            }
            
            self.test_results.append(test_result)
            
            # 记录日志
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "Media Crawler 搜索功能",
                "status": status,
                "duration": result.get('search_time', 0) if result else 0
            })
            
            return test_result
            
        except Exception as e:
            print(f"\n❌ 搜索功能测试异常: {e}")
            import traceback
            traceback.print_exc()
            
            # 记录测试结果
            test_result = {
                "test_name": "Media Crawler 搜索功能",
                "status": "error",
                "error": str(e)
            }
            
            self.test_results.append(test_result)
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "Media Crawler 搜索功能",
                "status": "error",
                "error": str(e)
            })
            
            return test_result
    
    async def test_crawler_scroll(self):
        """测试 1.2: Media Crawler 滚动功能"""
        print("\n" + "="*60)
        print("📜 步骤 1.2: Media Crawler 滚动功能测试")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # 测试滚动功能
            result = await self.crawler.scroll_notes(
                profile_id="6852c081000000001d0092d5",
                scroll_times=15,
                timeout=180
            )
            
            # 验证结果
            if result and result.get('notes_count', 0) > 0:
                print(f"\n✅ 滚动功能测试通过")
                print(f"   加载笔记: {result['notes_count']} 篇")
                print(f"   滚动次数: {result['scroll_times']}")
                print(f"   滚动耗时: {result['scroll_time']:.2f} 秒")
                print(f"   总笔记数: {result['total_notes']}")
                
                status = "passed"
            else:
                print(f"\n❌ 滚动功能测试失败")
                print(f"   未加载到任何笔记")
                status = "failed"
            
            # 记录测试结果
            test_result = {
                "test_name": "Media Crawler 滚动功能",
                "status": status,
                "notes_count": result.get('notes_count', 0) if result else 0,
                "total_notes": result.get('total_notes', 0) if result else 0,
                "scroll_times": result.get('scroll_times', 0) if result else 0,
                "scroll_time": result.get('scroll_time', 0) if result else 0,
                "notes": result.get('notes', [])[:10] if result else []
            }
            
            self.test_results.append(test_result)
            
            # 记录日志
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "Media Crawler 滚动功能",
                "status": status,
                "duration": result.get('scroll_time', 0) if result else 0
            })
            
            return test_result
            
        except Exception as e:
            print(f"\n❌ 滚动功能测试异常: {e}")
            import traceback
            traceback.print_exc()
            
            # 记录测试结果
            test_result = {
                "test_name": "Media Crawler 滚动功能",
                "status": "error",
                "error": str(e)
            }
            
            self.test_results.append(test_result)
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "Media Crawler 滚动功能",
                "status": "error",
                "error": str(e)
            })
            
            return test_result
    
    async def test_trend_analysis(self):
        """测试 1.3: 趋势分析"""
        print("\n" + "="*60)
        print("📈 步骤 1.3: 趋势分析测试")
        print("="*60)
        
        try:
            # 执行市场情报收集
            intelligence_result = await self.crawler.collect_market_intelligence(
                profile_id="6852c081000000001d0092d5",
                search_keywords=["AI工具", "自媒体运营", "爆款文案", "涨粉技巧", "内容创作"],
                scroll_times=15,
                save_to_file=True
            )
            
            # 验证结果
            if intelligence_result:
                summary = intelligence_result['report']['summary']
                top_hot_topics = intelligence_result['analysis_result']['top_hot_topics']
                
                print(f"\n✅ 趋势分析测试通过")
                print(f"   总收集笔记: {summary['total_notes_collected']} 篇")
                print(f"   热点话题: {summary['hot_topics']} 个")
                print(f"   耗时: {intelligence_result['duration_seconds']:.2f} 秒")
                
                print(f"\n🔥 热点话题 TOP 5:")
                for i, topic in enumerate(top_hot_topics[:5]):
                    print(f"   {i+1}. {topic['title'][:40]}... (❤️ {topic['likes']} ⭐ {topic['collects']})")
                
                status = "passed"
            else:
                print(f"\n❌ 趋势分析测试失败")
                status = "failed"
            
            # 记录测试结果
            test_result = {
                "test_name": "趋势分析",
                "status": status,
                "total_notes": intelligence_result['report']['summary']['total_notes_collected'] if intelligence_result else 0,
                "hot_topics": intelligence_result['analysis_result']['hot_topics_count'] if intelligence_result else 0,
                "top_hot_topics": intelligence_result['analysis_result']['top_hot_topics'][:5] if intelligence_result else [],
                "duration": intelligence_result['duration_seconds'] if intelligence_result else 0,
                "recommendations": intelligence_result['report']['recommendations'][:10] if intelligence_result else []
            }
            
            self.test_results.append(test_result)
            
            # 记录日志
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "趋势分析",
                "status": status,
                "duration": intelligence_result['duration_seconds'] if intelligence_result else 0
            })
            
            return test_result
            
        except Exception as e:
            print(f"\n❌ 趋势分析测试异常: {e}")
            import traceback
            traceback.print_exc()
            
            # 记录测试结果
            test_result = {
                "test_name": "趋势分析",
                "status": "error",
                "error": str(e)
            }
            
            self.test_results.append(test_result)
            self.test_log.append({
                "timestamp": datetime.now().isoformat(),
                "test": "趋势分析",
                "status": "error",
                "error": str(e)
            })
            
            return test_result
    
    async def run_phase1_tests(self):
        """运行阶段 1 的所有测试（集成 Media Crawler）"""
        print("\n" + "="*60)
        print("🚀 开始阶段 1: 趋势研究功能测试（集成 Media Crawler）")
        print("="*60)
        
        phase_start = time.time()
        
        # 测试 1.1: Media Crawler 搜索功能
        print(f"\n⏱️ 测试 1.1: Media Crawler 搜索功能 ({time.strftime('%H:%M:%S')})")
        search_result = await self.test_crawler_search()
        
        # 测试 1.2: Media Crawler 滚动功能
        print(f"\n⏱️ 测试 1.2: Media Crawler 滚动功能 ({time.strftime('%H:%M:%S')})")
        scroll_result = await self.test_crawler_scroll()
        
        # 测试 1.3: 趋势分析
        print(f"\n⏱️ 测试 1.3: 趋势分析 ({time.strftime('%H:%M:%S')})")
        trend_result = await self.test_trend_analysis()
        
        phase_end = time.time()
        phase_duration = phase_end - phase_start
        
        # 汇总阶段 1 结果
        print("\n" + "="*60)
        print("📊 阶段 1 测试汇总（集成 Media Crawler）")
        print("="*60)
        
        # 统计测试结果
        total_tests = len(self.test_results)
        passed_tests = sum(1 for t in self.test_results if t.get('status') == 'passed')
        failed_tests = sum(1 for t in self.test_results if t.get('status') == 'failed')
        error_tests = sum(1 for t in self.test_results if t.get('status') == 'error')
        
        print(f"\n✅ 测试状态: 完成")
        print(f"📊 测试耗时: {phase_duration:.2f} 秒 ({phase_duration/60:.1f} 分钟)")
        
        print(f"\n📋 测试结果:")
        print(f"  总测试数: {total_tests}")
        print(f"  通过测试: {passed_tests}")
        print(f"  失败测试: {failed_tests}")
        print(f"  异常测试: {error_tests}")
        print(f"  成功率: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%")
        
        print(f"\n📝 详细结果:")
        for i, test in enumerate(self.test_results):
            status_icon = "✅" if test.get('status') == 'passed' else "❌" if test.get('status') == 'failed' else "⚠️"
            print(f"  {status_icon} {i+1}. {test['test_name']}: {test['status']}")
            if test.get('notes_count', 0) > 0:
                print(f"      笔记数: {test['notes_count']}")
            if test.get('hot_topics', 0) > 0:
                print(f"      热点话题: {test['hot_topics']}")
            if test.get('duration', 0) > 0:
                print(f"      耗时: {test['duration']:.2f} 秒")
        
        # 生成测试报告
        report = {
            "phase": 1,
            "phase_name": "趋势研究功能（集成 Media Crawler）",
            "start_time": phase_start,
            "end_time": phase_end,
            "duration_seconds": phase_duration,
            "tests": self.test_results,
            "test_log": self.test_log,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "overall_status": "success" if passed_tests == total_tests else "partial_success" if passed_tests > 0 else "failed"
            },
            "integrated_tools": ["Media Crawler"],
            "key_metrics": {
                "total_notes_collected": sum(t.get('notes_count', 0) for t in self.test_results),
                "total_hot_topics": sum(t.get('hot_topics', 0) for t in self.test_results),
                "total_duration": sum(t.get('duration', 0) for t in self.test_results)
            }
        }
        
        return report
    
    async def save_report(self, report):
        """保存测试报告"""
        import os
        
        # 确保目录存在
        tests_dir = "/home/vimalinx/.openclaw/workspace/tests"
        reports_dir = os.path.join(tests_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase1_integrated_media_crawler_report_{timestamp}.json"
        filepath = os.path.join(reports_dir, filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 测试报告已保存: {filepath}")
        return filepath
    
    def generate_progress_report(self, report):
        """生成实时进展报告"""
        print("\n" + "="*60)
        print("📊 阶段 1 测试 - 实时进展报告（集成 Media Crawler）")
        print("="*60)
        
        # 总体进展
        total_tests = len(report.get('tests', []))
        passed_tests = sum(1 for t in report.get('tests', []) if t.get('status') == 'passed')
        failed_tests = sum(1 for t in report.get('tests', []) if t.get('status') == 'failed')
        error_tests = sum(1 for t in report.get('tests', []) if t.get('status') == 'error')
        progress = (passed_tests + error_tests * 0.5) / total_tests * 100 if total_tests > 0 else 0
        
        # 整合工具
        integrated_tools = report.get('integrated_tools', [])
        
        # 关键指标
        key_metrics = report.get('key_metrics', {})
        
        print(f"\n🔄 整合工具:")
        for tool in integrated_tools:
            print(f"  ✅ {tool}")
        
        print(f"\n📊 测试状态:")
        print(f"  总测试数: {total_tests}")
        print(f"  通过测试: {passed_tests}")
        print(f"  失败测试: {failed_tests}")
        print(f"  异常测试: {error_tests}")
        print(f"  完成度: {progress:.1f}%")
        
        print(f"\n📈 关键指标:")
        print(f"  总收集笔记: {key_metrics.get('total_notes_collected', 0)} 篇")
        print(f"  总热点话题: {key_metrics.get('total_hot_topics', 0)} 个")
        print(f"  总执行时间: {key_metrics.get('total_duration', 0):.2f} 秒")
        
        print(f"\n✅ 整体状态: {report['summary']['overall_status']}")
        
        # 显示热点话题
        if any(t.get('top_hot_topics', []) for t in report.get('tests', [])):
            print(f"\n🔥 热点话题 TOP 5:")
            for test in report.get('tests', []):
                top_hot_topics = test.get('top_hot_topics', [])
                for i, topic in enumerate(top_hot_topics[:3]):
                    print(f"  {i+1}. {topic['title'][:40]}... (❤️ {topic['likes']} ⭐ {topic['collects']})")


async def main():
    """主函数"""
    print("\n" + "="*60)
    print("🧪 自媒体运营系统 - 阶段 1 测试（集成 Media Crawler）")
    print("="*60)
    
    tester = IntegratedTrendTester()
    
    try:
        # 运行阶段 1 测试
        report = await tester.run_phase1_tests()
        
        # 保存报告
        report_path = await tester.save_report(report)
        
        # 生成进度报告
        tester.generate_progress_report(report)
        
        print("\n" + "="*60)
        print("✅ 阶段 1 测试完成!")
        print("="*60)
        
        print(f"\n📊 测试概览:")
        print(f"  整合工具: {', '.join(report.get('integrated_tools', []))}")
        print(f"  总测试数: {report['summary']['total_tests']}")
        print(f"  通过测试: {report['summary']['passed_tests']}")
        print(f"  成功率: {(report['summary']['passed_tests']/report['summary']['total_tests']*100):.1f}%")
        print(f"  总耗时: {report['duration_seconds']:.2f} 秒 ({report['duration_seconds']/60:.1f} 分钟)")
        print(f"  整体状态: {report['summary']['overall_status']}")
        
        return report
        
    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
