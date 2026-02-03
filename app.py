import streamlit as st
import json
import urllib.request
import urllib.error

# --- 1. 基础配置 ---
st.set_page_config(page_title="皮皮鹦鹉", page_icon="🦜")

# 你的 Key (验证通过的那个)
API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 2. 核心功能: 连接 Gemini Pro ---
def talk_to_parrot(user_text):
    # 🔴 关键修改：听从诊断建议，使用 gemini-pro 模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    # 鹦鹉的人设 (Gemini Pro 最好把人设放在第一句)
    system_text = "你现在是一只3岁的宠物鹦鹉叫皮皮。规则：1.回复要简短(20字以内)可爱。2.喜欢重复词语(如'好吃好吃')。3.每句话结尾必须加'呱！'。4.如果不懂就说要吃瓜子。"
    
    # 构造请求数据
    payload = {
        "contents": [
            # 伪造第一轮对话来确立人设（这是 Gemini Pro 最稳的写法）
            {"role": "user", "parts": [{"text": system_text}]}, 
            {"role": "model", "parts": [{"text": "收到！我是皮皮！好吃好吃！呱！"}]},
            # 用户的真实问题
            {"role": "user", "parts": [{"text": user_text}]}
        ]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 提取回答
            return result['candidates'][0]['content']['parts'][0]['text']
            
    except urllib.error.HTTPError as e:
        return f"呱！服务器报错了 (代码 {e.code})，请检查网络！"
    except Exception as e:
        return f"呱！脑子卡住了 ({str(e)})"

# --- 3. 界面设计 (护眼风) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; }
    header { visibility: hidden; }
    
    .parrot-container { text-align: center; margin-top: 20px; }
    .parrot-avatar { 
        font-size: 100px; 
        display: inline-block; 
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
    }
    
    @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-15px);} }
    
    .chat-bubble {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        font-size: 18px;
        color: #4e342e;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 页面布局 ---
st.markdown("<div class='parrot-container'><div class='parrot-avatar'>🦜</div><h2>我是皮皮，快跟我说话！</h2></div>", unsafe_allow_html=True)

# --- 5. 交互区域 ---
# 简单的聊天输入框
user_input = st.chat_input("输入文字，皮皮会读给你听...")

if user_input:
    # 1. 显示用户输入
    st.write(f"👤 **你**: {user_input}")
    
    # 2. 思考中
    with st.spinner("皮皮正在思考..."):
        reply = talk_to_parrot(user_input)
    
    # 3. 显示回复
    st.markdown(f"<div class='chat-bubble'>🦜 **皮皮**: {reply}</div>", unsafe_allow_html=True)
    
    # 4. 自动朗读 (浏览器原生能力，不需要任何库)
    safe_reply = reply.replace("\n", " ").replace('"', '\"')
    js_code = f"""
    <script>
        window.speechSynthesis.cancel(); // 停止之前的说话
        var msg = new SpeechSynthesisUtterance("{safe_reply}");
        msg.lang = "zh-CN"; // 设置中文
        msg.rate = 1.3;     // 语速快一点，像鹦鹉
        msg.pitch = 1.5;    // 音调高一点
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)
