import streamlit as st
import json
import urllib.request
import urllib.error
import ssl

st.set_page_config(page_title="Key 验尸官", page_icon="🕵️‍♂️")

# 你的 Key (这是你截图里的那个)
TARGET_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

st.title("🕵️‍♂️ API Key 验尸报告")
st.write(f"正在测试 Key: `{TARGET_KEY[:5]}...{TARGET_KEY[-5:]}`")

def test_key():
    # 测试 1: 基础连接测试 (列出可用模型)
    # 这个接口最灵敏，只要 Key 是活的，权限开了，它就会返回 200
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={TARGET_KEY}"
    
    try:
        # 忽略 SSL 证书验证 (排除 Mac 网络证书干扰)
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
    
    # 检查是否支持 gemini-1.5-flash
    if 'models/gemini-1.5-flash' in model_names:
        st.success("🚀 **完美！你的账号支持 gemini-1.5-flash (最新版)！**")
        st.info("下一步：你可以放心地使用鹦鹉代码了。")
    else:
        st.warning("⚠️ **注意**：你的列表里没有 flash 模型。请在之后的代码里使用 `gemini-pro`。")

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
    
    # 提供代理修复建议
    st.warning("🚑 **急救建议**：请在侧边栏手动配置代理端口 (7890 或 10809)。")

else:
    st.error(f"💥 **未知错误**：{result}")
