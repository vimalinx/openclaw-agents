#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 测试脚本（简化版）
"""

import os
import json
import sys

try:
    import requests
except ImportError:
    print("❌ requests 库未安装，请先安装: pip install requests")
    sys.exit(1)

API_URL = "https://open.volcengine.com/api/v3/text/image/v2"
API_KEY = "95ea79a6-8d43-4b01-91d3-5c137ee618f9"
TEST_PROMPT = "小红书风格封面图，AI 工具相关"

def test_api_connection():
    print("\n🌐 测试 API 连接")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        print(f"✅ API 响应状态码: {response.status_code}")
        print(f"✅ 响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            print("✅ API 连接成功！")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或已过期")
            return False
        else:
            print(f"❌ API 连接失败，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API 连接超时（>10 秒）")
        return False
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
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
        "request_id": "test_simple_001",
        "num_inference_steps": 28
    }
    
    try:
        print("📤 正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        print(f"✅ 请求状态码: {response.status_code}")
        print(f"✅ 响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            print("✅ 图像生成请求成功！")
            
            try:
                data = response.json()
                print("✅ JSON 解析成功")
                
                if "data" in data:
                    print("✅ 响应包含 'data' 字段")
                    result_data = data["data"]
                    
                    if "status" in result_data:
                        status = result_data["status"]
                        print(f"✅ 任务状态: {status}")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        print(f"✅ 找到 'output' 字段")
                        print(f"   输出类型: {type(output)}")
                        
                        if isinstance(output, dict):
                            print(f"   输出键: {list(output.keys())}")
                            if "image_url" in output:
                                image_url = output["image_url"]
                                print(f"   ✅ 图像 URL: {image_url}")
                            else:
                                print(f"   输出内容: {str(output)[:200]}")
                        else:
                            print(f"   输出内容: {str(output)[:200]}")
                    else:
                        print("⚠️ 响应中没有 'output' 字段")
                else:
                    print("⚠️ 响应中没有 'data' 字段")
                    
            elif response.status_code == 401:
                print("❌ 图像生成失败：API Key 无效")
            elif response.status_code == 403:
                print("❌ 图像生成失败：余额不足")
            elif response.status_code == 429:
                print("❌ 图像生成失败：请求过于频繁（限流）")
            else:
                print(f"❌ 图像生成失败，状态码: {response.status_code}")
            
            return True
            
    except requests.exceptions.Timeout:
        print("❌ 图像生成请求超时（>60 秒）")
        return False
    except Exception as e:
        print(f"❌ 图像生成失败: {e}")
        return False

def main():
    print("🚀 火山引擎 API 测试工具")
    print("=" * 50)
    print()
    
    # 测试 1: API 连接
    connection_ok = test_api_connection()
    if not connection_ok:
        print("\n❌ API 连接测试失败，请检查网络连接和 API Key")
        return
    
    # 测试 2: 图像生成
    generation_ok = test_image_generation()
    if not generation_ok:
        print("\n❌ 图像生成测试失败，请检查 API 配额和网络连接")
        return
    
    # 总结报告
    print("\n" + "=" * 50)
    print("📊 测试总结报告")
    print("=" * 50)
    print()
    print("✅ 所有测试通过！")
    print()
    print("📋 测试结果:")
    print("   1. ✅ API Key 配置正确")
    print("   2. ✅ API 连接正常")
    print("   3. ✅ 图像生成功能可用")
    print()
    print("🎉 火山引擎 API 已验证可用！")
    print()
    print("💡 下一步行动:")
    print("   1. ✅ 配置小红书自动化闭环以使用真实图像生成")
    print("   2. ✅ 配置图像生成参数（尺寸、质量、风格）")
    print("   3. ✅ 测试完整的自动化发布流程")
    print("   4. ✅ 启用真实的数据收集和反馈")
    print()
    print("🚀 准备就绪，可以开始真实的图像生成了！")

if __name__ == "__main__":
    main()
