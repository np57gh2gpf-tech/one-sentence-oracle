import streamlit as st
import streamlit.components.v1 as components

# --- 1. 页面配置 ---
st.set_page_config(page_title="皮皮鹦鹉 (AI版)", page_icon="🦜", layout="centered")

# 隐藏无关菜单
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #fceea7; }
</style>
""", unsafe_allow_html=True)

# --- 2. 配置 API Key (已写入) ---
# ⚠️ 注意：请保管好你的 Key，不要泄露给陌生人
# 这里的 Key 会被传给下面的 JavaScript 代码
USER_API_KEY = "AIzaSyDbE2a89o6fshlklYKso-0uvBKoL9e51kk"

# --- 3. 核心代码 ---
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Parrot AI</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "Comic Sans MS", sans-serif;
            background-color: #fceea7;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
            height: 100vh; margin: 0; padding-top: 20px;
            overflow: hidden; touch-action: manipulation;
        }}
        .card {{
            background: white; width: 90%; max-width: 380px;
            padding: 20px; border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border: 5px solid #ff6b6b; text-align: center;
            display: flex; flex-direction: column; height: 80vh;
        }}
        
        /* 鹦鹉头像 */
        .avatar-container {{
            flex-shrink: 0; /* 防止头像被挤压 */
            margin-bottom: 10px;
        }}
        .avatar {{
            width: 120px; height: 120px; border-radius: 50%;
            background: #e0f7fa; border: 4px solid #4ecdc4;
            margin: 0 auto; display: flex; align-items: center; justify-content: center;
            overflow: hidden;
        }}
        .emoji {{ font-size: 70px; animation: float 3s infinite; }}
        
        /* 聊天记录区 (占满剩余空间) */
        .chat-box {{
            flex-grow: 1; overflow-y: auto; background: #f9f9f9;
            border-radius: 10px; padding: 10px; margin-bottom: 15px;
            text-align: left; font-size: 15px; border: 1px solid #eee;
        }}
        .msg {{ margin-bottom: 10px; padding: 8px 12px; border-radius: 12px; max-width: 85%; line-height: 1.4; }}
        .msg.user {{ background: #d1ecf1; color: #0c5460; margin-left: auto; border-bottom-right-radius: 2px; }}
        .msg.ai {{ background: #fff3cd; color: #856404; margin-right: auto; border-bottom-left-radius: 2px; }}

        /* 底部控制区 */
        .controls {{ flex-shrink: 0; }}
        
        .mic-btn {{
            width: 75px; height: 75px; border-radius: 50%; border: none;
            background: #ff6b6b; color: white; font-size: 32px;
            box-shadow: 0 5px 0 #c0392b; cursor: pointer; transition: all 0.1s;
        }}
        .mic-btn:active {{ transform: translateY(5px); box-shadow: none; }}
        .mic-btn.listening {{ background: #2ecc71; animation: pulse 1.5s infinite; }}
        .mic-btn.thinking {{ background: #f1c40f; animation: spin 1s infinite; }}

        .status {{ font-size: 12px; color: #888; margin-top: 10px; min-height: 20px; }}

        /* 动画 */
        @keyframes float {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(-6px);}} }}
        @keyframes pulse {{ 0%{{transform:scale(1);}} 50%{{transform:scale(1.1);}} 100%{{transform:scale(1);}} }}
        @keyframes spin {{ 0%{{transform:rotate(0deg);}} 100%{{transform:rotate(360deg);}} }}
        .shaking {{ animation: shake 0.3s infinite; }}
        @keyframes shake {{ 0%{{transform:rotate(0deg);}} 25%{{transform:rotate(5deg);}} 75%{{transform:rotate(-5deg);}} }}
    </style>
</head>
<body>

<div class="card">
    <div class="avatar-container">
        <div class="avatar" id="avatar">
            <img src="parrot.jpg" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display='none';document.getElementById('e').style.display='block'">
            <div id="e" class="emoji" style="display:none">🦜</div>
        </div>
    </div>

    <div class="chat-box" id="chatBox">
        <div class="msg ai">呱！我是皮皮！我有超级大脑啦！<br>快问我问题！🍪</div>
    </div>
    
    <div class="controls">
        <button class="mic-btn" id="btn" onclick="toggleMic()">🎤</button>
        <div class="status" id="status">点击麦克风开始说话</div>
    </div>
</div>

<script>
    // --- 🔑 API 配置 ---
    const API_KEY = "{USER_API_KEY}"; // 这里自动填入了你的 Key
    const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + API_KEY;
    
    // --- 🦜 鹦鹉人设 (System Prompt) ---
    const SYSTEM_PROMPT = `
    你现在扮演一只叫"皮皮"的卡通鹦鹉，你的对话对象是3-6岁的小朋友。
    请严格遵守以下规则：
    1. 回复必须非常简短，最好在25个字以内。
    2. 必须模仿鹦鹉的说话方式，喜欢重复词语（如"好吃好吃"、"开心开心"）。
    3. 每一句话的结尾最好加上口癖"呱！"或者"扑棱扑棱！"。
    4. 永远保持热情、可爱、稍微有点傻乎乎的性格。
    5. 如果遇到太难的问题（如复杂的科学），就用小孩子能懂的童话方式解释。
    6. 不要使用Markdown格式，直接输出纯文本。
    `;

    // 对话历史
    let chatHistory = [
        {{ "role": "user", "parts": [{{ "text": SYSTEM_PROMPT }}] }},
        {{ "role": "model", "parts": [{{ "text": "收到！我是皮皮！好吃好吃！呱！" }}] }}
    ];

    // --- 组件 ---
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
        
        recognition.onerror = (e) => {{
            console.error(e);
            btn.className = 'mic-btn';
            if(e.error === 'not-allowed') {{
                status.innerText = "❌ 请允许麦克风权限";
                addMessage('ai', "我看不到你的麦克风权限！呱！😭");
            }} else {{
                status.innerText = "没听清，再试一次";
            }}
        }};
    }} else {{
        status.innerText = "❌ 浏览器不支持语音";
    }}

    function toggleMic() {{
        if (!recognition) return alert("不支持语音");
        if (synth) synth.cancel(); // 停止说话，准备听
        
        try {{
            recognition.start();
        }} catch(e) {{
            console.log("Mic start error:", e);
        }}
    }}

    // --- 🧠 核心逻辑：调用 Gemini API ---
    async function handleUserMessage(text) {{
        // 1. 上屏
        addMessage('user', text);
        
        // 2. 状态变化
        btn.className = 'mic-btn thinking';
        status.innerText = "🧠 皮皮正在思考...";
        
        // 3. 准备数据
        chatHistory.push({{ "role": "user", "parts": [{{ "text": text }}] }});

        try {{
            // 4. 发起请求
            const response = await fetch(API_URL, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{
                    "contents": chatHistory.slice(-12) // 发送最近12条记录保持记忆
                }})
            }});
            
            const data = await response.json();
            
            // 5. 错误检查
            if (data.error) {{
                throw new Error(data.error.message);
            }}
            
            // 6. 获取回复
            const reply = data.candidates[0].content.parts[0].text;
            
            // 7. 记录并展示
            chatHistory.push({{ "role": "model", "parts": [{{ "text": reply }}] }});
            
            btn.className = 'mic-btn';
            status.innerText = "点击麦克风";
            addMessage('ai', reply);
            speak(reply);
            
        }} catch (err) {{
            console.error(err);
            btn.className = 'mic-btn';
            status.innerText = "网络错误";
            addMessage('ai', "哎呀，脑子卡住了！是不是断网了？呱！");
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
        u.pitch = 1.6; // 语调高
        u.rate = 1.3;  // 语速快
        u.onend = () => {{ avatar.classList.remove('shaking'); }};
        synth.speak(u);
    }}
</script>
</body>
</html>
"""

# 渲染页面，高度设置大一点以适应聊天框
components.html(html_code, height=750)
