import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
token = os.getenv("PUSHPLUS_TOKEN")

def send_test(channel="wechat", channel_name="微信"):
    """执行具体的推送请求"""
    if not token:
        print(f"❌ 错误: 未在 .env 文件中找到 PUSHPLUS_TOKEN")
        return

    url = "http://www.pushplus.plus/send"
    title = f"💪 健身助手 - {channel_name}推送测试"
    content = f"""
### 🚀 PushPlus {channel_name}集成测试
这是一条来自您的 **AI 健身助手** 的测试消息。

**测试详情：**
- **推送通道**: {channel_name} ({channel})
- **当前状态**: 正在验证连通性
- **发送时间**: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}

---
如果您收到了这条消息，说明该通道已配置成功！
"""

    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown",
        "channel": channel  # 指定通道：wechat 或 mail
    }

    print(f"正在尝试发送【{channel_name}】测试 (Token: {token[:6]}***)...")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("code") == 200:
            print(f"✅ {channel_name}发送指令已下达！请检查。")
        else:
            print(f"⚠️ {channel_name}发送失败，返回码: {result.get('code')}")
            print(f"详情: {result.get('msg')}")
            
    except Exception as e:
        print(f"❌ 发生异常: {e}")

if __name__ == "__main__":
    # 1. 测试微信推送 (默认)
    send_test(channel="wechat", channel_name="微信")
    
    print("-" * 30)
    
    # 2. 测试邮件推送
    # 注意：需确保您在 pushplus.plus 后台已激活邮件通道并绑定了邮箱
    send_test(channel="mail", channel_name="邮件")
