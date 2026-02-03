import streamlit as st
import requests
import json
import time

# --- 1. 配置与密钥 ---
st.set_page_config(page_title="皮皮鹦鹉 (Python后端版)", page_icon="🦜", layout="centered")

# 你的 Key (Python 端调用，更安全稳定)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 核心函数: Python 调用 Google Gemini ---
def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # 鹦鹉人设
    system_prompt = """
    你现在是一只叫"皮皮"的鹦鹉，对话对象是3-6岁小朋友。
    规则：
    1. 回复必须简短(20字以内)。
    2. 必须模仿鹦鹉说话，喜欢重复(如"好吃好吃")。
    3. 句尾加上"呱！"。
    4. 热情、可爱、傻乎乎。
    """
    
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": text}]}
        ]
    }
    
    try:
        # 使用 proxies=None 确保遵循系统代理设置
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"呱！网络连不上啦！(错误码: {response.status_code})"
    except Exception as e:
        return f"呱！脑子卡住了！(错误: {str(e)})"

# --- 3. 样式注入 (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #fceea7; }
    /* 隐藏顶部Header */
    header {visibility: hidden;}
    
    /* 鹦鹉卡片 */
    .parrot-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 5px solid #ff6b6b;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    
    /* 鹦鹉动画 */
    .avatar {
        width: 120px; height: 120px; 
        border-radius: 50%;
        background: #e0f7fa; 
        border: 4px solid #4ecdc4;
        margin: 0 auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 70px;
        animation: float 3s infinite ease-in-out;
    }
    
    .chat-bubble {
        background: #4ecdc4;
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin-top: 15px;
        font-size: 18px;
        position: relative;
    }
    .chat-bubble::after {
        content: ''; position: absolute; top: -10px; left: 50%; margin-left: -10px;
        border-width: 0 10px 10px; border-style: solid; border-color: #4ecdc4 transparent;
    }

    @keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-10px);} }
</style>
""", unsafe_allow_html=True)

# --- 4. 界面布局 ---

# 初始化 Session State
if "history" not in st.session_state:
    st.session_state.history = "你好！我是皮皮！"
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# 显示鹦鹉区域
st.markdown(f"""
<div class="parrot-card">
    <div class="avatar">🦜</div>
    <div class="chat-bubble">{st.session_state.history}</div>
</div>
""", unsafe_allow_html=True)

# --- 5. 交互逻辑 (混合输入) ---

st.write("### 👇 和皮皮说话")

# 使用 Streamlit 表单来处理输入
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("在这里打字...", placeholder="比如：讲个故事")
    submitted = st.form_submit_button("发送 🚀")

if submitted and user_input:
    # 1. 获取 AI 回复
    ai_reply = ask_gemini(user_input)
    st.session_state.history = ai_reply
    
    # 2. 语音合成 (JS 自动播放 Hack)
    # 我们生成一段包含 SpeechSynthesis 的 HTML 自动执行
    js_code = f"""
    <script>
        var u = new SpeechSynthesisUtterance("{ai_reply}");
        u.lang = 'zh-CN';
        u.rate = 1.4;
        u.pitch = 1.6;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)
    
    # 3. 强制刷新界面显示最新文字
    st.rerun()

# --- 6. 语音输入 (如果你的 Streamlit 版本支持) ---
# 注意：st.audio_input 需要 Streamlit 1.40+ 版本
try:
    audio_value = st.audio_input("或者点击麦克风说话 🎤")
    if audio_value:
        st.warning("⚠️ 纯语音转文字需要额外的模型(OpenAI/Whisper)，为了不增加你的成本，目前建议使用打字，或者确保你的环境可以调用谷歌语音识别。")
except AttributeError:
    pass # 旧版本忽略

# --- 7. 调试帮助 ---
with st.expander("🛠️ 还是连不上？点这里"):
    st.write("""
    **为什么显示网络错误？**
    因为 Google 的服务在国内被屏蔽了。
    
    **怎么解决？**
    1. **开启 VPN**：确保你的电脑开启了 VPN，并且开启了“全局模式”或者让终端也能通过代理。
    2. **部署到云端**：把这个代码上传到 Streamlit Cloud (免费)，那边的服务器在美国，可以直接连通，不需要 VPN。
    """)
