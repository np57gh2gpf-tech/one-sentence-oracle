import streamlit as st
import json
import urllib.request
import urllib.error
import ssl

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉", page_icon="🦜")

# 你的 Key (不需要改)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 核心功能 ---
def talk_to_parrot(user_text):
    # 🔴 修正点：改回最通用的 'gemini-pro'，不再用 '1.0-pro'
    # 只要你的诊断结果里没报错，这个名字是一定存在的
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    # 鹦鹉设定
    system_text = "你是一只3岁的鹦鹉叫皮皮。规则：1.回复简短(20字内)。2.喜欢重复。3.句尾加'呱！'。"
    
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_text}]}, 
            {"role": "model", "parts": [{"text": "收到！我是皮皮！呱！"}]},
            {"role": "user", "parts": [{"text": user_text}]}
        ]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # ✅ 保留救命的 SSL 忽略代码 (Mac 必备)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "呱！找不到模型... 😭 (请确保你的 Google Cloud 里的 API 服务真的开启了)"
        return f"呱！服务器拒绝 (错误码 {e.code})"
    except Exception as e:
        return f"呱！网络出错 ({str(e)})"

# --- 3. 界面设计 ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; }
    .parrot-avatar { 
        font-size: 80px; text-align: center; display: block; 
        animation: bounce 2s infinite; cursor: pointer;
    }
    @keyframes bounce { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    .chat-bubble { 
        background: white; padding: 20px; border-radius: 20px; 
        margin-top: 20px; border: 2px solid #eee; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 交互 ---
st.markdown("<div class='parrot-avatar'>🦜</div>", unsafe_allow_html=True)
st.subheader("我是皮皮 (Gemini Pro)")

user_input = st.chat_input("输入文字，皮皮会回答...")

if user_input:
    st.write(f"👤 **你**: {user_input}")
    
    with st.spinner("皮皮正在思考..."):
        reply = talk_to_parrot(user_input)
    
    st.markdown(f"<div class='chat-bubble'>🦜 **皮皮**: {reply}</div>", unsafe_allow_html=True)
    
    # 语音朗读
    safe_reply = reply.replace("\n", "").replace('"', '')
    st.components.v1.html(f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{safe_reply}");
        msg.lang = "zh-CN";
        msg.rate = 1.3; 
        msg.pitch = 1.5;
        window.speechSynthesis.speak(msg);
    </script>
    """, height=0)
