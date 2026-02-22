#!/usr/bin/env python3
"""
PDF导出工具 - V8版本（优化timeout）
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def export_pdf_v8(html_path: Path, pdf_path: Path):
    """导出PDF，优化timeout"""
    print(f"📄 开始导出PDF...")
    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print("🌐 加载HTML（增加timeout）...")
        # 增加timeout到60秒
        await page.goto(f"file://{html_path.absolute()}", 
                     wait_until="domcontentloaded", 
                     timeout=60000)

        print("⏳ 等待图片加载（超时10秒）...")
        # 等待图片，如果超时就继续
        try:
            await page.wait_for_selector('img', state='attached', timeout=10000)
            print("✅ 图片已加载")
        except:
            print("⚠️ 部分图片可能未加载，继续导出...")

        # 额外等待确保图片渲染
        print("📄 渲染2秒...")
        await asyncio.sleep(2)

        print("📄 导出PDF中...")
        # 导出PDF
        await page.pdf(
            path=str(pdf_path),
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

    print(f"✅ PDF已导出: {pdf_path}")
    print(f"📊 文件大小: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    html_path = Path("travel_guides_v8/travel_guides.html")
    pdf_path = Path("travel_guides_v8/travel_guides.pdf")

    if not html_path.exists():
        print(f"❌ HTML文件不存在: {html_path}")
        exit(1)

    asyncio.run(export_pdf_v8(html_path, pdf_path))
