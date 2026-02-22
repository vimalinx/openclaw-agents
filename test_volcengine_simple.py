#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 简化测试脚本
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
API_KEY = os.getenv("VOLCENGINE_API_KEY", "")

def test_api_key():
    """测试 API Key"""
    print("🔑 测试 API Key")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置！")
        print("请先设置环境变量:")
        print("export VOLCENGINE_API_KEY='your_api_key'")
        return False
    
    print(f"✅ API Key 已设置: {API_KEY[:10]}...")
    print(f"📏 长度: {len(API_KEY)} 字符")
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
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        print(f"✅ API 响应状态码: {response.status_code}")
        print(f"⏱️ 响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            print("✅ API 连接成功！")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或已过期")
            print("请检查 API Key 是否正确")
            return False
        elif response.status_code == 403:
            print("❌ API 配额已用完")
            print("请检查账户余额")
            return False
        else:
            print(f"❌ API 连接失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API 连接超时（>10秒）")
        print("请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 火山引擎 API 简化测试工具")
    print("=" * 40)
    print()
    
    # 测试 1: API Key
    if not test_api_key():
        print("\n⚠️ 请先配置 API Key 后再试")
        return
    
    # 测试 2: API 连接
    if not test_api_connection():
        print("\n⚠️ 请检查 API Key 和网络连接后重试")
        return
    
    # 测试 3: 简单图像生成请求
    print("\n🎨 测试图像生成（简化版）")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 最简单的测试 payload
    payload = {
        "prompt": "test image",
        "request_id": "test_simple_001",
        "num_inference_steps": 28
    }
    
    try:
        print("📤 正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"✅ 请求状态码: {response.status_code}")
        print(f"⏱️  响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ 图像生成请求成功！")
                print(f"   响应数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
                
                if "data" in data:
                    result_data = data["data"]
                    if "status" in result_data:
                        status = result_data["status"]
                        print(f"   任务状态: {status}")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        print(f"   输出类型: {type(output)}")
                        print(f"   输出数据: {json.dumps(output, ensure_ascii=False, indent=2)[:300]}")
                
                print("\n🎉 测试完成！")
                print("=" * 40)
                print("✅ API Key 配置正确")
                print("✅ API 连接正常")
                print("✅ 图像生成功能可用")
                print("\n📋 下一步:")
                print("1. 修改 xhs-auto-pipeline.py")
                print("2. 启用真实图像生成功能")
                print("3. 配置图像参数（尺寸、质量、风格）")
                print("4. 测试完整的发布流程")
                
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON 解析失败: {e}")
                print(f"   响应内容: {response.text[:200]}")
        else:
            print(f"❌ 图像生成请求失败: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("❌ 图像生成请求超时（>60秒）")
        print("请检查网络连接和 API 配额")
    except Exception as e:
        print(f"❌ 图像生成测试失败: {e}")

if __name__ == "__main__":
    main()
