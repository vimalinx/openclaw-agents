#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎 API 测试脚本
功能：测试 API Key、连接、图像生成
"""

import os
import json
import requests
from pathlib import Path

# API 配置
API_URL = "https://open.volcengine.com/api/v3/text/image/v2"
API_KEY = os.getenv("VOLCENGINE_API_KEY", "")

# 测试参数
TEST_PROMPT = """
小红书风格封面图，AI 工具相关
主标题：AI 工具真的太好用了
副标题：效率神器
风格：简洁现代，使用蓝色为主色调
元素：包含 AI 工具相关图标或图形
文字：大标题突出，副标题补充说明
整体：干净整洁，吸引点击
"""

def test_api_connection():
    """测试 API 连接"""
    print("🔍 测试 1: API 连接")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # 测试 API 连接
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API 连接成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
        else:
            print(f"❌ API 连接失败！")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        print()
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ API 连接测试失败: {e}")
        print()
        return False

def test_image_generation():
    """测试图像生成"""
    print("🎨 测试 2: 图像生成")
    print("=" * 40)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": TEST_PROMPT,
        "request_id": f"test_{int(time.time())}",
        "num_inference_steps": 28
    }
    
    try:
        # 发送图像生成请求
        print("正在发送图像生成请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("✅ 图像生成请求成功！")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response.elapsed.total_seconds:.2f} 秒")
            
            # 检查响应内容
            try:
                response_json = response.json()
                if "data" in response_json:
                    print("   数据返回: ✅")
                    if "status" in response_json["data"]:
                        status = response_json["data"]["status"]
                        print(f"   任务状态: {status}")
                    
                    if "output" in response_json["data"]:
                        output = response_json["data"]["output"]
                        if isinstance(output, dict) and "image_url" in output:
                            image_url = output["image_url"]
                            print(f"   图像 URL: {image_url}")
                        else:
                            print(f"   输出类型: {type(output)}")
                else:
                    print("   数据返回: ❌")
                    print(f"   响应内容: {response.text[:200]}")
            else:
                print("   响应解析失败")
                print(f"   响应内容: {response.text[:200]}")
                
        else:
            print(f"❌ 图像生成失败！")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.text[:200]}")
        
        print()
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 图像生成测试失败: {e}")
        print()
        return False

def test_api_key_format():
    """测试 API Key 格式"""
    print("🔑 测试 3: API Key 格式验证")
    print("=" * 40)
    
    if not API_KEY:
        print("❌ API Key 未设置！")
        print("   请先设置环境变量: export VOLCENGINE_API_KEY='your_key'")
        print()
        return False
    
    # 验证 API Key 长度
    if len(API_KEY) < 20:
        print(f"❌ API Key 长度不足: {len(API_KEY)} 字符")
        print("   火山引擎 API Key 通常应该有 20+ 字符")
        print()
        return False
    
    # 检查空格
    if any(c.isspace() for c in API_KEY):
        print("❌ API Key 包含空格！")
        print("   请检查环境变量是否设置正确")
        print()
        return False
    
    # 检查特殊字符（允许常见的特殊字符）
    allowed_special_chars = "-_"
    invalid_chars = [c for c in API_KEY if not c.isalnum() and c not in allowed_special_chars]
    if invalid_chars:
        print(f"❌ API Key 包含非法字符: {invalid_chars[:10]}")
        print("   请检查环境变量是否设置正确")
        print()
        return False
    
    print("✅ API Key 格式验证通过！")
    print(f"   API Key 长度: {len(API_KEY)} 字符")
    print(f"   格式: 合格")
    print()
    return True

def main():
    """主函数"""
    import time
    
    print("🚀 火山引擎 API 测试工具")
    print("=" * 40)
    print()
    
    # 测试 1: API Key 格式验证
    key_valid = test_api_key_format()
    if not key_valid:
        print("⚠️  API Key 格式验证失败，请检查配置后重试")
        return
    
    # 测试 2: API 连接
    connection_ok = test_api_connection()
    if not connection_ok:
        print("⚠️  API 连接测试失败，请检查 API Key 和网络连接")
        return
    
    # 测试 3: 图像生成
    generation_ok = test_image_generation()
    if not generation_ok:
        print("⚠️  图像生成测试失败，请检查 API 配额和网络连接")
        return
    
    # 总结报告
    print("📊 测试总结报告")
    print("=" * 40)
    print("✅ 所有测试通过！")
    print()
    print("📋 下一步行动:")
    print("1. ✅ API Key 验证通过")
    print("2. ✅ API 连接正常")
    print("3. ✅ 图像生成功能可用")
    print()
    print("💡 建议配置:")
    print("- 将 API Key 添加到 ~/.bashrc 或 ~/.zshrc")
    print("- 修改 xhs-auto-pipeline.py 以使用真实 API")
    print("- 配置图像生成参数（尺寸、质量、风格）")
    print("- 测试真实的图像生成流程")
    print("- 开始真实的自动化发布")
    print()
    print("🎉 准备就绪，可以开始真实的图像生成！")


if __name__ == "__main__":
    main()
