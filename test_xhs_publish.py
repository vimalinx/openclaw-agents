#!/usr/bin/env python3
"""
测试小红书自动发布 - 使用已登录的浏览器
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import time

# 浏览器数据目录（保存登录态）
USER_DATA_DIR = Path.home() / '.cache' / 'playwright' / 'chrome-xiaohongshu'

async def test_publish():
    async with async_playwright() as p:
        # 使用持久化上下文，保存登录态
        browser = await p.chromium.launch_persistent_context(
            str(USER_DATA_DIR),
            headless=False,
            viewport={'width': 1280, 'height': 900},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )

        print("🌐 打开小红书...")
        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.goto('https://www.xiaohongshu.com', wait_until='networkidle')
        await page.wait_for_timeout(2000)

        print("📝 检查登录状态...")
        # 等待页面加载完成
        await page.wait_for_load_state('networkidle')

        # 检查是否已登录 - 查找登录按钮
        login_selectors = [
            '.login-btn',
            '[class*="login"]',
            'text=登录',
            'button:has-text("登录")',
        ]

        is_logged_in = True
        for selector in login_selectors:
            try:
                login_element = await page.wait_for_selector(selector, timeout=2000)
                if login_element and await login_element.is_visible():
                    is_logged_in = False
                    break
            except:
                continue

        if not is_logged_in:
            print("⚠️  未登录，请手动登录...")
            print("   登录完成后按 Enter 继续...")
            input()
        else:
            print("✅ 已登录！")

        print("➕ 打开发布页面...")
        await page.goto('https://creator.xiaohongshu.com/publish/publish', wait_until='domcontentloaded', timeout=60000)
        print("   等待页面加载...")
        await page.wait_for_timeout(8000)  # 等待更长时间让React渲染

        # 截图保存，方便调试
        screenshot_path = USER_DATA_DIR / 'screenshot.png'
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"   📸 页面截图已保存: {screenshot_path}")

        print("\n📝 开始填充内容...")

        # 填充标题
        title = "测试笔记 - Wilson自动发布"
        print(f"   标题: {title}")

        # 等待标题输入框出现
        try:
            # 尝试多种选择器
            title_selectors = [
                'input[placeholder*="填写标题"]',
                'input[placeholder*="笔记标题"]',
                'input[placeholder*="标题"]',
                'input[class*="title"]',
                '[class*="title"] input',
                'input[type="text"]',
            ]

            filled_title = False
            for selector in title_selectors:
                try:
                    print(f"   尝试选择器: {selector}")
                    title_inputs = await page.query_selector_all(selector)
                    for title_input in title_inputs:
                        if await title_input.is_visible():
                            await title_input.click()
                            await page.wait_for_timeout(300)
                            await title_input.fill(title[:20])
                            print(f"   ✅ 标题已填充！")
                            filled_title = True
                            break
                    if filled_title:
                        break
                except Exception as e:
                    print(f"   选择器失败: {selector} - {e}")
                    continue

            if not filled_title:
                print("   ⚠️  无法自动填充标题，请手动填写")
        except Exception as e:
            print(f"   ⚠️  填充标题时出错: {e}")

        # 填充正文
        content = """分享我的AI助手经验 📝

Wilson是我用OpenClaw打造的AI助手，帮我提升效率，自动化处理重复任务！

今天测试一下自动发布功能，看看能不能成功 🚀

#AI #效率 #工具 #OpenClaw #自动化""".strip()

        print(f"\n   内容长度: {len(content)} 字")

        try:
            # 尝试多种选择器
            content_selectors = [
                '[contenteditable="true"]',
                'textarea[placeholder*="正文"]',
                'textarea[placeholder*="填写正文"]',
                'textarea[placeholder*="内容"]',
                'textarea',
                'div[contenteditable][placeholder]',
            ]

            filled_content = False
            for selector in content_selectors:
                try:
                    print(f"   尝试选择器: {selector}")
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        if await element.is_visible():
                            await element.click()
                            await page.wait_for_timeout(500)
                            await element.fill(content)
                            print(f"   ✅ 内容已填充！")
                            filled_content = True
                            await page.wait_for_timeout(1000)
                            break
                    if filled_content:
                        break
                except Exception as e:
                    print(f"   选择器失败: {selector} - {e}")
                    continue

            if not filled_content:
                print("   ⚠️  无法自动填充内容，请手动填写")
                print(f"   👇 内容如下：")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"   ⚠️  填充内容时出错: {e}")

        print("\n🖼️  上传封面...")
        cover_path = Path('/home/vimalinx/.openclaw/workspace/wilson-avatar.png')
        if not cover_path.exists():
            print(f"   ⚠️  封面文件不存在: {cover_path}")
        else:
            try:
                # 先截个图看看当前状态
                screenshot_before = USER_DATA_DIR / 'screenshot_before_upload.png'
                await page.screenshot(path=str(screenshot_before), full_page=False)
                print(f"   📸 上传前截图: {screenshot_before}")

                # 尝试找上传按钮
                upload_selectors = [
                    'text="上传图片"',
                    'text="添加图片"',
                    'button:has-text("上传")',
                    'button:has-text("添加")',
                    '[class*="upload"]',
                    '[class*="image"] button',
                    '.upload-btn',
                ]

                clicked_upload = False
                for selector in upload_selectors:
                    try:
                        upload_btn = await page.wait_for_selector(selector, timeout=2000)
                        if upload_btn and await upload_btn.is_visible():
                            await upload_btn.click()
                            print(f"   ✅ 点击了上传按钮: {selector}")
                            clicked_upload = True
                            await page.wait_for_timeout(2000)
                            break
                    except:
                        continue

                if clicked_upload:
                    # 尝试找文件输入框
                    file_input = await page.wait_for_selector('input[type="file"]', timeout=5000)
                    if file_input:
                        await file_input.set_input_files(str(cover_path))
                        print(f"   ✅ 封面已上传: {cover_path.name}")
                        await page.wait_for_timeout(3000)
                    else:
                        print(f"   ⚠️  找不到文件输入框")
                else:
                    print(f"   ⚠️  找不到上传按钮，请手动上传封面")
                    print(f"   📁 封面路径: {cover_path}")

            except Exception as e:
                print(f"   ⚠️  上传封面时出错: {e}")

        # 最终截图
        screenshot_final = USER_DATA_DIR / 'screenshot_final.png'
        await page.screenshot(path=str(screenshot_final), full_page=False)
        print(f"\n   📸 最终截图: {screenshot_final}")

        print("\n" + "="*50)
        print("✅ 脚本执行完成！")
        print("="*50)
        print("👀 浏览器窗口应该显示发布页面")
        print(f"   - 标题: {title}")
        print(f"   - 内容: {len(content)} 字")
        print(f"   - 封面: {cover_path.name}")
        print("\n请检查页面内容，确认无误后:")
        print("   1. 手动填写未自动填充的内容")
        print("   2. 手动上传封面（如果未成功）")
        print("   3. 点击「发布」按钮")
        print("\n按 Enter 退出...")
        input()

        await browser.close()
        print("👋 已关闭浏览器")

if __name__ == '__main__':
    asyncio.run(test_publish())
