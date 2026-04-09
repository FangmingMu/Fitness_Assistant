import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
token = os.getenv("PUSHPLUS_TOKEN")

def test_push():
    """测试 PushPlus 推送功能"""
    if not token:
        print("❌ 错误: 未在 .env 文件中找到 PUSHPLUS_TOKEN")
        return

    url = "http://www.pushplus.plus/send"
    title = "💪 健身助手 - 微信推送测试"
    content = f"""
### 🚀 恭喜！PushPlus 集成成功
这是一条来自您的 **AI 健身助手** 的自动测试消息。

**测试详情：**
- **状态**: 正常运行
- **发送时间**: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}
- **项目路径**: `{os.getcwd()}`

---
如果您在微信上看到了这条消息，说明部署后的自动提醒功能已经准备就绪！
"""

    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown"
    }

    print(f"正在尝试发送测试消息 (Token: {token[:6]}***)...")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("code") == 200:
            print("✅ 发送成功！请检查您的微信通知。")
        else:
            print(f"⚠️ 发送失败，PushPlus 返回码: {result.get('code')}")
            print(f"消息详情: {result.get('msg')}")
            
    except Exception as e:
        print(f"❌ 发生异常: {e}")

if __name__ == "__main__":
    test_push()
