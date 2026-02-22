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
    print("请先安装: pip install requests")
    sys.exit(1)

API_URL = "https://open.volcengine.com/api/v3/text/image/v2"
API_KEY = os.getenv("VOLCENGINE_API_KEY", "")

TEST_PROMPT = "小红书风格封面图，AI 工具相关"

def test_api_key():
    print("🔑 测试 API Key")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置")
        print("请设置环境变量: export VOLCENGINE_API_KEY='your_api_key'")
        return False
    
    print(f"✅ API Key 已配置: {API_KEY[:20]}...")
    print(f"密钥长度: {len(API_KEY)} 字符")
    return True

def test_api_connection():
    print("\n🌐 测试 API 连接")
    print("=" * 40)
    
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
            return False
        else:
            print(f"❌ API 连接失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API 连接超时（>10 秒）")
        print("请检查网络连接")
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
            
            # 检查响应内容
            try:
                data = response.json()
                if "data" in data:
                    print("✅ 数据返回成功")
                    result_data = data["data"]
                    
                    if "status" in result_data:
                        status = result_data["status"]
                        print(f"   任务状态: {status}")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        
                        if isinstance(output, dict):
                            print(f"   输出类型: 字典")
                            if "image_url" in output:
                                image_url = output["image_url"]
                                print(f"   图像 URL: {image_url}")
                            else:
                                print(f"   输出键: {list(output.keys())}")
                        else:
                            print(f"   输出类型: {type(output)}")
                            print(f"   输出内容: {str(output)[:200]}")
                else:
                    print("⚠️ 响应中没有 data 字段")
            else:
                print("⚠️ 响应不是 JSON 格式")
                print(f"   响应内容: {response.text[:100]}")
                
        elif response.status_code == 401:
            print("❌ 图像生成失败：API Key 无效")
        elif response.status_code == 403:
            print("❌ 图像生成失败：账户余额不足")
        elif response.status_code == 429:
            print("❌ 图像生成失败：请求过于频繁（限流）")
        else:
            print(f"❌ 图像生成失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:100]}")
            
        return response.status_code == 200
            
    except requests.exceptions.Timeout:
        print("❌ 图像生成请求超时（>60 秒）")
        print("请检查网络连接和 API 配额")
        return False
    except Exception as e:
        print(f"❌ 图像生成失败: {e}")
        return False

def main():
    print("🚀 火山引擎 API 测试工具")
    print("=" * 50)
    print()
    
    # 测试 1: API Key 验证
    if not test_api_key():
        print("\n❌ API Key 配置失败，请检查后重试")
        return
    
    # 测试 2: API 连接
    if not test_api_connection():
        print("\n❌ API 连接失败，请检查网络连接")
        return
    
    # 测试 3: 图像生成
    if not test_image_generation():
        print("\n❌ 图像生成测试失败")
        return
    
    # 总结报告
    print("\n" + "=" * 50)
    print("📊 测试总结报告")
    print("=" * 50)
    print()
    print("✅ 所有测试通过")
    print()
    print("📋 下一步行动:")
    print("1. ✅ API Key 验证通过")
    print("2. ✅ API 连接正常")
    print("3. ✅ 图像生成功能可用")
    print()
    print("💡 建议配置:")
    print("- 修改 xhs-auto-pipeline.py 以使用真实 API")
    print("- 配置图像生成参数（尺寸、质量、风格）")
    print("- 测试完整的发布流程")
    print()
    print("🎉 准备就绪，可以开始真实的图像生成和发布了！")
    print("=" * 50)

if __name__ == "__main__":
    main()
