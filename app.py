import streamlit as st
import json
import urllib.request
import urllib.error

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉", page_icon="🦜", layout="centered")

# 你的 Key
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# 【网络急救包】
# 如果你开了VPN还是连不上，请把下面这行的 # 号去掉，
# 并根据你的VPN软件把端口改成 7890 或 10809
# import os
# os.environ["https_proxy"] = "http://127.0.0.1:7890"

# --- 2. 核心功能: 使用原生 Python 连接 AI (不需安装库) ---
def talk_to_gemini(user_text, history_context):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # 鹦鹉人设提示词
    system_prompt = """
    你现在是"皮皮鹦鹉"。
    规则：
    1. 必须非常可爱、傻乎乎。
    2. 喜欢重复词语 (如: "好吃好吃")。
    3. 句尾必须加 "呱！"。
    4. 回复要简短 (20字以内)。
    """
    
    # 构造请求数据
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]},
            *history_context, # 放入历史记忆
            {"role": "user", "parts": [{"text": user_text}]}
        ]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.URLError as e:
        return f"呱！网络连不上！(请检查VPN)"
    except Exception as e:
        return f"呱！脑子坏掉了！({str(e)})"

# --- 3. 界面美化 (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #fceea7; }
    header { visibility: hidden; }
    
    .parrot-box {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 20px;
        border: 4px solid #ff6b6b;
        margin-bottom: 20px;
    }
    .avatar { font-size: 80px; animation: bounce 2s infinite; display: inline-block; }
    
    @keyframes bounce { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    
    .chat-row { display: flex; margin-bottom: 10px; }
    .bubble { padding: 10px 15px; border-radius: 15px; font-size: 16px; max-width: 80%; }
    .user-bubble { background: #d1ecf1; margin-left: auto; color: #0c5460; }
    .ai-bubble { background: #fff3cd; margin-right: auto; color: #856404; border: 1px solid #ffeeba; }
</style>
""", unsafe_allow_html=True)

# --- 4. 逻辑处理 ---
if "history" not in st.session_state:
    st.session_state.history = [] # 记忆列表

# 标题区
st.markdown("""
<div class="parrot-box">
    <div class="avatar">🦜</div>
    <h3>我是皮皮！快跟我说话！</h3>
</div>
""", unsafe_allow_html=True)

# 显示历史对话
for msg in st.session_state.history:
    role_class = "user-bubble" if msg['role'] == "user" else "ai-bubble"
    st.markdown(f"<div class='chat-row'><div class='bubble {role_class}'>{msg['parts'][0]['text']}</div></div>", unsafe_allow_html=True)

# --- 5. 交互区 (文字+自动语音) ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("在这里打字...", placeholder="比如：讲个故事")
    submitted = st.form_submit_button("发送 / 说")

if submitted and user_input:
    # 1. 记录用户说的话
    # 注意：为了发给API，我们需要转换格式
    context_for_api = st.session_state.history[-6:] # 只记最近6句，防止token爆炸
    
    # 2. 调用 AI (不依赖任何安装库)
    reply = talk_to_gemini(user_input, context_for_api)
    
    # 3. 更新界面
    st.session_state.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.history.append({"role": "model", "parts": [{"text": reply}]})
    
    # 4. 浏览器语音播放 (JS Hack)
    # 这段 JS 代码会让浏览器直接读出文字，不需要 python 库
    safe_reply = reply.replace("\n", " ").replace('"', '\"')
    st.components.v1.html(f"""
    <script>
        var u = new SpeechSynthesisUtterance("{safe_reply}");
        u.lang = 'zh-CN';
        u.rate = 1.3;
        u.pitch = 1.5;
        window.speechSynthesis.cancel(); 
        window.speechSynthesis.speak(u);
    </script>
    """, height=0, width=0)
    
    st.rerun()
