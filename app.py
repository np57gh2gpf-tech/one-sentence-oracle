import streamlit as st
import json
import urllib.request
import urllib.error
import ssl

st.set_page_config(page_title="Key 验尸官", page_icon="🕵️‍♂️")

# 你的 Key
TARGET_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

st.title("🕵️‍♂️ API Key 验尸报告")
st.write(f"正在测试 Key: `{TARGET_KEY[:5]}...{TARGET_KEY[-5:]}`")

def test_key():
    # 测试 1: 基础连接测试 (列出可用模型)
    # 这个接口最灵敏，只要 Key 是活的，权限开了，它就会返回 200
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={TARGET_KEY}"
    
    try:
        # 忽略 SSL 证书验证 (排除网络证书干扰)
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "ALIVE", data
            
    except urllib.error.HTTPError as e:
        return "HTTP_ERROR", e.code
    except urllib.error.URLError as e:
        return "NETWORK_ERROR", e.reason
    except Exception as e:
        return "UNKNOWN", str(e)

# --- 开始运行测试 ---
with st.spinner("正在进行尸检..."):
    status, result = test_key()

st.divider()

if status == "ALIVE":
    st.success("🎉 **恭喜！这个 Key 是活的！**")
    st.balloons()
    st.write("### 详细诊断：")
    st.write("1. ✅ **网络没问题**：Python 成功连上了 Google。")
    st.write("2. ✅ **Key 没问题**：Google 验证通过。")
    st.write("3. ✅ **权限没问题**：API 服务已开启。")
    
    # 打印可用的模型，看看你的账号能用哪些
    model_names = [m['name'] for m in result.get('models', [])]
    st.info(f"你的账号可以用这些模型：\n{model_names}")
    
    if 'models/gemini-1.5-flash' in model_names:
        st.write("🚀 **太棒了，你支持 gemini-1.5-flash (最新版)！**")
    else:
        st.warning("⚠️ 注意：你的列表里没有 flash 模型，建议代码里改用 gemini-pro。")

elif status == "HTTP_ERROR":
    st.error(f"💀 **测试失败：服务器拒绝 (错误码 {result})**")
    
    if result == 400:
        st.write("❌ **诊断：Key 无效**。")
        st.write("原因：Key 可能复制错了，或者被删除了。")
        
    elif result == 403:
        st.write("🔒 **诊断：Key 是对的，但门没开！**")
        st.write("原因：你没有在 Google Cloud Console 启用 **'Generative Language API'**。")
        st.markdown("[👉 点击这里去开启](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)")
        
    elif result == 404:
        st.write("❓ **诊断：找不到资源**。")
        st.write("这种情况很少见，可能是接口地址变了。")

elif status == "NETWORK_ERROR":
    st.error("🔌 **测试失败：网络完全不通**")
    st.write(f"错误信息：`{result}`")
    st.write("💡 **原因**：你的 VPN 没开，或者 Python 没走代理。")
    st.write("🚑 **急救**：请在侧边栏手动配置代理端口。")

else:
    st.error(f"💥 **未知错误**：{result}")import streamlit as st
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
