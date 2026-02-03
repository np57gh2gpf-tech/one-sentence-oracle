import streamlit as st
import urllib.request
import json
import ssl
import os

st.set_page_config(page_title="API 诊断室", page_icon="👨‍⚕️")

st.title("👨‍⚕️ API 连接诊断室")
st.write("正在检查你的 API Key 和网络连接，请稍候...")

# 你的 Key
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# 定义一个检查函数
def check_connection(proxy=None):
    # 如果指定了代理，临时设置一下
    if proxy:
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy
    else:
        #如果不指定，清除系统变量干扰（保持纯净）
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    data = json.dumps({"contents": [{"parts": [{"text": "Hello"}]}]}).encode('utf-8')
    
    try:
        # 忽略证书验证 (防止 SSL 报错)
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 发送请求 (5秒超时)
        with urllib.request.urlopen(req, context=context, timeout=5) as response:
            return "SUCCESS", response.code
            
    except urllib.error.HTTPError as e:
        return "KEY_ERROR", e.code
    except urllib.error.URLError as e:
        return "NETWORK_ERROR", str(e.reason)
    except Exception as e:
        return "UNKNOWN_ERROR", str(e)

# --- 开始自动诊断 ---

# 1. 第一轮：直接连接
with st.spinner("正在尝试直接连接 Google..."):
    status, msg = check_connection()

if status == "SUCCESS":
    st.success("✅ **直接连接成功！**")
    st.write("结论：你的网络环境非常好，Key 也是对的。之前的代码跑不通可能是代码写复杂了。")
    st.balloons()

elif status == "KEY_ERROR":
    st.error(f"❌ **网络通了，但 Key 错了** (错误码: {msg})")
    st.write("结论：你的 Python 成功连上了谷歌，但是谷歌拒绝了你的密码。")
    st.warning("建议：请去 Google AI Studio 重新生成一个 Key。")

elif status == "NETWORK_ERROR":
    st.error(f"❌ **直接连接失败** ({msg})")
    st.write("正在尝试自动修复（测试常用代理端口 7890/10809）...")
    
    # 2. 第二轮：尝试自动挂代理
    proxies_to_try = ["http://127.0.0.1:7890", "http://127.0.0.1:10809", "http://127.0.0.1:1080"]
    success_proxy = None
    
    for p in proxies_to_try:
        with st.spinner(f"正在尝试代理 {p} ..."):
            s, m = check_connection(proxy=p)
            if s == "SUCCESS":
                success_proxy = p
                break
    
    if success_proxy:
        st.success(f"✅ **修复成功！** 发现你的有效代理端口是：`{success_proxy}`")
        st.markdown(f"""
        ### 💡 怎么解决？
        请在你之后的代码里，**必须**加上这两行代码才能跑通：
        ```python
        import os
        os.environ["http_proxy"] = "{success_proxy}"
        os.environ["https_proxy"] = "{success_proxy}"
        ```
        """)
    else:
        st.error("💀 **彻底失败**：试了所有常用端口都连不上。")
        st.write("原因：你的 VPN 可能没有开启，或者不是这几个常见端口。")
