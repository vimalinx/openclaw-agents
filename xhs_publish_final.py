#!/usr/bin/env python3
"""
小红书发布脚本 - 最终版
简单直接，易于使用
"""
import sys
import time
from playwright.sync_api import sync_playwright

def main():
    if len(sys.argv) < 2:
        print("用法: python3 xhs_publish_final.py \"标题\"")
        print("示例: python3 xhs_publish_final.py \"测试笔记 - Wilson\"")
        sys.exit(1)

    title = sys.argv[1]

    # 标题截断（20字限制）
    if len(title) > 20:
        print(f"⚠️  标题过长（{len(title)} 字），截断到20字")
        title = title[:20]

    content = """分享我的AI助手经验 📝

Wilson是我用OpenClaw打造的AI助手，帮我提升效率，自动化处理重复任务！

今天测试一下自动发布功能，看看能不能成功 🚀

#AI #效率 #工具 #OpenClaw #自动化"""

    cover = "/home/vimalinx/.openclaw/workspace/wilson-avatar.png"

    print("="*50)
    print("🚀 小红书发布脚本")
    print("="*50)
    print(f"标题: {title}")
    print(f"内容: {len(content)} 字")
    print(f"封面: {cover}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🌐 打开发布页面...")
        page.goto("https://creator.xiaohongshu.com/publish/publish")
        time.sleep(5)

        # 检查登录
        if "/login" in page.url or "登录" in page.content():
            print("\n⚠️  未登录！请在浏览器中扫码登录...")
            print("   登录完成后按 Enter 继续...")
            input()
            time.sleep(2)

        print("📤 上传封面...")
        try:
            # 方法1：直接找隐藏的文件输入框
            file_inputs = page.locator("input[type='file']")
            if file_inputs.count() > 0:
                file_inputs.first.set_input_files(cover)
                print("   ✅ 封面已上传（使用隐藏输入框）")
                time.sleep(3)
            else:
                # 方法2：点击上传区域
                upload_area = page.locator(".upload-area, [class*='upload'], text=上传")
                if upload_area.count() > 0:
                    upload_area.first.click()
                    time.sleep(1)
                    file_inputs = page.locator("input[type='file']")
                    if file_inputs.count() > 0:
                        file_inputs.first.set_input_files(cover)
                        print("   ✅ 封面已上传")
                        time.sleep(3)
                    else:
                        print("   ⚠️  请手动上传封面")
                else:
                    print("   ⚠️  请手动上传封面")
        except Exception as e:
            print(f"   ⚠️  上传失败: {e}")
            print("   👉 请手动上传封面")

        print("\n📝 填写标题...")
        try:
            title_selectors = [
                "input[placeholder*='标题']",
                "input[placeholder*='填写标题']",
            ]
            for sel in title_selectors:
                title_input = page.locator(sel)
                if title_input.count() > 0 and title_input.first.is_visible():
                    title_input.first.click()
                    time.sleep(0.3)
                    title_input.first.fill(title)
                    print(f"   ✅ 已填标题: {title}")
                    time.sleep(0.5)
                    break
            else:
                print("   ⚠️  请手动填标题")
        except Exception as e:
            print(f"   ⚠️  填写标题失败: {e}")

        print("\n📝 填写内容...")
        try:
            content_selectors = [
                "[contenteditable='true']",
                "textarea",
            ]
            filled = False
            for sel in content_selectors:
                elems = page.locator(sel)
                if elems.count() > 0:
                    for i in range(elems.count()):
                        elem = elems.nth(i)
                        if elem.is_visible():
                            elem.click()
                            time.sleep(0.5)
                            elem.fill(content)
                            print("   ✅ 已填内容")
                            filled = True
                            break
                if filled:
                    break
            if not filled:
                print("   ⚠️  请手动填内容")
        except Exception as e:
            print(f"   ⚠️  填写内容失败: {e}")

        print("\n" + "="*50)
        print("✅ 脚本执行完成！")
        print("="*50)
        print("\n👀 请在浏览器中：")
        print("   1. 检查内容是否正确")
        print("   2. 手动完成未自动填充的部分")
        print("   3. 点击「发布」按钮")
        print("\n按 Enter 退出...")
        input()

        browser.close()
        print("\n👋 已关闭浏览器")

if __name__ == "__main__":
    main()
