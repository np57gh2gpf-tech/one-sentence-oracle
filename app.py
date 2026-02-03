import streamlit as st
import json
import urllib.request
import urllib.error

# --- 1. 核心配置区 ---
st.set_page_config(page_title="鹦鹉皮皮", page_icon="🦜", layout="centered")

# 你的 API Key (直接写入，方便运行)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 鹦鹉的大脑 (纯 Python 原生实现，不依赖任何第三方库) ---
def ask_gemini_native(text, history):
    # 这是 Gemini 的 API 地址
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # 鹦鹉的人设 (System Prompt)
    system_instruction = """
    你现在是一只叫“皮皮”的鹦鹉。
    1. 你只能用非常简短的话回答（15个字以内）。
    2. 你非常喜欢模仿和重复（例如：“好吃！好吃！”）。
    3. 你的每一句话结尾必须带上“呱！”。
    4. 你只有3岁的智商，不懂复杂的道理。
    """
    
    # 构造请求数据
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction}]},
            *history, # 放入之前的对话记忆
            {"role": "user", "parts": [{"text": text}]}
        ]
    }
    
    # 发送请求 (使用 Python 自带的 urllib)
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        # 这里的 timeout=10 是指等待 10 秒，连不上就报错
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 提取 AI 的回答
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except Exception as e:
        return f"呱！脑子卡住了！(原因: {e})"

# --- 3. 界面设计 (可爱风) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; } /* 米黄色护眼背景 */
    header { visibility: hidden; }
    
    /* 鹦鹉头像动画 */
    .avatar-box { text-align: center; margin-bottom: 20px; }
    .avatar { 
        font-size: 80px; 
        display: inline-block; 
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
    }
    @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    
    /* 聊天气泡 */
    .chat-msg {
        padding: 15px; border-radius: 15px; margin-bottom: 10px;
        max-width: 80%; font-size: 16px; line-height: 1.5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .user { background: #e3f2fd; margin-left: auto; color: #1565c0; border-bottom-right-radius: 2px; }
    .ai { background: #ffffff; margin-right: auto; color: #4e342e; border-bottom-left-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 4. 逻辑控制 ---
if "messages" not in st.session_state:
    # 初始状态
    st.session_state.messages = []

# 显示标题和鹦鹉
st.markdown("<div class='avatar-box'><div class='avatar'>🦜</div><h3>我是皮皮，跟我说话！</h3></div>", unsafe_allow_html=True)

# 显示历史对话
for msg in st.session_state.messages:
    css = "user" if msg["role"] == "user" else "ai"
    st.markdown(f"<div class='chat-msg {css}'>{msg['parts'][0]['text']}</div>", unsafe_allow_html=True)

# --- 5. 交互区域 (文字 + 自动语音) ---
# 既然要“重新设计”，我们用最稳的 Chat Input
user_input = st.chat_input("在这里输入，或者点击上面的麦克风(如果有的话)...")

if user_input:
    # 1. 显示用户的话
    st.session_state.messages.append({"role": "user", "parts": [{"text": user_input}]})
    
    # 2. 调用 AI (只传最近 6 句记忆，省流量)
    ai_reply = ask_gemini_native(user_input, st.session_state.messages[-6:])
    
    # 3. 记录 AI 的话
    st.session_state.messages.append({"role": "model", "parts": [{"text": ai_reply}]})
    
    # 4. 浏览器自动朗读 (JavaScript Hack)
    # 这段代码会注入到网页里，强行让浏览器读出声音，不需要任何后端库
    safe_text = ai_reply.replace("\n", " ").replace('"', '\"')
    js = f"""
    <script>
        function speak() {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{safe_text}");
            msg.lang = "zh-CN";
            msg.rate = 1.2; // 语速稍快
            msg.pitch = 1.4; // 音调稍高，像鹦鹉
            window.speechSynthesis.speak(msg);
        }}
        speak();
    </script>
    """
    st.components.v1.html(js, height=0, width=0)
    
    # 刷新页面显示新消息
    st.rerun()
