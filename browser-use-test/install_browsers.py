#!/usr/bin/env python3
"""
Install Playwright browsers without system dependencies
"""
import asyncio
from playwright.sync_api import sync_playwright

def main():
    print("🐺 Installing Playwright Chromium browser...")
    try:
        # Try installing without system dependencies
        import subprocess
        result = subprocess.run(
            ['playwright', 'install', 'chromium'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("STDERR:", result.stderr)
            return False
        print("✅ Chromium installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()
