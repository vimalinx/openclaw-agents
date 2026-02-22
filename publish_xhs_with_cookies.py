#!/usr/bin/env python3
"""
使用 cookies 发布小红书笔记
"""
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Cookie 文件路径
COOKIES_FILE = Path('/home/vimalinx/MakeMoney/Package_1/config/xhs_cookies.json')

async def publish_with_cookies():
    # 读取 cookies
    with open(COOKIES_FILE, 'r') as f:
        cookies_data = json.load(f)

    # 转换为 Playwright cookies 格式
    cookies = []
    for key, value in cookies_data.items():
        cookies.append({
            'name': key,
            'value': str(value),
            'domain': '.xiaohongshu.com',
            'path': '/',
        })

    # 用户 ID
    user_id = cookies_data.get('x-user-id-creator.xiaohongshu.com', '')
    print(f"👤 用户 ID: {user_id}")

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )

        # 注入 cookies
        await context.add_cookies(cookies)
        print("✅ Cookies 已加载")

        page = await context.new_page()

        # 访问小红书创作者中心
        print("🌐 访问小红书...")
        await page.goto('https://creator.xiaohongshu.com/publish/publish', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)

        # 检查登录状态
        is_logged_in = False
        try:
            # 检查是否跳转到登录页
            if 'login' not in page.url.lower():
                is_logged_in = True
                print("✅ 已登录！")
            else:
                print("⚠️  登录可能已过期")
        except:
            pass

        if is_logged_in:
            # 等待页面完全加载
            await page.wait_for_timeout(5000)

            # 截图
            screenshot_path = Path('/tmp/xhs_publish_cookies.png')
            await page.screenshot(path=str(screenshot_path), full_page=False)
            print(f"📸 截图已保存: {screenshot_path}")

            # 内容
            title = "测试笔记 - Wilson自动发布"
            content = """分享我的AI助手经验 📝

Wilson是我用OpenClaw打造的AI助手，帮我提升效率，自动化处理重复任务！

今天测试一下自动发布功能，看看能不能成功 🚀

#AI #效率 #工具 #OpenClaw #自动化""".strip()

            print(f"\n📝 标题: {title}")
            print(f"📝 内容长度: {len(content)} 字")

            # 尝试找到输入框并填充
            print("\n🔍 查找输入框...")

            # 尝试多个选择器
            selectors_to_try = [
                ('标题', ['input[placeholder*="标题"]', 'input[class*="title"]']),
                ('正文', ['[contenteditable="true"]', 'textarea']),
            ]

            for field_name, selectors in selectors_to_try:
                found = False
                for selector in selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            if await element.is_visible():
                                text_to_fill = title if field_name == '标题' else content
                                await element.click()
                                await page.wait_for_timeout(300)
                                await element.fill(text_to_fill)
                                print(f"   ✅ {field_name} 已填充: {selector}")
                                found = True
                                break
                        if found:
                            break
                    except:
                        continue

                if not found:
                    print(f"   ⚠️  {field_name} 未自动填充，请手动填写")

            # 上传封面
            cover_path = Path('/home/vimalinx/.openclaw/workspace/wilson-avatar.png')
            print(f"\n🖼️  上传封面: {cover_path.name}")

            try:
                # 点击上传按钮
                upload_button = await page.wait_for_selector('button:has-text("上传"), button:has-text("添加")', timeout=5000)
                if upload_button:
                    await upload_button.click()
                    await page.wait_for_timeout(2000)

                    # 找文件输入框
                    file_input = await page.wait_for_selector('input[type="file"]', timeout=5000)
                    if file_input:
                        await file_input.set_input_files(str(cover_path))
                        print(f"   ✅ 封面已上传")
                        await page.wait_for_timeout(3000)
            except Exception as e:
                print(f"   ⚠️  上传失败: {e}")
                print(f"   📁 请手动上传: {cover_path}")

            # 最终截图
            screenshot_final = Path('/tmp/xhs_publish_final.png')
            await page.screenshot(path=str(screenshot_final), full_page=False)
            print(f"\n📸 最终截图: {screenshot_final}")

        print("\n" + "="*50)
        print("✅ 请检查浏览器页面")
        print("="*50)
        if is_logged_in:
            print("确认内容无误后，点击「发布」按钮")
        else:
            print("可能需要重新登录")
        print("\n按 Enter 退出...")
        input()

        await browser.close()
        print("👋 已关闭浏览器")

if __name__ == '__main__':
    asyncio.run(publish_with_cookies())
