#!/usr/bin/env python3
"""
PDF导出工具 - V7版本
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def export_pdf_with_images(html_path: Path, pdf_path: Path):
    """导出PDF，等待图片加载"""
    print(f"📄 开始导出PDF...")
    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print("🌐 加载HTML...")
        await page.goto(f"file://{html_path.absolute()}", wait_until="domcontentloaded", timeout=60000)

        print("⏳ 等待图片加载...")
        # 等待所有图片加载完成或超时
        try:
            await page.wait_for_selector('img', timeout=10000)
            print("✅ 图片加载中...")
            # 额外等待图片加载
            await asyncio.sleep(3)
        except:
            print("⚠️ 部分图片可能未加载")

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
    html_path = Path("travel_guides_v7/travel_guides.html")
    pdf_path = Path("travel_guides_v7/travel_guides.pdf")

    if not html_path.exists():
        print(f"❌ HTML文件不存在: {html_path}")
        exit(1)

    asyncio.run(export_pdf_with_images(html_path, pdf_path))
