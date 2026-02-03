import streamlit as st
import json
import urllib.request
import urllib.error

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉 (自动寻路版)", page_icon="🦜", layout="centered")

# 你的 Key (已验证是好的)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 核心黑科技: 自动寻找 VPN 通道 ---
def request_with_auto_proxy(url, data):
    # 这里的 None 代表直连，后面两个是 Mac 最常见的 VPN 端口
    # 代码会一个一个试，哪个能通就走哪个
    proxies_to_try = [
        None,                        # 先试直连
        "http://127.0.0.1:7890",     # ClashX / Clash Verge 默认端口
        "http://127.0.0.1:10809",    # V2RayU 默认端口
        "http://127.0.0.1:1080",     # Shadowsocks 默认端口
        "http://127.0.0.1:33210"     # 其他常见端口
    ]
    
    last_error = None
    
    for proxy in proxies_to_try:
        try:
            # 配置代理处理器
            if proxy:
                proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
                opener = urllib.request.build_opener(proxy_handler)
            else:
                opener = urllib.request.build_opener()
            
            # 准备请求
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            # 发送请求 (设置5秒超时，快速切换)
            with opener.open(req, timeout=5) as response:
                # 如果成功了，直接返回结果！
                return json.loads(response.read().decode('utf-8'))
                
        except Exception as e:
            last_error = e
            continue # 失败了？试下一个！

    # 如果所有路都堵死了，抛出最后一个错误
    raise last_error

# --- 3. 鹦鹉大脑 ---
def talk_to_parrot(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"你是一只3岁的鹦鹉叫皮皮。请用简短、可爱、重复的语气回答小朋友的话。每句话结尾加'呱！'。小朋友说：{text}"
            }]
        }]
    }
    
    try:
        data = json.dumps(prompt).encode('utf-8')
        result = request_with_auto_proxy(url, data)
        return result['candidates'][0]['content']['parts'][0]['text']
            
    except Exception as e:
        return f"呱！我连不上网... (请确保你的梯子是打开的)"

# --- 4. 界面设计 ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; }
    .parrot-container { text-align: center; margin-bottom: 20px; }
    .parrot-avatar { 
        font-size: 80px; display: inline-block; 
        animation: float 3s ease-in-out infinite; cursor: pointer;
    }
    @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
    
    .bubble { padding: 15px; border-radius: 15px; margin-bottom: 15px; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .user-msg { background: #e3f2fd; color: #1565c0; margin-left: 20px; text-align: right; }
    .ai-msg { background: #fff; color: #333; margin-right: 20px; text-align: left; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# --- 5. 交互区域 ---
st.markdown("<div class='parrot-container'><div class='parrot-avatar'>🦜</div><h3>我是皮皮，我在听！</h3></div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示对话
for msg in st.session_state.messages:
    cls = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f"<div class='bubble {cls}'>{msg['text']}</div>", unsafe_allow_html=True)

# 输入框
user_input = st.chat_input("跟皮皮说话...")

if user_input:
    # 1. 记录
    st.session_state.messages.append({"role": "user", "text": user_input})
    
    # 2. 思考 (自动寻路)
    with st.spinner("皮皮正在连接大脑..."):
        reply = talk_to_parrot(user_input)
    
    # 3. 回复
    st.session_state.messages.append({"role": "ai", "text": reply})
    
    # 4. 朗读
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
    
    st.rerun()
