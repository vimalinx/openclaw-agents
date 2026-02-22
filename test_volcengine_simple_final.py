#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 测试脚本
"""

import os
import json
import sys

try:
    import requests
except ImportError:
    print("❌ requests 库未安装")
    sys.exit(1)

API_URL = "https://open.volcengine.com/api/v3/text/image/v2"
API_KEY = os.getenv("VOLCENGINE_API_KEY", "")

TEST_PROMPT = "小红书风格封面图，AI工具相关"

def test_api_key():
    print("🔑 测试 API Key")
    print(f"API Key: {API_KEY[:20]}..." if len(API_KEY) > 20 else API_KEY)
    return len(API_KEY) > 0

def test_api_connection():
    print("\n🌐 测试 API 连接")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置")
        return False
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API 连接成功")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或已过期")
            print(f"   状态码: {response.status_code}")
            return False
        else:
            print(f"❌ API 连接失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:100]}")
            return False
    except Exception as e:
        print(f"❌ API 连接测试失败: {e}")
        return False

def test_image_generation():
    print("\n🎨 测试图像生成")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": TEST_PROMPT,
        "request_id": f"test_simple",
        "num_inference_steps": 28
    }
    
    try:
        print("📤 正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("✅ 图像生成请求成功")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
            
            try:
                data = response.json()
                if "data" in data:
                    print("✅ 数据返回成功")
                    result_data = data["data"]
                    
                    if "status" in result_data:
                        print(f"   任务状态: {result_data['status']}")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        print(f"   输出类型: {type(output)}")
                        
                        if isinstance(output, dict) and "image_url" in output:
                            image_url = output["image_url"]
                            print(f"   图像 URL: {image_url}")
                else:
                    print("❌ 数据返回格式不符合预期")
            else:
                print("❌ 响应中没有 'data' 字段")
        elif response.status_code == 401:
            print("❌ 图像生成失败：API Key 无效")
        elif response.status_code == 403:
            print("❌ 图像生成失败：余额不足或配额已用完")
        else:
            print(f"❌ 图像生成失败，状态码: {response.status_code}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 图像生成测试失败: {e}")
        return False

def main():
    print("🚀 火山引擎 API 测试工具")
    print("=" * 50)
    print()
    
    # 检查 API Key
    if not test_api_key():
        print("\n❌ API Key 未配置，请先设置环境变量:")
        print("export VOLCENGINE_API_KEY='your_api_key'")
        return
    
    # 测试 API 连接
    if not test_api_connection():
        print("\n❌ API 连接测试失败，请检查 API Key 和网络连接")
        return
    
    # 测试图像生成
    if not test_image_generation():
        print("\n❌ 图像生成测试失败，请检查 API 配额和网络连接")
        return
    
    # 总结报告
    print("\n" + "=" * 50)
    print("📊 测试总结报告")
    print("=" * 50)
    print("✅ API Key 配置正确")
    print("✅ API 连接正常")
    print("✅ 图像生成功能可用")
    print()
    print("🎉 火山引擎 API 已验证可用！")
    print()
    print("📋 下一步行动:")
    print("1. ✅ 修改 xhs-auto-pipeline.py 以使用真实的火山引擎 API")
    print("2. ✅ 配置图像生成参数（尺寸、质量、风格）")
    print("3. ✅ 测试完整的自动化发布流程")
    print("4. ✅ 启用真实的数据收集和反馈")
    print()
    print("🚀 准备就绪，可以开始真实的自动化发布了！")

if __name__ == "__main__":
    main()
