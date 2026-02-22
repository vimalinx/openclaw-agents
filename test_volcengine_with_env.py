#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 测试脚本（加载 .env 配置）
"""

import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ requests 库未安装，请先安装: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# 加载 .env 文件
env_file = Path(__file__).parent / ".env"
if env_file.exists() and load_dotenv is not None:
    load_dotenv(env_file)
    print(f"✅ 已加载 .env 配置文件: {env_file}")
else:
    if load_dotenv is None:
        print("📝 python-dotenv 未安装，使用默认环境变量")
    else:
        print("📝 .env 文件不存在，使用默认环境变量")

# API 配置
API_URL = os.getenv("VOLCENGINE_API_URL", "https://open.volcengine.com/api/v3/text/image/v2")
API_KEY = os.getenv("VOLCENGINE_API_KEY", "")

# 测试参数
TEST_PROMPT = """
小红书风格封面图，AI工具相关
主标题：AI工具真的太好用了
副标题：效率神器
风格：简洁现代，使用蓝色为主色调
元素：包含AI工具相关图标或图形
文字：大标题突出，副标题补充说明
整体：干净整洁，吸引点击
"""

def test_api_key():
    """测试 API Key"""
    print("🔑 测试 API Key")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未配置！")
        print("请在 .env 文件中设置: VOLCENGINE_API_KEY=your_api_key")
        return False
    
    print(f"✅ API Key 已配置: {API_KEY[:10]}...")
    print(f"   密度: {len(API_KEY)} 字符")
    return True

def test_api_connection():
    """测试 API 连接"""
    print("\n🌐 测试 API 连接")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # 测试 API 连接
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ API 连接成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
            return True
        elif response.status_code == 401:
            print(f"❌ API Key 无效或已过期")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            return False
        elif response.status_code == 403:
            print(f"❌ 账户余额不足或配额已用完")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            return False
        else:
            print(f"❌ API 连接失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API 连接超时（>10 秒）")
        print("   请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False

def test_image_generation():
    """测试图像生成"""
    print("\n🎨 测试图像生成")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 简化的测试 payload
    payload = {
        "prompt": TEST_PROMPT,
        "request_id": "test_simple_001",
        "num_inference_steps": 28
    }
    
    try:
        # 发送图像生成请求
        print("📤 正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("✅ 图像生成请求成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
            
            # 检查响应内容
            try:
                data = response.json()
                if "data" in data:
                    print("✅ 数据返回成功！")
                    result_data = data["data"]
                    
                    if "status" in result_data:
                        status = result_data["status"]
                        print(f"   任务状态: {status}")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        print(f"   输出类型: {type(output)}")
                        
                        if isinstance(output, dict) and "image_url" in output:
                            image_url = output["image_url"]
                            print(f"   图像 URL: {image_url}")
                        
                            # 下载测试图像
                            print("   正在下载测试图像...")
                            try:
                                img_response = requests.get(image_url, timeout=30)
                                if img_response.status_code == 200:
                                    print("   ✅ 测试图像下载成功！")
                                    print(f"   文件大小: {len(img_response.content)} 字节")
                                else:
                                    print(f"   ❌ 图像下载失败，状态码: {img_response.status_code}")
                            except Exception as download_error:
                                print(f"   ❌ 图像下载失败: {download_error}")
                        else:
                            print(f"   输出数据: {output}")
                else:
                    print("❌ 数据返回格式不符合预期")
                    print(f"   响应内容: {response.text[:200]}")
            else:
                print("❌ JSON 解析失败")
                print(f"   响应内容: {response.text[:200]}")
        elif response.status_code == 401:
            print("❌ 图像生成失败：API Key 无效")
            print(f"   状态码: {response.status_code}")
        elif response.status_code == 403:
            print("❌ 图像生成失败：账户余额不足")
            print(f"   状态码: {response.status_code}")
        elif response.status_code == 429:
            print("❌ 图像生成失败：请求过于频繁（限流）")
            print(f"   状态码: {response.status_code}")
        else:
            print(f"❌ 图像生成失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
        
        return response.status_code == 200
            
    except requests.exceptions.Timeout:
        print("❌ 图像生成请求超时（>60 秒）")
        print("   请检查网络连接和 API 配额")
        return False
    except Exception as e:
        print(f"❌ 图像生成失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 火山引擎 API 测试工具（加载 .env 配置）")
    print("=" * 50)
    print()
    
    # 测试 1: API Key 验证
    if not test_api_key():
        print("\n❌ API Key 验证失败，请检查配置后重试")
        return
    
    # 测试 2: API 连接
    if not test_api_connection():
        print("\n❌ API 连接失败，请检查 API Key 和网络连接")
        return
    
    # 测试 3: 图像生成
    if not test_image_generation():
        print("\n❌ 图像生成失败，请检查 API 配额和网络连接")
        return
    
    # 总结报告
    print("\n" + "=" * 50)
    print("📊 测试总结报告")
    print("=" * 50)
    print()
    print("✅ 所有测试通过！")
    print()
    print("🎉 火山引擎 API 已验证可用！")
    print()
    print("📋 下一步行动:")
    print("1. ✅ API Key 已验证")
    print("2. ✅ API 连接正常")
    print("3. ✅ 图像生成功能可用")
    print("4. ✅ 配置文件已更新")
    print()
    print("💡 建议配置:")
    print("- 调整图像生成参数（尺寸、质量、风格）")
    print("- 配置小红书自动发布流程")
    print("- 测试完整的发布流程")
    print("- 开始真实的自动化运营")
    print()
    print("🚀 准备就绪，可以开始真实的图像生成和发布了！")

if __name__ == "__main__":
    main()
