#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 测试脚本（加载 .env 配置）
"""

import os
import json
import sys

try:
    from dotenv import load_dotenv
    import requests
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请安装缺失的库: pip install python-dotenv requests")
    sys.exit(1)

# 加载 .env 文件
load_dotenv()

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
    print(f"📏 密钥长度: {len(API_KEY)} 字符")
    return True

def test_api_connection():
    """测试 API 连接"""
    print("\n🌐 测试 API 连接")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置，跳过连接测试")
        return False
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # 测试 API 连接
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        print(f"✅ API 响应状态码: {response.status_code}")
        print(f"⏱️ 响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            print("✅ API 连接成功！")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或已过期")
            return False
        elif response.status_code == 403:
            print("❌ API 权限不足")
            return False
        elif response.status_code == 429:
            print("❌ 请求过于频繁（限流）")
            return False
        else:
            print(f"❌ API 连接失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ API 连接超时（>10秒）")
        print("   请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False

def test_image_generation():
    """测试图像生成"""
    print("\n🎨 测试图像生成")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置，跳过图像生成测试")
        return False
    
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
        # 发送图像生成请求
        print("📤 正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"✅ 请求状态码: {response.status_code}")
        print(f"⏱️ 响应时间: {response.elapsed.total_seconds:.2f} 秒")
        
        if response.status_code == 200:
            print("✅ 图像生成请求成功！")
            
            # 检查响应内容
            try:
                data = response.json()
                print(f"✅ 响应数据解析成功")
                
                if "data" in data:
                    print("✅ 响应包含 'data' 字段")
                    result_data = data["data"]
                    
                    if "status" in result_data:
                        status = result_data["status"]
                        print(f"   任务状态: {status}")
                    else:
                        print("⚠️  响应中没有 'status' 字段")
                    
                    if "output" in result_data:
                        output = result_data["output"]
                        print(f"   输出类型: {type(output)}")
                        
                        if isinstance(output, dict):
                            print(f"   输出键: {list(output.keys())}")
                            
                            if "image_url" in output:
                                image_url = output["image_url"]
                                print(f"   ✅ 图像 URL: {image_url}")
                            else:
                                print(f"   输出内容: {str(output)[:200]}")
                        else:
                            print(f"   输出类型: {type(output)}")
                    else:
                        print("⚠️  响应中没有 'output' 字段")
                else:
                    print("⚠️  响应中没有 'data' 字段")
                    print(f"   响应内容: {response.text[:200]}")
                    
        elif response.status_code == 401:
            print("❌ 图像生成失败：API Key 无效")
        elif response.status_code == 403:
            print("❌ 图像生成失败：API 权限不足")
        elif response.status_code == 429:
            print("❌ 图像生成失败：请求过于频繁（限流）")
        else:
            print(f"❌ 图像生成失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
            
        return response.status_code == 200
        
    except requests.exceptions.Timeout:
        print("❌ 图像生成请求超时（>60秒）")
        print("   请检查网络连接和 API 额度")
        return False
    except Exception as e:
        print(f"❌ 图像生成失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 火山引擎 API 测试工具")
    print("=" * 50)
    print(f"API URL: {API_URL}")
    print(f"API Key: {API_KEY[:10]}..." if API_KEY else "未设置")
    print()
    
    # 测试 1: API Key 验证
    key_valid = test_api_key()
    if not key_valid:
        print("\n❌ API Key 配置失败，请检查 .env 文件")
        print("配置文件: xiaohongshu-auto-reply/.env")
        return
    
    # 测试 2: API 连接
    connection_ok = test_api_connection()
    if not connection_ok:
        print("\n❌ API 连接测试失败，请检查网络连接和 API Key")
        return
    
    # 测试 3: 图像生成
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
    print("   1. ✅ API Key 验证通过")
    print("   2. ✅ API 连接正常")
    print("   3. ✅ 图像生成功能可用")
    print()
    print("🎉 火山引擎 API 已验证可用！")
    print()
    print("💡 下一步行动:")
    print("   1. ✅ 修改 xhs-auto-pipeline.py 以使用真实 API")
    print("   2. ✅ 配置图像生成参数（尺寸、质量、风格）")
    print("   3. ✅ 测试完整的自动化发布流程")
    print("   4. ✅ 开始真实的自动化运营")
    print()
    print("🚀 准备就绪，可以开始真实的图像生成了！")

if __name__ == "__main__":
    main()
