#!/usr/bin/env python3
"""
小红书登录脚本 - 在有显示器的电脑上运行
登录后会保存 cookie 到文件
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import sys

def main():
    # 有头模式
    options = Options()
    # 如果有 Chrome 可以在本地改成 Chrome 路径
    # options.binary_location = '/usr/bin/chromium'
    
    driver = webdriver.Chrome(options=options)
    
    print('='*50)
    print('请在弹出的浏览器中登录小红书')
    print('='*50)
    
    driver.get('https://www.xiaohongshu.com/explore')
    
    # 等待用户手动登录
    input('登录完成后，回车继续...')
    
    # 保存 cookie
    cookies = driver.get_cookies()
    with open('xiaohongshu_cookies.json', 'w') as f:
        json.dump(cookies, f)
    
    print('Cookie 已保存到 xiaohongshu_cookies.json')
    print('请把这个文件发给 Wilson')
    
    driver.quit()

if __name__ == '__main__':
    main()
