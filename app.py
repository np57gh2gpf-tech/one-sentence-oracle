import streamlit as st
import streamlit.components.v1 as components

# --- 1. 页面配置 ---
st.set_page_config(page_title="Gemini 智能鹦鹉", page_icon="🦜", layout="centered")

# 隐藏无关菜单
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #fceea7; }
</style>
""", unsafe_allow_html=True)

# --- 2. API Key 输入区 ---
st.title("🦜 Gemini 智能鹦鹉")

# 为了安全，不要把 Key 写死在代码里，而是通过网页输入
# 如果你自己用，也可以直接把下面的 value="" 改成 value="你的sk-xxx"
api_key = st.text_input("AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk", type="password", help="输入以 sk- 开头的谷歌 API 密钥")

if not api_key:
    st.warning("👈 请先在上方输入你的 API Key，皮皮才能变聪明哦！")
    st.stop()  # 没有 Key 就不加载后面的代码

# --- 3. 核心代码 (前端 JS 调用 Gemini) ---
# 我们把 Python 里的 api_key 传给 JavaScript 变量
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            background-color: #fceea7;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            height: 100vh; margin: 0; padding: 10px;
        }}
        .card {{
            background: white; width: 90%; max-width: 380px;
            padding: 20px; border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border: 4px solid #ff6b6b; text-align: center;
        }}
        .avatar {{
            width: 120px; height: 120px; border-radius: 50%;
            background: #e0f7fa; border: 4px solid #4ecdc4;
            margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;
        }}
        .emoji {{ font-size: 70px; animation: float 3s infinite; }}
        
        .chat-box {{
            height: 200px; overflow-y: auto; background: #f9f9f9;
            border-radius: 10px; padding: 10px; margin-bottom: 15px;
            text-align: left; font-size: 14px; border: 1px solid #eee;
        }}
        .msg {{ margin-bottom: 8px; padding: 5px 10px; border-radius: 10px; max-width: 80%; }}
        .msg.user {{ background: #d1ecf1; color: #0c5460; margin-left: auto; }}
        .msg.ai {{ background: #fff3cd; color: #856404; margin-right: auto; }}

        .mic-btn {{
            width: 70px; height: 70px; border-radius: 50%; border: none;
            background: #ff6b6b; color: white; font-size: 30px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; transition: all 0.1s;
        }}
        .mic-btn:active {{ transform: translateY(5px); box-shadow: none; }}
        .mic-btn.listening {{ background: #2ecc71; animation: pulse 1.5s infinite; }}
        .mic-btn.thinking {{ background: #f1c40f; animation: spin 1s infinite; }}

        .status {{ font-size: 12px; color: #888; margin-top: 10px; }}

        @keyframes float {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(-6px);}} }}
        @keyframes pulse {{ 0%{{transform:scale(1);}} 50%{{transform:scale(1.1);}} 100%{{transform:scale(1);}} }}
        @keyframes spin {{ 0%{{transform:rotate(0deg);}} 100%{{transform:rotate(360deg);}} }}
        .shaking {{ animation: shake 0.3s infinite; }}
        @keyframes shake {{ 0%{{transform:rotate(0deg);}} 25%{{transform:rotate(5deg);}} 75%{{transform:rotate(-5deg);}} }}
    </style>
</head>
<body>

<div class="card">
    <div class="avatar" id="avatar"><div class="emoji">🦜</div></div>
    <div class="chat-box" id="chatBox">
        <div class="msg ai">呱！我是连了网的超级皮皮！快跟我说话！</div>
    </div>
    <button class="mic-btn" id="btn" onclick="toggleMic()">🎤</button>
    <div class="status" id="status">点击麦克风开始</div>
</div>

<script>
    // --- 配置区 ---
    const API_KEY = "{api_key}"; // 从 Python 传进来的 Key
    const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + API_KEY;
    
    // --- 鹦鹉人设 (Prompt Engineering) ---
    // 这是核心！告诉 Gemini 它现在是谁
    const SYSTEM_PROMPT = `
    你现在扮演一只叫"皮皮"的卡通鹦鹉，你的对话对象是3-6岁的小朋友。
    请严格遵守以下规则：
    1. 回复必须非常简短，最好在20个字以内。
    2. 必须模仿鹦鹉的说话方式，喜欢重复词语（如"好吃好吃"、"开心开心"）。
    3. 每一句话的结尾必须加上口癖"呱！"。
    4. 永远保持热情、可爱、稍微有点傻乎乎的性格。
    5. 如果遇到太难的问题，就说"皮皮听不懂，皮皮要吃饼干！"。
    6. 不要使用Markdown格式，直接输出纯文本。
    `;

    // 对话历史 (用于保持上下文)
    let chatHistory = [
        {{ "role": "user", "parts": [{{ "text": SYSTEM_PROMPT }}] }},
        {{ "role": "model", "parts": [{{ "text": "收到！我是皮皮！好吃好吃！呱！" }}] }}
    ];

    // --- 语音与交互组件 ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    const btn = document.getElementById('btn');
    const status = document.getElementById('status');
    const chatBox = document.getElementById('chatBox');
    const avatar = document.getElementById('avatar');
    
    let recognition = null;
    if (SpeechRecognition) {{
        recognition = new SpeechRecognition();
        recognition.lang = 'zh-CN';
        recognition.continuous = false;
        
        recognition.onstart = () => {{
            btn.className = 'mic-btn listening';
            status.innerText = "👂 在听你说...";
        }};
        
        recognition.onend = () => {{
            if (btn.className.includes('listening')) {{
                btn.className = 'mic-btn';
                status.innerText = "点击麦克风";
            }}
        }};
        
        recognition.onresult = (e) => {{
            const text = e.results[0][0].transcript;
            handleUserMessage(text);
        }};
    }} else {{
        status.innerText = "浏览器不支持语音，请用 Chrome";
    }}

    function toggleMic() {{
        if (!recognition) return alert("不支持语音");
        if (synth) synth.cancel(); // 停止之前的说话
        
        try {{
            recognition.start();
        }} catch(e) {{
            console.log(e);
        }}
    }}

    // --- 核心逻辑：调用 Gemini API ---
    async function handleUserMessage(text) {{
        // 1. 上屏用户消息
        addMessage('user', text);
        
        // 2. 状态变为思考中
        btn.className = 'mic-btn thinking';
        status.innerText = "🧠 皮皮正在思考...";
        
        // 3. 准备发送给 API 的数据
        // Gemini API 需要要把新的用户消息加到历史里
        chatHistory.push({{ "role": "user", "parts": [{{ "text": text }}] }});

        try {{
            // 4. 发起网络请求
            const response = await fetch(API_URL, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{
                    "contents": chatHistory.slice(-10) // 只发最近10条，节省token
                }})
            }});
            
            const data = await response.json();
            
            // 5. 解析 API 返回
            if (data.error) {{
                throw new Error(data.error.message);
            }}
            
            const reply = data.candidates[0].content.parts[0].text;
            
            // 6. 把 AI 回复也加到历史里
            chatHistory.push({{ "role": "model", "parts": [{{ "text": reply }}] }});
            
            // 7. 展示并朗读
            btn.className = 'mic-btn';
            status.innerText = "点击麦克风";
            addMessage('ai', reply);
            speak(reply);
            
        }} catch (err) {{
            console.error(err);
            btn.className = 'mic-btn';
            status.innerText = "出错了: " + err.message;
            addMessage('ai', "哎呀，脑子卡住了！呱！(API错误)");
        }}
    }}

    function addMessage(role, text) {{
        const div = document.createElement('div');
        div.className = 'msg ' + role;
        div.innerText = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }}

    function speak(text) {{
        avatar.classList.add('shaking');
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.pitch = 1.6; // 鹦鹉音调
        u.rate = 1.3;
        u.onend = () => {{ avatar.classList.remove('shaking'); }};
        synth.speak(u);
    }}
</script>
</body>
</html>
"""

components.html(html_code, height=650)
