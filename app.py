import streamlit as st
import json
import urllib.request
import urllib.error

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉", page_icon="🦜")

# 你的 Key (我在截图里看到的那个)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 核心功能: 极简连接 AI ---
def talk_to_parrot(text):
    # 這是谷歌 AI 的接口地址
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # 鹦鹉的设定
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"你是一只3岁的鹦鹉叫皮皮。请用简短、可爱、重复的语气回答小朋友的话。每句话结尾加'呱！'。小朋友说：{text}"
            }]
        }]
    }
    
    try:
        data = json.dumps(prompt).encode('utf-8')
        # 创建请求
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 发送! (这里需要你的电脑能访问谷歌)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.HTTPError as e:
        if e.code == 403 or e.code == 400:
            return "呱！请去网页上搜索 'Generative Language API' 并点击启用！"
        return f"呱！服务器拒绝了我 (错误码 {e.code})"
    except Exception as e:
        return "呱！网络不通... (请确保你的梯子/VPN是开着的)"

# --- 3. 界面设计 ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; }
    .parrot { font-size: 80px; text-align: center; display: block; animation: float 3s infinite; }
    @keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-10px);} }
    .chat-bubble { background: white; padding: 15px; border-radius: 15px; margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- 4. 交互区域 ---
st.markdown("<div class='parrot'>🦜</div>", unsafe_allow_html=True)
st.subheader("我是皮皮，跟我说话吧！")

# 简单的输入框
user_input = st.chat_input("输入你想说的话...")

if user_input:
    # 1. 显示你的话
    st.write(f"👤 **你**: {user_input}")
    
    # 2. 鹦鹉思考
    with st.spinner("皮皮正在思考..."):
        reply = talk_to_parrot(user_input)
    
    # 3. 显示鹦鹉的话
    st.markdown(f"<div class='chat-bubble'>🦜 **皮皮**: {reply}</div>", unsafe_allow_html=True)
    
    # 4. 自动朗读 (利用浏览器能力)
    # 这里的代码会让你的浏览器把字读出来，不用装任何库
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
