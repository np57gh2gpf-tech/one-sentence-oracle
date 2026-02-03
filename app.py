import urllib.request
import json
import ssl

# 你的 Key
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

def doctor_check():
    print("🩺 正在诊断中... 请稍等...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    data = json.dumps({"contents": [{"parts": [{"text": "Hello"}]}]}).encode('utf-8')
    
    try:
        # 尝试发送请求
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        # 创建一个忽略证书验证的上下文（排除证书干扰）
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            print("\n✅ 诊断结果：【一切正常】")
            print("恭喜！你的 API Key 是好的，网络也是通的！")
            print("如果你之前的代码跑不通，那是代码写错了，不是你的问题。")
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ 诊断结果：【API Key 有问题】(错误码: {e.code})")
        print("你的网络是通的（连上谷歌了），但是谷歌拒绝了你。")
        if e.code == 400:
            print("原因：Key 无效，或者该模型不可用。")
        elif e.code == 403:
            print("原因：权限不足，可能要在 Google AI Studio 里把这个 Key 绑定一下项目。")
            
    except urllib.error.URLError as e:
        print("\n❌ 诊断结果：【网络完全不通】")
        print("原因：你的 Python 程序完全连不上谷歌。")
        print("详细错误：", e.reason)
        print("💡 即使你开了 VPN，Python 可能也没走代理。")
        
    except Exception as e:
        print(f"\n❌ 诊断结果：【其他未知错误】\n{e}")

if __name__ == "__main__":
    doctor_check()
