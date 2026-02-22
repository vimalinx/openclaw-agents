#!/usr/bin/env python3
"""Test if browser-use can be imported and initialized"""
import asyncio
from browser_use import Browser

async def test():
    try:
        print("🐺 Creating browser instance...")
        browser = Browser()
        print("✅ Browser created successfully!")
        print("   This means browser-use is working!")
        # Browser session auto-closes, no need to manually close
        print("✅ Test completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
