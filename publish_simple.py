#!/usr/bin/env python3
"""
小红书发布脚本 - 简化版
直接跳到发布页面，假设已登录
"""
import sys
import time
from playwright.sync_api import sync_playwright

def publish_simple(title: str, content: str):
    """简化版发布脚本"""
    print(f"🚀 开始发布...")
    print(f"标题: {title}")
    print(f"内容长度: {len(content)} 字\n")

    with sync_playwright() as p:
        # 启动浏览器（使用已登录的 profile）
        context = p.chromium.launch_persistent_context(
            user_data_dir="/home/vimalinx/.aionui/xiaohongshu-chrome-profile",
            headless=False,
            viewport={'width': 1280, 'height': 900}
        )

        page = context.new_page()

        try:
            # 直接跳到发布页面
            print("🌐 打开发布页面...")
            page.goto("https://creator.xiaohongshu.com/publish/publish", wait_until="domcontentloaded")
            time.sleep(3)

            # 截图
            page.screenshot(path="/tmp/xhs_step1.png")
            print("📸 已截图: /tmp/xhs_step1.png")

            # 检查是否需要登录
            if "/login" in page.url:
                print("\n⚠️  需要登录！")
                print("请在浏览器中扫码登录，登录后按 Enter 继续...")
                input()
                time.sleep(2)

            # 等待图片上传区域
            print("\n⏳ 等待上传区域...")
            for i in range(15):
                if page.locator("text=上传图片").count() > 0:
                    print("✅ 找到上传区域")
                    break
                time.sleep(1)
            else:
                print("⚠️  未找到上传区域")

            # 点击上传区域（触发文件选择）
            print("\n📤 准备上传图片...")
            try:
                page.locator("text=上传图片").click()
                time.sleep(1)

                # 找文件输入框
                file_inputs = page.locator("input[type='file']")
                if file_inputs.count() > 0:
                    print("✅ 找到文件输入框")
                    file_inputs.first.set_input_files("/home/vimalinx/.openclaw/workspace/wilson-avatar.png")
                    print("✅ 图片已上传")
                    time.sleep(3)
                else:
                    print("⚠️  未找到文件输入框")
            except Exception as e:
                print(f"⚠️  上传失败: {e}")

            # 截图
            page.screenshot(path="/tmp/xhs_step2.png")
            print("📸 已截图: /tmp/xhs_step2.png")

            # 等待标题输入框
            print("\n⏳ 等待标题输入框...")
            for i in range(15):
                selectors = [
                    "input[placeholder*='标题']",
                    "input[placeholder*='填写标题']",
                ]
                for sel in selectors:
                    if page.locator(sel).count() > 0:
                        title_input = page.locator(sel).first
                        if title_input.is_visible():
                            print("✅ 找到标题输入框")
                            # 填写标题
                            if len(title) > 20:
                                title = title[:20]
                                print(f"⚠️  标题过长，截断到20字")
                            title_input.fill(title)
                            print(f"✅ 已填标题: {title}")
                            time.sleep(1)
                            break
                if "✅ 找到标题输入框" in locals():
                    break
                time.sleep(1)

            # 等待内容输入框
            print("\n⏳ 等待内容输入框...")
            for i in range(15):
                content_selectors = [
                    "[contenteditable='true']",
                    "textarea",
                ]
                for sel in content_selectors:
                    elements = page.locator(sel)
                    if elements.count() > 0:
                        for j in range(elements.count()):
                            elem = elements.nth(j)
                            if elem.is_visible():
                                elem.click()
                                time.sleep(0.5)
                                elem.fill(content)
                                print("✅ 已填内容")
                                time.sleep(1)
                                break
                        break
                if "✅ 已填内容" in locals():
                    break
                time.sleep(1)

            # 最终截图
            page.screenshot(path="/tmp/xhs_step3.png")
            print("📸 最终截图: /tmp/xhs_step3.png")

            print("\n" + "="*50)
            print("✅ 内容已填充！")
            print("="*50)
            print("\n请在浏览器中检查内容，确认无误后:")
            print("1. 点击「发布」按钮")
            print("\n按 Enter 退出...")
            input()

        except Exception as e:
            print(f"\n❌ 出错: {e}")
            print("浏览器将保持打开...")
            input()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 publish_simple.py \"标题\"")
        sys.exit(1)

    title_arg = sys.argv[1]

    # 默认内容
    content = """分享我的AI助手经验 📝

Wilson是我用OpenClaw打造的AI助手，帮我提升效率，自动化处理重复任务！

今天测试一下自动发布功能，看看能不能成功 🚀

#AI #效率 #工具 #OpenClaw #自动化"""

    publish_simple(title_arg, content)
