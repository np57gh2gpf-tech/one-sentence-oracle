import streamlit as st
import json
import urllib.request
import urllib.error
import os

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉 (网络修复版)", page_icon="🦜", layout="centered")

# 你的 Key
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 侧边栏：网络设置 (关键修复点) ---
with st.sidebar:
    st.header("🔧 网络急救箱")
    st.write("如果连不上，请在这里调整代理。")
    
    use_proxy = st.checkbox("开启 VPN 代理加速", value=True)
    proxy_port = st.text_input("代理端口 (Mac通常是7890)", value="7890")
    
    if use_proxy:
        proxy_url = f"http://127.0.0.1:{proxy_port}"
        os.environ["http_proxy"] = proxy_url
        os.environ["https_proxy"] = proxy_url
        st.success(f"已配置代理: {proxy_url}")
    else:
        # 清除代理设置
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

# --- 3. 核心功能 ---
def talk_to_gemini(user_text, history_context):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    system_prompt = """
    你现在是"皮皮鹦鹉"。
    规则：
    1. 必须非常可爱、傻乎乎。
    2. 喜欢重复词语 (如: "好吃好吃")。
    3. 句尾必须加 "呱！"。
    4. 回复要简短 (20字以内)。
    """
    
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]},
            *history_context, 
            {"role": "user", "parts": [{"text": user_text}]}
        ]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        # 创建请求
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 发送请求 (超时设置稍微长一点: 15秒)
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.URLError as e:
        # 详细报错，方便排查
        return f"呱！网络连不上！(错误: {e.reason}) \n请尝试在左边侧边栏修改端口号！"
    except Exception as e:
        return f"呱！脑子坏掉了！({str(e)})"

# --- 4. 界面美化 ---
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
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .avatar { font-size: 80px; animation: bounce 2s infinite; display: inline-block; }
    
    @keyframes bounce { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    
    .chat-row { display: flex; margin-bottom: 10px; }
    .bubble { padding: 12px 18px; border-radius: 15px; font-size: 16px; max-width: 80%; line-height: 1.5; }
    .user-bubble { background: #d1ecf1; margin-left: auto; color: #0c5460; border-bottom-right-radius: 2px; }
    .ai-bubble { background: #fff3cd; margin-right: auto; color: #856404; border: 1px solid #ffeeba; border-bottom-left-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 5. 逻辑处理 ---
if "history" not in st.session_state:
    st.session_state.history = [] 

# 标题区
st.markdown("""
<div class="parrot-box">
    <div class="avatar">🦜</div>
    <h3>我是皮皮！(VPN版)</h3>
</div>
""", unsafe_allow_html=True)

# 显示历史对话
for msg in st.session_state.history:
    role_class = "user-bubble" if msg['role'] == "user" else "ai-bubble"
    st.markdown(f"<div class='chat-row'><div class='bubble {role_class}'>{msg['parts'][0]['text']}</div></div>", unsafe_allow_html=True)

# --- 6. 交互区 ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("在这里打字...", placeholder="比如：讲个故事")
    submitted = st.form_submit_button("发送")

if submitted and user_input:
    context_for_api = st.session_state.history[-6:]
    
    # 调用 AI
    with st.spinner("皮皮正在思考... (如果太久没反应，请检查左侧代理)"):
        reply = talk_to_gemini(user_input, context_for_api)
    
    st.session_state.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.history.append({"role": "model", "parts": [{"text": reply}]})
    
    # 语音播放
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
